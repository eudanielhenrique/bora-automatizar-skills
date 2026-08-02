# Integracao 9 — RD Station CRM (Brasil)

Cliente Python pra **RD Station CRM** — CRM mais usado em PME brasileira.

> Por que esta no pack? A maioria dos templates de integracao online cobre Salesforce e HubSpot. No Brasil de verdade, quem usa eh **RD Station, Pipedrive e Kommo** (esta integracao + a proxima). Por isso esta aqui.

## O que da pra fazer

| Funcao | O que faz |
|---|---|
| `listar_deals(estagio=None)` | Lista deals (negocios) por estagio |
| `criar_deal(nome, valor, contato)` | Cria deal novo |
| `mover_deal(deal_id, estagio)` | Move pra outro estagio do funil |
| `criar_contato(nome, email, telefone)` | Cria contato novo |
| `buscar_contato(email_ou_telefone)` | Procura contato |
| `adicionar_atividade(deal_id, descricao, tipo)` | Registra atividade no deal |
| `lead_score_atualizar(contato_id, score)` | Atualiza lead score |
| `deals_perdidos_recentes(dias=30)` | Deals perdidos com motivo |
| `resumo_funil()` | Volume + valor por estagio |

## Setup — 10 minutos

### 1. Token de API

1. Logue em https://app.rdstation.com.br/crm.
2. Avatar → **Configuracoes** → **Integracoes** → **Outras integracoes**.
3. **Token de instancia** → copie.
4. Guarde em `~/.credentials/rd-station.env`:

```
RD_TOKEN=seu_token_aqui
```

### 2. Descobrir IDs dos estagios

A RD usa IDs para estagios. Liste os seus:

```bash
export $(cat ~/.credentials/rd-station.env | xargs)
curl "https://crm.rdstation.com/api/v1/deal_stages?token=$RD_TOKEN" | python3 -m json.tool
```

Anote os IDs do `deal_stages` (ex: `Prospeccao=5a1...`, `Qualificacao=5a2...`).

## Uso

```bash
# Listar deals abertos
python rd_cliente.py listar-deals

# Resumo funil (volume + valor por estagio)
python rd_cliente.py resumo-funil

# Deals perdidos nos ultimos 30 dias
python rd_cliente.py deals-perdidos 30
```

```python
from rd_cliente import RDStationCRM
rd = RDStationCRM()
deals = rd.listar_deals()
for d in deals:
    print(f"{d['nome']} — R$ {d['valor']:.2f} — {d['estagio_nome']}")
```

## Casos de uso prontos

Veja **`exemplos.md`** — 5 receitas (lead novo do form → deal RD, follow-up automatico, dashboard de funil no WhatsApp, alerta de deal parado, win-back de perdidos).

## Segurança

- Token de instancia tem acesso TOTAL ao CRM. Trate como senha.
- Pra revogar: Configuracoes → Integracoes → Excluir token.

## Limites da API

- 120 requests/minuto.
- Webhooks da RD podem complementar (notificacao real-time em vez de poll).

---

