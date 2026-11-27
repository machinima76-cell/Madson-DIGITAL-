# MADSON DIGITAL — Site institucional

Site estático, responsivo e acessível para a agência **MADSON DIGITAL**. HTML, CSS e JavaScript puros, sem dependências externas, sem build obrigatório e pronto para **Cloudflare Pages e Workers Builds**.

---

## 1. Estrutura de arquivos

```
madson-digital/
├── index.html                    Página principal (todas as seções)
├── 404.html                      Página de erro (404-page no Workers / automático no Pages)
├── privacidade.html              Política de privacidade / LGPD
├── _headers                      Segurança + cache (Pages e Workers static assets)
├── wrangler.toml                 ★ Configuração para Workers Builds / Wrangler 4
├── .assetsignore                 Exclui arquivos de dev do upload de assets
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── assets/
│   ├── css/
│   │   ├── styles.css            Design system, componentes e seções
│   │   └── demos.css             Estilos das páginas de demonstração
│   ├── js/
│   │   ├── config.js             ★ Configuração central de contato
│   │   └── main.js               Navegação, abas, validação e envio
│   ├── fonts/                    Manrope + Cormorant Garamond (woff2 locais)
│   └── img/                      Fotografias WebP, favicon, ícones e OG image
├── demos/
│   ├── industrial.html
│   ├── gastronomia.html
│   ├── automotivo.html
│   └── engenharia.html
└── tools/
    ├── build_demos.py            Gerador opcional das 4 demonstrações
    └── check_site.py             Validador estático de links, SEO e formulário
```

As quatro páginas de demonstração são **HTML estático pronto**. O script `tools/build_demos.py` existe apenas para manter o markup consistente; execute `python3 tools/build_demos.py` se quiser alterar o conteúdo das quatro de uma só vez. Ele não é necessário para publicar.

O validador `python3 tools/check_site.py` confere links internos, âncoras, arquivos referenciados, imagens, metadados, JSON-LD e consistência do formulário. Não requer bibliotecas externas.

---

## 2. Como visualizar localmente

```bash
cd madson-digital
python3 -m http.server 8080 --bind 0.0.0.0
# abra http://localhost:8080
```

Também funciona com `npx serve .` ou abrindo `index.html` diretamente (os caminhos são relativos). Não há etapa de compilação.

---

## 3. Publicação na Cloudflare

### 3.1 Identifique o tipo de projeto criado

A Cloudflare oferece dois fluxos para site estático conectado ao Git. O log de implantação diz qual é:

| Trecho do log | Tipo | Requisito |
|---|---|---|
| `Executing user deploy command: npx wrangler deploy` | **Workers Builds** ("Deploy to Workers") | `wrangler.toml` com `[assets]` |
| `Deploying to Cloudflare Pages` / upload do build output | **Pages clássico** | apenas diretório de saída |

Este projeto já inclui `wrangler.toml` e `.assetsignore`, então funciona nos dois.

### 3.2 Workers Builds (Git / "Deploy to Workers")

Sem o `wrangler.toml`, o Wrangler 4 aborta com:

```
✘ [ERRO] Não foi possível detectar um diretório contendo arquivos estáticos
         (e.g. html, css e js) for the project
Falha: ocorreu um erro ao executar o comando de implantação
```

Configuração no painel do projeto:

- **Root directory:** `/` (vazio)
- **Build command:** vazio — é um site estático, não há compilação
- **Deploy command:** `npx wrangler deploy`
- **`name` em `wrangler.toml`:** deve ser **exatamente** o nome do Worker/projeto no painel

Validação local (requer Node ≥ 22.12, igual ao ambiente da Cloudflare):

```bash
npx wrangler@4.168.0 deploy --dry-run
# OK: "Read N files from the assets directory" e código de saída 0
```

`.assetsignore` impede que `README.md`, `tools/`, `wrangler.toml` e afins sejam publicados. **Não** adicione `_headers` a essa lista: a Cloudflare o lê como regras de cabeçalho.

### 3.3 Pages clássico (Git ou upload direto)

1. *Workers & Pages → Create → Pages → Upload assets*, ou conecte o repositório escolhendo **Pages**.
2. Envie o **conteúdo** da pasta (ou o ZIP descompactado), não a pasta que o contém.
3. **Framework preset:** None · **Build command:** vazio · **Build output directory:** `/` (ou `.`).
4. `404.html`, `_headers`, `robots.txt` e `sitemap.xml` são reconhecidos automaticamente.

### 3.4 Estrutura do repositório (causa comum de falha)

`index.html` deve estar na **raiz do repositório**. Não commite o arquivo `.zip`: extraia-o antes de enviar. Se você subiu os arquivos dentro de uma pasta (ex.: `madson-digital/`), ajuste `wrangler.toml`:

```toml
[assets]
directory = "./madson-digital"
```

e mova `.assetsignore` para dentro dessa pasta — ele precisa ficar na raiz de `assets.directory`. Alternativa: defina **Root directory** como `madson-digital` no painel e mantenha `directory = "./"`.

Domínio customizado: *projeto → Custom domains → Set up a custom domain*. O HTTPS é gratuito.

---

## 4. ⚠️ Ajustes obrigatórios antes de publicar

| O que | Onde | Valor atual |
|---|---|---|
| Domínio canônico | `assets/js/config.js` (`siteUrl`) | `https://madson-digital.pages.dev` |
| Domínio no HTML | `canonical`, `og:url`, `og:image`, `twitter:image` em **todos** os HTML | `https://madson-digital.pages.dev` |
| Domínio em `sitemap.xml` e `robots.txt` | raiz | `https://madson-digital.pages.dev` |
| Domínio no gerador | `SITE` em `tools/build_demos.py` | `https://madson-digital.pages.dev` |

Substitua pelo domínio real (ou pelo `*.pages.dev` que a Cloudflare atribuir ao projeto). Domínio incorreto quebra canonical, Open Graph e sitemap.

**Contato já configurado e funcional:**

- WhatsApp: `+55 47 99713-9043` → `wa.me/5547997139043`
- E-mail: `madsonsantos661@gmail.com`

Esses valores vivem em `assets/js/config.js` e, como fallback sem JavaScript, também aparecem nos `href` marcados com `data-whatsapp` / `data-email` no HTML. Se trocar número ou e-mail, atualize **ambos** os lugares. O `main.js` reescreve todos os links a partir de `config.js` quando o JavaScript está ativo.

**Redes sociais:** nenhuma URL foi informada, então **nenhum link falso foi criado**. A coluna "Redes sociais" do rodapé está oculta. Para ativá-la, edite `socials` em `assets/js/config.js`:

```js
socials: [
  { name: 'Instagram', url: 'https://instagram.com/seuperfil' },
  { name: 'LinkedIn',  url: 'https://linkedin.com/company/suaempresa' }
]
```

---

## 5. Como o formulário funciona (sem simulação)

O formulário valida no navegador (nome, telefone com DDD, e-mail, tipo de projeto, descrição mínima e consentimento LGPD) e entrega a mensagem por um **canal real**, escolhido pelo visitante:

- **Enviar pelo WhatsApp** → abre `https://wa.me/...?text=...` com a mensagem completa já preenchida, em nova aba.
- **Enviar por e-mail** → abre `mailto:...?subject=...&body=...` no aplicativo de e-mail do visitante.

O visitante confirma o envio no aplicativo. Não há `fetch()`, não há backend, não há banco de dados e não há tela de "mensagem enviada" fingindo sucesso. Por isso não é necessário nenhum serviço pago ou chave de API. Se no futuro quiser receber os dados automaticamente em um servidor, substitua `initForm()` em `assets/js/main.js` por uma Cloudflare Pages Function — o restante do site não muda.

Os links de planos e serviços (`data-prefill`) levam ao formulário e **pré-selecionam** a opção correspondente no campo "Tipo de projeto". As abas de planos são navegáveis por teclado (setas, Home e End).

---

## 6. Decisões de projeto

- **Identidade:** preto `#101116`, grafite `#20232B`, dourado `#B99B65`, off-white `#E8E5DF`, branco. Tipografia local (Manrope + Cormorant Garamond). Fotografia realista; sem robôs, circuitos, gradientes neon ou estética genérica de IA.
- **Sem dados inventados:** não há depoimentos, clientes, números de resultados ou preços. Planos exibem "Sob consulta". As quatro demonstrações estão identificadas como conteúdo fictício.
- **Acessibilidade:** link "pular para o conteúdo", foco visível, `aria-*` em menu/abas/formulário, mensagens de erro associadas via `aria-describedby`, `role="status"` para feedback, contraste revisado, `prefers-reduced-motion`, navegação completa por teclado e textos alternativos.
- **SEO:** `lang="pt-BR"`, título/descrição/canonical/Open Graph/Twitter por página, JSON-LD (`Organization` + `WebPage`), hierarquia de cabeçalhos, `robots.txt`, `sitemap.xml` e URLs amigáveis.
- **Performance:** fontes `woff2` locais com `preload`, imagens WebP otimizadas com `srcset` no hero e `loading="lazy"`/`decoding="async"` no restante, dimensões declaradas para evitar CLS, CSS/JS enxutos e sem bibliotecas de terceiros.
- **Privacidade:** sem cookies, analytics, pixels ou scripts externos. Veja `privacidade.html`.
- **Custo:** apenas Cloudflare Pages (plano gratuito). Domínio, se houver, é contratado à parte pelo cliente.

---

## 7. Verificação rápida antes do deploy

Execute `python3 tools/check_site.py` (deve terminar com `OK`). Em seguida:

- [ ] Substituir o domínio nos arquivos listados na seção 4
- [ ] Conferir número de WhatsApp e e-mail em `config.js` e nos `href`
- [ ] Adicionar redes sociais em `config.js` (ou manter a coluna oculta)
- [ ] Testar o formulário nos dois modos de envio
- [ ] Testar links do menu, das quatro demonstrações e da página 404
- [ ] Verificar no celular, tablet e desktop
