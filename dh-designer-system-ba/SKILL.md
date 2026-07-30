---
name: dh-designer-system-ba
description: Aplica o design system real do Bora Automatizar (boraautomatizar.com.br) — tipografia Sora + Neue Haas Grotesk, paleta azul #0060F0, botões pill, estrutura de seções obrigatória, animação fade+blur+slide. Tokens extraídos direto do Elementor da home, não são estimativa. Use ao construir ou restilizar landing pages, seções ou componentes que devem seguir essa identidade visual.
---

# /dh-designer-system-ba — Design System Bora Automatizar

Você está agora no **modo design system Bora Automatizar**. Aplique estes tokens visuais — extraídos diretamente do Elementor da home real (page ID 73), não estimados — em qualquer página, seção ou componente que o usuário pedir.

## Princípio central

Esses valores são fonte da verdade, não ponto de partida. Não arredonde, não "melhore", não substitua por valor parecido de outro design system. Se um token que você precisa não está listado aqui, sinalize que está extrapolando — não invente como se fosse extraído.

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
| Azul primário                  | `#0060F0`                        |
| Azul badge / overlay           | `#0060F0C9`                      |
| Fundo seção clara A             | `#F5F5F7`                        |
| Fundo seção clara B             | `#FFFFFF`                        |
| Fundo hero / CTA escuro          | herdado do tema (dark)           |
| Texto principal                 | `#000000`                        |
| Texto secundário                | `#666666` / `#888888`            |
| Texto hero                      | `#FFFFFF`                        |
| Texto hero secundário           | `#FFFFFFB3`                      |
| Amarelo (acento secundário)     | `#D9E021` — usar com moderação   |

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

Padrão em todo elemento que entra na viewport:

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

## Como aplicar num projeto

1. **Identifique a stack** (CSS puro, Tailwind, CSS-in-JS, design tokens de outro sistema) e traduza os tokens acima pro formato certo — variáveis CSS, `tailwind.config`, tema de componentes. Não copie tabelas markdown pro código.
2. **Aplique a hierarquia tipográfica exata**, peso por peso — o erro de H2 em 600 é o mais comum, cheque isso especificamente.
3. **Siga a estrutura de seções obrigatória** ao montar uma landing/página nova do zero. Se a página já existe e só está sendo restilizada, mantenha a ordem de conteúdo mas ajuste cores/tipografia/espaçamento pros tokens.
4. **Aplique a animação de entrada** nos elementos que entram na viewport (scroll reveal), não em tudo de uma vez.
5. **Confirme que é o projeto certo** antes de aplicar — esse design system é do Bora Automatizar especificamente. Se o usuário está trabalhando em outro cliente/produto e pede "aquele design que a gente usa", confirme que é este antes de aplicar.

## Regras

- Fonte da verdade são os valores extraídos do Elementor real — nunca estime ou aproxime.
- Peso 600 em H2 de seção é proibido — sempre 400.
- Amarelo `#D9E021` é acento secundário — usar com moderação, nunca como cor dominante.
- Botões sempre pill (`border-radius: 50px`), nunca cantos retos ou levemente arredondados.
- Se um token necessário não estiver nesta lista (ex: espaçamento entre seções, breakpoints), diga explicitamente que está extrapolando em vez de apresentar como extraído.
