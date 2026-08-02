# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [1.6.0] — 2026-08-02

### Skills

- `/ba-integracoes` (nova) — conecta um cliente Eter a sistemas que já usa: Sheets/ClickUp/Notion/Trello (MCP), Stripe/Shopify/Calendly/RD Station/Pipedrive (cliente Python), webhook genérico, orquestrador de fluxos YAML e deploy Docker/Coolify. Adaptada de um pacote de terceiros (asv-digital/pack-integracoes) — removida a marca original. Módulo de notificação WhatsApp/Zappfy removido (Bora Automatizar já tem sistema próprio); notificador ficou só Slack/Discord/Telegram.
- `/ba-controle-operacional` (nova) — substitui a planilha de um cliente Eter por controle via CSV + linguagem natural: financeiro, estoque, vendas, clientes, fornecedores, tarefas, funcionários, projetos, relatório mensal e dashboard rápido. Adaptada de um pacote de terceiros (asv-digital/skills-fim-das-planilhas) — removida a marca original.
- `/eter-scope` (nova) — dado um cliente do Eter CRM, lê respostas do formulário e anotações da call e produz o desenho técnico da solução: mapeamento do processo atual vs. automatizado, módulos a construir, stack recomendada (n8n/Make, Evolution API/Z-API, GPT-4o, Typebot, etc.), integrações necessárias, dependências do cliente, fora do escopo, estimativa de complexidade (pequena/média/grande) e prazo. Output alimenta diretamente o `/eter-proposta`.

## [1.5.0] — 2026-08-02

### Breaking

- Repositório renomeado de `daniel-skills` para `bora-automatizar-skills` (novo remote: `eudanielhenrique/bora-automatizar-skills`).
- Todos os prefixos de skill trocados de `dh-` para `ba-`. `dh-designer-system-ba` virou `ba-designer-system` (suprimido o sufixo `-ba` redundante com o novo prefixo). Instalações antigas devem rodar a desinstalação do README e reinstalar do zero.

### Skills

- `/ba-monitoramento-equipe` (nova) — boletim diário e análise semanal de equipe de WhatsApp (TPR mediano, heatmap de demanda, mensagens críticas, distribuição de carga, alertas de tendência). Scripts Python stdlib-only, conversores pra export do WhatsApp Business e API Zappfy, envio automático via Zappfy. Adaptada de um pacote de terceiros (asv-digital/skill-monitoramento-equipe) — removida a marca original e as referências a outros módulos que não existem neste repositório.

## [1.4.0] — 2026-08-02

### Skills

- `/ba-designer-system` — adicionado o modo **Oferta/Produto**: tokens extraídos ao vivo do Projeto Éter (Next.js/Tailwind v4), a geração visual mais recente da marca — azul `#173CE0`, fundo quase-preto `#060608`, tipografia Inter peso 400 constante, tracking aberto em labels. Documentado como identidade distinta do modo Landing Page (azul `#0060F0`), não uma variação — os dois não devem se misturar.
- `/ba-proposta-comercial` — adicionada seção opcional **Cases** (setor, cliente, antes/depois, citação), inspirada no formato de prova social visto no Projeto Éter.
- `/ba-oferta-produtizada` (nova) — gera landing page de oferta produtizada em HTML single-file no padrão Oferta/Produto — hero com escassez, exemplos de serviço, cases reais, processo em etapas, prova social do founder, condições da oferta, FAQ. Baseada no Projeto Éter (boraautomatizar.com.br/eter).

## [1.3.0] — 2026-08-01

### Skills

- `/ba-proposta-comercial` — Gera proposta comercial em HTML single-file no padrão visual Bora Automatizar (mesmo CSS do modo Landing Page de `ba-designer-system`), com template + checklist de coleta de informação (escopo, cronograma, investimento parcelado, contato)

## [1.2.0] — 2026-07-30

### Skills

- `/ba-designer-system` — adicionado o modo **Sistema/App**: base para sidebar, tabelas e dashboards de ferramentas internas (dark-first, sem pill, escala tipográfica de UI). Compartilha cor de marca e tipografia com o modo Landing Page, mas estrutura, radius e paleta neutra são próprios — não são extraídos, são uma base desenhada, marcada como tal.

## [1.1.0] — 2026-07-30

### Skills

- `/ba-designer-system` — Aplica o design system do Bora Automatizar (tipografia, cores, botões, estrutura de seções, animação), extraído do Elementor da home real

### Infraestrutura

- `update` — script único que puxa o repo e reinstala os symlinks

## [1.0.0] — 2026-07-13

Release inicial.

### Skills

- `/ba-firestore-backup` — Backup do Firestore para JSON com logging e confirmação
- `/ba-firestore-restore` — Restore do Firestore com conversão de tipos, clearCollection e confirmação de destino

### Infraestrutura

- Setup script com symlinks automáticos para `~/.claude/skills/`
