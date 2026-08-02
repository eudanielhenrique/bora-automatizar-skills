#!/usr/bin/env python3
"""
Cliente RD Station CRM — deals, contatos, atividades, funil.

Uso CLI:
    python rd_cliente.py listar-deals
    python rd_cliente.py resumo-funil
    python rd_cliente.py deals-perdidos 30

Credencial: RD_TOKEN (instancia, gerado em app.rdstation.com.br/crm).

"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any

try:
    import requests
except ImportError:
    sys.exit("erro: pip install requests")


BASE = "https://crm.rdstation.com/api/v1"


class RDStationCRM:
    def __init__(self, token: str | None = None, timeout: int = 30):
        self.token = token or os.environ.get("RD_TOKEN")
        if not self.token:
            sys.exit("erro: defina RD_TOKEN")
        self.timeout = timeout
        self._stages_cache: list[dict] | None = None

    def _get(self, path: str, params: dict | None = None) -> Any:
        p = {**(params or {}), "token": self.token}
        r = requests.get(f"{BASE}{path}", params=p, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"RD {r.status_code}: {r.text[:200]}")
        return r.json()

    def _post(self, path: str, data: dict) -> Any:
        r = requests.post(f"{BASE}{path}?token={self.token}", json=data, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"RD {r.status_code}: {r.text[:200]}")
        return r.json()

    def _put(self, path: str, data: dict) -> Any:
        r = requests.put(f"{BASE}{path}?token={self.token}", json=data, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"RD {r.status_code}: {r.text[:200]}")
        return r.json()

    # ------------------------------------------------------------- stages
    def stages(self) -> list[dict]:
        if self._stages_cache is None:
            self._stages_cache = self._get("/deal_stages").get("deal_stages", [])
        return self._stages_cache

    def stage_nome(self, sid: str) -> str:
        for s in self.stages():
            if s["_id"] == sid:
                return s["name"]
        return "—"

    # -------------------------------------------------------------- deals
    def listar_deals(self, estagio: str | None = None, page: int = 1, limit: int = 200) -> list[dict]:
        params = {"page": page, "limit": limit}
        if estagio:
            params["deal_stage_id"] = estagio
        out = []
        while True:
            j = self._get("/deals", params=params)
            for d in j.get("deals", []):
                out.append({
                    "id": d["_id"],
                    "nome": d.get("name"),
                    "valor": float(d.get("amount_total") or 0),
                    "estagio_id": (d.get("deal_stage") or {}).get("_id"),
                    "estagio_nome": (d.get("deal_stage") or {}).get("name"),
                    "criado_em": d.get("created_at"),
                    "atualizado_em": d.get("updated_at"),
                    "user": (d.get("user") or {}).get("name"),
                    "campaign": (d.get("campaign") or {}).get("name"),
                })
            if not j.get("has_more"):
                break
            params["page"] += 1
        return out

    def criar_deal(self, nome: str, valor: float, contato_id: str | None = None, estagio_id: str | None = None) -> dict:
        data = {
            "deal": {
                "name": nome,
                "deal_stage_id": estagio_id or (self.stages()[0]["_id"] if self.stages() else None),
            },
            "deal_product": {"name": nome, "price": valor, "amount": 1},
        }
        if contato_id:
            data["contacts"] = [{"id": contato_id}]
        return self._post("/deals", data)

    def mover_deal(self, deal_id: str, estagio_id: str) -> dict:
        return self._put(f"/deals/{deal_id}", {"deal": {"deal_stage_id": estagio_id}})

    def deals_perdidos_recentes(self, dias: int = 30) -> list[dict]:
        # estagios "perdidos" geralmente tem campo "lost=true"
        perdidos_ids = [s["_id"] for s in self.stages() if s.get("nickname") == "lost" or "perdid" in s.get("name", "").lower()]
        corte = datetime.utcnow() - timedelta(days=dias)
        out = []
        for sid in perdidos_ids:
            for d in self.listar_deals(estagio=sid):
                try:
                    upd = datetime.fromisoformat((d["atualizado_em"] or "").replace("Z", "+00:00")).replace(tzinfo=None)
                    if upd >= corte:
                        out.append(d)
                except (ValueError, AttributeError):
                    continue
        return out

    def resumo_funil(self) -> dict:
        resumo = {}
        for s in self.stages():
            deals = self.listar_deals(estagio=s["_id"])
            resumo[s["name"]] = {
                "quantidade": len(deals),
                "valor_total": round(sum(d["valor"] for d in deals), 2),
                "valor_medio": round(sum(d["valor"] for d in deals) / len(deals), 2) if deals else 0,
            }
        return resumo

    # ----------------------------------------------------------- contatos
    def buscar_contato(self, termo: str) -> list[dict]:
        params = {"email": termo} if "@" in termo else {"phone": termo}
        j = self._get("/contacts", params)
        return [{"id": c["_id"], "nome": c.get("name"), "email": c.get("email"),
                 "telefone": c.get("phone")} for c in j.get("contacts", [])]

    def criar_contato(self, nome: str, email: str | None = None, telefone: str | None = None) -> dict:
        data = {"contact": {"name": nome}}
        if email:
            data["contact"]["emails"] = [{"email": email}]
        if telefone:
            data["contact"]["phones"] = [{"phone": telefone, "type": "cellphone"}]
        return self._post("/contacts", data)

    # -------------------------------------------------------- atividades
    def adicionar_atividade(self, deal_id: str, descricao: str, tipo: str = "note") -> dict:
        # tipo: note, call, email, meeting, task
        return self._post(f"/deals/{deal_id}/notes", {"note": {"text": descricao}})


# ----------------------------------------------------------------- CLI
def _p(o):
    print(json.dumps(o, default=str, indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: rd_cliente.py <listar-deals | resumo-funil | deals-perdidos [N]>")
    cmd = sys.argv[1]
    c = RDStationCRM()
    if cmd == "listar-deals":
        _p(c.listar_deals())
    elif cmd == "resumo-funil":
        _p(c.resumo_funil())
    elif cmd == "deals-perdidos":
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        _p(c.deals_perdidos_recentes(dias))
    else:
        sys.exit(f"comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
