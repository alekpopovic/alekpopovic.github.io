#!/usr/bin/env python3
"""Publish the complete English manuscript locally as PDF, EPUB, and Markdown."""
from __future__ import annotations

import hashlib
import html
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
NAME = 'secret-contract-operator-book'
MD = MarkdownIt('commonmark', {'html': False, 'xhtmlOut': True}).enable('table')


def meta():
    return json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))


def selection():
    paths = sorted((ROOT / 'chapters').glob('*.md'))
    if len(paths) != 27:
        raise ValueError('Expected the preface, 22 chapters, and four appendices')
    return paths


def title(path):
    return next(line[2:].strip() for line in path.read_text().splitlines() if line.startswith('# '))


def slug(value):
    value = html.unescape(re.sub(r'<[^>]+>', '', value)).lower()
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'\s+', '-', value.strip()) or 'section'


def render(path, mode):
    tokens = MD.parse(path.read_text(encoding='utf-8'))
    used = {}
    chapter_names = {p: f'ch{i:03}.xhtml' for i, p in enumerate(selection(), 1)}
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            base = path.stem if token.tag == 'h1' else slug(tokens[i + 1].content)
            if mode == 'print' and token.tag != 'h1':
                base = path.stem + '-' + base
            count = used.get(base, 0)
            used[base] = count + 1
            token.attrSet('id', base if count == 0 else f'{base}-{count}')
        for child in token.children or []:
            attribute = 'src' if child.type == 'image' else 'href' if child.type == 'link_open' else None
            if not attribute:
                continue
            target = child.attrGet(attribute)
            url = urlsplit(target)
            if url.scheme or url.netloc:
                if attribute == 'src':
                    raise ValueError('Publication images must be local')
                continue
            destination = (path.parent / url.path).resolve() if url.path else path
            if not destination.is_relative_to(ROOT) or not destination.is_file():
                raise ValueError(f'Invalid publication reference: {path}: {target}')
            if attribute == 'src':
                child.attrSet(attribute, '../media/' + destination.with_suffix('.png').name
                              if mode == 'epub' else destination.as_uri())
            elif destination in chapter_names:
                if mode == 'print':
                    anchor = destination.stem + '-' + url.fragment if url.fragment else destination.stem
                    child.attrSet(attribute, '#' + anchor)
                else:
                    child.attrSet(attribute, chapter_names[destination] + ('#' + url.fragment if url.fragment else ''))
    return MD.renderer.render(tokens, MD.options, {})


def build_assets():
    from cairosvg import svg2png
    for source in sorted((ROOT / 'assets').glob('*.svg')):
        svg2png(url=str(source), write_to=str(source.with_suffix('.png')))


def xhtml(page_title, body):
    document = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>{html.escape(page_title)}</title><link rel="stylesheet" type="text/css" href="../styles/epub.css" /></head><body>{body}</body></html>'''
    ET.fromstring(document)
    return document


def epub():
    m, paths = meta(), selection()
    contents = {
        'text/cover.xhtml': xhtml('Cover', '<section epub:type="cover"><img class="cover" src="../media/cover.png" alt="Secret Contract Operator — Designing a Safe Kubernetes Operator" /></section>'),
        'text/title.xhtml': xhtml(m['title'], f'<h1>{html.escape(m["title"])}</h1><h2>{html.escape(m["subtitle"])}</h2><p>{m["author"]}</p><p>Codepop Engineering · English edition {m["edition"]} · October 10, 2026</p><p>The supplied publication has no text or code license grant.</p>')
    }
    navigation = []
    for i, path in enumerate(paths, 1):
        name = f'text/ch{i:03}.xhtml'
        contents[name] = xhtml(title(path), render(path, 'epub'))
        navigation.append(f'<li><a href="ch{i:03}.xhtml">{html.escape(title(path))}</a></li>')
    contents['text/nav.xhtml'] = xhtml('Contents', '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>' + ''.join(navigation) + '</ol></nav>')
    seed = (json.dumps(m, sort_keys=True) + ''.join(p.read_text() for p in paths)).encode()
    identifier = 'urn:sha256:' + hashlib.sha256(seed).hexdigest()
    manifest = '<item id="css" href="styles/epub.css" media-type="text/css" />'
    for i, name in enumerate(contents):
        properties = ' properties="nav"' if name == 'text/nav.xhtml' else ''
        manifest += f'<item id="item{i}" href="{name}" media-type="application/xhtml+xml"{properties} />'
    images = sorted((ROOT / 'assets').glob('*.png'))
    for image in images:
        properties = ' properties="cover-image"' if image.stem == 'cover' else ''
        manifest += f'<item id="{image.stem}" href="media/{image.name}" media-type="image/png"{properties} />'
    spine = ''.join(f'<itemref idref="item{i}" />' for i, name in enumerate(contents) if name != 'text/nav.xhtml')
    opf = f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{identifier}</dc:identifier><dc:title>{html.escape(m['title'] + ': ' + m['subtitle'])}</dc:title><dc:creator>{m['author']}</dc:creator><dc:language>en</dc:language><dc:date>{m['date']}</dc:date><dc:rights>No text or code license grant is supplied with this publication.</dc:rights><meta property="dcterms:modified">{m['date']}T00:00:00Z</meta></metadata><manifest>{manifest}</manifest><spine>{spine}</spine></package>'''
    ET.fromstring(opf)
    container = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" /></rootfiles></container>'
    def add(archive, name, data, compression=zipfile.ZIP_DEFLATED):
        entry = zipfile.ZipInfo(name, (2026, 10, 10, 0, 0, 0))
        entry.compress_type = compression
        archive.writestr(entry, data.encode('utf-8') if isinstance(data, str) else data)
    with zipfile.ZipFile(DIST / (NAME + '.epub'), 'w') as archive:
        add(archive, 'mimetype', 'application/epub+zip', zipfile.ZIP_STORED)
        add(archive, 'META-INF/container.xml', container)
        add(archive, 'EPUB/package.opf', opf)
        add(archive, 'EPUB/styles/epub.css', (ROOT / 'styles/epub.css').read_text())
        for name, document in contents.items():
            add(archive, 'EPUB/' + name, document)
        for image in images:
            add(archive, 'EPUB/media/' + image.name, image.read_bytes())


def pdf():
    from weasyprint import HTML
    from weasyprint.urls import URLFetcher
    m, paths = meta(), selection()
    toc = '<section class="toc"><h1>Contents</h1><ol>' + ''.join(
        f'<li><a href="#{p.stem}">{html.escape(title(p))}</a></li>' for p in paths) + '</ol></section>'
    chapters = ''.join('<section class="chapter">' + render(p, 'print') + '</section>' for p in paths)
    document = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>{html.escape(m['title'] + ': ' + m['subtitle'])}</title><meta name="author" content="{m['author']}" /><meta name="description" content="{html.escape(m['description'])}" /><style>{(ROOT / 'styles/print.css').read_text()}</style></head><body><section class="cover"><img src="{(ROOT / 'assets/cover.svg').as_uri()}" alt="Secret Contract Operator — English edition" /></section>{toc}{chapters}</body></html>'''
    (DIST / (NAME + '.html')).write_text(document, encoding='utf-8')
    class LocalURLFetcher(URLFetcher):
        def fetch(self, url, **kwargs):
            if urlsplit(url).scheme not in {'file', 'data'}:
                raise ValueError('Book builds cannot fetch external assets')
            return super().fetch(url, **kwargs)
    HTML(string=document, base_url=str(ROOT), url_fetcher=LocalURLFetcher()).write_pdf(str(DIST / (NAME + '.pdf')))


def build():
    DIST.mkdir(exist_ok=True)
    build_assets()
    m = meta()
    combined = f'# {m["title"]}\n\n{m["subtitle"]}\n\n{m["author"]} · English edition {m["edition"]}\n\n'
    combined += '\n\n'.join(p.read_text() for p in selection())
    (DIST / (NAME + '.md')).write_text(combined, encoding='utf-8')
    epub()
    pdf()
    entries = []
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS' and '__pycache__' not in path.parts:
            entries.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}')
    (ROOT / 'SHA256SUMS').write_text('\n'.join(entries) + '\n')
    print('Secret Contract Operator: English PDF, EPUB, Markdown, cover, and diagrams built', flush=True)


if __name__ == '__main__':
    build()
