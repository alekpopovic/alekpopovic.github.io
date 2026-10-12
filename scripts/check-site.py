#!/usr/bin/env python3
"""Validate SEO output, search, feeds, aliases, metadata and all local links."""
import json
import hashlib
import os
import re
import sys
import zipfile
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
        self.verification = []
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
            if attrs.get('name') == 'google-site-verification':
                self.verification.append(attrs.get('content'))
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
    verification_file = CONFIG.get('google_verification_file', '')
    verification_path = None
    if verification_file:
        require(bool(re.fullmatch(r'google[a-f0-9]+\.html', verification_file)), 'Invalid Google verification filename')
        verification_path = SITE / verification_file
        require(verification_path.is_file() and verification_path.read_text().strip() == f'google-site-verification: {verification_file}', 'Google verification resource must retain its original content')
    # Google's opaque verification resource is not an HTML document. All actual
    # pages still require their layout, metadata, and exactly one configured tag.
    pages = {path: Page(path) for path in SITE.rglob('*.html') if path != verification_path}
    checked = 0
    indexed = set()
    google_analytics = CONFIG.get('google_analytics', '')
    newsletter = CONFIG.get('newsletter_url', '')
    require(not newsletter or (urlsplit(newsletter).scheme == 'https' and urlsplit(newsletter).netloc), 'Newsletter signup must use the owner\'s HTTPS form URL')
    documentation = [urlsplit(project['documentation']) for project in json.loads((ROOT / '_data/projects.json').read_text())]
    external_roots = [url.path for url in documentation if url.netloc == urlsplit(ORIGIN).netloc and url.path not in ['', '/']]
    for path, page in pages.items():
        relative = '/' + path.relative_to(SITE).as_posix()
        url = relative[:-10] if relative.endswith('index.html') else relative
        require(len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {relative}')
        require(len(page.canonicals) == 1, f'Missing or duplicate canonical: {relative}')
        require(page.canonicals[0].startswith(ORIGIN + '/'), f'Non-production canonical: {relative}')
        require(len(page.google_tags) == int(bool(google_analytics)), f'Missing, duplicate or unconfigured Google tag: {relative}')
        if CONFIG.get('google_site_verification'):
            require(page.verification == [CONFIG['google_site_verification']], f'Missing or duplicate Search Console verification tag: {relative}')
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
    learning_paths = yaml.safe_load((ROOT / '_data/learning_paths.yml').read_text())
    quizzes = yaml.safe_load((ROOT / '_data/knowledge_checks.yml').read_text())
    glossary = yaml.safe_load((ROOT / '_data/glossary.yml').read_text())
    workshops = yaml.safe_load((ROOT / '_data/workshops.yml').read_text())
    require(set(glossary) == {book['id'] for book in books}, 'Every book needs a glossary')
    for book in books:
        slugs = {chapter['slug'] for chapter in book['chapters']}
        require(len(glossary[book['id']]) >= 3, f'Book glossary needs substantive terms: {book["id"]}')
        for term in glossary[book['id']]:
            require(term.get('term') and term.get('definition') and term.get('chapter') in slugs, f'Invalid glossary term in {book["id"]}')
    require(len({item['id'] for item in workshops}) == len(workshops), 'Workshop IDs must be unique')
    browser_labs = json.loads((SITE / 'assets/labs/browser-workshops.json').read_text())
    require({item['id'] for item in browser_labs} == {item['id'] for item in workshops}, 'Browser exercises must match the workshop catalog')
    for lab in browser_labs:
        folder = ROOT / 'labs/ai-workshops' / lab['id']
        require(lab['starter'] == (folder / 'app.mjs').read_text() and lab['solution'] == (folder / 'solution.mjs').read_text(), f'Workshop sources drifted: {lab["id"]}')
        require(lab['display_tests'] == (folder / 'test.mjs').read_text(), f'Browser tests drifted: {lab["id"]}')
        require(any(item['url'] == lab['guide'] for item in index), f'Missing workshop guide: {lab["id"]}')
    require(set(quizzes) == {path['id'] for path in learning_paths}, 'Every learning path needs its knowledge check')
    for quiz_id, quiz in quizzes.items():
        questions = quiz.get('questions', [])
        require(len(questions) >= 3 and len({question['id'] for question in questions}) == len(questions), f'Incomplete knowledge check: {quiz_id}')
        for question in questions:
            require(question.get('prompt') and question.get('explanation') and len(question.get('options', [])) >= 2, f'Incomplete quiz scenario: {quiz_id}')
            require(type(question.get('answer')) is int and 0 <= question['answer'] < len(question['options']), f'Invalid quiz answer: {quiz_id}')
            require(any(item['url'] == question.get('url') for item in index), f'Quiz references missing content: {quiz_id}')
    for learning in learning_paths:
        require(all(learning.get(key) for key in ['id', 'title', 'description', 'prerequisites', 'outcome', 'steps']), f'Incomplete learning path: {learning.get("id")}')
        require(len(learning['steps']) >= 3, f'Learning path needs at least three steps: {learning["id"]}')
        require(any(item['url'] == f'/learn/{learning["id"]}/' for item in index), f'Search omits learning path: {learning["id"]}')
        for step in learning['steps']:
            require(all(step.get(key) for key in ['title', 'url', 'kind', 'goal', 'exercise', 'evidence']), f'Incomplete learning step in {learning["id"]}')
            require(step['url'].startswith('/') and any(item['url'] == step['url'] for item in index), f'Learning step references missing indexed content: {step["url"]}')
            require(all(id in {item['id'] for item in workshops} for id in step.get('workshops', [])), f'Learning step references an unknown workshop: {learning["id"]}')
    updates = yaml.safe_load((ROOT / '_data/updates.yml').read_text())
    require(len({item['id'] for item in updates}) == len(updates), 'Changelog IDs must be unique and stable')
    ET.parse(SITE / 'updates.xml')
    offline = json.loads((SITE / 'offline-manifest.json').read_text())
    require({item['url'] for item in offline['chapters']} == {chapter['url'] for book in books for chapter in book['chapters']}, 'Offline manifest omits book sections')
    for url in offline['assets'] + [url for chapter in offline['chapters'] for url in chapter['assets']]:
        require(url.startswith('/assets/') and (SITE / url.lstrip('/')).is_file(), f'Broken offline reading asset: {url}')
        require(not url.lower().endswith(('.pdf', '.epub')), 'Full downloads must never be precached')
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
    archive_path = SITE / 'assets/labs/ai-workshops.zip'
    archive_data = archive_path.read_bytes()
    archive_manifest = json.loads((SITE / 'assets/labs/manifest.json').read_text())
    require(archive_manifest == {'file': archive_path.name, 'sha256': hashlib.sha256(archive_data).hexdigest(), 'bytes': len(archive_data)}, 'Workshop archive checksum or size differs')
    workshop_source = ROOT / 'labs/ai-workshops'
    workshop_files = {f'ai-workshops/{path.relative_to(workshop_source).as_posix()}': path for path in workshop_source.rglob('*') if path.is_file() and path.suffix in {'.md', '.mjs', '.json'}}
    with zipfile.ZipFile(archive_path) as archive:
        require(set(archive.namelist()) == set(workshop_files), 'Workshop archive omits files or includes unmanaged content')
        require(all(archive.read(name) == path.read_bytes() for name, path in workshop_files.items()), 'Workshop archive contains stale source files')
    projects = {project['id']: project for project in json.loads((ROOT / '_data/projects.json').read_text())}
    demos = json.loads((ROOT / '_data/project_demos.json').read_text())
    require(set(demos) == set(projects), 'Featured projects need a scoped recording')
    for project_id, demo in demos.items():
        require(demo['source_commit'] == projects[project_id]['source_commit'], f'Demo uses another source revision: {project_id}')
        require(all(demo.get(key) for key in ['title', 'scope', 'captured_at', 'video', 'poster']), f'Incomplete demo metadata: {project_id}')
        require((SITE / demo['video'].lstrip('/')).read_bytes().startswith(b'\x1a\x45\xdf\xa3'), f'Invalid WebM recording: {project_id}')
        require(image_size(SITE / demo['poster'].lstrip('/')) == (1280, 800), f'Invalid demo poster: {project_id}')
        require(all(step['exit_code'] == 0 and step['command'] and step['output'] for step in demo['steps']), f'Demo contains a failed or empty command: {project_id}')
    for path in (ROOT / '_posts').glob('*.md'):
        metadata = yaml.safe_load(path.read_text().split('---', 2)[1])
        require(all(metadata.get(key) for key in ['layout', 'title', 'description', 'category', 'illustration', 'tags']), f'Incomplete post metadata: {path}')
        require(metadata['layout'] == 'post', f'Unexpected post layout: {path}')
        if metadata.get('section') == 'ai':
            require(all(metadata.get(key) for key in ['tool', 'surface', 'format', 'verified_at', 'sources']), f'Incomplete AI guide metadata: {path}')
            tools = yaml.safe_load((ROOT / '_data/ai_tools.yml').read_text())
            require(metadata['tool'] in [tool['id'] for tool in tools] + ['workflow'], f'Unknown AI tool: {path}')
            require(all(source.get('title') and urlsplit(source.get('url', '')).scheme == 'https' and urlsplit(source['url']).netloc for source in metadata['sources']), f'AI guide needs source links: {path}')
            require(metadata.get('level') in ['Beginner', 'Intermediate'], f'AI guide needs an editorial level: {path}')
            require(isinstance(metadata.get('environments'), list) and metadata['environments'] and set(metadata['environments']) <= {'web', 'desktop', 'cli', 'ide'}, f'AI guide needs valid environments: {path}')
            if metadata['format'] == 'Workshop':
                require(metadata.get('workshop_id') in {item['id'] for item in workshops}, f'AI workshop needs a runnable exercise: {path}')
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
