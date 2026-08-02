# Shopify — Exemplos de Uso

## 1. Alerta diário de estoque baixo no WhatsApp

```bash
#!/bin/bash
# alerta-estoque.sh
export $(cat ~/.credentials/shopify.env | xargs)
export $(cat ~/.credentials/zappfy.env | xargs)

ALERTA=$(python shopify_cliente.py estoque-baixo 10 | python3 -c "
import json, sys
items = json.load(sys.stdin)
if not items:
    print('Estoque OK — nenhum produto abaixo de 10')
else:
    print(f'⚠️ {len(items)} produtos com estoque baixo:')
    for it in items[:10]:
        print(f'- {it[\"produto\"]} {it[\"variante\"]} — {it[\"estoque\"]} unid')
    if len(items) > 10:
        print(f'... (+{len(items)-10})')
")

curl -X POST $URL_WEBHOOK_ZAPPFY \
     -H "Content-Type: application/json" \
     -d "$(jq -n --arg para "$SEU_NUMERO" --arg msg "$ALERTA" '{para: $para, mensagem: $msg}')"
```

Cron:
```cron
# Todo dia útil às 9h
0 9 * * 1-5 /caminho/alerta-estoque.sh
```

## 2. Resumo de vendas do dia (final do expediente)

```bash
python shopify_cliente.py resumo-dia
```

Output:
```json
{
  "dia": "2026-05-24",
  "pedidos": 42,
  "faturamento": 12487.50,
  "ticket_medio": 297.32,
  "top_produtos": [
    {"titulo": "Camiseta Premium", "qtd": 18, "receita": 2682.00},
    ...
  ],
  "pendentes": 3,
  "cancelados": 1
}
```

Combine com Claude:
> "Lê o JSON do resumo-dia, formata como relatório executivo
> e me devolve em texto pra colar no WhatsApp."

## 3. Pedidos pendentes pra encarar

```python
from shopify_cliente import ShopifyCliente
sp = ShopifyCliente()
pendentes = sp.pedidos_status("pending")

for p in pendentes:
    print(f"{p['numero']} — {p['cliente']} — R$ {p['valor']:.2f}")
    # combinar com ClickUp: cria task pra cada pendente que esta ha mais de 24h
```

## 4. Top clientes do mês

```python
from collections import defaultdict
from datetime import datetime
from shopify_cliente import ShopifyCliente

sp = ShopifyCliente()
inicio = datetime(2026, 5, 1)
fim = datetime(2026, 5, 31, 23, 59, 59)
pedidos = sp.pedidos_por_periodo(inicio, fim)

receita_cliente = defaultdict(float)
for p in pedidos:
    receita_cliente[p["cliente"]] += p["valor"]

top10 = sorted(receita_cliente.items(), key=lambda x: -x[1])[:10]
for email, valor in top10:
    print(f"{email}: R$ {valor:,.2f}")
```

## 5. Pedido pra reembolsar / atender suporte

```
Cliente reclamou no WhatsApp: "pedido #1234 ainda não chegou".

Roda: python shopify_cliente.py pedido 1234

Devolve o JSON do pedido. Cole no Claude:

> "Lê esse JSON e me diz: foi pago? foi enviado? quantos dias se passaram?
> Que ação tomar agora?"
```

## Combo poderoso

```
Toda manhã às 8h:
1. shopify_cliente.py resumo-dia (dia anterior)
2. shopify_cliente.py estoque-baixo 5
3. shopify_cliente.py pedidos pendentes

Consolida em 1 mensagem:
- Faturou X reais ontem em N pedidos (▲/▼ vs anteontem)
- Y produtos com estoque baixo: lista
- Z pedidos pendentes há > 24h: lista

Manda no meu WhatsApp.
Se faturamento caiu > 30% vs anteontem, abre task urgente no ClickUp.
```

---

