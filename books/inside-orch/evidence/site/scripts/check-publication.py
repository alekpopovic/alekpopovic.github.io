#!/usr/bin/env python3
"""Check the deployed origin, metadata, readers, downloads and true 404 responses."""
import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree


class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonical, self.tags, self.og, self.verification = [], [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('property') == 'og:url': self.og.append(attrs.get('content'))
        if tag == 'meta' and attrs.get('name') == 'google-site-verification': self.verification.append(attrs.get('content'))
        if tag == 'script' and attrs.get('src', '').startswith('https://www.googletagmanager.com/gtag/js'): self.tags.append(attrs['src'])


def read(base, path, limit=2_000_000, ranged=False):
    headers = {'User-Agent': 'CodePop-Publication-Check/1.0', 'Cache-Control': 'no-cache'}
    if ranged: headers['Range'] = 'bytes=0-7'
    request = Request(urljoin(base.rstrip('/') + '/', path.lstrip('/')), headers=headers)
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, {key.lower(): value for key, value in response.headers.items()}, response.read(limit), response.geturl()
    except HTTPError as error:
        with error:
            return error.code, {key.lower(): value for key, value in error.headers.items()}, error.read(limit), error.geturl()


def verify(base, origin, measurement='', revision=None, verification='', verification_file=''):
    status, _, body, _ = read(base, '/publication-manifest.json')
    assert status == 200, f'Publication manifest: HTTP {status}'
    manifest = json.loads(body)
    assert manifest['origin'].rstrip('/') == origin.rstrip('/'), 'Published origin differs from configuration'
    if revision: assert manifest['revision'] == revision, 'New deployment is not visible at the public origin yet'
    paths = manifest['pages']
    assert '/' in paths and any(path.startswith('/books/') for path in paths), 'Incomplete publication manifest'

    def page(path):
        status, headers, body, final_url = read(base, path)
        assert status == 200 and 'text/html' in headers.get('content-type', ''), f'{path}: expected HTML 200, got {status}'
        assert urlsplit(final_url).netloc == urlsplit(base).netloc, f'{path}: redirected away from the tested host'
        meta = Metadata(body.decode('utf-8'))
        assert meta.canonical == [origin.rstrip('/') + path], f'{path}: incorrect canonical {meta.canonical}'
        assert meta.og == meta.canonical, f'{path}: sharing URL differs from canonical'
        expected_tag = ['https://www.googletagmanager.com/gtag/js?id=' + measurement] if measurement else []
        assert meta.tags == expected_tag, f'{path}: missing, duplicated or unconfigured Google tag'
        if verification: assert meta.verification == [verification], f'{path}: incorrect Search Console verification tag'

    def download(item):
        status, headers, body, _ = read(base, item['url'], limit=8, ranged=True)
        assert status in (200, 206), f'{item["url"]}: download HTTP {status}'
        kind = headers.get('content-type', '').split(';')[0].lower()
        if item['format'] == 'pdf':
            assert body.startswith(b'%PDF-') and kind in ('application/pdf', 'application/octet-stream'), f'{item["url"]}: invalid PDF bytes or MIME type'
        else:
            assert body.startswith(b'PK\x03\x04') and kind in ('application/epub+zip', 'application/zip', 'application/octet-stream'), f'{item["url"]}: invalid EPUB bytes or MIME type'

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(page, paths))
        list(pool.map(download, manifest['downloads']))
    if verification_file:
        assert re.fullmatch(r'google[a-f0-9]+\.html', verification_file), 'Invalid verification resource filename'
        status, _, body, _ = read(base, '/' + verification_file, limit=1000)
        assert status == 200 and body.decode().strip() == f'google-site-verification: {verification_file}', 'Google verification resource is missing or changed'
    status, _, body, _ = read(base, '/sitemap.xml')
    assert status == 200, f'Sitemap HTTP {status}'
    urls = [element.text for element in ElementTree.fromstring(body).iter() if element.tag.endswith('}loc')]
    assert urls and all(url.startswith(origin.rstrip('/') + '/') for url in urls), 'Sitemap contains another origin'
    for path in ['/feed.xml', '/updates.xml', '/newsletter.xml']:
        status, _, body, _ = read(base, path)
        assert status == 200, f'{path}: HTTP {status}'
        feed = ElementTree.fromstring(body)
        links = [element.attrib['href'] for element in feed.iter() if element.tag.endswith('}link')]
        assert links and all(url.startswith(origin.rstrip('/') + '/') for url in links), f'{path}: incorrect feed origin'
    status, _, body, _ = read(base, '/robots.txt')
    assert status == 200 and (origin.rstrip('/') + '/sitemap.xml') in body.decode(), 'Robots sitemap points elsewhere'
    status, _, _, _ = read(base, '/__publication-check-missing-page-62e6db.html')
    assert status == 404, f'Missing page returned HTTP {status}; expected a genuine 404'
    print(f'Published site OK: {len(paths)} pages, {len(manifest["downloads"])} downloads, canonical URLs, feeds, sitemap and genuine 404.')


def main():
    config = (Path(__file__).resolve().parents[1] / '_config.yml').read_text()
    origin = re.search(r'^url:\s*[\"\']?([^\"\'\s]+)', config, re.M)[1]
    measurement = re.search(r'^google_analytics:\s*\"([^\"]*)\"', config, re.M)[1]
    verification = re.search(r'^google_site_verification:\s*\"([^\"]*)\"', config, re.M)[1]
    file_match = re.search(r'^google_verification_file:\s*\"([^\"]*)\"', config, re.M)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=origin)
    parser.add_argument('--expected-sha')
    parser.add_argument('--attempts', type=int, default=1)
    parser.add_argument('--retry-delay', type=float, default=10)
    args = parser.parse_args()
    for attempt in range(args.attempts):
        try:
            verify(args.base_url, origin, measurement, args.expected_sha, verification, file_match[1] if file_match else '')
            return
        except Exception as error:
            print(f'Publication check {attempt + 1}/{args.attempts}: {error}', flush=True)
            if attempt + 1 == args.attempts: raise SystemExit(1)
            time.sleep(args.retry_delay)


if __name__ == '__main__': main()
