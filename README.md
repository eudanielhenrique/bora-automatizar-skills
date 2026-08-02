# bora-automatizar-skills

**O padrão não fica na sua cabeça. Fica no código.**

Skills operacionais para o [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Cada skill coloca o agente num modo específico com um trabalho específico — sem você precisar explicar o contexto toda vez.

---

### O problema

Você abre o Claude Code. O agente não sabe qual é a sua barra. Não sabe que "funciona" não é suficiente. Não sabe que segurança não é opcional. Não sabe como você quer confirmar antes de escrever em produção.

Então você repete. Toda sessão, todo projeto.

bora-automatizar-skills resolve isso. Você codifica o padrão uma vez. Depois ele está sempre lá.

---

### Skills disponíveis

| Skill | O que faz |
|---|---|
| `/ba-firestore-backup` | Exporta collections do Firestore para JSON — todas ou seleção específica, com subcollections e logging |
| `/ba-firestore-restore` | Restaura dados no Firestore com conversão de tipos, clearCollection e confirmação explícita de destino |
| `/ba-designer-system` | Aplica a identidade Bora Automatizar em três modos — Landing Page (extraído do site WordPress), Sistema/App (base para sidebar/tabelas/dashboards) e Oferta/Produto (extraído do Projeto Éter, geração mais recente) |
| `/ba-proposta-comercial` | Gera proposta comercial em HTML único no padrão visual Bora Automatizar — hero, cases, escopo, cronograma, investimento parcelado, CTA com WhatsApp/e-mail |
| `/ba-oferta-produtizada` | Gera landing page de oferta produtizada em HTML único — escassez, exemplos, cases, processo, prova social do founder, FAQ |
| `/ba-monitoramento-equipe` | Boletim diário/semanal da equipe de WhatsApp — TPR, heatmap de demanda, mensagens críticas, distribuição de carga |

---

### Como funciona

Cada skill é um arquivo `SKILL.md` com instruções que o Claude Code carrega quando você invoca o comando. O agente entra num modo específico com um trabalho específico — e sabe exatamente o que fazer sem você guiar passo a passo.

Exemplo:

```
Você:  /ba-firestore-backup

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
git clone https://github.com/eudanielhenrique/bora-automatizar-skills.git ~/.claude/skills/bora-automatizar-skills && cd ~/.claude/skills/bora-automatizar-skills && chmod +x setup && ./setup
```

### Atualização

```bash
~/.claude/skills/bora-automatizar-skills/update
```

Puxa o que tiver de novo e reinstala os symlinks.

### Desinstalação

```bash
for s in ba-firestore-backup ba-firestore-restore ba-designer-system ba-proposta-comercial ba-oferta-produtizada ba-monitoramento-equipe; do rm -rf ~/.claude/skills/$s; done && rm -rf ~/.claude/skills/bora-automatizar-skills
```

---

MIT — [Daniel Henrique](https://github.com/eudanielhenrique)
