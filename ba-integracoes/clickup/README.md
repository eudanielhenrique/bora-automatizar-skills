# Integração 2 — ClickUp

Conecta o Claude Code ao ClickUp. Você pede em PT-BR:

> "Cria uma task no Space 'Vendas', lista 'Follow-up', chamada 'Ligar pra Pedro Fulano' e atribui pro João."

> "Lista as tasks que estão 'In Progress' atribuídas pra mim com prioridade alta."

> "Move a task #abc123 pra coluna 'Done' e adiciona o comentário 'Cliente fechou'."

## O que dá pra fazer

| Ação | Exemplo |
|---|---|
| **Criar task** | "Cria task 'Reunião com Roberto' na lista 'Comercial' amanhã 14h" |
| **Listar/filtrar** | "Lista tasks atrasadas da lista 'Suporte' atribuídas pra mim" |
| **Mover de coluna** | "Move task #abc123 de 'To Do' pra 'In Progress'" |
| **Comentar** | "Adiciona comentário 'Cliente confirmou' na task #abc123" |
| **Subtarefas** | "Cria 3 subtarefas em 'Setup do cliente novo'" |
| **Time tracking** | "Começa cronômetro na task #abc123" |
| **Documentos** | "Cria uma página 'Reunião 24/05' no doc 'Atas'" |
| **Chat** | "Manda mensagem no canal 'Comercial' avisando que o cliente fechou" |

## Setup — 5 minutos

### 1. Gerar a API key

1. Logue em https://app.clickup.com.
2. Avatar (canto superior esquerdo) → **Settings** → **Apps** → **API Token**.
3. Clique em **Generate** (se ainda não tem). Copie o token (começa com `pk_`).
4. **Guarde com segurança** — esse token tem acesso total à sua conta.

> Se você é admin de workspace e quer escopo mais limitado, use uma **OAuth App** no menu Apps → Apps. Pra começar, a Personal API Token resolve.

### 2. Configurar o MCP no Claude Code

```bash
claude mcp add clickup --env CLICKUP_API_TOKEN=pk_seu_token_aqui \
  -- npx -y @taazkareem/clickup-mcp-server
```

Ou edite o `~/.claude.json` colando o bloco do `mcp-config.json` deste bônus e trocando o token.

### 3. Descobrir os IDs principais

O Claude Code pode descobrir o ID do seu **Team / Space / List** automaticamente — peça:

> "Lista meus Spaces e Lists do ClickUp."

Anote os IDs principais (Space "Vendas", List "Follow-up", etc.) — vai usar muito.

### 4. Reiniciar e testar

```
> Cria uma task de teste chamada "Teste MCP" no Space "Vendas" e me devolve o link.
```

Se vier um link real do ClickUp, está conectado.

## Teste rápido

```
> Lista minhas tasks de hoje no ClickUp, ordenadas por prioridade.

> Cria uma task "Limpar pipeline" pra amanhã 9h na lista "Comercial",
  com prioridade Urgent.
```

## Casos de uso prontos

Veja **`funcoes-prontas.md`** — 8 fluxos comuns (criar task a partir do WhatsApp, fechar e arquivar, etc).

## Segurança

- O token Personal API tem **acesso de admin** ao seu workspace. Trate como senha.
- Para times com várias pessoas, prefira criar uma **OAuth App** com escopo limitado.
- Em projetos compartilhados, use `.mcp.json` por projeto (não `~/.claude.json` global) — assim o token fica isolado.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `401 Unauthorized` | Token errado ou revogado | Gere novamente em Settings → API Token |
| `Task not found` | ID da task com prefixo `CU-` desnecessário | Use só o sufixo (`abc123`, não `CU-abc123`) |
| MCP não aparece | Claude Code não reiniciado | Feche e abra |

---

