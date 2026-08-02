#!/usr/bin/env python3
"""
Cliente Pipedrive — deals, pessoas, organizacoes, atividades.

Uso CLI:
    python pipedrive_cliente.py listar-deals
    python pipedrive_cliente.py pipeline-resumo
    python pipedrive_cliente.py deals-perdidos 30

Credenciais:
    PIPEDRIVE_TOKEN=
    PIPEDRIVE_DOMAIN=seu-dominio (sem .pipedrive.com)

"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    sys.exit("erro: pip install requests")


class PipedriveCliente:
    def __init__(self, token: str | None = None, domain: str | None = None, timeout: int = 30):
        self.token = token or os.environ.get("PIPEDRIVE_TOKEN")
        self.domain = domain or os.environ.get("PIPEDRIVE_DOMAIN")
        if not self.token or not self.domain:
            sys.exit("erro: defina PIPEDRIVE_TOKEN e PIPEDRIVE_DOMAIN")
        self.base = f"https://{self.domain}.pipedrive.com/api/v1"
        self.timeout = timeout

    def _get(self, path: str, params: dict | None = None):
        p = {**(params or {}), "api_token": self.token}
        r = requests.get(f"{self.base}{path}", params=p, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Pipedrive {r.status_code}: {r.text[:200]}")
        return r.json()

    def _post(self, path: str, data: dict):
        r = requests.post(f"{self.base}{path}?api_token={self.token}", json=data, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Pipedrive {r.status_code}: {r.text[:200]}")
        return r.json()

    def _put(self, path: str, data: dict):
        r = requests.put(f"{self.base}{path}?api_token={self.token}", json=data, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Pipedrive {r.status_code}: {r.text[:200]}")
        return r.json()

    # ------------------------------------------------------------- stages
    def stages(self) -> list[dict]:
        return self._get("/stages").get("data") or []

    # -------------------------------------------------------------- deals
    def listar_deals(self, stage_id: int | None = None, status: str = "open") -> list[dict]:
        # status: open, won, lost, deleted, all_not_deleted
        params = {"status": status, "limit": 500}
        if stage_id:
            params["stage_id"] = stage_id
        deals = self._get("/deals", params).get("data") or []
        return [
            {
                "id": d["id"],
                "titulo": d["title"],
                "valor": float(d.get("value") or 0),
                "moeda": d.get("currency", "BRL"),
                "stage_id": d.get("stage_id"),
                "status": d.get("status"),
                "owner": (d.get("user_id") or {}).get("name") if isinstance(d.get("user_id"), dict) else d.get("user_id"),
                "criado_em": d.get("add_time"),
                "atualizado_em": d.get("update_time"),
                "expected_close": d.get("expected_close_date"),
            }
            for d in deals
        ]

    def criar_deal(self, titulo: str, valor: float, pessoa_id: int | None = None,
                   stage_id: int | None = None, org_id: int | None = None) -> dict:
        data: dict = {"title": titulo, "value": valor, "currency": "BRL"}
        if pessoa_id:
            data["person_id"] = pessoa_id
        if stage_id:
            data["stage_id"] = stage_id
        if org_id:
            data["org_id"] = org_id
        return self._post("/deals", data)

    def mover_deal(self, deal_id: int, stage_id: int) -> dict:
        return self._put(f"/deals/{deal_id}", {"stage_id": stage_id})

    def ganhar_deal(self, deal_id: int) -> dict:
        return self._put(f"/deals/{deal_id}", {"status": "won"})

    def perder_deal(self, deal_id: int, motivo: str = "") -> dict:
        return self._put(f"/deals/{deal_id}", {"status": "lost", "lost_reason": motivo})

    # ---------------------------------------------------------- pessoas
    def buscar_pessoa(self, termo: str) -> list[dict]:
        # email ou telefone
        if "@" in termo:
            params = {"term": termo, "fields": "email"}
        else:
            params = {"term": termo, "fields": "phone"}
        j = self._get("/persons/search", params)
        return [
            {"id": p["item"]["id"], "nome": p["item"]["name"]}
            for p in (j.get("data", {}).get("items") or [])
        ]

    def criar_pessoa(self, nome: str, email: str | None = None, telefone: str | None = None) -> dict:
        data = {"name": nome}
        if email:
            data["email"] = [email]
        if telefone:
            data["phone"] = [telefone]
        return self._post("/persons", data)

    def criar_organizacao(self, nome: str) -> dict:
        return self._post("/organizations", {"name": nome})

    # ------------------------------------------------------- atividades
    def adicionar_atividade(self, deal_id: int, titulo: str, tipo: str = "call",
                            quando: datetime | None = None) -> dict:
        data: dict = {"deal_id": deal_id, "subject": titulo, "type": tipo, "done": 0}
        if quando:
            data["due_date"] = quando.strftime("%Y-%m-%d")
            data["due_time"] = quando.strftime("%H:%M")
        return self._post("/activities", data)

    # ------------------------------------------------------------ resumo
    def pipeline_resumo(self) -> dict:
        resumo = {}
        for s in self.stages():
            deals = self.listar_deals(stage_id=s["id"])
            resumo[s["name"]] = {
                "quantidade": len(deals),
                "valor_total": round(sum(d["valor"] for d in deals), 2),
                "valor_medio": round(sum(d["valor"] for d in deals) / len(deals), 2) if deals else 0,
            }
        return resumo

    def deals_perdidos_recentes(self, dias: int = 30) -> list[dict]:
        deals = self.listar_deals(status="lost")
        corte = datetime.utcnow() - timedelta(days=dias)
        out = []
        for d in deals:
            try:
                upd = datetime.strptime(d["atualizado_em"], "%Y-%m-%d %H:%M:%S")
                if upd >= corte:
                    out.append(d)
            except (TypeError, ValueError):
                continue
        return out


# ------------------------------------------------------------------- CLI
def _p(o):
    print(json.dumps(o, default=str, indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: pipedrive_cliente.py <listar-deals | pipeline-resumo | deals-perdidos [N]>")
    cmd = sys.argv[1]
    c = PipedriveCliente()
    if cmd == "listar-deals":
        _p(c.listar_deals())
    elif cmd == "pipeline-resumo":
        _p(c.pipeline_resumo())
    elif cmd == "deals-perdidos":
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        _p(c.deals_perdidos_recentes(dias))
    else:
        sys.exit(f"comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
