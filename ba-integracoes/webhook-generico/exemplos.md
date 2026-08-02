# Webhook Genérico — 5 Receitas

## 1. Stripe → WhatsApp (notificar venda em tempo real)

**Receptor:** rodando no VPS em `https://seu-dom.com/webhook`.

**Configuração no Stripe:**
- Dashboard → Developers → Webhooks → Add endpoint.
- URL: `https://seu-dom.com/webhook`.
- Eventos: `payment_intent.succeeded`, `charge.refunded`.
- Stripe envia automaticamente o header `Stripe-Signature`.

**Handler no `webhook_receiver.py`:**

```python
def handle_stripe_payment(payload):
    obj = payload["data"]["object"]
    valor = obj["amount"] / 100
    moeda = obj["currency"].upper()
    cliente = obj.get("receipt_email", "—")
    disparar_zappfy(
        para=os.environ["MEU_WHATSAPP"],
        mensagem=f"💰 Pagamento aprovado!\n{moeda} {valor:.2f}\nCliente: {cliente}",
    )
    return {"ok": True}

HANDLERS["payment_intent.succeeded"] = handle_stripe_payment
```

## 2. Shopify → Google Sheets (todo pedido vira linha)

**Configuração no Shopify:** Admin → Settings → Notifications → Webhooks → Add `orders/create` apontando pra `https://seu-dom.com/webhook`.

**Handler:**

```python
def handle_shopify_order(payload):
    # Combinar com integracao google-sheets (chamada via MCP nao funciona dentro do receiver — use API direta).
    # Aqui exemplificamos com requests pra Apps Script ou um endpoint que escreve.
    requests.post(
        os.environ["SHEETS_APPSCRIPT_URL"],  # um Google Apps Script publicado como Web App
        json={
            "aba": "Pedidos",
            "linha": {
                "numero": payload["order_number"],
                "valor": payload["total_price"],
                "cliente": payload["customer"]["email"],
                "data": payload["created_at"],
            },
        },
    )
    return {"ok": True}

HANDLERS["orders/create"] = handle_shopify_order
```

## 3. Calendly → ClickUp (toda reunião agendada vira task)

**Configuração no Calendly:** /integrations/api_webhooks → Create webhook → eventos `invitee.created`, `invitee.canceled` → URL `https://seu-dom.com/webhook`.

**Handler:**

```python
def handle_calendly_invitee(payload):
    p = payload["payload"]
    nome = p["name"]
    email = p["email"]
    titulo = p["event_type"]["name"]
    quando = p["start_time"]

    # Cria task no ClickUp via API direta
    requests.post(
        f"https://api.clickup.com/api/v2/list/{LIST_ID_FOLLOWUP}/task",
        headers={"Authorization": CLICKUP_TOKEN, "Content-Type": "application/json"},
        json={
            "name": f"Reunião com {nome}",
            "description": f"Email: {email}\nQuando: {quando}\nTipo: {titulo}",
            "due_date": int(_iso_to_ms(quando)),
            "priority": 2,
        },
    )
    return {"ok": True}

HANDLERS["invitee.created"] = handle_calendly_invitee
```

## 4. Typeform / JotForm → CRM

**Configuração:** No form, "Connect → Webhooks" → URL `https://seu-dom.com/webhook`.

**Handler:** o payload do form vira lead na planilha + cria task de follow-up.

```python
def handle_form_submit(payload):
    respostas = {a["field"]["title"]: a["text"] or a["choice"]["label"]
                 for a in payload["form_response"]["answers"]}
    nome = respostas.get("Qual seu nome?")
    telefone = respostas.get("Telefone")

    # 1) registra na planilha (via apps script ou API)
    # 2) cria task no ClickUp
    # 3) manda no WhatsApp do SDR
    disparar_zappfy(
        para=os.environ["SDR_WHATSAPP"],
        mensagem=f"🟢 Lead novo:\n{nome}\n{telefone}\nResponder em <5min",
    )
    return {"ok": True}

HANDLERS["form_response"] = handle_form_submit
```

## 5. Monitoramento de erro de API

**Cenário:** sua aplicação interna dispara webhook quando algo crítico falha.

**No disparador (`disparar_webhook.py`):**

```python
from disparar_webhook import disparar
disparar(
    url="https://seu-dom.com/webhook",
    evento="erro.critico",
    dados={
        "servico": "checkout",
        "erro": "timeout no gateway",
        "stacktrace": "...",
    },
    secret=os.environ["WEBHOOK_SECRET"],
)
```

**Handler:** dispara mensagem urgente no WhatsApp do CTO + cria task urgente no ClickUp.

```python
def handle_erro_critico(payload):
    d = payload["dados"]
    disparar_zappfy(
        para=os.environ["CTO_WHATSAPP"],
        mensagem=f"🚨 ERRO CRÍTICO\nServiço: {d['servico']}\nErro: {d['erro']}",
    )
    return {"ok": True}

HANDLERS["erro.critico"] = handle_erro_critico
```

## Subir em produção (Coolify / VPS)

`docker-compose.yml`:

```yaml
services:
  webhook:
    build: .
    environment:
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
      - WEBHOOK_PORT=8080
    ports:
      - "8080:8080"
    restart: unless-stopped
```

`Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY webhook_receiver.py .
COPY disparar_webhook.py .
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "webhook_receiver.py"]
```

Coloque atrás de um reverse proxy (Caddy / Traefik / nginx) com HTTPS automático.

---

