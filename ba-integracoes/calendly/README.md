# Integração 6 — Calendly

Cliente Python pra puxar **reuniões agendadas, no-shows, cancelamentos** do Calendly.

## O que dá pra fazer

| Função | O que faz |
|---|---|
| `eventos_hoje()` | Reuniões agendadas pra hoje |
| `eventos_amanha()` | Reuniões agendadas pra amanhã |
| `eventos_por_periodo(inicio, fim)` | Reuniões num intervalo |
| `eventos_cancelados_recentes(dias=7)` | Cancelados nos últimos N dias |
| `evento_detalhe(uri)` | Detalhe completo (convidado, e-mail, notas, status) |
| `cancelar_evento(uri, motivo)` | Cancela um evento |
| `resumo_semana()` | Quantos agendados, cancelados, no-shows |

## Setup — 5 minutos

### 1. Gerar Personal Access Token

1. Logue em https://calendly.com/integrations/api_webhooks.
2. **+ Get a new token** → confirme.
3. Copie o token (começa com `eyJ...`, JWT).

> **Plano Standard** ou superior do Calendly é necessário pra usar a API.

### 2. Pegar seu User URI

Rode uma vez:

```bash
curl -H "Authorization: Bearer SEU_TOKEN" https://api.calendly.com/users/me
```

Procure no JSON o campo `"uri": "https://api.calendly.com/users/SEU_ID"`. Guarde isso.

### 3. Instalar dependência

```bash
pip install requests
```

### 4. Configurar credencial

Crie `~/.credentials/calendly.env`:

```
CALENDLY_TOKEN=eyJ...seu_token_completo
CALENDLY_USER_URI=https://api.calendly.com/users/SEU_ID
```

## Uso

### Via terminal

```bash
export $(cat ~/.credentials/calendly.env | xargs)

python calendly_cliente.py hoje
python calendly_cliente.py amanha
python calendly_cliente.py resumo-semana
python calendly_cliente.py cancelados 7
```

### Em Python

```python
from calendly_cliente import CalendlyCliente
c = CalendlyCliente()
eventos = c.eventos_amanha()
for e in eventos:
    print(f"{e['inicio']} — {e['convidado_email']} — {e['titulo']}")
```

### Via Claude Code

```
Roda o script calendly_cliente.py com a opção amanha. Pra cada reunião:
- pega o email do convidado
- procura ele no Stripe (cliente_buscar)
- se for cliente, marca a reunião como "Cliente"
- se for lead, marca como "Lead"

Me devolve a agenda de amanhã pré-classificada.
```

## Exemplos de uso

Veja **`exemplos.md`** — 5 cenários (briefing pré-reunião, alerta de no-show, follow-up de cancelamento, etc).

## Segurança

- O token Calendly é Personal. Trate como senha.
- Pra revogar: https://calendly.com/integrations/api_webhooks → **Revoke**.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `401` | Token errado | Gere novo em /integrations/api_webhooks |
| `403 — Plan insufficient` | Plano Free não tem API | Upgrade Calendly pra Standard+ |
| `0 eventos` mas tem agenda | User URI errado | Confira com `curl /users/me` |

---

