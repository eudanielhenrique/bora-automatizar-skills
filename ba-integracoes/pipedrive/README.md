# Integracao 10 — Pipedrive

Cliente Python pra **Pipedrive** — CRM com bom uso no Brasil pra equipes comerciais 5-50 vendedores.

## O que da pra fazer

| Funcao | O que faz |
|---|---|
| `listar_deals(stage=None, status="open")` | Lista deals |
| `criar_deal(titulo, valor, pessoa_id, stage_id)` | Cria deal |
| `mover_deal(deal_id, stage_id)` | Move entre etapas |
| `ganhar_deal(deal_id)` / `perder_deal(deal_id, motivo)` | Fecha o deal |
| `criar_pessoa(nome, email, telefone)` | Cria contato |
| `criar_organizacao(nome)` | Cria empresa |
| `adicionar_atividade(deal_id, titulo, tipo, quando)` | Agenda atividade |
| `pipeline_resumo()` | Volume + valor por etapa |
| `deals_perdidos_recentes(dias=30)` | Perdidos com motivo |

## Setup — 5 minutos

1. Logue em https://app.pipedrive.com → avatar → **Configuracoes pessoais** → **API**.
2. Copie o **API token**.
3. Anote o **subdominio** da sua conta (`SEU_DOMINIO.pipedrive.com`).
4. Crie `~/.credentials/pipedrive.env`:

```
PIPEDRIVE_TOKEN=seu_token
PIPEDRIVE_DOMAIN=seu-dominio
```

5. Liste seus stages pra anotar IDs:

```bash
export $(cat ~/.credentials/pipedrive.env | xargs)
curl "https://${PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/stages?api_token=${PIPEDRIVE_TOKEN}" | python3 -m json.tool
```

## Uso

```bash
python pipedrive_cliente.py listar-deals
python pipedrive_cliente.py pipeline-resumo
python pipedrive_cliente.py deals-perdidos 30
```

```python
from pipedrive_cliente import PipedriveCliente
pd = PipedriveCliente()
deals = pd.listar_deals()
```

## Veja `exemplos.md` para 5 receitas

Iguais à RD Station, mas com chamadas Pipedrive.

## Segurança

- API token = acesso total à sua conta. Trate como senha.
- Pra revogar: Configuracoes pessoais → API → Reset token.

---

