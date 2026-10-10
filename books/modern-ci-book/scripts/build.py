#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the trusted local manuscript as a website, print PDF, or EPUB."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
MD = MarkdownIt('commonmark', {'html': False, 'xhtmlOut': True}).enable('table')

def meta() -> dict:
    return json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))

def selection(sample: bool = False) -> list[Path]:
    name = 'Sample.txt' if sample else 'Book.txt'
    entries = (ROOT / 'manuscript' / name).read_text().splitlines()
    result = []
    for entry in entries:
        if not entry.strip():
            continue
        path = (ROOT / 'manuscript' / entry.strip()).resolve()
        if path.parent != ROOT / 'manuscript' or path.suffix != '.md' or not path.is_file():
            raise ValueError(f'Invalid manuscript entry: {entry}')
        result.append(path)
    if len(result) != len(set(result)):
        raise ValueError('Duplicate manuscript entries')
    return result

def title(path: Path) -> str:
    return next(line[2:].strip() for line in path.read_text().splitlines() if line.startswith('# '))

def slug(text: str) -> str:
    match = re.match(r'^(S\d{2})\.', text)
    if match:
        return match[1].lower()
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def render(path: Path, mode: str) -> str:
    tokens = MD.parse(path.read_text(encoding='utf-8'))
    used: dict[str, int] = {}
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            text = tokens[i + 1].content
            base = path.stem if token.tag == 'h1' else slug(text)
            if mode == 'print' and token.tag != 'h1' and not re.fullmatch(r's\d{2}', base):
                base = path.stem + '-' + base
            count = used.get(base, 0); used[base] = count + 1
            token.attrSet('id', base if count == 0 else f'{base}-{count}')
        for child in token.children or []:
            if child.type == 'link_open':
                href = child.attrGet('href') or ''
                if href.startswith(('https://', 'http://', 'mailto:', '#')):
                    continue
                filepart, sep, fragment = href.partition('#')
                if filepart.endswith('.md'):
                    if mode == 'print':
                        child.attrSet('href', '#' + (fragment or Path(filepart).stem))
                    else:
                        suffix = '.xhtml' if mode == 'epub' else '.html'
                        child.attrSet('href', str(Path(filepart).with_suffix(suffix)) + (sep + fragment if sep else ''))
    rendered = MD.renderer.render(tokens, MD.options, {})
    if mode == 'print':
        # Keep each exercise and its answer together in the reading edition.
        marker = re.search(r'<h2[^>]*>Exercise</h2>', rendered)
        if marker:
            rendered = rendered[:marker.start()] + '<div class="exercise-group">' + rendered[marker.start():] + '</div>'
    return rendered

def cover(m: dict, sample: bool = False) -> str:
    note = 'READING SAMPLE' if sample else 'OPEN EDITION ' + html.escape(m['edition'])
    return f'''<section class="cover"><p class="eyebrow">THE ENGINEERING SERIES / {note}</p>
<div class="cover-rule"></div><p class="cover-title">MODERN<br />CI</p>
<h1 class="cover-subtitle">Building a Reliable<br />CI/CD Platform</h1>
<p class="cover-tech">Go · Angular · PostgreSQL<br />Independent Git repositories</p>
<div class="cover-bottom"><p class="cover-author">{html.escape(m['author'])}</p>
<p>24 chapters · Practical laboratory · Operational field guide</p>
<p>October 2026 · Text CC BY 4.0 · Code MIT</p></div></section>'''

def print_html(sample: bool = False) -> Path:
    m = meta(); paths = selection(sample)
    toc = '<section class="toc"><h1>Contents</h1><ol>' + ''.join(
        f'<li><a href="#{p.stem}">{html.escape(title(p))}</a></li>' for p in paths) + '</ol></section>'
    contents = ''.join(f'<section class="chapter">{render(p,"print")}</section>' for p in paths)
    name = 'modern-ci-sample' if sample else 'modern-ci-book'
    css = (ROOT / 'styles' / 'print.css').read_text()
    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" />
<title>{html.escape(m['title'] + ': ' + m['subtitle'])}</title>
<meta name="author" content="{html.escape(m['author'])}" />
<meta name="description" content="{html.escape(m['description'])}" />
<style>{css}</style></head><body>{cover(m,sample)}{toc}{contents}</body></html>'''
    DIST.mkdir(exist_ok=True)
    out = DIST / f'{name}.html'; out.write_text(doc,encoding='utf-8'); return out

def pdf(sample: bool = False) -> Path:
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError('Install requirements-print.txt before PDF export') from exc
    document = print_html(sample)
    out = document.with_suffix('.pdf')
    # No external images, scripts, styles, or font downloads are part of the manuscript.
    HTML(filename=str(document)).write_pdf(str(out))
    return out

def epub() -> Path:
    m = meta(); paths = selection(); DIST.mkdir(exist_ok=True)
    contents: dict[str, str] = {}
    namespace = 'http://www.w3.org/1999/xhtml'
    def xhtml(page_title: str, body: str) -> str:
        text = f'''<?xml version="1.0" encoding="utf-8"?><html xmlns="{namespace}" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>{html.escape(page_title)}</title><link rel="stylesheet" type="text/css" href="book.css" /></head><body>{body}</body></html>'''
        ET.fromstring(text)
        return text
    contents['title.xhtml'] = xhtml(m['title'], f'<section><h1>{html.escape(m["title"])}</h1><h2>{html.escape(m["subtitle"])}</h2><p>{html.escape(m["author"])}</p><p>Open edition {m["edition"]} · October 2026</p><p>Text CC BY 4.0 · Original code MIT</p></section>')
    for p in paths:
        contents[p.stem + '.xhtml'] = xhtml(title(p), render(p, 'epub'))
    navitems = '<li><a href="title.xhtml">Title page</a></li>' + ''.join(f'<li><a href="{p.stem}.xhtml">{html.escape(title(p))}</a></li>' for p in paths)
    contents['nav.xhtml'] = xhtml('Contents', f'<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{navitems}</ol></nav>')
    seed = ''.join(p.read_text() for p in paths).encode()
    identifier = 'urn:sha256:' + hashlib.sha256(seed).hexdigest()
    manifest = '<item id="css" href="book.css" media-type="text/css" />'
    manifest += ''.join(f'<item id="item{i}" href="{name}" media-type="application/xhtml+xml"'+(' properties="nav"' if name=='nav.xhtml' else '')+' />' for i,name in enumerate(contents))
    spine = ''.join(f'<itemref idref="item{i}" />' for i,name in enumerate(contents) if name!='nav.xhtml')
    opf = f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{identifier}</dc:identifier><dc:title>{html.escape(m['title']+': '+m['subtitle'])}</dc:title><dc:creator>{html.escape(m['author'])}</dc:creator><dc:language>en</dc:language><dc:date>{m['date']}</dc:date><dc:rights>Text CC BY 4.0; original code MIT. Copyright 2026 Aleksandar Popovic.</dc:rights><meta property="dcterms:modified">{m['date']}T00:00:00Z</meta></metadata><manifest>{manifest}</manifest><spine>{spine}</spine></package>'''
    ET.fromstring(opf)
    container = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" /></rootfiles></container>'
    out = DIST / 'modern-ci-book.epub'
    def add(z: zipfile.ZipFile, name: str, data: str, compress: int = zipfile.ZIP_DEFLATED) -> None:
        info=zipfile.ZipInfo(name,(2026,10,10,0,0,0));info.compress_type=compress
        z.writestr(info,data.encode('utf-8'))
    with zipfile.ZipFile(out,'w') as z:
        add(z,'mimetype','application/epub+zip',zipfile.ZIP_STORED)
        add(z,'META-INF/container.xml',container)
        add(z,'EPUB/package.opf',opf)
        add(z,'EPUB/book.css',(ROOT/'styles'/'epub.css').read_text())
        for name,data in contents.items():add(z,'EPUB/'+name,data)
    return out

def site() -> Path:
    m=meta();paths=selection();out=DIST/'site'
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy2(ROOT/'styles'/'site.css',out/'site.css')
    nav = '<nav aria-label="Book chapters"><p class="nav-title"><a href="index.html">MODERN CI</a></p><p class="nav-sub">Building a Reliable<br />CI/CD Platform</p><ol>' + ''.join(f'<li><a href="{p.stem}.html">{html.escape(title(p))}</a></li>' for p in paths) + '</ol><p><a href="license.html">Licensing</a></p></nav>'
    footer='<footer>© 2026 Aleksandar Popovic · Text CC BY 4.0 · Original code MIT</footer>'
    def page(t: str, body: str) -> str:
        return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{html.escape(m['description'])}"><title>{html.escape(t)} · Modern CI</title><link rel="stylesheet" href="site.css"></head><body><a class="skip" href="#content">Skip to content</a>{nav}<main id="content">{body}{footer}</main></body></html>'''
    downloads=[]
    for name in ['modern-ci-book.pdf','modern-ci-book.epub','modern-ci-sample.pdf']:
        if (DIST/name).is_file():
            (out/'downloads').mkdir(exist_ok=True);shutil.copy2(DIST/name,out/'downloads'/name)
            downloads.append(f'<a class="button" href="downloads/{name}">{html.escape(name.removeprefix("modern-ci-").upper())}</a>')
    index=f'<p class="eyebrow">OPEN ENGINEERING BOOK / EDITION {m["edition"]}</p><h1 class="hero-title">Modern CI</h1><p class="lead">Building a Reliable CI/CD Platform</p><p>{html.escape(m["description"])}</p><p class="byline">Aleksandar Popovic · 24 chapters · Five appendices</p><p><a class="button" href="00-preface.html">Start reading</a> '+ ' '.join(downloads)+'</p><h2>Read, test, and build</h2><p>Learn the architecture, run the isolated Go laboratory, and use the implementation map to plan a full platform. The examples are not a complete production service.</p><h2>Contents</h2><ol class="contents">'+''.join(f'<li><a href="{p.stem}.html">{html.escape(title(p))}</a></li>' for p in paths)+'</ol>'
    (out/'index.html').write_text(page('Home',index))
    for i,p in enumerate(paths):
        links=[]
        if i:links.append(f'<a href="{paths[i-1].stem}.html">← Previous</a>')
        if i+1<len(paths):links.append(f'<a href="{paths[i+1].stem}.html">Next →</a>')
        body='<article>'+render(p,'site')+'</article><div class="pager">'+' '.join(links)+'</div>'+f'<p class="source"><a href="source/{p.name}">Markdown source</a></p>'
        (out/(p.stem+'.html')).write_text(page(title(p),body))
    (out/'source').mkdir()
    for p in paths:shutil.copy2(p,out/'source'/p.name)
    for name in ['LICENSE.md','LICENSE-BOOK.md','LICENSE-CODE.txt']:
        shutil.copy2(ROOT/name,out/name)
    lic=MD.render((ROOT/'LICENSE.md').read_text())
    (out/'license.html').write_text(page('Licensing',lic))
    (out/'.nojekyll').write_text('')
    return out

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('format',choices=['site','pdf','epub','sample','all'])
    args=parser.parse_args()
    if args.format=='all':
        print(epub());print(pdf());print(pdf(True));print(site())
    elif args.format=='site':print(site())
    elif args.format=='epub':print(epub())
    else:print(pdf(args.format=='sample'))
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,RuntimeError) as exc:
        print(f'Build failed: {exc}',file=sys.stderr);sys.exit(1)
