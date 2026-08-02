# Integração 5 — Shopify

Cliente Python pra puxar **pedidos, produtos, clientes e estoque** da sua loja Shopify.

## O que dá pra fazer

| Função | O que faz |
|---|---|
| `pedidos_do_dia()` | Pedidos criados no dia atual |
| `pedidos_por_periodo(inicio, fim)` | Pedidos entre datas |
| `pedidos_status(status)` | Pedidos por status (`paid`, `pending`, `fulfilled`, `cancelled`) |
| `pedido(numero)` | Pega um pedido específico pelo número (`#1234`) |
| `produtos_estoque_baixo(limite=5)` | Produtos com estoque abaixo de N |
| `cliente_buscar(email_ou_nome)` | Acha customer |
| `resumo_dia()` | Total bruto, ticket médio, qtd pedidos |
| `atualizar_estoque(variant_id, novo_estoque)` | Ajusta estoque de uma variante |

## Setup — 10 minutos

### 1. Criar um Custom App no Shopify

1. Logue no Shopify Admin → **Apps and sales channels** → **Develop apps** (canto inferior — se não aparecer, clique em "Allow custom app development").
2. **Create an app** → nome `Claude Code Integration`.
3. **Configure Admin API scopes**. Para começar:
   - `read_orders` (leitura de pedidos)
   - `read_products`, `write_products` (produtos e estoque)
   - `read_customers` (clientes)
   - `read_inventory`, `write_inventory` (estoque)
4. **Install app** → confirme.
5. Em **API credentials**, copie o **Admin API access token** (começa com `shpat_`). Esse é o token.
6. Anote também o domínio da sua loja: `sua-loja.myshopify.com`.

### 2. Instalar dependência

```bash
pip install requests
```

### 3. Configurar credencial

Crie `~/.credentials/shopify.env`:

```
SHOPIFY_SHOP=sua-loja.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_seu_token_aqui
```

## Uso

### Via terminal

```bash
export $(cat ~/.credentials/shopify.env | xargs)

# Pedidos de hoje
python shopify_cliente.py pedidos-hoje

# Resumo do dia
python shopify_cliente.py resumo-dia

# Estoque baixo (< 5 unidades)
python shopify_cliente.py estoque-baixo 5

# Pedido específico
python shopify_cliente.py pedido 1234
```

### Em Python

```python
from shopify_cliente import ShopifyCliente

sp = ShopifyCliente()
pedidos = sp.pedidos_do_dia()
print(f"Pedidos hoje: {len(pedidos)} | Faturamento: R$ {sum(p['valor'] for p in pedidos):,.2f}")
```

### Via Claude Code

```
Roda o script shopify_cliente.py com a opção resumo-dia e me devolve em
formato de relatório com top 5 produtos mais vendidos do dia.
```

## Exemplos de uso

Veja **`exemplos.md`** — 5 cenários (alerta de estoque baixo, pedidos pendentes, top clientes do mês, etc).

## Segurança

- O access token tem o **escopo do que você marcou no setup**. Não marque mais do que precisa.
- `shopify.env` no `.gitignore`. Nunca comite.
- Pra revogar: Apps → seu Custom App → Uninstall.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `401` | Token errado ou app desinstalado | Re-confira em Apps → Custom App → API credentials |
| `403 — Insufficient scope` | Falta um scope no Custom App | Edite o app, adicione o scope, reinstale |
| `429 — Throttled` | API rate limit (40 req/s) | Adicione `time.sleep(0.5)` entre chamadas |

---

