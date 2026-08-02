#!/usr/bin/env python3
"""
Receiver de webhook generico — recebe POSTs, valida HMAC e roteia por evento.

Configuracao via variaveis de ambiente:
    WEBHOOK_SECRET — secret usado pra validar HMAC (obrigatorio)
    WEBHOOK_PORT   — porta (default 8080)

Para registrar um handler, adicione no dict HANDLERS:
    HANDLERS["payment_intent.succeeded"] = handle_stripe_payment

Para subir:
    export WEBHOOK_SECRET=...
    python webhook_receiver.py

Para testar:
    python disparar_webhook.py http://localhost:8080/webhook \\
        --evento teste --dados '{"mensagem":"ola"}' --secret $WEBHOOK_SECRET

"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import sys
from datetime import datetime

try:
    from flask import Flask, request, jsonify
except ImportError:
    sys.exit("erro: instale 'flask' (pip install flask)")


WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "").encode()
PORT = int(os.environ.get("WEBHOOK_PORT", "8080"))

if not WEBHOOK_SECRET:
    sys.exit("erro: defina WEBHOOK_SECRET (ex: export WEBHOOK_SECRET=hex_de_64_chars)")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("webhook")


# ---------------------------------------------------------------------------
# Handlers — registre os seus aqui
# ---------------------------------------------------------------------------

def handle_teste(payload: dict) -> dict:
    log.info(f"[teste] payload recebido: {payload}")
    return {"ok": True, "echo": payload}


def handle_stripe_payment(payload: dict) -> dict:
    """Exemplo — Stripe payment_intent.succeeded"""
    obj = payload.get("data", {}).get("object", {})
    valor_centavos = obj.get("amount", 0)
    moeda = (obj.get("currency") or "brl").upper()
    log.info(f"[stripe] pagamento {valor_centavos/100:.2f} {moeda}")
    # disparar_zappfy(f"💰 {moeda} {valor_centavos/100:.2f} caiu no Stripe")
    return {"ok": True}


def handle_shopify_order(payload: dict) -> dict:
    """Exemplo — Shopify orders/create"""
    numero = payload.get("order_number")
    valor = float(payload.get("total_price", 0))
    cliente = (payload.get("customer") or {}).get("email", "—")
    log.info(f"[shopify] pedido #{numero} | R$ {valor:.2f} | {cliente}")
    # disparar_zappfy(f"🛍️ Pedido #{numero} - R$ {valor:.2f} - {cliente}")
    return {"ok": True}


def handle_calendly_invitee(payload: dict) -> dict:
    """Exemplo — Calendly invitee.created"""
    convidado = (payload.get("payload") or {}).get("email", "—")
    evento = (payload.get("payload") or {}).get("event_type", {}).get("name", "—")
    log.info(f"[calendly] {convidado} agendou: {evento}")
    return {"ok": True}


HANDLERS = {
    "teste": handle_teste,
    "payment_intent.succeeded": handle_stripe_payment,
    "orders/create": handle_shopify_order,
    "invitee.created": handle_calendly_invitee,
    # registre os seus aqui
}


# ---------------------------------------------------------------------------
# HMAC
# ---------------------------------------------------------------------------

def _verificar_hmac(body: bytes, signature_header: str | None) -> bool:
    """Aceita formato 'sha256=HEX' (Stripe-style) ou 'HEX' puro."""
    if not signature_header:
        return False
    valor = signature_header.split("=", 1)[-1]
    esperado = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, valor)


# ---------------------------------------------------------------------------
# App Flask
# ---------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"ok": True, "ts": datetime.utcnow().isoformat() + "Z"})


@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data() or b""

    # 1) Validacao HMAC (header X-Signature ou Stripe-Signature)
    sig = request.headers.get("X-Signature") or request.headers.get("Stripe-Signature")
    if not _verificar_hmac(body, sig):
        log.warning(f"hmac invalido — origem {request.remote_addr}")
        return jsonify({"erro": "signature mismatch"}), 401

    # 2) Parse JSON
    try:
        payload = json.loads(body.decode("utf-8") or "{}")
    except json.JSONDecodeError as e:
        log.warning(f"payload invalido: {e}")
        return jsonify({"erro": "json invalido"}), 400

    # 3) Identifica o evento (campo "evento" do disparador OU "type" do Stripe etc.)
    evento = payload.get("evento") or payload.get("type") or payload.get("event_type") or "desconhecido"

    handler = HANDLERS.get(evento)
    if not handler:
        log.info(f"evento sem handler: {evento}")
        return jsonify({"ok": False, "motivo": f"sem handler pra '{evento}'"}), 200

    try:
        resultado = handler(payload)
    except Exception as e:
        log.exception(f"erro no handler '{evento}': {e}")
        return jsonify({"erro": str(e)}), 500

    return jsonify(resultado), 200


if __name__ == "__main__":
    log.info(f"webhook receiver subindo na porta {PORT}")
    log.info(f"handlers registrados: {sorted(HANDLERS.keys())}")
    # debug=False em producao; reloader=False evita rodar 2x
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)
