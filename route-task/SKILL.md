---
name: route-task
description: >
  Classifica uma tarefa por complexidade (modelo barato julga) e despacha pro agente/modelo
  certo via Orca orchestration — Claude Haiku pra trivial, Claude Sonnet pra média, Codex pra
  pesada/agentic longa, Antigravity (Gemini) pra pesquisa. Use quando o usuário pedir pra
  "delegar", "rotear por complexidade", "mandar pro codex/gemini/agy conforme o peso da
  tarefa", ou quando o próprio agente decidir que uma subtarefa merece outro
  modelo/agente em vez de continuar ele mesmo.
---

# route-task

Script único (`bin/route-task`), bash puro, sem dependência de projeto. Roda em qualquer
máquina com `orca`, `claude` CLI e `jq` instalados.

## Uso

```
route-task "<descrição da tarefa>" [--worktree current|new-child|<selector>] [--dry-run]
```

`--dry-run` mostra a categoria e o comando sem despachar nada — use sempre que só quiser
checar a classificação.

## Pré-requisitos pra despachar de verdade (não precisa pra --dry-run)

1. Rodar de **dentro de um terminal/pane aberto pelo app Orca** — não vale shell solto
   (Warp, iTerm, VS Code integrado). Confirma com `echo $ORCA_TERMINAL_HANDLE`; vazio não serve.
2. `orca`, `claude` e `jq` no PATH.
3. Esse terminal precisa de um Run vinculado — o script cria um sozinho (`run-create`) se não
   tiver, não precisa fazer nada manual.

## Categorias e destino

| categoria | agente       | modelo               | effort | quando |
|-----------|--------------|-----------------------|--------|--------|
| trivial   | claude       | claude-haiku-5-5      | low    | fix pontual, 1-2 arquivos, pergunta direta |
| media     | claude       | claude-sonnet-5-5     | medium | feature pequena, refactor local, debug |
| pesada    | codex        | (próprio do codex)    | —      | tarefa agentic longa, multi-arquivo, multi-etapa |
| pesquisa  | antigravity  | (próprio do antigravity) | —   | pesquisa, comparação, análise web/multimodal |

## Instalar numa máquina nova

Essa pasta (`~/.claude/skills/route-task/`) é a fonte de verdade — `bin/route-task` é o
script real. Pra poder chamar `route-task` como comando solto:

```
ln -sf ~/.claude/skills/route-task/bin/route-task ~/.local/bin/route-task
```

(ajusta `~/.local/bin` pro diretório que já estiver no seu `PATH` — em geral é onde o `claude`
CLI também mora: `which claude`.)

Pra propagar a skill inteira pra outra máquina: copia essa pasta pra
`~/.claude/skills/route-task/` lá (git/dotfiles, `orca skills share` + `orca skills install`,
ou `scp -r`), depois roda o symlink acima.

## Erros conhecidos (já corrigidos no script, documentado pra não repetir debug)

- `worker-start requires the coordinator terminal currently bound to the Task Run` — faltava
  `run-create`. `run-current` retorna `ok:true` mesmo sem Run (`result.run: null`), então o
  script checa `result.run.id`, não `ok`.
- `New worktrees require --name` — `--worktree new-child`/`new-top-level` exigem `--name`;
  `current`/seletor existente rejeita `--name`. O script só adiciona quando cria worktree nova.
