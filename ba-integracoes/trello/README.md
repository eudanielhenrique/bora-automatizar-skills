# Integração 7 — Trello

Conecta o Claude Code ao Trello. Pede em PT-BR:

> "Cria um card 'Ligar pra Pedro Fulano' na lista 'Follow-up' do board 'Vendas'."

> "Move o card 'Reunião ACME' pra lista 'Em andamento'."

> "Lista todos os cards atrasados do board 'Operação'."

## O que dá pra fazer

| Ação | Exemplo |
|---|---|
| **Criar card** | "Cria card 'Reunião ACME' na lista 'A fazer'" |
| **Mover entre listas** | "Move card abc123 de 'To Do' pra 'Doing'" |
| **Comentar** | "Adiciona comentário 'Cliente confirmou' no card abc123" |
| **Adicionar membro** | "Atribui o card abc123 pro João" |
| **Definir prazo** | "Marca prazo do card abc123 pra sexta 18h" |
| **Adicionar checklist** | "Cria checklist 'Onboarding' no card abc123 com 5 itens" |
| **Listar cards** | "Lista os 10 cards mais recentes do board 'Vendas'" |
| **Arquivar** | "Arquiva todos os cards da lista 'Concluído'" |

## Setup — 5 minutos

### 1. Gerar API key + Token

1. Logue em https://trello.com.
2. Vá em https://trello.com/app-key.
3. Copie a **API Key** que aparece no topo.
4. Logo abaixo, clique em "**Token**" (ou em "Generate a Token") → autorize → copie o **Token**.

> Você vai precisar de **2 strings**: API Key e Token. Guarde as duas com segurança.

### 2. Descobrir IDs do board / lista

A primeira vez que você conectar, peça ao Claude Code:

> "Lista meus boards do Trello com seus IDs."

> "Lista as listas do board com ID 'abc123' e me devolve cada uma com nome e ID."

Anote os IDs principais (board "Vendas" = `xyz`, lista "Follow-up" = `abc`). Vai usar muito.

### 3. Configurar o MCP no Claude Code

```bash
claude mcp add trello \
  --env TRELLO_API_KEY=sua_api_key \
  --env TRELLO_TOKEN=seu_token \
  -- npx -y @mcp-mirror/delorenj_mcp-server-trello
```

Ou cole o bloco do `mcp-config.json` em `~/.claude.json`.

### 4. Reiniciar e testar

```
> Lista meus boards no Trello.

> Cria card de teste "Teste MCP" na primeira lista do board "Vendas".
```

## Teste rápido

```
> Cria 3 cards de teste na lista "A fazer" do board "Sandbox" com
  títulos "Teste 1", "Teste 2", "Teste 3", cada um com prazo +1 dia.

> Lista o que foi criado.
```

## Casos de uso prontos

Veja **`funcoes-prontas.md`** — 8 fluxos.

## Segurança

- API Key + Token = **acesso total** à sua conta Trello. Trate como senha.
- Pra revogar: https://trello.com/u/SEU_USUARIO/account → **Account Settings** → **Power-Ups / API Tokens** → Revoke.
- Em projetos compartilhados, prefira tokens **read-only** se a integração só precisa ler.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Unauthorized` | Token expirado ou inválido | Gere novamente em trello.com/app-key |
| `Not found` | ID errado (board/lista) | Use o comando "Lista meus boards" pra descobrir |
| MCP não aparece | Claude Code não reiniciado | Feche e abra |

---

