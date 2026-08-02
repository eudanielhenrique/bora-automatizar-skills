# Stripe — Exemplos de Uso

## 1. Relatório financeiro diário (no seu WhatsApp)

```bash
#!/bin/bash
# relatorio-stripe-diario.sh
export $(cat ~/.credentials/stripe.env | xargs)

RESUMO=$(python stripe_cliente.py pagamentos-hoje | python3 -c "
import json, sys
data = json.load(sys.stdin)
total = sum(p['valor'] for p in data)
qtd = len(data)
print(f'💰 Stripe hoje: R\$ {total:,.2f} em {qtd} transacoes')
print()
for p in data[:5]:
    print(f'- R\$ {p[\"valor\"]:>8.2f}  {p[\"criado_em\"][:16]}  {p[\"descricao\"]}')
if qtd > 5:
    print(f'... (+{qtd-5})')
")

# Manda no seu WhatsApp via webhook
curl -X POST $URL_WEBHOOK_ZAPPFY \
     -H "Content-Type: application/json" \
     -d "$(jq -n --arg para "$SEU_NUMERO" --arg msg "$RESUMO" '{para: $para, mensagem: $msg}')"
```

Cron:
```cron
# Todo dia útil às 20h
0 20 * * 1-5  /caminho/relatorio-stripe-diario.sh
```

## 2. Régua de cobrança de fatura em aberto

```python
from stripe_cliente import StripeCliente
from datetime import datetime, timezone

s = StripeCliente()
abertas = s.faturas_em_aberto()

for f in abertas:
    if not f["vencimento"]:
        continue
    dias_atraso = (datetime.now(timezone.utc) - f["vencimento"]).days
    if dias_atraso < 0:
        continue  # ainda nao venceu
    if dias_atraso in (1, 3, 7, 15, 30):
        # dispara WhatsApp com o link da fatura
        print(f"Cliente {f['cliente_id']} — {dias_atraso}d em atraso — {f['url_hosted']}")
```

Combine com **integração `webhook-generico`** pra disparar a mensagem.

## 3. Fechamento mensal automático

```bash
# 1º dia útil do mês às 8h
0 8 1 * *  python stripe_cliente.py resumo-mes $(date -d "last month" +"%Y %m") > /relatorios/stripe-$(date -d "last month" +"%Y-%m").json
```

E peça pro Claude:

> "Lê o JSON `stripe-2026-05.json` e gera um relatório executivo de fechamento mensal, comparando com o mês anterior se houver."

## 4. Dashboard MRR no Google Sheets

```python
from stripe_cliente import StripeCliente
s = StripeCliente()

resumo = s.resumo_mes(2026, 5)
# Combinar com integracao google-sheets:
# "No Sheets, adiciona linha no painel MRR com: mes=2026-05, mrr=X, ativas=Y, churn=Z%"
```

## 5. Alerta de churn (cancelamento recente)

```python
from stripe_cliente import StripeCliente
s = StripeCliente()
cancelados = s.assinaturas_canceladas_recentes(dias=7)

for c in cancelados:
    # busca o cliente pelo id
    print(f"⚠️ Cancelamento: {c['cliente_id']} — motivo: {c['motivo']}")
    # combinar com ClickUp pra criar task de win-back
```

## Combo poderoso

```
Toda manhã às 8h, roda o resumo-mes do Stripe.
Compara com o mês anterior.
Salva no Google Sheets (aba "Histórico Mensal").
Manda no meu WhatsApp em formato executivo.
Se MRR caiu mais de 5% vs mês anterior, abre task urgente no ClickUp.
```

Isso é tudo combinável usando as 4 integrações (Stripe + Sheets + WhatsApp + ClickUp).

---

