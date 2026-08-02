# Instalacao no Coolify

Coolify e a alternativa self-hosted ao Render/Railway/Heroku. Se voce ja roda Coolify, este pack instala em 10 minutos.

## Pre-requisitos

- Coolify v4+ rodando.
- Um dominio com DNS apontando pro IP do Coolify (ex: `webhook.seudominio.com.br`).

## Passo 1 — Criar o repo

Coloque o `10-pack-integracoes/` num repo Git privado seu (GitHub, GitLab, Gitea):

```bash
cd /Users/bravy/Documents/www/11-criacao-materiais
gh repo create asv-digital/pack-integracoes --private
cd 10-pack-integracoes
git init && git add . && git commit -m "initial" && git push -u origin main
```

## Passo 2 — Criar Application no Coolify

1. Coolify Dashboard → **+ New → Resource → Application**.
2. **Type:** Public/Private Repository.
3. **Repository URL:** `git@github.com:asv-digital/pack-integracoes.git` (use deploy key se privado).
4. **Branch:** `main`.
5. **Build Pack:** Docker Compose.
6. **Base Directory:** `deploy/`.
7. **Docker Compose Location:** `docker-compose.yml`.

## Passo 3 — Variaveis de ambiente

Em **Environment Variables**, cole o `.env.template` preenchido com suas credenciais reais.

**Atencao:**
- Gere o `WEBHOOK_SECRET` com `python3 -c "import secrets; print(secrets.token_hex(32))"`.
- Os tokens de Stripe/Shopify/RD/Pipedrive sao opcionais — preencha so o que voce vai usar.

## Passo 4 — Dominio + HTTPS

1. Em **Domains**, adicione `webhook.seudominio.com.br`.
2. Coolify gerencia HTTPS via Lets Encrypt automaticamente (com Traefik).
3. Se voce usar o `Caddyfile` que vem no pack em vez do Traefik do Coolify, ajuste pra o `webhook` ficar acessivel pelo proxy interno do Coolify.

## Passo 5 — Deploy

Clique em **Deploy**. Acompanhe os logs.

Após o build terminar:
- `https://webhook.seudominio.com.br/healthz` deve responder `{"ok":true}`.
- O container `scheduler` deve aparecer rodando (cron interno).

## Passo 6 — Smoke test

```bash
python /caminho/local/webhook-generico/disparar_webhook.py \
    https://webhook.seudominio.com.br/webhook \
    --evento teste \
    --dados '{"mensagem":"smoke"}' \
    --secret $WEBHOOK_SECRET
```

No Coolify, vá em **Logs** do container `webhook` e confira a entrada do payload.

## Passo 7 — Configurar webhooks nos SaaS

Cada SaaS aponta pra `https://webhook.seudominio.com.br/webhook`:

| SaaS | Onde configurar | Eventos uteis |
|---|---|---|
| **Stripe** | Dashboard → Developers → Webhooks | `payment_intent.succeeded`, `charge.refunded`, `customer.subscription.deleted` |
| **Shopify** | Admin → Settings → Notifications → Webhooks | `orders/create`, `orders/paid` |
| **Calendly** | /integrations/api_webhooks | `invitee.created`, `invitee.canceled` |
| **RD Station** | Configuracoes → Integracoes → Webhooks | `deal.won`, `deal.lost` |
| **Typeform** | Form → Connect → Webhooks | `form_response` |

## Passo 8 — Monitoramento

- Coolify mostra healthcheck status na dashboard.
- Logs persistem em `/var/log/integracoes/` dentro do container `scheduler` (mapeie como volume se quiser persistir entre restarts).
- Se algum cron falhar, configure um `notificador.py` extra com canal `telegram` pra te avisar.

## Troubleshooting

| Sintoma | Causa | Solucao |
|---|---|---|
| Build falha em `pip install` | Versao Python errada | Confirme `FROM python:3.11-slim` no Dockerfile |
| Container reinicia em loop | `.env` faltando WEBHOOK_SECRET | Coolify → Env Vars |
| Webhook responde 401 | Secret mal configurado | Re-gere e atualize nos 2 lados |
| Cron nao roda | Container `scheduler` parado | `docker compose logs scheduler` |
| HTTPS nao funciona | DNS nao propagou | `dig webhook.seudominio.com.br` deve apontar pro IP do Coolify |

---

