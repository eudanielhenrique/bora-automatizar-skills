---
name: dh-designer-system-ba
description: Aplica a identidade visual do Bora Automatizar em dois modos — Landing Page (tokens extraídos do Elementor real, para marketing/institucional) e Sistema/App (base desenhada para sidebar, tabelas e dashboards, para ferramentas internas densas em dados). Use ao construir ou restilizar qualquer produto do Bora Automatizar; confirme o modo antes de aplicar.
---

# /dh-designer-system-ba — Design System Bora Automatizar

Você está agora no **modo design system Bora Automatizar**. Essa skill tem duas seções estruturalmente incompatíveis entre si — **não misture**. Identifique qual se aplica antes de escrever qualquer CSS.

## Qual modo usar

| Se o projeto é...                                                    | Use            |
| --------------------------------------------------------------------- | -------------- |
| Site institucional, landing page, página de campanha, proposta comercial | **Landing Page** |
| Ferramenta interna, painel admin, SaaS com sidebar/tabelas/dashboards, CRUD | **Sistema/App**  |

Se não estiver óbvio, pergunte. Aplicar H1 de 75px ou botão pill numa tabela densa de dados é o erro que gerou essa separação — não repita.

## Princípio central

Os tokens da seção **Landing Page** são fonte da verdade — extraídos direto do Elementor da home real (page ID 73), não estimados. Não arredonde, não "melhore", não substitua por valor parecido.

Os tokens da seção **Sistema/App** são uma base desenhada, não extraída — não existe hoje um painel/admin real do Bora Automatizar pra extrair de lá. Eles reaproveitam a identidade de marca (cor primária, tipografia, acento) mas a estrutura, escala e paleta neutra foram desenhadas do zero para densidade de dados. Trate como ponto de partida sólido, não como valor imutável — ao contrário da seção Landing Page.

Se um token que você precisa não está listado em nenhuma das duas seções, sinalize que está extrapolando — não invente como se fosse extraído.

---

## Identidade compartilhada (vale nos dois modos)

- **Cor de marca:** `#0060F0` (azul primário) — ação principal, foco, destaque.
- **Acento raro:** `#D9E021` (amarelo) — usar com moderação extrema, nunca como cor dominante.
- **Tipografia:** Sora em tudo. Neue Haas Grotesk Text Pro é exclusiva de botões/CTA de marketing (ver Landing Page) — em UI de sistema, Sora cobre tudo, inclusive botões.

Tudo o mais — escala tipográfica, radius, paleta neutra, estrutura — diverge por completo entre os dois modos abaixo.

---

# Modo Landing Page (extraído — fonte da verdade)

Para site institucional, páginas de campanha, propostas comerciais.

## Tipografia

| Elemento           | Fonte                      | Tamanho | Peso    | Observação                            |
| ------------------ | --------------------------- | ------- | ------- | ------------------------------------- |
| H1 hero            | Sora                        | 75px    | 600     | line-height 85px, letter-spacing -2px |
| H2 seções          | Sora                        | 45px    | **400** | line-height 60px, letter-spacing -1px |
| Subtítulo hero     | Sora                        | 19px    | 300     | line-height 1.7em                     |
| Corpo / descrições | Sora                        | 14–16px | 400     | —                                     |
| Botões             | Neue Haas Grotesk Text Pro  | 18px    | 500     | —                                     |
| Labels / badges    | Sora                        | 11–13px | 600     | uppercase, letter-spacing 2px         |
| FAQ heading        | Sora                        | 94px    | 400     | azul #0060F0, decorativo              |

**Erro comum a evitar:** peso 600 nos H2 de seção. A home usa 400 — peso 600 deixa a página pesada, com cara de "landing page de infoproduto".

## Cores

| Uso                          | Cor                             |
| ----------------------------- | -------------------------------- |
| Azul badge / overlay           | `#0060F0C9`                      |
| Fundo seção clara A             | `#F5F5F7`                        |
| Fundo seção clara B             | `#FFFFFF`                        |
| Fundo hero / CTA escuro          | herdado do tema (dark)           |
| Texto principal                 | `#000000`                        |
| Texto secundário                | `#666666` / `#888888`            |
| Texto hero                      | `#FFFFFF`                        |
| Texto hero secundário           | `#FFFFFFB3`                      |

## Botões

```
Primário:
  background: #0060F0
  border-radius: 50px (pill)
  font: Neue Haas Grotesk Text Pro, 500, 17–18px
  padding: 20px 40–50px

Secundário:
  background: transparent
  border: 2px solid #FFFFFF (em fundo escuro) ou #CCCCCC (em fundo claro)
  border-radius: 50px (pill)
  font: Neue Haas Grotesk Text Pro, 500, 17–18px
```

## Estrutura de seções

Padrão obrigatório — toda página nova segue essa sequência:

1. **Hero escuro** — dark bg, H1 branco 75px, badge azul, 2 botões pill
2. **Seção #F5F5F7** — H2 45px peso 400, cards/conteúdo
3. **Seção #FFFFFF** — alternância
4. **Seção destaque** — fundo `#0060F0` para momento de conversão (ex: preços, LGPD)
5. **CTA final** — dark bg, heading 52–64px, 2 botões

## Animação de entrada

```css
selector {
  opacity: 0;
  filter: blur(7px);
  transform: translate(0px, 80px);
  animation: showFromBottom 0.5s ease forwards;
}

@keyframes showFromBottom {
  from { opacity: 0; filter: blur(7px); transform: translate(0px, 80px); }
  to   { opacity: 1; filter: blur(0);   transform: translate(0, 0); }
}
```

## Regras — Landing Page

- Fonte da verdade são os valores extraídos do Elementor real — nunca estime ou aproxime.
- Peso 600 em H2 de seção é proibido — sempre 400.
- Botões sempre pill (`border-radius: 50px`), nunca cantos retos ou levemente arredondados.

---

# Modo Sistema/App (desenhado — base para ferramentas internas)

Para painéis internos, SaaS com sidebar/tabelas/dashboards, qualquer CRUD. Dark-first, densidade de dados acima de impacto visual. Pill e escala tipográfica de hero **não pertencem aqui**.

## Paleta neutra (dark-first)

| Uso                        | Cor       |
| --------------------------- | --------- |
| Fundo base (app shell)      | `#0B0D12` |
| Fundo surface (sidebar, card) | `#12151B` |
| Fundo elevado (modal, dropdown, popover) | `#181C24` |
| Borda / hairline            | `#22262F` |
| Borda hover                 | `#2E333D` |
| Texto primário               | `#F5F5F7` |
| Texto secundário             | `#8A8F99` |
| Texto terciário / disabled   | `#565B66` |

Tema claro (se necessário): inverta usando `#FFFFFF`/`#F5F5F7`/`#EDEEF1` como base/surface/elevado e `#000000`/`#666666`/`#9AA0AA` como texto — mas dark é o padrão, só desvie com justificativa.

## Tipografia (escala de UI, não de hero)

| Elemento              | Tamanho | Peso | Observação                          |
| ---------------------- | ------- | ---- | ------------------------------------ |
| Título de página        | 24px    | 600  | —                                    |
| Título de seção/card     | 16–18px | 600  | —                                    |
| Header de tabela          | 12px    | 600  | uppercase, letter-spacing 1px, texto secundário |
| Corpo / célula            | 13–14px | 400  | —                                    |
| Número de dashboard (stat)| 32–40px | 600  | tabular-nums                         |
| Label de sidebar           | 13px    | 500  | —                                    |
| Caption / micro            | 11px    | 500  | texto terciário                      |

## Sidebar

```
width: 264px expandida / 72px colapsada (ícone só)
background: fundo surface (#12151B)
item:
  height: 40px, radius 8px, padding 0 12px
  ícone 18–20px + label 13px/500
  hover: bg neutro sutil (borda hairline em opacidade baixa)
  ativo: bg rgba(0,96,240,0.12) + texto/ícone #0060F0
label de seção (grupo de nav):
  uppercase, 11px/600, letter-spacing 1px, texto terciário
  padding-top 20px antes de novo grupo
```

## Tabelas

```
row height: 44px padrão (36px denso, 52px confortável — expor como opção, não fixar)
header: sticky, bg surface, border-bottom 1px hairline, label uppercase 12px/600
cell: 13–14px/400, padding 12px 16px
divisor entre linhas: border-bottom hairline — não zebra por padrão
  (zebra é aceitável em tabelas muito longas: bg surface alternado, nunca cor de marca)
hover de linha: bg neutro sutil
números: tabular-nums, alinhados à direita
ações de linha: aparecem no hover, alinhadas à direita
estado vazio / loading: obrigatório — nunca renderizar tabela em branco sem feedback
```

## Dashboards

```
grid: 12 colunas, gap 20–24px
stat tile:
  bg surface, radius 12px, border 1px hairline, padding 20–24px
  label uppercase pequeno no topo (12px/600, texto secundário)
  número grande abaixo (32–40px/600, tabular-nums)
  delta (seta + %) com cor semântica — verde/vermelho para positivo/negativo,
    NUNCA #0060F0 pra delta (azul é ação/marca, não status)
card de conteúdo: radius 12–16px, bg surface, border 1px hairline
gráficos: seguir a skill `dataviz` para paleta, formas e acessibilidade —
  #0060F0 como cor primária de série, não reinventar paleta aqui
```

## Botões (Sistema/App)

```
Primário:
  background: #0060F0
  border-radius: 8px
  font: Sora, 500, 14px
  padding: 8px 16px

Secundário:
  background: transparent
  border: 1px solid borda hairline
  border-radius: 8px
  font: Sora, 500, 14px

Destrutivo:
  background: transparent (borda/texto vermelho semântico) — mesma geometria do secundário
```

## Regras — Sistema/App

- Nunca use pill (`border-radius: 50px`) em UI de sistema — radius 6–8px em botões, 12–16px em cards.
- Nunca use a escala tipográfica de hero (75px, 45px) aqui — o teto é ~40px, reservado a números de dashboard.
- Azul `#0060F0` é ação e marca — não use como cor de status (sucesso/erro/aviso têm paleta semântica própria, fora desta skill).
- Tabela sem estado vazio/loading é bug de UX, não detalhe.
- Se o projeto pedir tema claro, inverta a paleta neutra mas mantenha `#0060F0` como está — não escureça/clareie a cor de marca.

---

## Como aplicar num projeto

1. **Confirme o modo** (Landing Page vs Sistema/App) antes de escrever qualquer token — são incompatíveis entre si.
2. **Identifique a stack** (CSS puro, Tailwind, CSS-in-JS, design tokens de outro sistema) e traduza os tokens pro formato certo — variáveis CSS, `tailwind.config`, tema de componentes. Não copie tabelas markdown pro código.
3. **Landing Page:** siga a hierarquia tipográfica e a estrutura de seções à risca — são extraídas, não interpretáveis.
4. **Sistema/App:** use a base como ponto de partida — ajuste densidade (row height, padding) ao produto real, mas mantenha cor de marca, tipografia Sora e a ausência de pill.
5. **Confirme que é o projeto certo** — essa identidade é do Bora Automatizar especificamente. Se o usuário pede "aquele design que a gente usa" em outro cliente/produto, confirme antes de aplicar.
