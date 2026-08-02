#!/usr/bin/env python3
"""
Orquestrador de fluxos — combina varias integracoes do pack.

Definicao em YAML (ou JSON):

    nome: Pedidos diarios
    etapas:
      - id: pedidos
        cmd: python ../shopify/shopify_cliente.py pedidos-hoje
        formato: json

      - id: notificar
        cmd: python ../slack-discord-telegram/notificador.py --canal slack
        stdin: "Total de pedidos: {{pedidos.count}}"

Uso:
    python orquestrador.py fluxos/pedidos-diarios.yaml
    python orquestrador.py fluxos/x.yaml --dry-run
    python orquestrador.py fluxos/x.yaml --etapa-de notificar

"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml  # pyyaml
except ImportError:
    yaml = None


VAR_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_\.]+)\s*\}\}")


@dataclass
class Etapa:
    id: str
    cmd: str
    formato: str = "texto"  # texto | json
    stdin: str = ""
    condicao: str = ""
    continuar_em_erro: bool = False
    retries: int = 0
    timeout: int = 120


def carregar(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"erro: {path} nao existe")
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if not yaml:
            sys.exit("erro: pip install pyyaml (ou use .json)")
        return yaml.safe_load(raw)
    return json.loads(raw)


def expandir_vars(template: str, contexto: dict) -> str:
    def sub(m):
        chave = m.group(1)
        partes = chave.split(".")
        val = contexto
        for p in partes:
            if isinstance(val, dict) and p in val:
                val = val[p]
            else:
                return m.group(0)  # mantem se nao achou
        return str(val)
    return VAR_REGEX.sub(sub, template)


def avaliar_condicao(expr: str, contexto: dict) -> bool:
    if not expr:
        return True
    expandida = expandir_vars(expr, contexto)
    # avaliacao SEGURA — so permite numeros, comparacoes e parenteses
    if not re.match(r"^[\d\.\s\(\)<>=!&|\-\+\*\/]+$", expandida):
        print(f"  ⚠️  condicao com expressao nao-segura: '{expandida}' — pulando", file=sys.stderr)
        return False
    try:
        return bool(eval(expandida, {"__builtins__": {}}, {}))  # noqa: S307 (filtro acima)
    except Exception as e:
        print(f"  ⚠️  erro na condicao '{expandida}': {e}", file=sys.stderr)
        return False


def executar_etapa(etapa: Etapa, contexto: dict, dry_run: bool = False) -> dict:
    cmd = expandir_vars(etapa.cmd, contexto)
    stdin = expandir_vars(etapa.stdin, contexto) if etapa.stdin else ""

    print(f"\n▶ {etapa.id}")
    print(f"  cmd: {cmd[:120]}{'...' if len(cmd) > 120 else ''}")
    if stdin:
        print(f"  stdin: {stdin[:60]}{'...' if len(stdin) > 60 else ''}")

    if dry_run:
        print("  [DRY-RUN] nao executado")
        return {"raw": "[dry-run]"}

    tentativa = 0
    while True:
        tentativa += 1
        t0 = time.time()
        try:
            r = subprocess.run(
                cmd if cmd.startswith("(") or "|" in cmd else shlex.split(cmd),
                shell=("|" in cmd or cmd.startswith("(")),
                input=stdin if stdin else None,
                capture_output=True,
                text=True,
                timeout=etapa.timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"  ⏱️  timeout após {etapa.timeout}s")
            if tentativa <= etapa.retries:
                wait = 2 ** tentativa
                print(f"  ⟳ retry em {wait}s (tentativa {tentativa+1}/{etapa.retries+1})")
                time.sleep(wait)
                continue
            if etapa.continuar_em_erro:
                return {"raw": "", "_erro": "timeout"}
            sys.exit(1)

        dur = time.time() - t0
        if r.returncode == 0:
            print(f"  ✅ ok ({dur:.1f}s)")
            saida = r.stdout
            if etapa.formato == "json":
                try:
                    j = json.loads(saida)
                    # enriquecimento: count, total, etc se for lista de dicts numericos
                    extras = _extrair_extras(j)
                    return {"raw": saida, "json": j, **extras}
                except json.JSONDecodeError:
                    print(f"  ⚠️  saida nao e JSON valido")
                    return {"raw": saida}
            return {"raw": saida}
        else:
            print(f"  ❌ falha (code {r.returncode}): {r.stderr[:200]}")
            if tentativa <= etapa.retries:
                wait = 2 ** tentativa
                print(f"  ⟳ retry em {wait}s")
                time.sleep(wait)
                continue
            if etapa.continuar_em_erro:
                return {"raw": r.stderr, "_erro": r.stderr}
            sys.exit(r.returncode)


def _extrair_extras(j) -> dict:
    """Se j eh uma lista de dicts, extrai count e somas."""
    extras: dict = {}
    if isinstance(j, list):
        extras["count"] = len(j)
        # se itens tem 'valor' (float), soma
        if j and isinstance(j[0], dict):
            for chave in ("valor", "total", "amount", "faturamento"):
                if chave in j[0]:
                    try:
                        extras["total"] = round(sum(float(item.get(chave, 0)) for item in j), 2)
                    except (TypeError, ValueError):
                        pass
                    break
            # maior valor
            if j and "valor" in j[0]:
                maior = max(j, key=lambda x: x.get("valor", 0))
                extras["maior_valor"] = maior.get("valor")
                extras["maior_id"] = maior.get("id") or maior.get("numero")
    elif isinstance(j, dict):
        extras["count"] = len(j)
    return extras


def main():
    parser = argparse.ArgumentParser(description="Orquestrador de fluxos")
    parser.add_argument("fluxo", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--etapa-de", default=None, help="comeca a partir desta etapa")
    args = parser.parse_args()

    spec = carregar(args.fluxo)
    nome = spec.get("nome", args.fluxo.name)
    etapas_raw = spec.get("etapas", [])

    contexto: dict = {}
    pulando = bool(args.etapa_de)
    print(f"━━━ {nome} ━━━")

    for raw in etapas_raw:
        etapa = Etapa(**raw)
        if pulando:
            if etapa.id == args.etapa_de:
                pulando = False
            else:
                print(f"… pulando {etapa.id}")
                continue
        if not avaliar_condicao(etapa.condicao, contexto):
            print(f"… {etapa.id}: condicao falsa, pulando")
            continue
        resultado = executar_etapa(etapa, contexto, dry_run=args.dry_run)
        contexto[etapa.id] = resultado

    print("\n━━━ fim ━━━")


if __name__ == "__main__":
    main()
