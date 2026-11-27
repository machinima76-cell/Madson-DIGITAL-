#!/usr/bin/env python3
"""
Verificação estática do site MADSON DIGITAL.

Uso:  python3 tools/check_site.py
Checa: links internos e âncoras, arquivos referenciados, imagens, metadados
       básicos de SEO, JSON-LD, rótulos de formulário e consistência de
       pré-preenchimento. Não requer bibliotecas externas.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import json
import re
import sys
import xml.dom.minidom

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(ROOT.rglob('*.html'))
errors = []
warnings = []


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.refs = []          # (kind, value)
        self.labels_for = []
        self.controls = []      # aria-controls / aria-labelledby / aria-describedby
        self.images = []
        self.fields = []
        self.prefill = []
        self.options = []
        self.jsonld = []
        self.metas = {}
        self.title = ''
        self._in_title = False
        self._in_script_ld = False
        self._ld_buf = []
        self.lang = None
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src', 'srcset', 'imagesrcset'):
            if key in a:
                self.refs.append((key, a[key]))
        for key in ('aria-controls', 'aria-labelledby', 'aria-describedby'):
            if key in a:
                self.controls.extend((key, token) for token in a[key].split())
        if tag == 'link' and a.get('rel') == 'canonical':
            self.refs.append(('canonical', a.get('href', '')))
        if tag == 'img':
            self.images.append(a)
        if tag in ('input', 'select', 'textarea') and a.get('name'):
            self.fields.append((tag, a.get('id'), a.get('name')))
        if tag == 'label' and a.get('for'):
            self.labels_for.append(a['for'])
        if tag == 'option':
            self.options.append(a.get('value', ''))
        if 'data-prefill' in a:
            self.prefill.append(a['data-prefill'])
        if tag == 'meta':
            key = a.get('property') or a.get('name')
            if key:
                self.metas[key] = a.get('content', '')
        if tag == 'title':
            self._in_title = True
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self._in_script_ld = True
            self._ld_buf = []
        if tag == 'button' and not a.get('type'):
            warnings.append(f'{self._rel()}: <button> sem atributo type')

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        if tag == 'script' and self._in_script_ld:
            self.jsonld.append(''.join(self._ld_buf))
            self._in_script_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_script_ld:
            self._ld_buf.append(data)

    def _rel(self):
        return str(self.path.relative_to(ROOT))


def split_refs(value):
    """Extrai alvos de srcset / imagesrcset."""
    return [part.strip().split()[0] for part in value.split(',') if part.strip()]


def check_page(page, all_pages):
    rel = page._rel()
    ids = set(page.ids)

    if page.lang != 'pt-BR':
        errors.append(f'{rel}: lang deve ser pt-BR (encontrado {page.lang!r})')
    if not page.title.strip():
        errors.append(f'{rel}: <title> ausente')
    for needed in ('description', 'viewport', 'og:title', 'og:image'):
        if needed not in page.metas:
            errors.append(f'{rel}: metadado ausente: {needed}')
    if 'canonical' not in dict(page.refs):
        errors.append(f'{rel}: canonical ausente')

    for key, token in page.controls:
        if token not in ids:
            errors.append(f'{rel}: {key} aponta para id inexistente #{token}')

    for tag, field_id, name in page.fields:
        if field_id and field_id not in page.labels_for and tag != 'input':
            errors.append(f'{rel}: campo {name} sem <label for>')
        if field_id and field_id not in ids:
            errors.append(f'{rel}: campo {name} com id duplicado/ausente')

    for img in page.images:
        if 'alt' not in img:
            errors.append(f'{rel}: <img src={img.get("src")!r}> sem alt')
        for attr in ('width', 'height'):
            if attr not in img:
                warnings.append(f'{rel}: imagem {img.get("src")!r} sem {attr}')

    for block in page.jsonld:
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f'{rel}: JSON-LD inválido: {exc}')

    for kind, value in page.refs:
        if kind == 'canonical':
            if not value.startswith('https://'):
                errors.append(f'{rel}: canonical não absoluto: {value}')
            continue
        targets = split_refs(value) if kind in ('srcset', 'imagesrcset') else [value]
        for target in targets:
            target = target.strip()
            if not target:
                errors.append(f'{rel}: {kind} vazio')
                continue
            if target.startswith(('https://', 'http://', 'mailto:', 'tel:', 'data:')):
                if 'example.com' in target or 'SUBSTITUIR' in target:
                    warnings.append(f'{rel}: link externo com placeholder: {target}')
                continue
            if target in ('#', ''):
                errors.append(f'{rel}: link decorativo/quebrado: {kind}="{target}"')
                continue
            if target.startswith('#'):
                if target[1:] not in ids:
                    errors.append(f'{rel}: âncora inexistente {target}')
                continue
            path_part, _, fragment = unquote(target).partition('#')
            resolved = (page.path.parent / path_part).resolve()
            if not resolved.is_file():
                errors.append(f'{rel}: arquivo inexistente {target}')
                continue
            if fragment:
                target_page = all_pages.get(resolved)
                if target_page is None:
                    target_page = Page(resolved)
                    all_pages[resolved] = target_page
                if fragment not in set(target_page.ids):
                    errors.append(f'{rel}: âncora #{fragment} inexistente em {target}')


def main():
    if not HTML_FILES:
        errors.append('nenhum HTML encontrado')
    pages = {p.resolve(): Page(p) for p in HTML_FILES}
    for page in pages.values():
        check_page(page, pages)

    # Consistência: valores de data-prefill precisam existir no <select id="tipo">
    index = pages.get((ROOT / 'index.html').resolve())
    if index:
        options = set(index.options)
        for page in pages.values():
            for value in page.prefill:
                if value not in options:
                    errors.append(f'{page._rel()}: data-prefill {value!r} sem <option> correspondente')
        for field in ('nome', 'empresa', 'telefone', 'email', 'tipo', 'descricao', 'consent'):
            if not any(name == field for _, _, name in index.fields):
                errors.append(f'index.html: campo obrigatório ausente no formulário: {field}')
        for name in ('nome', 'telefone', 'email', 'tipo', 'descricao', 'consent'):
            if f'err-{name}' not in set(index.ids):
                errors.append(f'index.html: mensagem de erro ausente para {name}')

    # Configuração de deploy (Cloudflare Workers Builds / Wrangler 4)
    try:
        import tomllib
        with (ROOT / 'wrangler.toml').open('rb') as fh:
            wcfg = tomllib.load(fh)
        if not wcfg.get('name'):
            errors.append('wrangler.toml: campo name ausente')
        assets = wcfg.get('assets', {})
        asset_dir = assets.get('directory')
        if not asset_dir:
            errors.append('wrangler.toml: assets.directory ausente')
        elif not (ROOT / asset_dir).is_dir():
            errors.append(f'wrangler.toml: assets.directory inexistente: {asset_dir}')
        elif not (ROOT / asset_dir / 'index.html').is_file():
            errors.append(f'wrangler.toml: index.html não encontrado em {asset_dir}')
        if assets.get('not_found_handling') != '404-page':
            warnings.append('wrangler.toml: not_found_handling diferente de 404-page')
    except FileNotFoundError:
        errors.append('arquivo obrigatório ausente: wrangler.toml')
    except Exception as exc:
        errors.append(f'wrangler.toml inválido: {exc}')

    ignore = ROOT / '.assetsignore'
    if not ignore.is_file():
        errors.append('arquivo obrigatório ausente: .assetsignore')
    else:
        lines = [l.strip() for l in ignore.read_text(encoding='utf-8').splitlines()]
        for reserved in ('_headers', '_redirects'):
            if reserved in lines:
                errors.append(f'.assetsignore não deve ignorar {reserved} (são regras de roteamento)')

    # Arquivos de publicação
    for needed in ('_headers', 'robots.txt', 'sitemap.xml', 'site.webmanifest', '404.html',
                   'assets/js/config.js', 'assets/js/main.js', 'assets/css/styles.css',
                   'assets/img/favicon.svg', 'assets/img/og-image.jpg'):
        if not (ROOT / needed).is_file():
            errors.append(f'arquivo obrigatório ausente: {needed}')
    xml.dom.minidom.parse(str(ROOT / 'sitemap.xml'))
    json.loads((ROOT / 'site.webmanifest').read_text(encoding='utf-8'))

    # CSS: equilíbrio de chaves
    for css in (ROOT / 'assets/css').glob('*.css'):
        text = css.read_text(encoding='utf-8')
        if text.count('{') != text.count('}'):
            errors.append(f'{css.name}: chaves CSS desbalanceadas')

    print(f'Verificadas {len(pages)} páginas HTML e {sum(len(p.refs) for p in pages.values())} referências.')
    for w in warnings:
        print('  AVISO:', w)
    for e in errors:
        print('  ERRO :', e)
    if errors:
        print(f'\nFALHA: {len(errors)} erro(s).')
        return 1
    print('\nOK: navegação, âncoras, arquivos, metadados e formulário consistentes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
