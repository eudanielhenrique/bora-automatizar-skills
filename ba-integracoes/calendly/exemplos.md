# Calendly — Exemplos de Uso

## 1. Briefing automático antes da reunião do dia seguinte

```bash
# briefing-amanha.sh
export $(cat ~/.credentials/calendly.env | xargs)

AGENDA=$(python calendly_cliente.py amanha)

# Manda pro Claude pra montar o briefing
claude -p "
Lê esse JSON de reuniões do Calendly de amanhã: $AGENDA

Pra cada reunião:
- Resume quem é o convidado (nome, email, respostas das perguntas)
- Sugere 3 perguntas pra fazer
- Sugere 1 ângulo de abertura

Devolve em formato de briefing executivo pra eu ler antes de cada call.
" > briefing-amanha.txt
```

Cron — todo dia às 18h prepara o dia seguinte:
```cron
0 18 * * 1-5  /caminho/briefing-amanha.sh
```

## 2. Alerta no WhatsApp 30min antes da reunião

```bash
# alerta-reuniao-proxima.sh
export $(cat ~/.credentials/calendly.env | xargs)

python3 -c "
from calendly_cliente import CalendlyCliente
from datetime import datetime, timezone, timedelta
c = CalendlyCliente()
agora = datetime.now(timezone.utc)
for e in c.eventos_hoje():
    inicio = datetime.fromisoformat(e['inicio'].replace('Z','+00:00'))
    delta_min = (inicio - agora).total_seconds() / 60
    if 25 <= delta_min <= 35:
        print(f'⏰ Reuniao em {int(delta_min)}min')
        print(f'Com: {e[\"convidado_nome\"]} ({e[\"convidado_email\"]})')
        print(f'Titulo: {e[\"titulo\"]}')
        if e['questoes']:
            print('Respostas do form:')
            for q in e['questoes']:
                print(f'  - {q[\"pergunta\"]}: {q[\"resposta\"]}')
" | curl -X POST $URL_WEBHOOK_ZAPPFY -H "Content-Type: application/json" \
    -d "$(jq -n --arg para "$SEU_NUMERO" --rawfile msg /dev/stdin '{para: $para, mensagem: $msg}')"
```

Rode a cada 5min:
```cron
*/5 9-18 * * 1-5  /caminho/alerta-reuniao-proxima.sh
```

## 3. Follow-up automático pós-reunião

```python
from calendly_cliente import CalendlyCliente
from datetime import datetime, timezone, timedelta

c = CalendlyCliente()
# eventos que terminaram nas ultimas 2h
agora = datetime.now(timezone.utc)
recentes = c.eventos_por_periodo(agora - timedelta(hours=2), agora, status="active")

for e in recentes:
    fim = datetime.fromisoformat(e["fim"].replace("Z", "+00:00"))
    if fim > agora:
        continue  # ainda nao terminou
    # combinar com integracao webhook: dispara mensagem pro convidado
    print(f"Disparar follow-up pra {e['convidado_email']}")
```

## 4. Investigar no-shows

```python
# Reunioes "ativas" cuja janela ja passou — provavel no-show se nao houve cancelamento
from calendly_cliente import CalendlyCliente
from datetime import datetime, timezone, timedelta

c = CalendlyCliente()
ontem = datetime.now(timezone.utc) - timedelta(days=1)
for e in c.eventos_por_periodo(ontem.replace(hour=0), ontem.replace(hour=23, minute=59), status="active"):
    print(f"{e['inicio']} — {e['convidado_email']} — ver se compareceu")
```

> Calendly não marca no-show automático. Combine com integração de calendário (Google Calendar) ou com a sua plataforma de reunião (Zoom/Meet) pra detectar quem entrou de fato.

## 5. Re-engajar quem cancelou

```python
from calendly_cliente import CalendlyCliente
c = CalendlyCliente()
cancelados = c.eventos_cancelados_recentes(dias=14)

for e in cancelados:
    print(f"⚠️ Cancelou: {e['convidado_email']} — motivo: {e['motivo_cancelamento']}")
    # combinar com ClickUp: cria task "Re-engajar Pedro Fulano em 7 dias"
```

## Combo poderoso

```
Toda manha às 7h:
1. Pega agenda de hoje no Calendly
2. Pra cada convidado, busca no Stripe (cliente ou nao)
3. Pra cada um, busca no Notion (notas anteriores)
4. Monta briefing personalizado pra cada reuniao
5. Salva como pagina no Notion "Briefings 24/05"
6. Manda link no meu WhatsApp
```

---

