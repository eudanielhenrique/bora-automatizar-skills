#!/usr/bin/env python3
"""
Notificador unificado — Slack, Discord, Telegram.

WhatsApp fica de fora: o Bora Automatizar ja tem sistema proprio pra isso.

Mesma interface pra qualquer canal:

    n = Notificador.do_env()
    n.enviar("Mensagem")

Configuracao via env:
    NOTIFICADOR_CANAL=slack | discord | telegram
    SLACK_WEBHOOK_URL=...
    DISCORD_WEBHOOK_URL=...
    TELEGRAM_BOT_TOKEN=... + TELEGRAM_CHAT_ID=...

Uso CLI:
    echo "mensagem" | python notificador.py [--canal slack|discord|telegram]
    echo "alerta" | python notificador.py --canal "slack,telegram"  # multi
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Iterable

try:
    import requests
except ImportError:
    sys.exit("erro: pip install requests")


class _BackendBase:
    nome = ""
    def enviar(self, msg: str) -> None:
        raise NotImplementedError


class SlackBackend(_BackendBase):
    nome = "slack"
    def __init__(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL nao definido")
        self.url = webhook_url

    def enviar(self, msg: str) -> None:
        # slack suporta markdown leve e tem limite de 40k chars (mais que suficiente)
        r = requests.post(self.url, json={"text": msg}, timeout=20)
        r.raise_for_status()


class DiscordBackend(_BackendBase):
    nome = "discord"
    def __init__(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL nao definido")
        self.url = webhook_url

    def enviar(self, msg: str) -> None:
        # discord limita 2000 chars; quebra em pedacos automaticamente
        for chunk in _chunks(msg, 1900):
            r = requests.post(self.url, json={"content": chunk}, timeout=20)
            r.raise_for_status()


class TelegramBackend(_BackendBase):
    nome = "telegram"
    def __init__(self, token: str, chat_id: str):
        if not (token and chat_id):
            raise ValueError("TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID obrigatorios")
        self.token = token
        self.chat_id = chat_id

    def enviar(self, msg: str) -> None:
        # telegram limita 4096 chars
        for chunk in _chunks(msg, 4000):
            r = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat_id, "text": chunk, "disable_web_page_preview": True},
                timeout=20,
            )
            r.raise_for_status()


def _chunks(s: str, n: int) -> Iterable[str]:
    s = s or ""
    if len(s) <= n:
        yield s
        return
    while s:
        yield s[:n]
        s = s[n:]


class Notificador:
    """Camada que envia em 1 canal OU em varios."""
    def __init__(self, backends: list[_BackendBase]):
        if not backends:
            raise ValueError("pelo menos 1 backend")
        self.backends = backends

    def enviar(self, msg: str) -> None:
        erros = []
        for b in self.backends:
            try:
                b.enviar(msg)
            except Exception as e:
                erros.append(f"{b.nome}: {e}")
        if erros:
            raise RuntimeError("falhas: " + " | ".join(erros))

    # ---------- factories ----------
    @classmethod
    def do_env(cls, canal_override: str | None = None) -> "Notificador":
        canal = canal_override or os.environ.get("NOTIFICADOR_CANAL", "slack")
        canais = [c.strip().lower() for c in canal.split(",") if c.strip()]
        backends: list[_BackendBase] = []
        for c in canais:
            if c == "slack":
                backends.append(SlackBackend(os.environ.get("SLACK_WEBHOOK_URL", "")))
            elif c == "discord":
                backends.append(DiscordBackend(os.environ.get("DISCORD_WEBHOOK_URL", "")))
            elif c == "telegram":
                backends.append(TelegramBackend(
                    os.environ.get("TELEGRAM_BOT_TOKEN", ""),
                    os.environ.get("TELEGRAM_CHAT_ID", ""),
                ))
            else:
                raise ValueError(f"canal desconhecido: {c}")
        return cls(backends)

    @classmethod
    def multi(cls, notificadores: list["Notificador"]) -> "Notificador":
        backends = [b for n in notificadores for b in n.backends]
        return cls(backends)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enviar mensagem em Slack/Discord/Telegram")
    parser.add_argument("--canal", default=None, help="slack | discord | telegram (csv pra multi)")
    parser.add_argument("--mensagem", default=None, help="se nao passar, le de stdin")
    parser.add_argument("--prefixo", default="")
    args = parser.parse_args()

    texto = args.mensagem if args.mensagem else sys.stdin.read()
    if not texto.strip():
        sys.exit("erro: mensagem vazia")
    n = Notificador.do_env(canal_override=args.canal)
    n.enviar(args.prefixo + texto)
    print(f"OK enviado em {len(n.backends)} canal(is)", file=sys.stderr)


if __name__ == "__main__":
    main()
