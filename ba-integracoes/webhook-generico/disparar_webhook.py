#!/usr/bin/env python3
"""
Helper pra disparar webhook (com assinatura HMAC opcional).

Uso CLI:
    python disparar_webhook.py URL --evento NOME --dados '{"k":"v"}' [--secret SECRET]

Uso programatico:
    from disparar_webhook import disparar
    disparar(
        url="https://hooks.zapier.com/...",
        evento="lead.novo",
        dados={"nome": "Pedro", "telefone": "5521..."},
        secret="opcional_hmac_secret",
    )

"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys

try:
    import requests
except ImportError:
    sys.exit("erro: instale 'requests' (pip install requests)")


def disparar(url: str, evento: str, dados: dict, secret: str | None = None, timeout: int = 15) -> dict:
    """
    Dispara webhook em URL com evento+dados. Se `secret` for fornecido,
    assina o body com HMAC-SHA256 no header X-Signature.
    """
    payload = {"evento": evento, "dados": dados}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if secret:
        sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        headers["X-Signature"] = f"sha256={sig}"

    r = requests.post(url, data=body, headers=headers, timeout=timeout)
    return {
        "ok": r.ok,
        "status": r.status_code,
        "resposta": _try_json(r.text),
    }


def _try_json(t: str):
    try:
        return json.loads(t)
    except Exception:
        return t


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispara webhook para URL")
    parser.add_argument("url", help="URL do webhook receiver")
    parser.add_argument("--evento", required=True, help="Nome do evento")
    parser.add_argument("--dados", default="{}", help="JSON com os dados (string)")
    parser.add_argument("--secret", default=None, help="Secret HMAC (opcional)")
    args = parser.parse_args()

    try:
        dados = json.loads(args.dados)
    except json.JSONDecodeError:
        sys.exit("erro: --dados precisa ser JSON valido")

    resp = disparar(args.url, args.evento, dados, secret=args.secret)
    print(json.dumps(resp, indent=2, ensure_ascii=False))
    sys.exit(0 if resp["ok"] else 1)


if __name__ == "__main__":
    main()
