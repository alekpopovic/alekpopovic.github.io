#!/usr/bin/env python3
"""Validate SEO output, search, feeds, aliases, metadata and all local links."""
import json
import os
import re
import sys
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / '.venv/bin/python').exists() and Path(sys.prefix).resolve() != (ROOT / '.venv').resolve():
    os.execv(str(ROOT / '.venv/bin/python'), [str(ROOT / '.venv/bin/python'), __file__])
import yaml
from PIL import Image

SITE = ROOT / '_site'
CONFIG = yaml.safe_load((ROOT / '_config.yml').read_text())
ORIGIN = CONFIG['url'].rstrip('/')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links, self.ids, self.meta, self.canonicals = [], [], {}, []
        self.schema, self.script = [], None
        self.google_tags = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ['href', 'src', 'data-index']:
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get('srcset'):
            self.links.extend(item.strip().split()[0] for item in attrs['srcset'].split(','))
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.script = ''
        if tag == 'script' and attrs.get('src', '').startswith('https://www.googletagmanager.com/gtag/js'):
            self.google_tags.append(attrs)

    def handle_data(self, data):
        if self.script is not None:
            self.script += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.schema.append(json.loads(self.script))
            self.script = None


def require(condition, message):
    if not condition:
        raise ValueError(message)


@cache
def image_size(path):
    # A valid header or HTTP 200 is insufficient: reject empty/truncated assets.
    with Image.open(path) as image:
        image.load()
        return image.size


def main():
    pages = {path: Page(path) for path in SITE.rglob('*.html')}
    checked = 0
    indexed = set()
    google_analytics = CONFIG.get('google_analytics', '')
    documentation = [urlsplit(project['documentation']) for project in json.loads((ROOT / '_data/projects.json').read_text())]
    external_roots = [url.path for url in documentation if url.netloc == urlsplit(ORIGIN).netloc and url.path not in ['', '/']]
    for path, page in pages.items():
        relative = '/' + path.relative_to(SITE).as_posix()
        url = relative[:-10] if relative.endswith('index.html') else relative
        require(len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {relative}')
        require(len(page.canonicals) == 1, f'Missing or duplicate canonical: {relative}')
        require(page.canonicals[0].startswith(ORIGIN + '/'), f'Non-production canonical: {relative}')
        require(len(page.google_tags) == int(bool(google_analytics)), f'Missing, duplicate or unconfigured Google tag: {relative}')
        if google_analytics:
            tag = page.google_tags[0]
            require('async' in tag and parse_qs(urlsplit(tag['src']).query).get('id') == [google_analytics], f'Incorrect Google tag: {relative}')
        if 'noindex' not in (page.meta.get('robots') or ''):
            indexed.add(ORIGIN + url)
            require(bool(page.meta.get('description')), f'Missing description: {relative}')
            require(bool(page.schema), f'Missing structured data: {relative}')
            image = page.meta.get('og:image', '')
            require(image.startswith(ORIGIN + '/assets/social/'), f'Missing social image: {relative}')
            image_file = SITE / urlsplit(image).path.lstrip('/')
            require(image_file.is_file(), f'Missing social image file: {image}')
            require(image_size(image_file) == (1200, 630), f'Invalid social image dimensions: {image}')
            require(page.meta.get('twitter:card') == 'summary_large_image', f'Missing Twitter card: {relative}')
        for link in page.links:
            target = urlsplit(urljoin(ORIGIN + url, link))
            if target.scheme not in ['http', 'https'] or target.netloc != urlsplit(ORIGIN).netloc:
                continue
            if any(target.path.startswith(root) for root in external_roots):
                continue  # Other repositories publish their own Pages sites here.
            dest = SITE / unquote(target.path).lstrip('/')
            if dest.is_dir():
                dest /= 'index.html'
            require(dest.is_file(), f'Broken link in {relative}: {link}')
            if dest.suffix.lower() in {'.png', '.webp', '.jpg', '.jpeg'}:
                image_size(dest)
            if target.fragment and dest in pages:
                require(unquote(target.fragment) in pages[dest].ids, f'Broken anchor in {relative}: {link}')
            checked += 1
    sitemap = ET.parse(SITE / 'sitemap.xml')
    locations = [item.text for item in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    require(len(locations) == len(set(locations)) and set(locations) == indexed, 'Sitemap does not match indexable HTML pages')
    entries = ET.parse(SITE / 'feed.xml').findall('{http://www.w3.org/2005/Atom}entry')
    require(len(entries) == min(30, len(list((ROOT / '_posts').glob('*.md')))), 'Feed omits current posts')
    index = json.loads((SITE / 'search-index.json').read_text())
    books = json.loads((ROOT / '_data/books.json').read_text())
    require(sum(item['type'] == 'chapters' for item in index) == sum(len(book['chapters']) for book in books), 'Search omits book chapters')
    require(sum(item['type'] == 'posts' for item in index) == len(list((ROOT / '_posts').glob('*.md'))), 'Search omits posts')
    for item in index:
        path = SITE / urlsplit(item['url']).path.lstrip('/')
        require((path / 'index.html').is_file() if path.is_dir() else path.is_file(), f'Broken search result: {item["url"]}')
        require(bool(item.get('text')), f'Empty search document: {item["title"]}')
    for book in books:
        for extension in ['pdf', 'epub']:
            source = SITE / book[extension].lstrip('/')
            legacy = SITE / 'books' / book['id'] / 'downloads' / source.name
            require(source.read_bytes() == legacy.read_bytes(), f'Legacy download differs: {legacy}')
    for path in (ROOT / '_posts').glob('*.md'):
        metadata = yaml.safe_load(path.read_text().split('---', 2)[1])
        require(all(metadata.get(key) for key in ['layout', 'title', 'description', 'category', 'illustration', 'tags']), f'Incomplete post metadata: {path}')
        require(metadata['layout'] == 'post', f'Unexpected post layout: {path}')
        if metadata.get('section') == 'ai':
            require(all(metadata.get(key) for key in ['tool', 'surface', 'format', 'verified_at', 'sources']), f'Incomplete AI guide metadata: {path}')
            tools = yaml.safe_load((ROOT / '_data/ai_tools.yml').read_text())
            require(metadata['tool'] in [tool['id'] for tool in tools] + ['workflow'], f'Unknown AI tool: {path}')
            require(all(source.get('title') and urlsplit(source.get('url', '')).scheme == 'https' and urlsplit(source['url']).netloc for source in metadata['sources']), f'AI guide needs source links: {path}')
        else:
            require(metadata.get('book_id') and metadata.get('chapter_slug'), f'Book note needs chapter metadata: {path}')
        require(metadata['illustration'] in ['clock', 'queue', 'shield', 'network', 'package', 'logs'], f'Unknown post illustration: {path}')
    require('fonts.googleapis.com' not in (ROOT / 'assets/css/site.css').read_text(), 'Remote font import remains')
    require(not (SITE / 'modern-ci-book.pdf').exists(), 'Unmanaged root PDF was published')
    print(f'Site OK: {len(indexed)} indexable pages, {len(index)} search documents, {len(entries)} feed entries, {checked} local links, complete legacy downloads.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, ET.ParseError) as exc:
        raise SystemExit(f'Site check failed: {exc}') from exc
