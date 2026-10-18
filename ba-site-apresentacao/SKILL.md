---
name: ba-site-apresentacao
description: Aplica ou audita a arquitetura visual de apresentação scrollytelling de alto impacto da BoraAutomatizar (Dark Obsidian Canvas, iluminação em azul elétrico #0060F0/#297FFF, tipografia editorial peso 400, header cápsula compactável, barra de progresso, modo apresentação/keynote, consoles operacionais no padrão Linear/SaaS de alta densidade, feixe de borda cônico giratório e simulador financeiro interativo). Use ao criar ou reformular landing pages, hotsites ou páginas de apresentação da BoraAutomatizar.
allowed-tools: Read Write Edit Bash Grep Glob
user-invocable: true
---

# /ba-site-apresentacao — Arquitetura Visual de Apresentação & Scrollytelling BoraAutomatizar

Você está agora no modo **site de apresentação de alto impacto da BoraAutomatizar**.
Este padrão transforma sites institucionais, hotsites e landing pages em experiências imersivas de apresentação (*keynote contínuo*), unindo estética dark-first com rigor de engenharia de software e telemetria de alta densidade.

> **Princípio Central:** Azul Elétrico como **Luz, Não Tinta**. O canvas é obsidiana azulada (`#02050b`). As cores de marca (`#0060F0`, `#297FFF`, `#7AB8FF`) atuam como emissores de luz (feixes cônicos, halos difusos, pontos de telemetria pulsantes), nunca como baldes de tinta cobrindo grandes superfícies.

---

## 1. Tokens de Design & Atmosfera

### Paleta Obsidiana & Azul Elétrico
| Token | Valor | Uso |
|---|---|---|
| `--ba-bg` | `#02050b` | Canvas base da aplicação (obsidiana azulada) |
| `--ba-bg-2` | `#060b16` | Superfícies elevadas e cartões |
| `--ba-bg-surface` | `rgba(235, 244, 255, 0.038)` | Fundos de vidro sutil (cards secundários) |
| `--ba-bg-elevated` | `rgba(10, 18, 34, 0.84)` | Modais, dropdowns e consoles de telemetria |
| `--ba-ink` | `#f0f6ff` | Texto primário de alto contraste |
| `--ba-ink-2` | `rgba(240, 246, 255, 0.72)` | Texto secundário (subtítulos, descrições) |
| `--ba-ink-dim` | `rgba(240, 246, 255, 0.42)` | Texto atenuado para contrastes editoriais |
| `--ba-line` | `rgba(232, 243, 255, 0.095)` | Bordas hairline internas (inset 1px) |
| `--ba-blue` | `#0060F0` | Azul primário da marca BoraAutomatizar |
| `--ba-neon` | `#297FFF` | Azul elétrico para destaques de emissão |
| `--ba-neon-2` | `#7AB8FF` | Azul luminoso para reflexos e destaques |

### Classes CSS Canônicas

```css
@property --ba-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

@keyframes ba-brotate {
  to { --ba-angle: 360deg; }
}

@keyframes ba-pulse-dot {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
    box-shadow: 0 0 12px #297FFF, 0 0 24px rgba(0, 96, 240, 0.65);
  }
  50% {
    transform: scale(1.25);
    opacity: 0.75;
    box-shadow: 0 0 18px #7AB8FF, 0 0 34px rgba(41, 127, 255, 0.9);
  }
}

/* Destaque Iluminado */
.ba-hl {
  color: #5ca3ff;
  text-shadow: 0 0 42px rgba(0, 96, 240, 0.55);
}

.ba-dim {
  color: rgba(240, 246, 255, 0.42);
}

/* Eyebrow Monospaçado com Ponto Pulsante */
.ba-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-geist-mono), monospace;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #7ab8ff;
}

.ba-eyebrow__dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #297FFF;
  box-shadow: 0 0 12px #297FFF;
  animation: ba-pulse-dot 2.4s ease-in-out infinite;
  flex-shrink: 0;
}

/* Matriz Halftone com Dissolve Radial (Sem cortes duros) */
.ba-halftone {
  background-image: radial-gradient(rgba(147, 197, 253, 0.28) 0.85px, transparent 1.35px);
  background-size: 18px 18px;
  mask-image: radial-gradient(ellipse 75% 65% at 50% 50%, #000 35%, transparent 95%);
}

/* Superfície de Vidro com Hairline Inset */
.ba-glass {
  background: linear-gradient(180deg, rgba(235, 244, 255, 0.048) 0%, rgba(235, 244, 255, 0.016) 100%);
  box-shadow: inset 0 0 0 1px rgba(232, 243, 255, 0.095);
  backdrop-filter: blur(16px) saturate(135%);
}

.ba-glass-strong {
  background: linear-gradient(180deg, rgba(12, 22, 42, 0.84) 0%, rgba(5, 10, 20, 0.92) 100%);
  box-shadow: inset 0 0 0 1px rgba(232, 243, 255, 0.12), 0 24px 60px rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(20px) saturate(140%);
}

/* Feixe de Borda Cônico Giratório */
.ba-border-beam {
  position: relative;
}

.ba-border-beam::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.5px;
  background: conic-gradient(
    from var(--ba-angle),
    transparent 0%,
    transparent 64%,
    rgba(0, 96, 240, 0.55) 76%,
    #5ca3ff 88%,
    #ffffff 94%,
    transparent 100%
  );
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: ba-brotate 3.2s linear infinite;
  pointer-events: none;
  z-index: 2;
}

/* Botão com Chip Circular Giratório */
.ba-btn {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  height: 52px;
  padding: 0 6px 0 24px;
  border-radius: 999px;
  background: linear-gradient(135deg, #0060F0 0%, #297FFF 60%, #5ca3ff 100%);
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 0 32px rgba(0, 96, 240, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.32);
  transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.ba-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 46px rgba(41, 127, 255, 0.68), inset 0 1px 0 rgba(255, 255, 255, 0.48);
}

.ba-btn__chip {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: #020712;
  color: #5ca3ff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.ba-btn:hover .ba-btn__chip {
  transform: rotate(45deg);
  color: #ffffff;
}

/* Foco e Desênfase em Grid de Cartões */
@media (hover: hover) {
  .ba-etrack:has(.ba-ecard:hover) .ba-ecard:not(:hover) {
    filter: opacity(0.42) saturate(0.65);
    transition: filter 0.35s ease;
  }
}
```

---

## 2. Padrões Estruturais Obrigatórios

### 1. Header Cápsula com Barra de Carga
* **Barra de Carga Superior:** Linha de `2.5px` fixada no topo (`z-index: 60`) que reflete o progresso do scroll com gradiente elétrico e sombra de brilho.
* **Cápsula Flutuante:** Inicialmente expandida (`max-w-[1440px]`). Ao rolar além de `40px`, transiciona suavemente para `max-w-[1080px]`, `rounded-full`, com fundo escuro translúcido e `backdrop-blur-2xl`.

### 2. Modo Apresentação (Keynote Deck)
* Permite que qualquer página funcione como uma apresentação executiva para reuniões e clientes.
* Acionado por atalho de teclado (`P` ou setas) ou botão **Apresentação** no header.
* Exibe barra flutuante inferior centralizada com controle de passos (`01 / 08`), navegação por setas (`←` e `→`) e suporte a tecla `ESC`.

### 3. Hero Editorial Restrito (Sem "Pill Fatigue")
* **Headline:** Peso `400` constante em títulos (`clamp(2.2rem, 4.4vw, 62px)`), tracking negativo (`-0.04em`), estruturado em duas frases equilibradas.
* **Selo Circular SVG Calibrado:** Selo com raio `r=44` (perímetro $\approx 276.4\text{px}$) com rotação suave contínua em `24s` sem colisão entre texto inicial e final.
* **Eliminação de Pill Fatigue:** Evitar empilhar múltiplos botões/pills no centro. Badges de telemetria devem ser integrados como régua hairline (`1px`) monospaçada no topo do console.

### 4. Console Operacional Agent-First (Showcase de Sistema)
* Não renderizar mockups decorativos sem utilidade.
* O console deve demonstrar a **ação autônoma do agente de IA** (triagem de áudio, classificação por intenção, movimentação de cards no kanban, agendamento de follow-ups).
* Ações humanas são apresentadas como **visibilidade e override** (intervir na conversa, assumir atendimento).

### 5. Iluminação de Texto Palavra por Palavra
* No manifesto ou proposta de valor, o texto acende progressivamente conforme o scroll:
  - Opacidade inicial: `0.22` (atenuado).
  - Opacidade ativa: `1.0` (branco puro).
  - Termos técnicos prioritários: classe `.ba-hl` com brilho azul.

### 6. Simulador Operacional Interativo com Recibo em Tempo Real
* Sliders ou botões de seleção de carga operacional (números de WhatsApp, atendentes, módulos extras).
* Exibição de recibo financeiro com números tabulares (`tabular-nums`) e recomendação automática do plano ideal.
* Geração dinâmica de link do WhatsApp com mensagem de diagnóstico pré-preenchida com os dados da simulação.

### 7. Globo de Malha Orbital WebGL/Canvas
* Renderizado via `<canvas>` com cálculo de esfera de Fibonacci (sem dependências pesadas externas).
* Conexões de arcos e nós pulsantes representando cidades e canais conectados no Brasil.
* Pausa automática quando fora do viewport via `IntersectionObserver`.

---

## 3. Checklist de Auditoria (/hm-designer)

Ao avaliar ou construir qualquer página no padrão BoraAutomatizar:
- [ ] **Canvas:** Está em `#02050b` (obsidiana azulada), nunca cinza neutro ou preto absoluto puro?
- [ ] **Luz:** O azul elétrico `#0060F0` / `#297FFF` atua como emissão de luz e destaques técnicos, sem fundos sólidos maciços desnecessários?
- [ ] **Bordas:** Cartões usam hairlines sutis `rgba(232, 243, 255, 0.095)` com cantos generosos (`rounded-[24px]` a `rounded-[28px]`)?
- [ ] **Tipografia:** Títulos usam peso `400` com tracking negativo (`-0.03em` a `-0.04em`)?
- [ ] **Números:** Métricas e valores financeiros utilizam `font-mono` com `tabular-nums`?
- [ ] **Responsividade:** Não há classes arbitrárias não-suportadas ou quebras de texto assimétricas em nenhum viewport?
- [ ] **Alinhamento:** Todas as páginas compartilham a mesma barra de navegação e rodapé monumental unificado?
