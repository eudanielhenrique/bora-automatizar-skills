# Integração 1 — Google Sheets

Conecta o Claude Code à sua conta do Google Sheets. Depois disso você pode pedir em PT-BR:

> "Pega a planilha 'CRM Leads', filtra os leads dos últimos 7 dias com status 'novo' e me mostra."

> "Adiciona uma linha na aba 'Pedidos' da planilha 'Operação' com cliente=Maria, valor=297, data=hoje."

> "Pega minha planilha 'Financeiro 2026', soma os valores da coluna 'Recebido' e me diz o total."

## O que dá pra fazer

| Ação | Exemplo |
|---|---|
| **Ler planilha** | "Lê a aba 'Vendas' da planilha 'X' e me mostra as 10 últimas linhas" |
| **Filtrar dados** | "Mostra os leads da aba CRM com status 'quente' e valor > 1000" |
| **Adicionar linha** | "Adiciona um lead novo: nome Pedro, telefone 21999..., status novo" |
| **Atualizar célula** | "Marca como 'fechado' o lead da linha 47" |
| **Somar / agregar** | "Soma a coluna 'Valor' da aba Pedidos do mês 05/2026" |
| **Criar planilha** | "Cria uma planilha nova chamada 'Relatório Maio'" |

## Setup — 5 minutos

### 1. Habilitar API do Google Sheets

Vá em https://console.cloud.google.com → crie um projeto (ou use um existente) → "APIs & Services" → "Library" → busque **Google Sheets API** e clique em **Enable**.

Faça o mesmo para **Google Drive API** (necessária pra criar planilha nova).

### 2. Criar uma Service Account

1. No mesmo projeto: "APIs & Services" → "Credentials" → "Create Credentials" → "Service Account".
2. Nome: `claude-code-sheets`. Clique em "Create and Continue".
3. Role: **Editor** (ou "Sheets Editor" se quiser limitar). Clique em "Continue" → "Done".
4. Clique na service account criada → aba **Keys** → "Add Key" → "Create new key" → **JSON** → baixar.
5. Salve o JSON em local seguro, por exemplo: `~/.credentials/google-sheets.json`.

### 3. Compartilhar planilhas com a Service Account

A service account tem um **email** (algo como `claude-code-sheets@SEU-PROJETO.iam.gserviceaccount.com`). Ela **não enxerga nenhuma planilha por padrão**.

Em cada planilha que você quer que o Claude acesse:
- Abra a planilha → "Compartilhar" (canto superior direito)
- Cole o email da service account → permissão **Editor** → "Enviar"

### 4. Configurar o MCP no Claude Code

Use o `mcp-config.json` deste bônus como modelo. Edite seu `~/.claude.json` (ou `.mcp.json` do projeto) adicionando o bloco abaixo, trocando os caminhos:

```bash
claude mcp add google-sheets \
  --env GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/Users/SEU_USUARIO/.credentials/google-sheets.json \
  -- npx -y @googleapis/sheets-mcp
```

### 5. Reiniciar o Claude Code e testar

Reinicie o Claude Code e teste:

> "Lista as planilhas que tenho acesso no Google Sheets."

Se aparecer uma lista, está conectado.

## Teste rápido

```
> Cria uma planilha nova chamada "Teste MCP" com a aba "Leads"
  e cabeçalho: nome, telefone, status, data.

> Adiciona 2 linhas de teste nessa planilha.
```

## Casos de uso prontos

Veja **`funcoes-prontas.md`** — 8 comandos de uso comum.

## Segurança

- O JSON da service account é **a chave da conta**. Trate como senha.
- Compartilhe a service account apenas com as planilhas que ela precisa acessar (princípio do menor privilégio).
- Se você for sair de um time / cliente, **rotacione a key** (Console → Credentials → service account → Keys → revoke).

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Permission denied` | Planilha não compartilhada com a service account | Compartilhe com o email da SA |
| `API not enabled` | Sheets API não habilitada | Console → APIs → Enable |
| `Invalid grant` | JSON da service account corrompido / vencido | Re-baixe o JSON |
| MCP não aparece | Claude Code não reiniciado | Feche e abra o Claude Code |

---

