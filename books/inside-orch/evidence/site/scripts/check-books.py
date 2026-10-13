#!/usr/bin/env python3
"""Check complete books, linked editorial posts, navigation, and downloads."""
from __future__ import annotations
import json
import posixpath
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from pypdf import PdfReader
from book_catalog import catalog, chapter_title, render

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.text = []
        self.article_text = []
        self.in_article = False
        self.post = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'href' in attrs:
            self.links.append(attrs['href'])
        if 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'article' and 'book-article' in attrs.get('class', '').split():
            self.in_article = True
        if tag == 'article' and 'post-article' in attrs.get('class', '').split():
            self.post = dict(book_id=attrs.get('data-book-id'), chapter_slug=attrs.get('data-chapter-slug'), section=attrs.get('data-section'))

    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False

    def handle_data(self, value):
        self.text.append(value)
        if self.in_article:
            self.article_text.append(value)


def normalized(parts: list[str]) -> str:
    return re.sub(r'\s+', ' ', ' '.join(parts)).strip()


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def edition_text(text: str) -> str:
    # Pandoc uses smart punctuation and PDF export wraps text across lines.
    punctuation = str.maketrans({'“': '"', '”': '"', '‘': "'", '’': "'", '—': '---', '–': '--', '…': '...'})
    return re.sub(r'\s+', '', text.translate(punctuation))


def check_editions(source, book):
    pdf = SITE / book['pdf'].lstrip('/')
    pdf_bytes = pdf.read_bytes()
    demand(pdf_bytes.startswith(b'%PDF-') and b'%%EOF' in pdf_bytes[-1024:], 'Invalid PDF download')
    demand(pdf_bytes == (source['editions'] / pdf.name).read_bytes(), 'PDF differs from the full edition')
    reader = PdfReader(pdf)
    demand(reader.metadata.author == book['author'], 'PDF author attribution differs')
    pdf_text = edition_text(''.join(page.extract_text() or '' for page in reader.pages))
    for path in source['paths']:
        demand(edition_text(chapter_title(source, path)) in pdf_text, f'PDF omits chapter: {path.name}')

    epub = SITE / book['epub'].lstrip('/')
    with zipfile.ZipFile(epub) as archive:
        demand(archive.testzip() is None, 'Corrupt EPUB download')
        first = archive.infolist()[0]
        demand(first.filename == 'mimetype' and first.compress_type == zipfile.ZIP_STORED, 'Invalid EPUB mimetype entry')
        demand(archive.read('mimetype') == b'application/epub+zip', 'Invalid EPUB mimetype')
        container = ET.fromstring(archive.read('META-INF/container.xml'))
        opf = container.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile').attrib['full-path']
        package = ET.fromstring(archive.read(opf))
        ns = {'opf': 'http://www.idpf.org/2007/opf', 'dc': 'http://purl.org/dc/elements/1.1/'}
        manifest = {item.attrib['id']: posixpath.normpath(posixpath.join(posixpath.dirname(opf), item.attrib['href']))
                    for item in package.findall('opf:manifest/opf:item', ns)}
        spine = [manifest[item.attrib['idref']] for item in package.findall('opf:spine/opf:itemref', ns)]
        demand(any(item.text == book['author'] for item in package.findall('opf:metadata/dc:creator', ns)), 'EPUB author attribution differs')
        demand(package.find('opf:metadata/dc:language', ns).text == book['language'], 'EPUB language differs')
        for i, path in enumerate(source['paths'], 1):
            default_name = f'EPUB/{path.stem}.xhtml' if source['id'] == 'modern-ci' else f'EPUB/text/ch{i + source.get("epub_offset", 0):03}.xhtml'
            names = source.get('epub_chapters', {}).get(path.stem, [default_name])
            bodies = []
            for name in names:
                demand(name in spine, f'EPUB spine omits chapter: {path.name}: {name}')
                document = ET.fromstring(archive.read(name))
                body = document.find('{http://www.w3.org/1999/xhtml}body')
                # Pandoc adds the image alt text as a visible figure caption.
                for parent in body.iter():
                    for child in list(parent):
                        if child.tag == '{http://www.w3.org/1999/xhtml}figcaption':
                            parent.remove(child)
                bodies.append(body)
            expected = edition_text(''.join(Page(render(source, path)).text))
            actual = edition_text(''.join(text for body in bodies for text in body.itertext()))
            demand(actual == expected, f'EPUB differs from the complete source: {path.name}')
        documents = {name: ET.fromstring(archive.read(name)) for name in archive.namelist()
                     if name.endswith(('.xml', '.opf', '.xhtml', '.ncx', '.svg'))}
        ids = {name: {node.attrib['id'] for node in doc.iter() if 'id' in node.attrib}
               for name, doc in documents.items()}
        for name, doc in documents.items():
            for node in doc.iter():
                for attr in ['href', 'src', '{http://www.w3.org/1999/xlink}href']:
                    link = node.attrib.get(attr)
                    if not link:
                        continue
                    url = urlsplit(link)
                    if url.scheme or url.netloc:
                        continue
                    dest = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name
                    demand(dest in archive.namelist(), f'EPUB missing local resource: {name}: {link}')
                    if url.fragment:
                        demand(unquote(url.fragment) in ids.get(dest, set()), f'EPUB missing local anchor: {name}: {link}')
        if source['id'] == 'logbranik':
            demand(archive.read('EPUB/media/book-cover.png') == (source['source'] / 'branding/book-cover.png').read_bytes(), 'EPUB cover differs')
            demand(archive.read('EPUB/media/file0.png') == (source['source'] / 'lessons/resources/architecture.png').read_bytes(), 'EPUB architecture figure differs')
        if source.get('cover'):
            demand(archive.read('EPUB/media/cover.png') == (source['source'] / source['cover']).read_bytes(), 'EPUB cover differs')
    demand(epub.read_bytes() == (source['editions'] / epub.name).read_bytes(), 'EPUB differs from the full edition')
    for old_name in book.get('legacy_download_filenames', []):
        for extension, current in [('pdf', pdf), ('epub', epub)]:
            for directory in [current.parent, SITE / 'books' / book['id'] / 'downloads']:
                alias = directory / f'{old_name}.{extension}'
                demand(alias.is_file() and alias.read_bytes() == current.read_bytes(),
                       f'Previous download address does not serve the current edition: {alias}')
    print(f'{book["title"]}: {len(source["paths"])} complete sections, {len(reader.pages)} PDF pages, full EPUB')


def check_posts(books, parsed):
    posts = {path: page for path, page in parsed.items() if page.post is not None}
    coverage = {book_id: set() for book_id in books}
    standalone = 0
    for path, page in posts.items():
        book_id, slug = page.post['book_id'], page.post['chapter_slug']
        if page.post['section'] == 'ai' and not (book_id or slug):
            standalone += 1
            continue
        demand(book_id in books, f'Post references an unknown book: {path}: {book_id}')
        book = books[book_id]
        chapter = next((chapter for chapter in book['chapters'] if chapter['slug'] == slug), None)
        demand(chapter is not None, f'Post references an unknown chapter: {path}: {slug}')
        demand(chapter['url'] in page.links, f'Post does not link to its chapter: {path}')
        if chapter['group'].lower() == book['chapter_unit']:
            coverage[book_id].add(slug)
    for book_id, chapters in coverage.items():
        demand(len(chapters) >= 3, f'Book {book_id} needs posts covering at least three different numbered chapters; found {len(chapters)}')
    print(f'Posts verified: {len(posts) - standalone} posts linked to valid chapters, {standalone} standalone AI guides, coverage for every book.')
    return list(posts)


def main() -> None:
    sources = catalog()
    books = {book['id']: book for book in json.loads((ROOT / '_data/books.json').read_text())}
    demand(set(books) == {source['id'] for source in sources}, 'The library omits a book')
    parsed = {p: Page(p.read_text(encoding='utf-8')) for p in SITE.rglob('*.html')}
    pages = [SITE / 'books/index.html', SITE / 'index.html', SITE / 'posts/index.html']
    pages.extend(check_posts(books, parsed))
    for source in sources:
        book = books[source['id']]
        demand(len(book['chapters']) == len(source['paths']), 'The contents omit manuscript sections')
        for path, chapter in zip(source['paths'], book['chapters'], strict=True):
            page_path = SITE / chapter['url'].lstrip('/')
            demand(page_path in parsed, f'Missing reading page: {path.name}')
            expected = Page(render(source, path))
            demand(normalized(expected.text) == normalized(parsed[page_path].article_text),
                   f'Published chapter differs from the complete source: {path.name}')
        pages.extend((SITE / book['url'].lstrip('/')).glob('*.html'))
        for name in source['licenses']:
            demand((SITE / source['files_url'].lstrip('/') / name).read_bytes() == (source['source'] / name).read_bytes(), f'License differs: {name}')
        check_editions(source, book)
        if source['id'] in {'agentplane', 'secret-contract-operator', 'universal-tracking'}:
            demand(not (SITE / 'books' / source['source'].name).exists(), 'Canonical publication package leaked into the site')
            for directory in ['chapters', 'book', 'examples', 'prompts']:
                demand(not (SITE / 'books' / source['id'] / directory).exists(), f'Canonical sources leaked: {source["id"]}/{directory}')
    links_checked = 0
    for path in pages:
        page = parsed[path]
        demand(len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {path}')
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = ((SITE / unquote(url.path).lstrip('/')) if url.path.startswith('/')
                      else path.parent / unquote(url.path)) if url.path else path
            if target.is_dir():
                target = target / 'index.html'
            target = target.resolve()
            demand(target.is_relative_to(SITE.resolve()), f'Link escapes site: {href}')
            demand(target.is_file(), f'Broken reading link: {path.relative_to(SITE)} → {href}')
            if url.fragment and target.suffix == '.html':
                demand(unquote(url.fragment) in parsed[target].ids, f'Missing anchor: {href}')
            links_checked += 1

    demand(not (SITE / 'books/modern-ci-book').exists(), 'Canonical build sources leaked into the site')
    demand(not (SITE / 'modern-ci-book-open-source.zip').exists(), 'Source archive leaked into the site')
    demand(not (SITE / 'books/logbranik/lessons').exists(), 'LogBranik manuscript leaked into the site')
    demand(not (SITE / 'books/logbranik/companion').exists(), 'LogBranik companion leaked into the site')
    demand(not (SITE / 'logbranik-leanpub-complete-pack.zip').exists(), 'LogBranik source archive leaked into the site')
    print(f'Books verified: {len(books)} books, {sum(len(source["paths"]) for source in sources)} complete sections, {links_checked} local links/assets/anchors.')


if __name__ == '__main__':
    main()
