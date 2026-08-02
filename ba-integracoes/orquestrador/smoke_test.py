#!/usr/bin/env python3
"""
Smoke test do pack — valida que todas integracoes configuradas respondem.

Le as variaveis de ambiente e roda um teste minimo (read-only) em cada
integracao habilitada. Mostra uma tabela de status.

Uso:
    python smoke_test.py

Saida (esperada):

  Stripe          [OK]   conectado (live mode)
  Shopify         [OK]   loja sua-loja.myshopify.com
  Calendly        [SKIP] CALENDLY_TOKEN nao definido
  RD Station      [OK]   3 deal_stages encontrados
  Pipedrive       [FAIL] 401 — confira PIPEDRIVE_TOKEN
  Slack webhook   [OK]   ok
  Discord webhook [SKIP] nao configurado
  Telegram        [OK]   bot @meubot, chat 12345

Codigo de saida:
  0 — tudo OK ou SKIP
  1 — alguma integracao FAIL
"""
from __future__ import annotations

import json
import os
import sys

try:
    import requests
except ImportError:
    sys.exit("erro: pip install requests")


VERDE = "\033[92m"
VERM = "\033[91m"
AMAR = "\033[93m"
RST = "\033[0m"

resultados: list[tuple[str, str, str]] = []  # (nome, status, detalhe)


def _add(nome, status, detalhe=""):
    cor = {"OK": VERDE, "FAIL": VERM, "SKIP": AMAR}[status]
    resultados.append((nome, f"{cor}[{status}]{RST}", detalhe))


def check_stripe():
    k = os.environ.get("STRIPE_API_KEY")
    if not k:
        return _add("Stripe", "SKIP", "STRIPE_API_KEY nao definido")
    try:
        r = requests.get("https://api.stripe.com/v1/account", auth=(k, ""), timeout=10)
        if r.ok:
            modo = "test" if "test" in k else "live"
            return _add("Stripe", "OK", f"conectado ({modo} mode)")
        return _add("Stripe", "FAIL", f"{r.status_code}: {r.text[:80]}")
    except Exception as e:
        return _add("Stripe", "FAIL", str(e)[:80])


def check_shopify():
    shop = os.environ.get("SHOPIFY_SHOP")
    tok = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    if not (shop and tok):
        return _add("Shopify", "SKIP", "SHOPIFY_SHOP/TOKEN nao definidos")
    try:
        r = requests.get(
            f"https://{shop}/admin/api/2024-10/shop.json",
            headers={"X-Shopify-Access-Token": tok},
            timeout=10,
        )
        if r.ok:
            return _add("Shopify", "OK", f"loja {shop}")
        return _add("Shopify", "FAIL", f"{r.status_code}")
    except Exception as e:
        return _add("Shopify", "FAIL", str(e)[:80])


def check_calendly():
    tok = os.environ.get("CALENDLY_TOKEN")
    if not tok:
        return _add("Calendly", "SKIP", "CALENDLY_TOKEN nao definido")
    try:
        r = requests.get(
            "https://api.calendly.com/users/me",
            headers={"Authorization": f"Bearer {tok}"},
            timeout=10,
        )
        if r.ok:
            usr = r.json().get("resource", {}).get("email", "—")
            return _add("Calendly", "OK", f"user {usr}")
        return _add("Calendly", "FAIL", f"{r.status_code}")
    except Exception as e:
        return _add("Calendly", "FAIL", str(e)[:80])


def check_rd():
    tok = os.environ.get("RD_TOKEN")
    if not tok:
        return _add("RD Station", "SKIP", "RD_TOKEN nao definido")
    try:
        r = requests.get(f"https://crm.rdstation.com/api/v1/deal_stages?token={tok}", timeout=10)
        if r.ok:
            qtd = len(r.json().get("deal_stages") or [])
            return _add("RD Station", "OK", f"{qtd} deal_stages encontrados")
        return _add("RD Station", "FAIL", f"{r.status_code}")
    except Exception as e:
        return _add("RD Station", "FAIL", str(e)[:80])


def check_pipedrive():
    tok = os.environ.get("PIPEDRIVE_TOKEN")
    dom = os.environ.get("PIPEDRIVE_DOMAIN")
    if not (tok and dom):
        return _add("Pipedrive", "SKIP", "TOKEN/DOMAIN nao definidos")
    try:
        r = requests.get(f"https://{dom}.pipedrive.com/api/v1/users/me?api_token={tok}", timeout=10)
        if r.ok:
            usr = (r.json().get("data") or {}).get("name", "—")
            return _add("Pipedrive", "OK", f"user {usr}")
        return _add("Pipedrive", "FAIL", f"{r.status_code}")
    except Exception as e:
        return _add("Pipedrive", "FAIL", str(e)[:80])


def check_slack():
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        return _add("Slack webhook", "SKIP", "SLACK_WEBHOOK_URL nao definido")
    if not url.startswith("https://hooks.slack.com/"):
        return _add("Slack webhook", "FAIL", "URL fora do formato esperado")
    return _add("Slack webhook", "OK", "URL valida (nao envia mensagem real)")


def check_discord():
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        return _add("Discord webhook", "SKIP", "DISCORD_WEBHOOK_URL nao definido")
    if "discord.com/api/webhooks" not in url:
        return _add("Discord webhook", "FAIL", "URL fora do formato")
    return _add("Discord webhook", "OK", "URL valida")


def check_telegram():
    tok = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not (tok and chat):
        return _add("Telegram", "SKIP", "TOKEN/CHAT nao definidos")
    try:
        r = requests.get(f"https://api.telegram.org/bot{tok}/getMe", timeout=10)
        if r.ok and r.json().get("ok"):
            return _add("Telegram", "OK", f"bot @{r.json()['result']['username']}, chat {chat}")
        return _add("Telegram", "FAIL", f"{r.status_code}")
    except Exception as e:
        return _add("Telegram", "FAIL", str(e)[:80])


def main():
    print("\nSmoke test do pack-integracoes\n" + "=" * 60)
    for fn in (
        check_stripe,
        check_shopify,
        check_calendly,
        check_rd,
        check_pipedrive,
        check_slack,
        check_discord,
        check_telegram,
    ):
        try:
            fn()
        except Exception as e:
            _add(fn.__name__, "FAIL", str(e)[:80])

    largura_nome = max(len(r[0]) for r in resultados)
    for nome, status, detalhe in resultados:
        print(f"  {nome.ljust(largura_nome)}  {status}  {detalhe}")

    falhas = sum(1 for _, s, _ in resultados if "FAIL" in s)
    oks = sum(1 for _, s, _ in resultados if "OK" in s)
    skips = sum(1 for _, s, _ in resultados if "SKIP" in s)

    print("=" * 60)
    print(f"  {oks} OK   {falhas} FAIL   {skips} SKIP")
    sys.exit(1 if falhas > 0 else 0)


if __name__ == "__main__":
    main()
