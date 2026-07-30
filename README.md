# daniel-skills

**O padrão não fica na sua cabeça. Fica no código.**

Skills operacionais para o [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Cada skill coloca o agente num modo específico com um trabalho específico — sem você precisar explicar o contexto toda vez.

---

### O problema

Você abre o Claude Code. O agente não sabe qual é a sua barra. Não sabe que "funciona" não é suficiente. Não sabe que segurança não é opcional. Não sabe como você quer confirmar antes de escrever em produção.

Então você repete. Toda sessão, todo projeto.

daniel-skills resolve isso. Você codifica o padrão uma vez. Depois ele está sempre lá.

---

### Skills disponíveis

| Skill | O que faz |
|---|---|
| `/dh-firestore-backup` | Exporta collections do Firestore para JSON — todas ou seleção específica, com subcollections e logging |
| `/dh-firestore-restore` | Restaura dados no Firestore com conversão de tipos, clearCollection e confirmação explícita de destino |
| `/dh-designer-system-ba` | Aplica o design system real do Bora Automatizar — tipografia, cores, botões, estrutura de seções e animação, extraídos do site em produção |

---

### Como funciona

Cada skill é um arquivo `SKILL.md` com instruções que o Claude Code carrega quando você invoca o comando. O agente entra num modo específico com um trabalho específico — e sabe exatamente o que fazer sem você guiar passo a passo.

Exemplo:

```
Você:  /dh-firestore-backup

Claude: [Verifica e instala o pacote automaticamente se necessário.
        Confirma serviceAccountKey.json. Pergunta quais collections.
        Executa o backup. Reporta: total de docs, arquivo gerado, tamanho.]

BACKUP CONCLUÍDO
Projeto:     whats-remember
Collections: accounts, sessions, users
Documentos:  435
Arquivo:     backup-2026-07-13T23-24-31-485Z.json (2.3 MB)
```

---

### Instalação

```bash
git clone https://github.com/eudanielhenrique/daniel-skills.git ~/.claude/skills/daniel-skills && cd ~/.claude/skills/daniel-skills && chmod +x setup && ./setup
```

### Atualização

```bash
~/.claude/skills/daniel-skills/update
```

Puxa o que tiver de novo e reinstala os symlinks.

### Desinstalação

```bash
for s in dh-firestore-backup dh-firestore-restore dh-designer-system-ba; do rm -rf ~/.claude/skills/$s; done && rm -rf ~/.claude/skills/daniel-skills
```

---

MIT — [Daniel Henrique](https://github.com/eudanielhenrique)
