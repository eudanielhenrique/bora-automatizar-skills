---
name: ba-seo-local
description: Analisa o contexto real de um projeto Bora Automatizar (serviços, área de atuação, domínio) e gera SEO local programático — matriz serviço×cidade, páginas hub por serviço (pra não ficarem órfãs), sitemap.xml, robots.txt e schema.org Service/LocalBusiness. Use quando o cliente precisa aparecer no Google pra buscas do tipo "[serviço] em [cidade]" / "[serviço] [cidade] [estado]", ao lançar um site novo com atuação multi-cidade, ou ao diagnosticar por que páginas de SEO local pararam de rankear (geralmente: páginas órfãs sem link interno).
allowed-tools: Read Write Edit Bash Grep Glob
user-invocable: true
---

# /ba-seo-local — SEO Local Programático

Você está agora no **modo SEO local**. Gera (ou corrige) a geração automática de páginas `[serviço] em [cidade] - [estado]` a partir do contexto real do projeto — nunca de um template genérico copiado de outro cliente. Cada projeto tem serviços diferentes, área de atuação diferente, stack diferente.

Aplica tanto pra **criar do zero** (projeto novo que precisa de SEO local) quanto pra **diagnosticar** um site que já tem essas páginas mas parou de aparecer no Google — nesse segundo caso vá direto pra seção "Diagnóstico de queda de ranking" no fim.

## Por que isso existe

SEO local programático (uma página por combinação serviço×cidade) é o jeito de aparecer pra milhares de buscas long-tail ("chatbot WhatsApp Vitória ES", "sistema de multiatendimento São Paulo") sem escrever cada página à mão. Funciona — **mas só se o Google conseguir confiar e rastrear essas páginas**. A causa nº 1 de essas páginas pararem de rankear (ou nunca decolarem) não é o conteúdo, é arquitetura de crawl: página que só existe no `sitemap.xml`, sem nenhum link interno apontando pra ela, é **página órfã**, e órfã é a primeira coisa que o Google deixa de rastrear quando reavalia o domínio (troca de host, outage, qualquer sinal de instabilidade).

## 1. Investigação do projeto real

Nunca gere a matriz sem antes extrair isso do projeto:

```bash
# Stack e framework (define onde a página vai morar)
cat package.json composer.json 2>/dev/null | head -30
ls next.config.* wp-config.php 2>/dev/null

# Domínio canônico real (não assuma — pode já estar quebrado/duplicado)
grep -rn "NEXT_PUBLIC_SITE_URL\|baseUrl\|SITE_URL" --include="*.ts" --include="*.env*" . 2>/dev/null | head -10

# Serviços já vendidos — nunca invente, extraia do copy real (home, planos, proposta comercial)
grep -rln "planos\|serviços\|solu\(ç\|c\)" src/app src/components 2>/dev/null | head -10
```

Colete, com o fundador se não estiver claro no código:
- **Lista real de serviços/produtos** vendidos (não "o que soaria bem pra SEO" — o que a empresa de fato entrega. Página que promete algo que o negócio não faz é doorway page, risco de penalização).
- **Área de atuação real**: nacional (todas as cidades do Brasil), estadual, ou só uma região metropolitana. Isso muda o tamanho da matriz — não gere 5.570 cidades pra uma empresa que atende só a Grande Vitória.
- **Domínio canônico único** — apex (`exemplo.com.br`) ou `www`, nunca os dois servindo conteúdo idêntico sem redirect 301 entre eles. Se os dois resolvem (`curl -I` em cada um), isso é duplicação de conteúdo esperando pra acontecer.

## 2. Modelo de dados

Dois arrays, serviços e cidades, combinados em runtime — nunca arquivos estáticos por cidade (inviável de manter em escala).

```ts
// lib/programmatic-seo.ts
export type SeoCity = { name: string; slug: string; stateCode: string; stateName: string };
export type SeoService = {
  slug: string;
  name: string;              // usado em UI e listagens ("chatbot para WhatsApp")
  title: string;              // "%%service_title%% em %%city%% - %%state%% | Marca" (<title> da página)
  description: string;        // meta description com %%city%%
  contentTitle: string;       // H1 da página
  contentDescription: string; // subtítulo/intro
};

export const seoServices: SeoService[] = [ /* extraído da investigação acima, nunca inventado */ ];
export const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://www.exemplo.com.br"; // www ou apex — o que o DNS realmente resolve sem erro

function slugify(v: string) {
  return v.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

// cidades: puxe de um dataset IBGE (município + UF) já existente no projeto, ou do público
// github.com/kelvins/municipios-brasileiros se a área de atuação for nacional/estadual.
// Pra área metropolitana restrita, uma lista curta à mão é melhor que filtrar um dataset gigante.

export function parseSeoSlug(slug: string) {
  const service = seoServices.find((s) => slug.startsWith(`${s.slug}-`));
  if (!service) return null;
  const rest = slug.slice(service.slug.length + 1);
  const match = rest.match(/^(.+)-([a-z]{2})$/);
  if (!match) return null;
  // resolva cidade por (uf, citySlug) num Map pré-indexado — nunca .find() num array de milhares em cada request
  return { service, city /* ... */, slug: `${service.slug}-${city.slug}-${city.stateCode.toLowerCase()}` };
}

export function buildSeoUrl(service: SeoService, city: SeoCity) {
  return `${baseUrl}/${service.slug}-${city.slug}-${city.stateCode.toLowerCase()}`;
}
```

URL no formato `servico-cidade-uf` (um segmento dinâmico `[slug]` só) é mais simples de rotear que `/servico/cidade/uf` (3 segmentos aninhados) e carrega a keyword inteira num path só, o que ajuda tanto SEO quanto legibilidade do link.

## 3. A página (Next.js App Router)

Em `app/[slug]/page.tsx`, um catch-all de um segmento resolve três casos — hub de serviço, página de cidade, e 404 — nessa ordem:

```tsx
export function generateStaticParams() {
  // estático só pra top N cidades (as de maior volume de busca/porte) — o resto
  // renderiza sob demanda (dynamicParams default é true, não precisa declarar).
  // Gerar as 5.570 cidades do Brasil estaticamente no build é desperdício de build time
  // pra cidades que nunca vão receber uma visita.
  const hubParams = seoServices.map((s) => ({ slug: s.slug }));
  const cityParams = seoServices.flatMap((s) => priorityCities.map((c) => ({ slug: `${s.slug}-${c.slug}-${c.stateCode.toLowerCase()}` })));
  return [...hubParams, ...cityParams];
}

export async function generateMetadata({ params }): Promise<Metadata> {
  const { slug } = await params;
  const hub = getSeoService(slug); // match exato do slug = página hub, sem cidade
  if (hub) return { title: `...`, alternates: { canonical: `${baseUrl}/${hub.slug}` } };

  const parsed = parseSeoSlug(slug);
  if (!parsed) return {};
  return {
    title: fillTemplate(parsed.service.title, parsed.service, parsed.city),
    description: fillTemplate(parsed.service.description, parsed.service, parsed.city),
    alternates: { canonical: buildSeoUrl(parsed.service, parsed.city) }, // SEMPRE absoluto, nunca relativo
    openGraph: { locale: "pt_BR", type: "article", url: buildSeoUrl(parsed.service, parsed.city) },
  };
}

export default async function Page({ params }) {
  const { slug } = await params;
  const hub = getSeoService(slug);
  if (hub) return <ServiceHubPage service={hub} />;   // ver seção 4 — isso é o que impede a página órfã

  const parsed = parseSeoSlug(slug);
  if (!parsed) notFound();

  const schema = {
    "@context": "https://schema.org",
    "@type": "Service",
    name: fillTemplate(parsed.service.title, parsed.service, parsed.city),
    provider: { "@type": "Organization", name: "Marca", url: baseUrl },
    areaServed: { "@type": "City", name: parsed.city.name, address: { "@type": "PostalAddress", addressRegion: parsed.city.stateCode, addressCountry: "BR" } },
  };

  return (
    <main>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      {/* H1 = contentTitle preenchido, CTA real (WhatsApp/formulário), link de volta pro hub — seção 4 */}
    </main>
  );
}
```

## 4. Hub por serviço — a parte que ninguém faz e é a que importa

Sem isso, as páginas de cidade só existem no sitemap. Crie uma página índice por serviço (`/[slug]` com slug = serviço puro, sem sufixo de cidade) que lista as cidades atendidas, **capital do estado primeiro** (não ordem alfabética — "Vitória" começa com V e fica de fora de um corte dos primeiros N se for alfabético, e capital é onde está o maior volume de busca):

```ts
export function getSeoStates() {
  const CAPITAL_BY_UF: Record<string, string> = { ES: "Vitória", SP: "São Paulo", /* ...27 */ };
  // agrupe allCities por stateCode, ordene alfabético, e dentro de cada estado
  // promova a capital pro topo da lista antes de truncar quantas cidades mostrar
}
```

E então, **link nos dois sentidos**:
- Hub → cada página de cidade (óbvio, é o índice).
- Página de cidade → de volta pro hub ("Ver outras cidades").
- **Footer/nav global do site → os hubs de serviço.** Esse é o link que de fato tira a árvore inteira da orfandade — sem ele, só quem já está numa página de cidade (ninguém, se é órfã) acha o hub. Adicione uma coluna "Por cidade" ou similar no footer compartilhado, com um link por serviço.

Cheque com `grep -rn "buildSeoUrl\|getSeoCities" src/components` se alguma dessas páginas já é referenciada de fora — se o único resultado for o próprio arquivo de rota, elas são órfãs.

## 5. `robots.txt` e `sitemap.xml`

Convenção nativa do Next.js (`app/robots.ts` e `app/sitemap.ts`), sem lib extra:

```ts
// app/sitemap.ts
export default function sitemap(): MetadataRoute.Sitemap {
  const cityUrls = seoServices.flatMap((s) => getSeoCities().map((c) => ({ url: buildSeoUrl(s, c), changeFrequency: "monthly" as const, priority: 0.7 })));
  const hubUrls = seoServices.map((s) => ({ url: `${baseUrl}/${s.slug}`, changeFrequency: "weekly" as const, priority: 0.8 }));
  return [{ url: baseUrl, priority: 1 }, ...hubUrls, ...cityUrls];
}
```

Sitemap é descoberta, não substitui link interno — ele é o que avisa o Google que a página existe, link interno é o que convence o Google a gastar crawl budget rastreando ela de novo depois.

## 6. Um domínio canônico só

Se `curl -I https://exemplo.com.br` e `curl -I https://www.exemplo.com.br` respondem os dois `200` com conteúdo igual, isso é duplicação. O `metadataBase`/canonical no código resolve pro Google (se os dois hosts emitirem `<link rel="canonical">` pro mesmo host escolhido), mas o ideal é fechar isso na borda: redirect 301 do host secundário pro canônico direto no provedor de DNS/hosting (configuração de domínio na Vercel, por exemplo — não em middleware, é mais barato e mais confiável resolvido na borda).

## 7. Evite doorway page

Página que só troca o nome da cidade e mantém o resto idêntico, multiplicada por milhares, é o padrão clássico que as diretrizes de spam do Google (useful content / doorway pages) miram. Mitigações mínimas:
- Varie pelo menos um bloco com informação real por cidade quando disponível (não invente — se não tem, omita o bloco, não invente dado falso).
- Não gere cidade sem nenhuma relação com a área de atuação real (seção 1) só porque "mais página é melhor" — gera custo de crawl budget sem ganho, e dilui a relevância média do conjunto.
- CTA e prova social (cases, depoimentos) podem — e devem — ser os reais da empresa, não fabricados "cliente satisfeito em [cidade]" genérico.

## Diagnóstico de queda de ranking

Se o pedido é "essas páginas rankeavam antes e pararam", rode nessa ordem antes de mexer em qualquer coisa:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://exemplo.com.br/
curl -s -o /dev/null -w "%{http_code}\n" https://www.exemplo.com.br/
curl -s https://www.exemplo.com.br/robots.txt
curl -sD - -o /dev/null https://www.exemplo.com.br/servico-cidade-uf | grep -i "x-robots\|http/"
curl -s https://www.exemplo.com.br/servico-cidade-uf | grep -io '<title>[^<]*</title>\|rel="canonical"[^>]*\|name="robots"[^>]*'
```

Depois:
1. `git log --format="%h %ad %s" --date=short -- <arquivos de SEO>` — alguma troca de domínio (apex↔www) coincidindo com a janela de queda? Troca de host é sinal de "site move" pro Google, gera reavaliação de confiança por semanas.
2. `grep -rln "buildSeoUrl\|getSeoCities\|<nome-do-slug-de-serviço>" src/components src/app` — alguma dessas URLs é referenciada fora do próprio arquivo de rota? Se não, são órfãs — vá pra seção 4.
3. Confirma que não existe `noindex` nem em `<meta name="robots">` nem em header `X-Robots-Tag`.
4. Confirma host único (seção 6).

Entrega: diagnóstico com causa raiz (não "pode ser isso ou aquilo" — teste e confirme) + fix aplicado + validação (`tsc --noEmit`, build local, `curl` na página corrigida mostrando título/canonical certos).
