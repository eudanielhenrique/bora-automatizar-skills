# Integração 3 — Notion

Conecta o Claude Code ao seu Notion (workspaces, páginas e databases). Você pede em PT-BR:

> "Cria uma página dentro do database 'Leads' com nome Pedro Fulano, telefone 5521..., status Novo."

> "Busca na minha base de conhecimento as páginas que falam sobre 'reembolso' e me resume."

> "No database 'Tarefas Diárias', lista o que está 'Em andamento' atribuído pra mim."

## O que dá pra fazer

| Ação | Exemplo |
|---|---|
| **Buscar páginas** | "Busca 'reembolso' no meu Notion" |
| **Criar página** | "Cria página 'Reunião 24/05' dentro de 'Atas'" |
| **Popular database** | "Adiciona uma linha no database 'CRM' com nome=Pedro, status=Novo" |
| **Atualizar propriedade** | "Marca o lead Pedro como 'Qualificado'" |
| **Ler conteúdo** | "Lê a página 'SOP Atendimento' e me resume em 5 bullets" |
| **Adicionar bloco** | "Adiciona um TODO na página 'Hoje': 'Ligar pra Roberto'" |
| **Buscar databases** | "Lista todos os databases que eu tenho acesso" |
| **Importar/Exportar** | "Exporta o database 'Leads' como CSV" |

## Setup — 10 minutos

> **Já comprou o Bônus 7 (MCP Notion)?** O setup é o mesmo. Pula direto pro `mcp-config.json` deste bônus se já configurou.

### 1. Criar uma integração no Notion

1. Vá em https://www.notion.so/my-integrations.
2. **+ New integration** → nome `Claude Code`, workspace que você quer conectar, type **Internal**.
3. Capabilities: marque **Read content**, **Update content** e **Insert content**.
4. **Save** → copie o **Internal Integration Secret** (começa com `ntn_`).

### 2. Compartilhar conteúdo com a integração

A integração **não enxerga nada do seu Notion por padrão**. Em cada página/database que você quer liberar:

- Abra → **•••** (canto superior direito) → **Connections** → **+ Add connections** → selecione `Claude Code`.

> **Dica:** compartilhe uma **página-mãe** com tudo dentro. A integração herda acesso aos filhos. Crie uma página "Claude Code" e mova o conteúdo a liberar pra dentro dela.

### 3. Configurar o MCP no Claude Code

```bash
claude mcp add notion --env NOTION_TOKEN=ntn_seu_token_aqui \
  -- npx -y @notionhq/notion-mcp-server
```

Ou cole o bloco do `mcp-config.json` deste bônus em `~/.claude.json`.

### 4. Reiniciar o Claude Code e testar

```
> Busca no meu Notion uma página chamada [nome de uma página compartilhada].
```

Se aparecer o conteúdo, está conectado.

## Teste rápido

```
> Lista os 5 databases que eu tenho acesso no Notion.

> Cria uma página de teste dentro da página-mãe "Claude Code" com o título
  "Teste MCP" e um parágrafo "Funcionou".
```

## Casos de uso prontos

Veja **`funcoes-prontas.md`** — 8 fluxos (registrar lead, gerar ata de reunião, salvar SOP, etc).

## Segurança

- O `Internal Integration Secret` é a chave da integração — trate como senha.
- A integração **só vê o que você compartilhar**. Bom princípio: criar uma página "Claude Code", liberar só ela, mover/linkar pra dentro o que pode acessar.
- Para revogar: my-integrations → integração → **Archive integration**.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Page not found` | Página não compartilhada com a integração | Adicione a integração em Connections |
| `Insufficient permissions` | Capability "Insert" ou "Update" desligada | Edite a integração em my-integrations |
| MCP não aparece | Claude Code não reiniciado | Feche e abra |

---

