# bora-automatizar-skills (v1.6)

Skills operacionais para o Claude Code: backup/restore do Firestore, design system, geração de proposta comercial / oferta produtizada, monitoramento de equipe e entrega de projetos Eter (integrações + controle operacional) do Bora Automatizar.

## Skills disponíveis

- `/ba-firestore-backup` — Exporta collections do Firestore para um arquivo JSON local
- `/ba-firestore-restore` — Restaura dados no Firestore a partir de um arquivo JSON de backup
- `/ba-designer-system` — Aplica o design system real do Bora Automatizar em 3 modos (Landing Page, Sistema/App, Oferta/Produto)
- `/ba-proposta-comercial` — Gera proposta comercial em HTML single-file no padrão visual Bora Automatizar
- `/ba-oferta-produtizada` — Gera landing page de oferta produtizada (escassez, cases, FAQ) no padrão visual mais recente da marca
- `/ba-monitoramento-equipe` — Boletim diário/semanal de equipe de WhatsApp (TPR, heatmap, palavras críticas, distribuição de carga)
- `/ba-integracoes` — Conecta o cliente Eter a sistemas que ele já usa (Sheets, ClickUp, Notion, Trello, Stripe, Shopify, Calendly, RD Station, Pipedrive, webhook genérico) + orquestrador de fluxos + deploy
- `/ba-controle-operacional` — Substitui a planilha do cliente Eter por controle via CSV + linguagem natural (financeiro, estoque, vendas, clientes, fornecedores, tarefas, funcionários, projetos, relatório mensal, dashboard)

Cada skill tem seu próprio SKILL.md na subpasta.
