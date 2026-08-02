# Integração 8 — Webhook Genérico

Dois utilitários pra trabalhar com **qualquer ferramenta que fale webhook**:

1. **`webhook_receiver.py`** — servidor HTTP leve que recebe POSTs, valida assinatura (HMAC) e dispara lógica.
2. **`disparar_webhook.py`** — helper pra mandar webhook (notificar você no privado quando algo acontecer, integrar com Zapier/Make/n8n, postar em Slack/Discord/Zappfy).

## Casos de uso

| Origem do webhook | O que dá pra fazer |
|---|---|
| Stripe (`payment_intent.succeeded`) | Manda WhatsApp "💰 R$ 297 caiu" + cria task no ClickUp |
| Shopify (`orders/create`) | Notifica seu privado + grava no Sheets |
| Calendly (`invitee.created`) | Cria lead no ClickUp + atualiza Notion |
| Typeform/JotForm | Adiciona lead na planilha + dispara régua de e-mail |
| ManyChat/RD Station | Cruza com Stripe pra ver se já é cliente |
| Zappfy / Cloud API | Você recebe a mensagem no webhook e o servidor responde |
| Qualquer SaaS com webhook | Plugue aqui |

## Setup — 10 minutos

### 1. Instalar dependências

```bash
pip install flask requests
```

### 2. Definir o secret

Gere um secret aleatório (usado pra validar assinatura HMAC do remetente):

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Salve em `~/.credentials/webhook.env`:

```
WEBHOOK_SECRET=cole_aqui_o_secret_de_64_hex
WEBHOOK_PORT=8080
```

### 3. Subir o receiver

```bash
export $(cat ~/.credentials/webhook.env | xargs)
python webhook_receiver.py
```

Vai abrir um servidor em `http://0.0.0.0:8080`. Pra expor pra internet:

- **Local com ngrok** (testes): `ngrok http 8080` — vai te dar uma URL `https://...ngrok.io`.
- **Servidor cloud** (produção): Coolify / Render / Railway / VPS — bind no `0.0.0.0` e configure HTTPS via reverse proxy.

### 4. Configurar no SaaS de origem

Cada SaaS tem uma seção "Webhooks". Cole a URL pública (`https://seu-dominio.com/webhook`) e configure os **eventos** que quer receber.

Onde encontrar:
- **Stripe:** Dashboard → Developers → Webhooks → Add endpoint
- **Shopify:** Admin → Settings → Notifications → Webhooks
- **Calendly:** /integrations/api_webhooks → Create Webhook
- **Typeform:** form → Connect → Webhooks
- **Zappfy:** Painel → Webhook configurável

### 5. Testar o disparo

```bash
python disparar_webhook.py "https://seu-dominio.com/webhook" \
    --evento teste \
    --dados '{"mensagem":"teste de fogo"}' \
    --secret $WEBHOOK_SECRET
```

Você deve ver no terminal do receiver o evento chegando.

## Como funciona (resumo técnico)

### Receiver

- `POST /webhook` recebe qualquer JSON.
- Header `X-Signature` é validado por HMAC-SHA256 com `WEBHOOK_SECRET`.
- Se válido, o evento é roteado pra um **handler** registrado por nome.
- Você adiciona handlers editando o `HANDLERS` dict no script.

Exemplo de handler:

```python
def handle_stripe_payment(payload):
    valor = payload["data"]["object"]["amount"] / 100
    moeda = payload["data"]["object"]["currency"].upper()
    # manda WhatsApp via Zappfy
    disparar_zappfy(f"💰 {moeda} {valor:.2f} caiu no Stripe")
    return {"ok": True}

HANDLERS = {
    "payment_intent.succeeded": handle_stripe_payment,
    # ...
}
```

### Disparador

```python
from disparar_webhook import disparar
disparar(
    url="https://hooks.zapier.com/...",
    evento="lead.novo",
    dados={"nome": "Pedro", "telefone": "5521..."},
    secret=None,  # se a outra ponta usar HMAC
)
```

## Notificação no WhatsApp via Zappfy (template)

Adicione em `webhook_receiver.py`:

```python
import os, requests

def disparar_zappfy(mensagem: str, para: str = None):
    para = para or os.environ.get("WHATSAPP_DESTINO")
    url = os.environ.get("ZAPPFY_URL_ENVIO")  # endpoint da sua instancia
    r = requests.post(url, json={"para": para, "mensagem": mensagem})
    r.raise_for_status()
```

## Exemplos prontos

Veja **`exemplos.md`** — 5 receitas (Stripe → WhatsApp, Shopify → Sheets, Calendly → ClickUp, formulário → CRM, monitoramento de erro de API).

## Segurança

- **Sempre valide HMAC.** O receiver já faz isso. Se desabilitar, qualquer um pode disparar seu handler.
- **Use HTTPS na URL pública.** Senão o secret vaza no caminho.
- **Rate limit / IP whitelist** em produção (atrás de Cloudflare ou reverse proxy).
- **Logs sem PII.** Não logue corpo inteiro do webhook — pode ter dado sensível do cliente.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Signature mismatch` | Secret diferente entre quem dispara e quem recebe | Confira `WEBHOOK_SECRET` nas duas pontas |
| Receiver não responde | Porta bloqueada / firewall | Confirme `lsof -i :8080` e abra a porta |
| 405 Method Not Allowed | Webhook está mandando GET | A maioria dos SaaS usa POST — confira config |

---

