# Deploy em produção (Coolify / VPS / Docker)

Pacote pra subir o webhook receiver + os scripts em um servidor que fica **ligado 24/7**.

## Por que precisa?

- Cron no seu Mac so roda se o Mac estiver ligado.
- Webhook receiver precisa de URL publica HTTPS — seu Mac nao tem.
- Servidor cloud cheap (R$ 20-40/mes) resolve.

## O que vem aqui

```
deploy/
├── Dockerfile
├── docker-compose.yml
├── .env.template
├── crontab-server
└── INSTALACAO-COOLIFY.md
```

## Stack recomendada

| Camada | Opcao |
|---|---|
| **VPS** | Coolify self-hosted (R$ 0 se ja tem) OU Railway/Render (R$ 30/mes) OU Hetzner CX11 (R$ 20/mes) |
| **HTTPS** | Caddy (HTTPS automatico) OU Traefik OU nginx + certbot |
| **Cron** | docker-compose service com `crond` OU host cron chamando `docker exec` |
| **Logs** | Stdout (capturado pelo Coolify/Docker) OU Logfire OU Better Stack |
| **Secrets** | `.env` no host (NUNCA no Dockerfile) OU Coolify env UI OU Doppler |

## Instalação rapida — Coolify (recomendado pra quem ja tem)

Veja **`INSTALACAO-COOLIFY.md`** — passo a passo com prints mentais (`Resources → New → Public Repository → este repo → ...`).

## Instalação rapida — Docker Compose puro

```bash
git clone <repo-com-este-pack> /opt/integracoes
cd /opt/integracoes/10-pack-integracoes/deploy

# 1) Crie .env com suas credenciais
cp .env.template .env
nano .env  # edite SLACK_WEBHOOK_URL, WEBHOOK_SECRET, etc.

# 2) Suba
docker compose up -d

# 3) Confira logs
docker compose logs -f webhook
```

O `docker-compose.yml` sobe:
- **webhook** (porta 8080) — receiver do `webhook-generico`
- **scheduler** (cron) — roda os fluxos do `orquestrador` nos horarios certos

## Configurar HTTPS publico

Se voce ja tem dominio:

```yaml
# adicione um reverse proxy ao docker-compose.yml
services:
  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
```

`Caddyfile`:
```
webhook.seudominio.com {
    reverse_proxy webhook:8080
}
```

Caddy renova certificado automaticamente. Setup HTTPS em <2 minutos.

## Smoke test depois do deploy

```bash
# 1) Healthcheck
curl https://webhook.seudominio.com/healthz
# espera: {"ok":true,"ts":"..."}

# 2) Disparar webhook de teste
python /opt/integracoes/10-pack-integracoes/webhook-generico/disparar_webhook.py \
    https://webhook.seudominio.com/webhook \
    --evento teste \
    --dados '{"mensagem":"ola"}' \
    --secret $WEBHOOK_SECRET

# 3) Cheque logs
docker compose logs --tail 20 webhook | grep teste
```

Se o log mostra "[teste] payload recebido" → deploy ok.

## Segurança

- **`.env` no host, nunca no Dockerfile.** Docker imagem nao pode conter secrets.
- **HTTPS sempre.** HTTP vaza o webhook secret.
- **Restringe a porta 8080** ao reverse proxy local (`expose: 8080` em vez de `ports: "8080:8080"`).
- **Firewall** so libera 80/443 publicamente.
- **Backups** das credenciais — voce nao quer recriar tokens manualmente se o host morrer.

---

