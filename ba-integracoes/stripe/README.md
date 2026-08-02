# Integração 4 — Stripe

Cliente Python pronto pra conversar com a **API do Stripe**. Use direto via terminal, dentro de cron, ou peça pro Claude Code rodar.

## O que dá pra fazer

| Função | O que faz |
|---|---|
| `pagamentos_do_dia()` | Lista pagamentos confirmados no dia atual |
| `pagamentos_por_periodo(inicio, fim)` | Lista pagamentos num intervalo |
| `assinaturas_ativas()` | Lista clientes com assinatura ativa |
| `assinaturas_canceladas_recentes(dias=30)` | Quem cancelou nos últimos N dias |
| `faturas_em_aberto()` | Faturas geradas e não pagas |
| `cliente_buscar(email_ou_nome)` | Acha customer por email/nome |
| `reembolsar(payment_intent_id, valor=None)` | Faz reembolso (total ou parcial) |
| `resumo_mes(mes, ano)` | Total bruto, líquido, número de transações, MRR |

## Setup — 5 minutos

### 1. Pegar a API key do Stripe

1. https://dashboard.stripe.com/apikeys
2. Use **Restricted keys** (não a Secret Key admin). Crie uma com permissões:
   - `Read` em: Customers, PaymentIntents, Subscriptions, Invoices, Charges
   - `Write` em: Refunds (só se for usar `reembolsar()`)
3. Copie a chave (começa com `rk_live_` ou `rk_test_`).

> **Em produção:** use a `live` key. Pra testar, use `test`.

### 2. Instalar dependência

```bash
pip install requests
```

(Não precisa do pacote oficial `stripe` — usamos `requests` direto pra ficar mais leve e auditável.)

### 3. Configurar credencial

Crie `~/.credentials/stripe.env` com:

```
STRIPE_API_KEY=rk_live_seu_token_aqui
```

E carregue no script:

```bash
export $(cat ~/.credentials/stripe.env | xargs)
```

Ou passe direto na hora:

```bash
STRIPE_API_KEY=rk_live_... python stripe_cliente.py resumo-mes
```

## Uso

### Via terminal

```bash
# Pagamentos de hoje
STRIPE_API_KEY=rk_... python stripe_cliente.py pagamentos-hoje

# Resumo do mês
STRIPE_API_KEY=rk_... python stripe_cliente.py resumo-mes 2026 05

# Assinaturas ativas
STRIPE_API_KEY=rk_... python stripe_cliente.py assinaturas-ativas

# Faturas em aberto
STRIPE_API_KEY=rk_... python stripe_cliente.py faturas-abertas
```

### Em Python (importando)

```python
from stripe_cliente import StripeCliente

s = StripeCliente()  # le STRIPE_API_KEY do ambiente
total = sum(p["valor"] for p in s.pagamentos_do_dia())
print(f"Recebido hoje: R$ {total/100:,.2f}")
```

### Via Claude Code

```
Roda o script stripe_cliente.py com a opção resumo-mes pro mês atual
e me devolve em formato de relatório executivo.
```

## Exemplos de uso

Veja **`exemplos.md`** — 5 cenários comuns (relatório financeiro diário, cobrança automática de inadimplente, fechamento mensal, dashboard MRR, alerta de churn).

## Segurança

- **Restricted Key** com permissões mínimas. Nunca use a Secret Key admin direto.
- `~/.credentials/stripe.env` no `.gitignore` global. Nunca comite.
- Em produção, considere usar o **Secrets Manager** do seu cloud (AWS Secrets Manager, GCP Secret Manager).
- Se vazar: **roll the key** imediatamente em https://dashboard.stripe.com/apikeys.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `401 Unauthorized` | Chave errada ou test/live trocado | Confira em dashboard.stripe.com/apikeys |
| `Permission denied` | Restricted key sem o scope | Adicione o scope necessário |
| `Rate limit` | Mais de 100 req/s | Adicione `time.sleep(0.1)` entre chamadas |

---

