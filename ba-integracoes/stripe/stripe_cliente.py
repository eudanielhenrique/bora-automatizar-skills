#!/usr/bin/env python3
"""
Cliente Stripe — funcoes prontas pra puxar pagamentos, assinaturas, faturas.

Uso CLI:
    python stripe_cliente.py pagamentos-hoje
    python stripe_cliente.py resumo-mes 2026 05
    python stripe_cliente.py assinaturas-ativas
    python stripe_cliente.py faturas-abertas

Uso programatico:
    from stripe_cliente import StripeCliente
    s = StripeCliente()
    print(s.pagamentos_do_dia())

Credencial: variavel de ambiente STRIPE_API_KEY (restricted key, rk_live_... ou rk_test_...).

"""
from __future__ import annotations

import os
import sys
import json
from datetime import date, datetime, timedelta, timezone
from typing import Iterator

try:
    import requests
except ImportError:
    sys.exit("erro: instale a dependencia 'requests' (pip install requests)")


STRIPE_BASE = "https://api.stripe.com/v1"


class StripeCliente:
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = api_key or os.environ.get("STRIPE_API_KEY")
        if not self.api_key:
            sys.exit("erro: defina STRIPE_API_KEY (rk_live_... ou rk_test_...)")
        self.timeout = timeout

    # ------------------------------------------------------------------ HTTP
    def _get(self, path: str, params: dict | None = None) -> dict:
        r = requests.get(
            f"{STRIPE_BASE}{path}",
            params=params or {},
            auth=(self.api_key, ""),
            timeout=self.timeout,
        )
        if not r.ok:
            raise RuntimeError(f"Stripe {r.status_code}: {r.text}")
        return r.json()

    def _post(self, path: str, data: dict) -> dict:
        r = requests.post(
            f"{STRIPE_BASE}{path}",
            data=data,
            auth=(self.api_key, ""),
            timeout=self.timeout,
        )
        if not r.ok:
            raise RuntimeError(f"Stripe {r.status_code}: {r.text}")
        return r.json()

    def _paginar(self, path: str, params: dict | None = None) -> Iterator[dict]:
        params = dict(params or {})
        params.setdefault("limit", 100)
        starting_after = None
        while True:
            if starting_after:
                params["starting_after"] = starting_after
            j = self._get(path, params)
            for item in j.get("data", []):
                yield item
            if not j.get("has_more"):
                break
            starting_after = j["data"][-1]["id"]

    # --------------------------------------------------------------- helpers
    @staticmethod
    def _ts(dt: datetime) -> int:
        return int(dt.replace(tzinfo=timezone.utc).timestamp())

    @staticmethod
    def _to_brl(amount_in_cents: int) -> float:
        return round(amount_in_cents / 100, 2)

    # ----------------------------------------------------------- pagamentos
    def pagamentos_por_periodo(self, inicio: datetime, fim: datetime) -> list[dict]:
        """PaymentIntents com status=succeeded entre inicio e fim (UTC)."""
        params = {
            "created[gte]": self._ts(inicio),
            "created[lte]": self._ts(fim),
        }
        out: list[dict] = []
        for pi in self._paginar("/payment_intents", params):
            if pi.get("status") != "succeeded":
                continue
            out.append(
                {
                    "id": pi["id"],
                    "valor": self._to_brl(pi["amount"]),
                    "moeda": pi["currency"].upper(),
                    "cliente_id": pi.get("customer"),
                    "criado_em": datetime.fromtimestamp(pi["created"], tz=timezone.utc),
                    "descricao": pi.get("description") or "",
                }
            )
        return out

    def pagamentos_do_dia(self, dia: date | None = None) -> list[dict]:
        dia = dia or date.today()
        inicio = datetime.combine(dia, datetime.min.time())
        fim = datetime.combine(dia, datetime.max.time())
        return self.pagamentos_por_periodo(inicio, fim)

    # ----------------------------------------------------------- assinaturas
    def assinaturas_ativas(self) -> list[dict]:
        out = []
        for s in self._paginar("/subscriptions", {"status": "active"}):
            out.append(
                {
                    "id": s["id"],
                    "cliente_id": s["customer"],
                    "plano": (s["items"]["data"][0]["price"].get("nickname")
                              or s["items"]["data"][0]["price"]["id"]),
                    "valor_mes": self._to_brl(s["items"]["data"][0]["price"]["unit_amount"]),
                    "criado_em": datetime.fromtimestamp(s["created"], tz=timezone.utc),
                }
            )
        return out

    def assinaturas_canceladas_recentes(self, dias: int = 30) -> list[dict]:
        corte = self._ts(datetime.utcnow() - timedelta(days=dias))
        out = []
        for s in self._paginar("/subscriptions", {"status": "canceled"}):
            if (s.get("canceled_at") or 0) < corte:
                continue
            out.append(
                {
                    "id": s["id"],
                    "cliente_id": s["customer"],
                    "cancelada_em": datetime.fromtimestamp(s["canceled_at"], tz=timezone.utc),
                    "motivo": (s.get("cancellation_details") or {}).get("reason"),
                }
            )
        return out

    # -------------------------------------------------------------- faturas
    def faturas_em_aberto(self) -> list[dict]:
        out = []
        for inv in self._paginar("/invoices", {"status": "open"}):
            out.append(
                {
                    "id": inv["id"],
                    "cliente_id": inv["customer"],
                    "valor": self._to_brl(inv["amount_due"]),
                    "vencimento": (datetime.fromtimestamp(inv["due_date"], tz=timezone.utc)
                                   if inv.get("due_date") else None),
                    "tentativas": inv.get("attempt_count", 0),
                    "url_hosted": inv.get("hosted_invoice_url"),
                }
            )
        return out

    # ----------------------------------------------------------- customers
    def cliente_buscar(self, termo: str) -> list[dict]:
        # tenta por email exato
        params = {"email": termo, "limit": 10}
        j = self._get("/customers", params)
        if j.get("data"):
            return [{"id": c["id"], "email": c.get("email"), "nome": c.get("name")}
                    for c in j["data"]]
        # fallback: busca todos e filtra por nome (so use em base pequena)
        out = []
        for c in self._paginar("/customers", {"limit": 100}):
            if termo.lower() in (c.get("name") or "").lower():
                out.append({"id": c["id"], "email": c.get("email"), "nome": c.get("name")})
            if len(out) >= 20:
                break
        return out

    # ----------------------------------------------------------- reembolso
    def reembolsar(self, payment_intent_id: str, valor: float | None = None) -> dict:
        data = {"payment_intent": payment_intent_id}
        if valor is not None:
            data["amount"] = int(round(valor * 100))
        return self._post("/refunds", data)

    # -------------------------------------------------------------- resumo
    def resumo_mes(self, ano: int, mes: int) -> dict:
        inicio = datetime(ano, mes, 1)
        # primeiro dia do mes seguinte
        if mes == 12:
            fim = datetime(ano + 1, 1, 1) - timedelta(seconds=1)
        else:
            fim = datetime(ano, mes + 1, 1) - timedelta(seconds=1)

        pagamentos = self.pagamentos_por_periodo(inicio, fim)
        ativas = self.assinaturas_ativas()
        canceladas = self.assinaturas_canceladas_recentes(dias=(fim - inicio).days + 1)
        canceladas_no_mes = [
            c for c in canceladas if inicio <= c["cancelada_em"].replace(tzinfo=None) <= fim
        ]
        mrr = sum(s["valor_mes"] for s in ativas)
        total = sum(p["valor"] for p in pagamentos)

        return {
            "periodo": f"{inicio.date()} a {fim.date()}",
            "transacoes": len(pagamentos),
            "total_recebido_brl": round(total, 2),
            "ticket_medio_brl": round(total / len(pagamentos), 2) if pagamentos else 0.0,
            "assinaturas_ativas": len(ativas),
            "mrr_atual_brl": round(mrr, 2),
            "cancelamentos_no_mes": len(canceladas_no_mes),
            "churn_mes_pct": round(len(canceladas_no_mes) / max(len(ativas) + len(canceladas_no_mes), 1) * 100, 2),
        }


# ---------------------------------------------------------------- CLI
def _print_json(data) -> None:
    print(json.dumps(data, default=str, indent=2, ensure_ascii=False))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(
            "uso: stripe_cliente.py <pagamentos-hoje | resumo-mes ANO MES | assinaturas-ativas | faturas-abertas>"
        )
    cmd = sys.argv[1]
    c = StripeCliente()
    if cmd == "pagamentos-hoje":
        _print_json(c.pagamentos_do_dia())
    elif cmd == "assinaturas-ativas":
        _print_json(c.assinaturas_ativas())
    elif cmd == "faturas-abertas":
        _print_json(c.faturas_em_aberto())
    elif cmd == "resumo-mes":
        if len(sys.argv) < 4:
            sys.exit("uso: stripe_cliente.py resumo-mes ANO MES")
        ano = int(sys.argv[2]); mes = int(sys.argv[3])
        _print_json(c.resumo_mes(ano, mes))
    else:
        sys.exit(f"comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
