#!/usr/bin/env python3
"""Check the exact built native edition without fetching external resources."""
import hashlib, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.canonicals=[]; self.tags=[]; self.schemas=[]
        self.headings=[]; self.h1=None; self.script=None
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a' and 'href' in attrs: self.links.append(attrs['href'])
        if tag=='link' and attrs.get('rel')=='canonical': self.canonicals.append(attrs['href'])
        if tag=='script' and attrs.get('type')=='application/ld+json': self.script=''
        if tag=='script' and attrs.get('src','').startswith('https://www.googletagmanager.com/gtag/js'): self.tags.append(attrs['src'])
        if tag=='h1': self.h1=''
    def handle_data(self, data):
        if self.h1 is not None: self.h1+=data
        if self.script is not None: self.script+=data
    def handle_endtag(self, tag):
        if tag=='h1' and self.h1 is not None: self.headings.append(self.h1); self.h1=None
        if tag=='script' and self.script is not None: self.schemas.append(json.loads(self.script)); self.script=None

BOOK = Path(__file__).resolve().parents[1]
SITE = BOOK.parents[1]
spec = importlib.util.spec_from_file_location('orch_pub', BOOK/'scripts/build.py')
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)
origin = 'https://www.alekpopovic.com'
output = SITE/'_site'
search = json.loads((output/'search-index.json').read_text())
search_by_url = {x['url']: x for x in search}
sitemap = {x.text for x in ET.parse(output/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
feed = (output/'feed.xml').read_text()
paths = pub.selection()
expected_urls = {'/books/inside-orch/'+p.stem+'.html' for p in paths}
checked = []
for path in paths:
    url = '/books/inside-orch/'+path.stem+'.html'
    soup = Page(output/url.lstrip('/'))
    assert soup.canonicals == [origin+url], url
    assert pub.title(path) in soup.headings, url
    assert expected_urls <= set(soup.links), url
    assert url in search_by_url and len(search_by_url[url]['text']) > 1000, url
    assert origin+url in sitemap, url
    assert len(soup.tags) == 1, url
    checked.append(url)
landing = Page(output/'books/inside-orch/index.html')
data = landing.schemas[0]
book = next(x['mainEntity'] for x in data['@graph'] if x.get('mainEntity',{}).get('@type')=='Book')
assert book['bookEdition'] == pub.meta()['edition']
assert not {'isbn','aggregateRating','review','numberOfPages'} & set(book)
assert expected_urls <= set(landing.links)
downloads = {}
for ext in ['pdf','epub']:
    canonical = BOOK/f'dist/inside-orch.{ext}'
    public = output/f'assets/books/inside-orch/downloads/inside-orch.{ext}'
    assert canonical.read_bytes() == public.read_bytes(), ext
    downloads[ext] = hashlib.sha256(canonical.read_bytes()).hexdigest()
posts = []
for path in sorted((SITE/'_posts').glob('2026-10-13-*.md')):
    text = path.read_text()
    if 'book_id: inside-orch' not in text:
        continue
    url = '/posts/'+path.stem[11:]+'/'
    assert origin+url in sitemap and origin+url in feed and url in search_by_url, url
    page = Page(output/url.lstrip('/')/'index.html')
    chapter_links = [u for u in page.links if u in checked]
    assert chapter_links, url
    assert any(url in (output/u.lstrip('/')).read_text() for u in set(chapter_links)), url
    posts.append(url)
assert len(posts) == 3
for forbidden in ['books/inside-orch/evidence','books/inside-orch/prompts','books/inside-orch/state',
                  'assets/books/inside-orch/evidence','assets/books/inside-orch/prompts']:
    assert not (output/forbidden).exists(), forbidden
r = {'status':'passed','checked_at_utc':datetime.now(timezone.utc).isoformat(),
     'source_sha':pub.meta()['source_sha'],'sections':checked,'original_posts':posts,
     'downloads':downloads,'canonical_book_metadata':book,
     'scope':'Actual built pages: metadata, complete full-text/sitemap discovery, feed posts, reciprocal links, shared tag, exact downloads and private-corpus path exclusion. Browser, full local-link and offline gates are separate.'}
(BOOK/'validation/publication/native-site-acceptance.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'status':'passed','sections':len(checked),'posts':len(posts),'downloads':downloads}))
