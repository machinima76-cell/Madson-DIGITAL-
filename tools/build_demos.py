#!/usr/bin/env python3
"""
Gerador das quatro páginas de demonstração do portfólio.

Uso:  python3 tools/build_demos.py
Saída: demos/{slug}.html

As páginas são HTML estático puro — este script existe apenas para evitar
duplicação de markup. Não é necessário executá-lo para publicar o site.
"""
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'demos'
OUT.mkdir(exist_ok=True)

SITE = 'https://madson-digital.pages.dev'

DEMOS = [
    {
        'slug': 'industrial',
        'brand': 'VETTA',
        'brand_sub': 'INDÚSTRIA DE PRECISÃO',
        'segment': 'Industrial',
        'image': 'projeto-industrial.webp',
        'image_alt': 'Linha de produção industrial com maquinário em aço e iluminação quente',
        'image2': 'demo-industrial-2.webp',
        'image2_alt': 'Componentes de aço usinado em bancada de fábrica',
        'page_desc': 'Demonstração de site institucional para o segmento industrial, criada pela Madson Digital: catálogo de capacidades, fichas técnicas e contato consultivo.',
        'hero_title': 'Precisão que se vê <em>antes do primeiro contato</em>.',
        'hero_lead': 'Uma apresentação institucional objetiva para indústrias que precisam explicar processos, capacidades e critérios técnicos a compradores e parceiros.',
        'about_kicker': 'A empresa',
        'about_title': 'Tecnologia aplicada com método.',
        'about_p1': 'A VETTA é uma empresa fictícia criada para esta demonstração. O conteúdo foi organizado para mostrar como um site industrial pode apresentar processos complexos sem perder clareza.',
        'about_p2': 'A navegação separa capacidades, materiais e formas de contato. Cada seção tem um objetivo único, e o visitante encontra o caminho para uma conversa comercial em qualquer ponto da página.',
        'quote': 'Quando o processo é complexo, a comunicação precisa ser simples.',
        'quote_cite': 'Direção de conteúdo · texto demonstrativo',
        'cards_kicker': 'Estrutura do site',
        'cards_title': 'O que esta demonstração apresenta',
        'cards_lead': 'Blocos de conteúdo pensados para o ciclo de decisão de um comprador industrial.',
        'cards': [
            ('01', 'Capacidades', 'Agrupamento de linhas de produção e serviços com descrições curtas e diretas.'),
            ('02', 'Fichas técnicas', 'Espaço para especificações, materiais, tolerâncias e documentos consultáveis.'),
            ('03', 'Contato consultivo', 'Formulário e chamadas que direcionam o visitante para uma conversa qualificada.'),
        ],
        'list_kicker': 'Detalhes de execução',
        'list_title': 'Do conteúdo à publicação',
        'list_lead': 'Elementos aplicados nesta página e replicáveis em projetos reais.',
        'list': [
            'Hierarquia visual para informações técnicas extensas',
            'Tipografia legível em telas pequenas',
            'Imagens otimizadas com carregamento sob demanda',
            'Seções ancoradas para navegação rápida',
            'Formulário e canais de contato reais no site principal',
            'Estrutura semântica preparada para SEO técnico',
        ],
        'cta_title': 'Quer uma presença digital com este nível de clareza?',
    },
    {
        'slug': 'gastronomia',
        'brand': 'CASA LUME',
        'brand_sub': 'COZINHA AUTORAL',
        'segment': 'Gastronomia',
        'image': 'projeto-gastronomia.webp',
        'image_alt': 'Mesa posta em restaurante de cozinha autoral com luz de velas',
        'image2': 'demo-gastronomia-2.webp',
        'image2_alt': 'Balcão de cozinha contemporânea com louças minimalistas',
        'page_desc': 'Demonstração de site para gastronomia criada pela Madson Digital: atmosfera, cardápio, reserva e fotografia integrada à identidade.',
        'hero_title': 'Uma experiência que começa <em>antes da reserva</em>.',
        'hero_lead': 'Um site que apresenta o ambiente, a proposta da cozinha e as informações práticas sem disputar atenção com a fotografia.',
        'about_kicker': 'A casa',
        'about_title': 'Atmosfera em primeiro plano.',
        'about_p1': 'A Casa Lume é um restaurante fictício criado para esta demonstração. A página foi construída com imagens amplas, intervalos generosos e tipografia elegante para transmitir o clima da experiência.',
        'about_p2': 'As informações essenciais — cardápio, horários e reserva — aparecem em blocos fáceis de localizar, inclusive no celular, onde a maior parte das decisões acontece.',
        'quote': 'O primeiro prato é servido pelos olhos.',
        'quote_cite': 'Direção de conteúdo · texto demonstrativo',
        'cards_kicker': 'Estrutura do site',
        'cards_title': 'O que esta demonstração apresenta',
        'cards_lead': 'Conteúdo organizado para informar sem quebrar o clima da marca.',
        'cards': [
            ('01', 'Cardápio', 'Seções por momentos da refeição, com espaço para descrições e atualizações sazonais.'),
            ('02', 'Atmosfera', 'Fotografia integrada ao layout, com cortes e proporções pensados para cada tela.'),
            ('03', 'Reserva', 'Informações de contato e localização em destaque, com chamada única e objetiva.'),
        ],
        'list_kicker': 'Detalhes de execução',
        'list_title': 'Leveza também é técnica',
        'list_lead': 'Como a estética foi preservada sem sacrificar desempenho.',
        'list': [
            'Imagens em WebP com dimensões declaradas',
            'Carregamento sob demanda fora da primeira tela',
            'Contraste revisado para leitura sobre fotografia',
            'Navegação por teclado e foco visível',
            'Layout responsivo com hierarquia preservada',
            'Textos alternativos descritivos em todas as imagens',
        ],
        'cta_title': 'Quer um site que traduza a atmosfera do seu negócio?',
    },
    {
        'slug': 'automotivo',
        'brand': 'VECTOR',
        'brand_sub': 'AUTOMOTIVO',
        'segment': 'Automotivo',
        'image': 'projeto-automotivo.webp',
        'image_alt': 'Sedã escuro em showroom de concreto com iluminação dourada discreta',
        'image2': 'demo-automotivo-2.webp',
        'image2_alt': 'Detalhe da dianteira e roda de um automóvel escuro em showroom',
        'page_desc': 'Demonstração de site automotivo criada pela Madson Digital: vitrine de veículos, fichas técnicas e contato comercial direto.',
        'hero_title': 'Cada detalhe <em>em primeiro plano</em>.',
        'hero_lead': 'Uma vitrine digital que valoriza o produto, organiza categorias e transforma interesse em uma conversa comercial.',
        'about_kicker': 'A marca',
        'about_title': 'O produto com espaço para respirar.',
        'about_p1': 'A Vector é uma marca fictícia criada para esta demonstração. A composição usa áreas generosas de fundo escuro para que o veículo seja o centro de atenção em qualquer largura de tela.',
        'about_p2': 'As fichas de produto seguem um padrão repetível: poucos dados em destaque, especificações agrupadas e uma única ação de contato ao final de cada bloco.',
        'quote': 'Uma boa vitrine não precisa de pressa, precisa de foco.',
        'quote_cite': 'Direção de conteúdo · texto demonstrativo',
        'cards_kicker': 'Estrutura do site',
        'cards_title': 'O que esta demonstração apresenta',
        'cards_lead': 'Componentes que sustentam uma vitrine de produtos sem excesso de elementos.',
        'cards': [
            ('01', 'Vitrine', 'Agrupamento por categoria com imagem, nome e link para detalhes.'),
            ('02', 'Ficha técnica', 'Especificações organizadas em blocos curtos, fáceis de comparar.'),
            ('03', 'Contato comercial', 'Chamada para atendimento presente na hero e ao fim de cada seção.'),
        ],
        'list_kicker': 'Detalhes de execução',
        'list_title': 'Desempenho para imagens grandes',
        'list_lead': 'Fotografia de produto sem comprometer o tempo de carregamento.',
        'list': [
            'Imagens responsivas e compactadas em WebP',
            'Dimensões declaradas para evitar deslocamento de layout',
            'Carregamento prioritário apenas na imagem principal',
            'Cartões com estados de foco e hover discretos',
            'Estrutura de cabeçalhos consistente',
            'Links internos funcionais em toda a página',
        ],
        'cta_title': 'Quer uma vitrine digital com esta presença?',
    },
    {
        'slug': 'engenharia',
        'brand': 'PRISMA',
        'brand_sub': 'ENGENHARIA & ARQUITETURA',
        'segment': 'Engenharia',
        'image': 'projeto-engenharia.webp',
        'image_alt': 'Maquete arquitetônica sobre mesa em estúdio de engenharia',
        'image2': 'demo-engenharia-2.webp',
        'image2_alt': 'Fachada de edifício contemporâneo em concreto e vidro ao anoitecer',
        'page_desc': 'Demonstração de site para engenharia criada pela Madson Digital: áreas de atuação, metodologia em etapas e apresentação técnica objetiva.',
        'hero_title': 'Método, precisão e <em>clareza estrutural</em>.',
        'hero_lead': 'Um site institucional que traduz processos técnicos em uma leitura ordenada, com linguagem profissional e navegação direta.',
        'about_kicker': 'O escritório',
        'about_title': 'Complexidade bem organizada.',
        'about_p1': 'A Prisma é uma empresa fictícia criada para esta demonstração. O objetivo aqui é mostrar como disciplinas, etapas de trabalho e documentos podem conviver em uma estrutura simples de navegar.',
        'about_p2': 'Em vez de longos blocos de texto, a informação foi dividida em seções numeradas, listas e cartões — um formato que facilita tanto a leitura quanto a manutenção futura do conteúdo.',
        'quote': 'Clareza é parte do projeto, não um detalhe da apresentação.',
        'quote_cite': 'Direção de conteúdo · texto demonstrativo',
        'cards_kicker': 'Estrutura do site',
        'cards_title': 'O que esta demonstração apresenta',
        'cards_lead': 'Blocos pensados para explicar serviços técnicos sem jargão desnecessário.',
        'cards': [
            ('01', 'Áreas de atuação', 'Disciplinas separadas em cartões com descrições curtas e consistentes.'),
            ('02', 'Metodologia', 'Etapas de trabalho numeradas, do briefing à entrega.'),
            ('03', 'Apresentação técnica', 'Espaço para documentos, imagens de projeto e contato por disciplina.'),
        ],
        'list_kicker': 'Detalhes de execução',
        'list_title': 'Base sólida para crescer',
        'list_lead': 'Escolhas técnicas aplicadas a esta demonstração.',
        'list': [
            'Componentes reutilizáveis entre seções',
            'Metadados, canonical e Open Graph próprios',
            'Cabeçalhos semânticos em hierarquia correta',
            'Links com estados de foco visíveis',
            'Imagens otimizadas e carregadas sob demanda',
            'Textos alternativos e navegação por teclado',
        ],
        'cta_title': 'Quer apresentar seu trabalho técnico com mais clareza?',
    },
]

TEMPLATE = Template(r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$brand — Demonstração $segment | MADSON DIGITAL</title>
  <meta name="description" content="$page_desc">
  <meta name="author" content="MADSON DIGITAL">
  <meta name="theme-color" content="#101116">
  <meta name="color-scheme" content="dark light">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="$site/demos/$slug.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MADSON DIGITAL">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:url" content="$site/demos/$slug.html">
  <meta property="og:title" content="$brand — Demonstração de site $segment_lc">
  <meta property="og:description" content="$page_desc">
  <meta property="og:image" content="$site/assets/img/$image">
  <meta property="og:image:width" content="900">
  <meta property="og:image:height" content="600">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="$brand — Demonstração de site $segment_lc">
  <meta name="twitter:description" content="$page_desc">
  <meta name="twitter:image" content="$site/assets/img/$image">
  <link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../assets/img/icon-192.png" sizes="192x192" type="image/png">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
  <link rel="manifest" href="../site.webmanifest">
  <link rel="preload" href="../assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../assets/fonts/cormorant-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../assets/css/styles.css">
  <link rel="stylesheet" href="../assets/css/demos.css">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "$brand — Demonstração $segment",
    "description": "$page_desc",
    "url": "$site/demos/$slug.html",
    "inLanguage": "pt-BR",
    "isPartOf": { "@type": "WebSite", "name": "MADSON DIGITAL", "url": "$site/" },
    "about": { "@type": "Thing", "name": "Projeto demonstrativo de site institucional" }
  }
  </script>
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<div class="demo-banner">
  <div class="container demo-banner__inner">
    <span>Projeto demonstrativo — empresa, textos e imagens fictícios criados pela Madson Digital.</span>
    <a href="../index.html#portfolio">Voltar ao portfólio ↗</a>
  </div>
</div>

<header class="demo-header">
  <div class="container demo-header__inner">
    <a class="demo-brand" href="#conteudo">
      <strong>$brand</strong><small>$brand_sub</small>
    </a>
    <nav class="demo-nav" aria-label="Navegação da demonstração">
      <a href="#empresa">Empresa</a>
      <a href="#solucoes">Estrutura</a>
      <a href="#processo">Execução</a>
      <a href="#contato">Contato</a>
    </nav>
    <a class="btn btn--outline-gold btn--sm" href="../index.html#contato">Solicitar orçamento</a>
  </div>
</header>

<main id="conteudo">
  <section class="demo-hero" aria-labelledby="demo-title">
    <div class="demo-hero__media">
      <img src="../assets/img/$image" width="900" height="600" fetchpriority="high" alt="$image_alt">
    </div>
    <div class="container demo-hero__content">
      <p class="demo-kicker reveal">Demonstração $segment · $brand</p>
      <h1 class="reveal" data-delay="1" id="demo-title">$hero_title</h1>
      <p class="reveal" data-delay="2">$hero_lead</p>
      <div class="demo-hero__actions reveal" data-delay="3">
        <a class="btn btn--gold" href="#solucoes">Explorar a estrutura</a>
        <a class="btn btn--outline-light" href="../index.html#portfolio">Ver outros projetos</a>
      </div>
    </div>
  </section>

  <section class="demo-section surface-light" id="empresa" aria-labelledby="empresa-title">
    <div class="container">
      <div class="demo-split">
        <figure class="reveal"><img src="../assets/img/$image2" width="900" height="600" loading="lazy" decoding="async" alt="$image2_alt"></figure>
        <div class="demo-split__body reveal" data-delay="1">
          <p class="demo-kicker">$about_kicker</p>
          <h2 id="empresa-title" style="font-family:var(--font-display);font-weight:400;font-size:clamp(2.2rem,4vw,3.2rem);line-height:1.1;margin-top:1.1rem">$about_title</h2>
          <p>$about_p1</p>
          <p>$about_p2</p>
          <hr class="u-hairline">
          <div class="demo-quote">
            <p>“$quote”</p>
            <small>$quote_cite</small>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="demo-section" id="solucoes" aria-labelledby="solucoes-title">
    <div class="container">
      <div class="demo-section__head reveal">
        <p class="demo-kicker">$cards_kicker</p>
        <h2 id="solucoes-title">$cards_title</h2>
        <p>$cards_lead</p>
      </div>
      <div class="demo-cards">
        $cards_markup
      </div>
    </div>
  </section>

  <section class="demo-section surface-light" id="processo" aria-labelledby="processo-title">
    <div class="container demo-split">
      <div class="demo-split__body reveal">
        <p class="demo-kicker">$list_kicker</p>
        <h2 id="processo-title" style="font-family:var(--font-display);font-weight:400;font-size:clamp(2.2rem,4vw,3.2rem);line-height:1.1;margin-top:1.1rem">$list_title</h2>
        <p>$list_lead</p>
        <ul class="demo-list">
          $list_markup
        </ul>
      </div>
      <figure class="reveal" data-delay="1"><img src="../assets/img/$image" width="900" height="600" loading="lazy" decoding="async" alt="$image_alt"></figure>
    </div>
  </section>

  <section class="demo-cta" id="contato" aria-labelledby="cta-title">
    <div class="container demo-cta__inner">
      <div class="reveal">
        <h2 id="cta-title">$cta_title</h2>
        <p>Esta é uma página demonstrativa. A Madson Digital adapta estrutura, conteúdo e identidade ao seu negócio.</p>
      </div>
      <div class="reveal" data-delay="1" style="display:flex;gap:.8rem;flex-wrap:wrap">
        <a class="btn btn--gold" href="../index.html#contato">Solicitar orçamento</a>
        <a class="btn btn--outline-light" href="../index.html#portfolio">Voltar ao portfólio</a>
      </div>
    </div>
  </section>
</main>

<footer class="demo-footer">
  <div class="container">
    <div class="demo-footer__grid">
      <div>
        <a class="demo-brand" href="#conteudo"><strong>$brand</strong><small>$brand_sub</small></a>
        <p>Projeto demonstrativo criado pela Madson Digital. Nome, textos e imagens são fictícios e não representam clientes ou resultados.</p>
      </div>
      <nav class="demo-footer__links" aria-label="Links da demonstração">
        <a href="#empresa">Empresa</a>
        <a href="#solucoes">Estrutura</a>
        <a href="#processo">Execução</a>
        <a href="../index.html#portfolio">Portfólio Madson Digital</a>
        <a href="../privacidade.html">Política de privacidade</a>
      </nav>
      <div class="demo-footer__links">
        <span style="color:var(--ink-faint)">Um projeto de</span>
        <a href="../index.html">MADSON DIGITAL ↗</a>
      </div>
    </div>
    <div class="demo-footer__bottom">
      <span>© <span data-year>2026</span> Demonstração $segment · conteúdo ilustrativo</span>
      <a href="../index.html">Voltar ao site principal</a>
    </div>
  </div>
</footer>

<script src="../assets/js/config.js" defer></script>
<script src="../assets/js/main.js" defer></script>
</body>
</html>
''')


def render(d):
    cards = '\n        '.join(
        '<article class="demo-card reveal" data-delay="{}"><span class="demo-card__num">{}</span>'
        '<h3>{}</h3><p>{}</p></article>'.format(i, num, title, desc)
        for i, (num, title, desc) in enumerate(d['cards'])
    )
    items = '\n          '.join('<li>{}</li>'.format(x) for x in d['list'])
    values = dict(d, site=SITE, segment_lc=d['segment'].lower(),
                  cards_markup=cards, list_markup=items)
    return TEMPLATE.substitute(values)


for demo in DEMOS:
    path = OUT / (demo['slug'] + '.html')
    path.write_text(render(demo), encoding='utf-8')
    print('gerado:', path.relative_to(ROOT))
