# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [1.4.0] — 2026-08-02

### Skills

- `/dh-designer-system-ba` — adicionado o modo **Oferta/Produto**: tokens extraídos ao vivo do Projeto Éter (Next.js/Tailwind v4), a geração visual mais recente da marca — azul `#173CE0`, fundo quase-preto `#060608`, tipografia Inter peso 400 constante, tracking aberto em labels. Documentado como identidade distinta do modo Landing Page (azul `#0060F0`), não uma variação — os dois não devem se misturar.
- `/dh-proposta-comercial` — adicionada seção opcional **Cases** (setor, cliente, antes/depois, citação), inspirada no formato de prova social visto no Projeto Éter.
- `/dh-oferta-produtizada` (nova) — gera landing page de oferta produtizada em HTML single-file no padrão Oferta/Produto — hero com escassez, exemplos de serviço, cases reais, processo em etapas, prova social do founder, condições da oferta, FAQ. Baseada no Projeto Éter (boraautomatizar.com.br/eter).

## [1.3.0] — 2026-08-01

### Skills

- `/dh-proposta-comercial` — Gera proposta comercial em HTML single-file no padrão visual Bora Automatizar (mesmo CSS do modo Landing Page de `dh-designer-system-ba`), com template + checklist de coleta de informação (escopo, cronograma, investimento parcelado, contato)

## [1.2.0] — 2026-07-30

### Skills

- `/dh-designer-system-ba` — adicionado o modo **Sistema/App**: base para sidebar, tabelas e dashboards de ferramentas internas (dark-first, sem pill, escala tipográfica de UI). Compartilha cor de marca e tipografia com o modo Landing Page, mas estrutura, radius e paleta neutra são próprios — não são extraídos, são uma base desenhada, marcada como tal.

## [1.1.0] — 2026-07-30

### Skills

- `/dh-designer-system-ba` — Aplica o design system do Bora Automatizar (tipografia, cores, botões, estrutura de seções, animação), extraído do Elementor da home real

### Infraestrutura

- `update` — script único que puxa o repo e reinstala os symlinks

## [1.0.0] — 2026-07-13

Release inicial.

### Skills

- `/dh-firestore-backup` — Backup do Firestore para JSON com logging e confirmação
- `/dh-firestore-restore` — Restore do Firestore com conversão de tipos, clearCollection e confirmação de destino

### Infraestrutura

- Setup script com symlinks automáticos para `~/.claude/skills/`
