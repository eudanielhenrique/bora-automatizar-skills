#!/usr/bin/env python3
"""
Cliente Shopify — pedidos, produtos, clientes, estoque.

Uso CLI:
    python shopify_cliente.py pedidos-hoje
    python shopify_cliente.py resumo-dia
    python shopify_cliente.py estoque-baixo 5
    python shopify_cliente.py pedido 1234

Credenciais:
    SHOPIFY_SHOP=sua-loja.myshopify.com
    SHOPIFY_ACCESS_TOKEN=shpat_...

"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from typing import Iterator

try:
    import requests
except ImportError:
    sys.exit("erro: instale 'requests' (pip install requests)")


API_VERSION = "2024-10"


class ShopifyCliente:
    def __init__(self, shop: str | None = None, token: str | None = None, timeout: int = 30):
        self.shop = (shop or os.environ.get("SHOPIFY_SHOP", "")).strip()
        self.token = (token or os.environ.get("SHOPIFY_ACCESS_TOKEN", "")).strip()
        if not self.shop or not self.token:
            sys.exit("erro: defina SHOPIFY_SHOP e SHOPIFY_ACCESS_TOKEN")
        if not self.shop.endswith(".myshopify.com"):
            sys.exit("erro: SHOPIFY_SHOP deve ser 'sua-loja.myshopify.com'")
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"https://{self.shop}/admin/api/{API_VERSION}{path}"

    def _headers(self) -> dict:
        return {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json",
        }

    def _get(self, path: str, params: dict | None = None) -> dict:
        r = requests.get(self._url(path), headers=self._headers(),
                         params=params or {}, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Shopify {r.status_code}: {r.text}")
        return r.json()

    def _put(self, path: str, data: dict) -> dict:
        r = requests.put(self._url(path), headers=self._headers(),
                         data=json.dumps(data), timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Shopify {r.status_code}: {r.text}")
        return r.json()

    def _paginar(self, path: str, params: dict | None = None, chave: str = "orders") -> Iterator[dict]:
        params = dict(params or {})
        params.setdefault("limit", 250)
        url = self._url(path)
        while True:
            r = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            if not r.ok:
                raise RuntimeError(f"Shopify {r.status_code}: {r.text}")
            data = r.json().get(chave, [])
            for item in data:
                yield item
            # paginacao por Link header (cursor-based)
            link = r.headers.get("Link", "")
            next_url = None
            for piece in link.split(","):
                if 'rel="next"' in piece:
                    next_url = piece.split(";")[0].strip(" <>")
                    break
            if not next_url:
                break
            url = next_url
            params = None  # parametros ja estao na URL

    # ------------------------------------------------------------- pedidos
    @staticmethod
    def _to_pedido(p: dict) -> dict:
        return {
            "id": p["id"],
            "numero": p.get("name") or f"#{p.get('order_number')}",
            "valor": float(p["total_price"]),
            "moeda": p["currency"],
            "status_pagamento": p.get("financial_status"),
            "status_envio": p.get("fulfillment_status"),
            "cliente": (p.get("customer") or {}).get("email") or "—",
            "criado_em": p["created_at"],
            "items": [
                {"titulo": li["title"], "qtd": li["quantity"], "preco": float(li["price"])}
                for li in p.get("line_items", [])
            ],
        }

    def pedidos_por_periodo(self, inicio: datetime, fim: datetime, status: str = "any") -> list[dict]:
        params = {
            "status": status,
            "created_at_min": inicio.isoformat(),
            "created_at_max": fim.isoformat(),
        }
        return [self._to_pedido(p) for p in self._paginar("/orders.json", params, "orders")]

    def pedidos_do_dia(self, dia: date | None = None) -> list[dict]:
        dia = dia or date.today()
        inicio = datetime.combine(dia, datetime.min.time(), tzinfo=timezone.utc)
        fim = datetime.combine(dia, datetime.max.time(), tzinfo=timezone.utc)
        return self.pedidos_por_periodo(inicio, fim)

    def pedidos_status(self, status: str) -> list[dict]:
        """status: 'paid', 'pending', 'fulfilled', 'cancelled', etc."""
        # Shopify usa parametros distintos pra cada status — usamos financial_status / fulfillment_status
        param_map = {
            "paid": ("financial_status", "paid"),
            "pending": ("financial_status", "pending"),
            "refunded": ("financial_status", "refunded"),
            "fulfilled": ("fulfillment_status", "fulfilled"),
            "unfulfilled": ("fulfillment_status", "unfulfilled"),
            "cancelled": ("status", "cancelled"),
        }
        if status not in param_map:
            raise ValueError(f"status desconhecido: {status}")
        key, val = param_map[status]
        params = {key: val, "status": "any"}
        return [self._to_pedido(p) for p in self._paginar("/orders.json", params, "orders")]

    def pedido(self, numero: str | int) -> dict | None:
        n = str(numero).lstrip("#")
        # Shopify nao permite busca por order_number direto. Pegamos os ultimos pedidos.
        for p in self._paginar("/orders.json", {"status": "any", "limit": 250}, "orders"):
            if str(p.get("order_number")) == n:
                return self._to_pedido(p)
        return None

    # ------------------------------------------------------------ produtos
    def produtos_estoque_baixo(self, limite: int = 5) -> list[dict]:
        baixo = []
        for prod in self._paginar("/products.json", {"limit": 250}, "products"):
            for v in prod.get("variants", []):
                if v.get("inventory_quantity") is None:
                    continue
                if v["inventory_quantity"] < limite:
                    baixo.append(
                        {
                            "produto": prod["title"],
                            "variante": v.get("title") or "",
                            "sku": v.get("sku") or "",
                            "estoque": v["inventory_quantity"],
                            "variant_id": v["id"],
                            "inventory_item_id": v.get("inventory_item_id"),
                        }
                    )
        baixo.sort(key=lambda x: x["estoque"])
        return baixo

    # ------------------------------------------------------------- resumo
    def resumo_dia(self, dia: date | None = None) -> dict:
        pedidos = self.pedidos_do_dia(dia)
        total = sum(p["valor"] for p in pedidos)
        produtos: dict[str, dict] = {}
        for p in pedidos:
            for li in p["items"]:
                if li["titulo"] not in produtos:
                    produtos[li["titulo"]] = {"titulo": li["titulo"], "qtd": 0, "receita": 0.0}
                produtos[li["titulo"]]["qtd"] += li["qtd"]
                produtos[li["titulo"]]["receita"] += li["qtd"] * li["preco"]
        top = sorted(produtos.values(), key=lambda x: -x["receita"])[:5]
        return {
            "dia": (dia or date.today()).isoformat(),
            "pedidos": len(pedidos),
            "faturamento": round(total, 2),
            "ticket_medio": round(total / len(pedidos), 2) if pedidos else 0.0,
            "top_produtos": top,
            "pendentes": sum(1 for p in pedidos if p["status_pagamento"] == "pending"),
            "cancelados": sum(1 for p in pedidos if p["status_pagamento"] == "refunded" or p.get("status") == "cancelled"),
        }

    # ----------------------------------------------------------- estoque
    def atualizar_estoque(self, inventory_item_id: int, location_id: int, novo_estoque: int) -> dict:
        """Ajusta o estoque absoluto de uma variante numa location."""
        data = {
            "location_id": location_id,
            "inventory_item_id": inventory_item_id,
            "available": novo_estoque,
        }
        r = requests.post(
            self._url("/inventory_levels/set.json"),
            headers=self._headers(),
            data=json.dumps(data),
            timeout=self.timeout,
        )
        if not r.ok:
            raise RuntimeError(f"Shopify {r.status_code}: {r.text}")
        return r.json()


# ----------------------------------------------------------------- CLI
def _print_json(obj) -> None:
    print(json.dumps(obj, default=str, indent=2, ensure_ascii=False))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: shopify_cliente.py <pedidos-hoje | resumo-dia | estoque-baixo [N] | pedido NUMERO>")
    cmd = sys.argv[1]
    c = ShopifyCliente()
    if cmd == "pedidos-hoje":
        _print_json(c.pedidos_do_dia())
    elif cmd == "resumo-dia":
        _print_json(c.resumo_dia())
    elif cmd == "estoque-baixo":
        limite = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        _print_json(c.produtos_estoque_baixo(limite))
    elif cmd == "pedido":
        if len(sys.argv) < 3:
            sys.exit("uso: shopify_cliente.py pedido NUMERO")
        p = c.pedido(sys.argv[2])
        if not p:
            sys.exit("nao encontrado")
        _print_json(p)
    else:
        sys.exit(f"comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
