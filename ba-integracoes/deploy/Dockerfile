FROM python:3.11-slim

# build-time deps (compilers para psycopg2 etc — leves)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala deps Python uma camada antes do copy pra cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o pack inteiro
COPY .. /app/pack/

# Pasta de logs
RUN mkdir -p /var/log/integracoes

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/Sao_Paulo

EXPOSE 8080

# Entrypoint: roda o webhook (overridable por docker-compose service)
CMD ["python", "/app/pack/webhook-generico/webhook_receiver.py"]
