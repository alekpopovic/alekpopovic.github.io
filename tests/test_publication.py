"""Exercise deployment failures against a real local HTTP server."""
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from threading import Thread
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from importlib import import_module
publication = import_module('check-publication')
ORIGIN = 'https://site.example'


class PublicationTests(unittest.TestCase):
    @contextlib.contextmanager
    def server(self, wrong_canonical=False, broken_pdf=False, soft_404=False):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass

            def do_GET(self):
                status, kind = 200, 'text/html'
                if self.path == '/publication-manifest.json':
                    kind = 'application/json'
                    body = json.dumps({'origin': ORIGIN, 'revision': 'abc', 'pages': ['/', '/books/sample/'], 'downloads': [{'url': '/book.pdf', 'format': 'pdf'}]}).encode()
                elif self.path in ['/', '/books/sample/']:
                    canonical = ('https://wrong.example' if wrong_canonical else ORIGIN) + self.path
                    body = f'<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}">'.encode()
                elif self.path == '/book.pdf':
                    kind = 'application/pdf'; body = b'<html>Missing</html>' if broken_pdf else b'%PDF-1.7'
                elif self.path == '/sitemap.xml':
                    kind = 'application/xml'; body = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url></urlset>'.encode()
                elif self.path in ['/feed.xml', '/updates.xml']:
                    kind = 'application/atom+xml'; body = f'<feed xmlns="http://www.w3.org/2005/Atom"><link href="{ORIGIN}/"/></feed>'.encode()
                elif self.path == '/robots.txt':
                    kind = 'text/plain'; body = f'Sitemap: {ORIGIN}/sitemap.xml'.encode()
                else:
                    status = 200 if soft_404 else 404; body = b'Not found'
                self.send_response(status); self.send_header('Content-Type', kind); self.end_headers(); self.wfile.write(body)
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True); thread.start()
        try: yield f'http://127.0.0.1:{server.server_port}'
        finally: server.shutdown(); server.server_close(); thread.join()

    def test_valid_publication(self):
        with self.server() as base: publication.verify(base, ORIGIN, revision='abc')

    def test_stale_deployment_is_rejected(self):
        with self.server() as base, self.assertRaisesRegex(AssertionError, 'not visible'):
            publication.verify(base, ORIGIN, revision='new')

    def test_incorrect_canonical_is_rejected(self):
        with self.server(wrong_canonical=True) as base, self.assertRaisesRegex(AssertionError, 'incorrect canonical'):
            publication.verify(base, ORIGIN)

    def test_html_instead_of_pdf_is_rejected(self):
        with self.server(broken_pdf=True) as base, self.assertRaisesRegex(AssertionError, 'invalid PDF'):
            publication.verify(base, ORIGIN)

    def test_soft_404_is_rejected(self):
        with self.server(soft_404=True) as base, self.assertRaisesRegex(AssertionError, 'genuine 404'):
            publication.verify(base, ORIGIN)


if __name__ == '__main__': unittest.main()
