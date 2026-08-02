# RD Station CRM — Exemplos

## 1. Lead novo do WhatsApp vira deal automaticamente

```python
from rd_cliente import RDStationCRM
rd = RDStationCRM()

# A skill whatsapp-atendente identificou um lead quente
lead = {"nome": "Pedro Fulano", "telefone": "5521999999999", "interesse": "Plano Premium R$ 597"}

# 1. Cria contato (ou pega existente)
existente = rd.buscar_contato(lead["telefone"])
if existente:
    contato_id = existente[0]["id"]
else:
    novo = rd.criar_contato(lead["nome"], telefone=lead["telefone"])
    contato_id = novo["contact"]["_id"]

# 2. Cria deal
deal = rd.criar_deal(f"{lead['nome']} — {lead['interesse']}", 597, contato_id=contato_id)

# 3. Registra atividade
rd.adicionar_atividade(deal["deal"]["_id"], "Chegou via WhatsApp — interesse no Premium. Followup amanha 9h.")
```

## 2. Dashboard de funil no privado toda segunda

```bash
#!/bin/bash
# funil-segunda.sh
export $(cat ~/.credentials/rd-station.env | xargs)
export $(cat ~/.credentials/zappfy.env | xargs)

RESUMO=$(python rd_cliente.py resumo-funil | python3 -c "
import json, sys
data = json.load(sys.stdin)
total_valor = sum(s['valor_total'] for s in data.values())
total_qtd = sum(s['quantidade'] for s in data.values())
print(f'📊 Funil RD — {total_qtd} deals | R\$ {total_valor:,.2f}')
print()
for nome, s in data.items():
    barra = '█' * min(20, s['quantidade'])
    print(f'{nome[:20].ljust(20)} {s[\"quantidade\"]:>3}  R\$ {s[\"valor_total\"]:>10,.2f}  {barra}')
")

curl -X POST $ZAPPFY_URL_ENVIO \
     -H "Authorization: Bearer $ZAPPFY_TOKEN" \
     -H "Content-Type: application/json" \
     -d "$(jq -n --arg para "$WHATSAPP_DESTINO" --arg msg "$RESUMO" '{phone: $para, message: $msg}')"
```

Cron:
```cron
# Toda segunda 8h
0 8 * * 1  /caminho/funil-segunda.sh
```

## 3. Alerta de deal parado >7 dias

```python
from rd_cliente import RDStationCRM
from datetime import datetime, timedelta

rd = RDStationCRM()
deals = rd.listar_deals()
hoje = datetime.utcnow()

parados = []
for d in deals:
    try:
        upd = datetime.fromisoformat(d["atualizado_em"].replace("Z", "+00:00")).replace(tzinfo=None)
        dias = (hoje - upd).days
        if dias > 7 and d["estagio_nome"] not in ("Ganho", "Perdido"):
            parados.append((dias, d))
    except (ValueError, AttributeError):
        continue

parados.sort(reverse=True)
for dias, d in parados[:10]:
    print(f"⚠️  {dias}d parado: {d['nome']} ({d['estagio_nome']}) — R$ {d['valor']:,.2f}")
```

## 4. Win-back de perdidos do mes passado

```python
from rd_cliente import RDStationCRM
rd = RDStationCRM()
perdidos = rd.deals_perdidos_recentes(dias=60)

for d in perdidos:
    # Combina com whatsapp-disparos (use skill 24-whatsapp-disparos)
    # ou com integracao webhook-generico pra disparar mensagem de reativacao
    print(f"Win-back candidate: {d['nome']} — R$ {d['valor']:.2f}")
```

## 5. Sincronizar lead-score com base no comportamento do WhatsApp

```
A skill monitoramento-equipe identificou clientes com keyword "fechamento" 5x na semana.
Logo, leads quentes.

Pra cada um:
  1. Busca contato na RD pelo telefone
  2. Atualiza lead_score via API
  3. Move deal pra estagio "Qualificado"
```

## Combo poderoso

```
Pipeline completo:
1. WhatsApp recebe mensagem → skill whatsapp-atendente classifica
2. Lead QUENTE → cria contato + deal na RD via rd_cliente.py
3. RD dispara webhook quando deal muda de estagio → webhook-generico recebe
4. Webhook notifica WhatsApp do vendedor responsavel
5. Toda segunda 8h: dashboard de funil cai no privado dos sócios
```

---

