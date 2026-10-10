# SPDX-License-Identifier: MIT
"""Structural publication tests. They do not replace a PDF or device review."""
from __future__ import annotations
import copy
import hashlib
import json
import posixpath
import tempfile
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
import build
import check


class Links(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if 'href' in a:
            self.hrefs.append(a['href'])


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)/'dist'
        with patch.object(build, 'DIST', cls.out):
            cls.epub = build.epub()
            cls.site = build.site()
            cls.print_html = build.print_html()
            cls.sample_html = build.print_html(True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_canonical_order(self):
        paths = build.selection()
        self.assertEqual(len(paths), 30)
        self.assertEqual(paths[0].name, '00-preface.md')
        self.assertEqual(paths[-1].name, 'e-sources.md')

    def test_sample_is_a_subset(self):
        self.assertEqual(len(build.selection(True)), 7)
        self.assertTrue(set(build.selection(True)).issubset(set(build.selection())))

    def test_selection_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'manuscript').mkdir()
            (root/'outside.md').write_text('# Outside\n')
            (root/'manuscript/Book.txt').write_text('../outside.md\n')
            with patch.object(build, 'ROOT', root), self.assertRaises(ValueError):
                build.selection()

    def test_selection_rejects_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'manuscript').mkdir()
            (root/'manuscript/a.md').write_text('# A\n')
            (root/'manuscript/Book.txt').write_text('a.md\na.md\n')
            with patch.object(build, 'ROOT', root), self.assertRaises(ValueError):
                build.selection()

    def test_source_slugs(self):
        self.assertEqual(build.slug('S08. Docker Engine security'), 's08')
        self.assertEqual(build.slug('Keep the lock scope small'), 'keep-the-lock-scope-small')

    def test_raw_html_is_not_executed(self):
        value=build.MD.render('<script>alert(1)</script>')
        self.assertNotIn('<script>', value)
        self.assertIn('&lt;script&gt;', value)

    def test_print_ids_are_unique_and_links_resolve(self):
        doc=Links(self.print_html.read_text())
        self.assertEqual(len(doc.ids), len(set(doc.ids)))
        for href in doc.hrefs:
            if href.startswith('#'):
                self.assertIn(href[1:], doc.ids)

    def test_sample_internal_links_resolve(self):
        doc=Links(self.sample_html.read_text())
        for href in doc.hrefs:
            if href.startswith('#'):
                self.assertIn(href[1:], doc.ids)

    def test_site_links_and_fragments(self):
        parsed={p.name:Links(p.read_text()) for p in self.site.glob('*.html')}
        for name, page in parsed.items():
            self.assertEqual(len(page.ids), len(set(page.ids)), name)
            for href in page.hrefs:
                u=urlsplit(href)
                if u.scheme or u.netloc:
                    continue
                target=(self.site/unquote(u.path)).resolve() if u.path else self.site/name
                self.assertTrue(target.is_relative_to(self.site), href)
                self.assertTrue(target.is_file(), f'{name}: {href}')
                if u.fragment and target.suffix=='.html':
                    self.assertIn(unquote(u.fragment), parsed[target.name].ids, href)

    def test_site_has_source_copies(self):
        for source in build.selection():
            self.assertEqual(source.read_bytes(), (self.site/'source'/source.name).read_bytes())
        self.assertTrue((self.site/'.nojekyll').is_file())

    def test_epub_mimetype_first_uncompressed(self):
        with zipfile.ZipFile(self.epub) as z:
            first=z.infolist()[0]
            self.assertEqual(first.filename, 'mimetype')
            self.assertEqual(first.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(z.read(first), b'application/epub+zip')

    def test_epub_xml_and_resources(self):
        with zipfile.ZipFile(self.epub) as z:
            names=set(z.namelist())
            for name in names:
                if name.endswith(('.xhtml','.xml','.opf')):
                    ET.fromstring(z.read(name))
            root=ET.fromstring(z.read('EPUB/package.opf'))
            ns={'o':'http://www.idpf.org/2007/opf'}
            items={x.attrib['id']:x for x in root.findall('o:manifest/o:item',ns)}
            for item in items.values():
                self.assertIn('EPUB/'+item.attrib['href'],names)
            spine=root.findall('o:spine/o:itemref',ns)
            self.assertEqual(len(spine),31)
            for ref in spine:
                self.assertIn(ref.attrib['idref'],items)
            self.assertEqual(sum(x.attrib.get('properties')=='nav' for x in items.values()),1)

    def test_epub_internal_links(self):
        with zipfile.ZipFile(self.epub) as z:
            names=set(z.namelist())
            parsed={n:Links(z.read(n).decode()) for n in names if n.endswith('.xhtml')}
            for name, doc in parsed.items():
                self.assertEqual(len(doc.ids),len(set(doc.ids)),name)
                for href in doc.hrefs:
                    u=urlsplit(href)
                    if u.scheme or u.netloc:
                        continue
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(u.path))) if u.path else name
                    self.assertIn(target,names,f'{name}: {href}')
                    if u.fragment:
                        self.assertIn(unquote(u.fragment),parsed[target].ids,href)

    def test_epub_is_content_reproducible(self):
        before=hashlib.sha256(self.epub.read_bytes()).digest()
        with patch.object(build,'DIST',self.out):
            after=hashlib.sha256(build.epub().read_bytes()).digest()
        self.assertEqual(before,after)

    def test_work_items_reject_completion_without_evidence(self):
        items=json.loads((build.ROOT/'implementation/work-items.json').read_text())
        items=copy.deepcopy(items)
        items[0]['status']='completed';items[0]['evidence']=[]
        with self.assertRaisesRegex(ValueError,'without evidence'):
            check.check_work_items(items)

    def test_work_items_reject_duplicate_identity(self):
        items=json.loads((build.ROOT/'implementation/work-items.json').read_text())
        items[1]['id']='000'
        with self.assertRaisesRegex(ValueError,'unique and ordered'):
            check.check_work_items(items)

    def test_repository_validation(self):
        result=check.check()
        self.assertEqual(result['chapters'],24)
        self.assertEqual(result['implementation_items'],80)


if __name__=='__main__':
    unittest.main()
