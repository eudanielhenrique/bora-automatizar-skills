# Notificadores (Slack, Discord, Telegram)

Modulo unico que envia mensagem em **qualquer um dos 3 canais** com a mesma interface. Pra voce nao precisar reescrever o disparador toda vez que muda de canal.

**WhatsApp fica de fora** — o Bora Automatizar ja tem sistema proprio pra isso. Use ele pro canal com o cliente; este modulo e pra alertas internos (time, socios, financeiro).

## Por que existe

- Time tecnico geralmente prefere **Slack** (canal `#alertas`, `#vendas`).
- Comunidade / clientes premium geralmente usa **Discord** (canal de role).
- Socios viajando / dia a dia mobile usa **Telegram** (bot que so chama o seu chat).

Este modulo entrega uma classe `Notificador` com 3 backends e a mesma assinatura `enviar(msg)`. Voce troca o canal mudando 1 variavel.

## O que da pra fazer

```python
from notificador import Notificador

# Pega o canal do env (NOTIFICADOR_CANAL=slack | discord | telegram)
n = Notificador.do_env()
n.enviar("🚨 Alerta: pedido #1234 nao foi processado")

# Multi-canal
echo "Lancamento ao vivo!" | python notificador.py --canal "slack,telegram"
```

## Setup por canal

### Slack — 2 minutos

1. https://api.slack.com/apps → **Create New App** → **From scratch**.
2. Nome, workspace.
3. **Incoming Webhooks** → **Activate** → **Add New Webhook to Workspace** → escolha o canal.
4. Copie a URL (`https://hooks.slack.com/services/T.../B.../...`).
5. `SLACK_WEBHOOK_URL=https://hooks.slack.com/...`

### Discord — 1 minuto

1. Canal Discord → engrenagem → **Editar canal** → **Integracoes** → **Webhooks** → **Novo Webhook**.
2. Copie a URL (`https://discord.com/api/webhooks/...`).
3. `DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...`

### Telegram — 3 minutos

1. No Telegram, fale com `@BotFather` → `/newbot` → de nome → recebe o **bot token**.
2. Mande qualquer mensagem PRA esse bot do seu Telegram pessoal.
3. Acesse `https://api.telegram.org/bot<TOKEN>/getUpdates` no navegador.
4. Procure o `"chat":{"id": NUMERO ...}` — esse e o `TELEGRAM_CHAT_ID`.
5. `TELEGRAM_BOT_TOKEN=...` e `TELEGRAM_CHAT_ID=...`.

## Configurar canal default via env

```bash
# Em ~/.credentials/notificador.env
NOTIFICADOR_CANAL=slack

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

## Uso

```bash
export $(cat ~/.credentials/notificador.env | xargs)

echo "Teste" | python notificador.py
echo "Teste" | python notificador.py --canal discord
echo "Alerta!" | python notificador.py --canal "slack,telegram"
```

Em scripts Python:

```python
from notificador import Notificador
n = Notificador.do_env()
n.enviar(open("relatorio.txt").read())
```

## Roteamento inteligente — quem recebe o que

| Tipo de alerta | Canal |
|---|---|
| Boletim diario do time | Slack #operacao |
| Relatorio semanal pra socios | Telegram privado dos socios |
| Pagamento Stripe (R$ < 500) | Discord #vendas |
| Pagamento Stripe (R$ > 5000) | Telegram do dono + Discord #vendas |
| Erro critico (CTO) | Telegram (vibra mesmo silenciado) |
| Resumo financeiro mensal | Slack #financeiro |
| Cliente / VIP em espera | Sistema proprio de WhatsApp — nao este modulo |

## Seguranca

- **Webhooks sao URLs secretas.** Qualquer um com a URL pode postar no seu canal.
- Nao commite as URLs. Use `~/.credentials/` no `.gitignore`.
- Pra revogar: re-gere o webhook na ferramenta de origem (Slack/Discord) ou re-cria o bot (Telegram).
