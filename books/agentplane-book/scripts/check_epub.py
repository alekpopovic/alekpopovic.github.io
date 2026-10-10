#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check EPUB packaging, XML, manifest, navigation and local references.

This is an internal structural checker, not a substitute for W3C EPUBCheck.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import posixpath
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

NS={'c':'urn:oasis:names:tc:opendocument:xmlns:container',
    'o':'http://www.idpf.org/2007/opf','dc':'http://purl.org/dc/elements/1.1/'}

def check(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names)), 'duplicate archive members'
        assert names[0]=='mimetype', 'mimetype must be first'
        assert z.read('mimetype')==b'application/epub+zip', 'wrong mimetype'
        assert z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED, 'compressed mimetype'
        for name in names:
            assert not name.startswith('/') and '..' not in Path(name).parts, 'unsafe member'
        container=ET.fromstring(z.read('META-INF/container.xml'))
        root=container.find('c:rootfiles/c:rootfile',NS)
        assert root is not None
        opf=root.attrib['full-path'];base=posixpath.dirname(opf)
        package=ET.fromstring(z.read(opf))
        assert package.attrib.get('version')=='3.0'
        assert package.find('.//dc:language',NS).text=='en'
        items=package.findall('o:manifest/o:item',NS)
        manifest={i.attrib['id']:i for i in items}
        assert len(manifest)==len(items), 'duplicate manifest ids'
        assert any('nav' in i.attrib.get('properties','').split() for i in items), 'missing navigation'
        assert any('cover-image' in i.attrib.get('properties','').split() for i in items), 'missing cover'
        for item in items:
            resource=posixpath.normpath(posixpath.join(base,unquote(item.attrib['href'])))
            assert resource in names, f'missing manifest item {resource}'
        for ref in package.findall('o:spine/o:itemref',NS):
            assert ref.attrib['idref'] in manifest, 'missing spine item'
        xml={}
        for name in names:
            if name.endswith(('.xhtml','.xml','.opf','.ncx','.svg')):
                xml[name]=ET.fromstring(z.read(name))
        ids={name:{el.attrib['id'] for el in tree.iter() if 'id' in el.attrib} for name,tree in xml.items()}
        count=0
        for name,tree in xml.items():
            for el in tree.iter():
                # OPF idrefs and NCX ordering are validated separately.
                for attr in ('href','src','{http://www.w3.org/1999/xlink}href'):
                    link=el.attrib.get(attr)
                    if not link:continue
                    url=urlsplit(link)
                    if url.scheme or link.startswith('//'):continue
                    dest=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(url.path))) if url.path else name
                    assert dest in names, f'{name}: missing local target {link}'
                    if url.fragment:
                        assert unquote(url.fragment) in ids.get(dest,set()), f'{name}: missing anchor {link}'
                    count+=1
        spine=package.findall('o:spine/o:itemref',NS)
        return {'members':len(names),'spine_items':len(spine),'local_references':count,'xml_documents':len(xml)}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('epub',type=Path,nargs='?',default=Path('dist/AgentPlane-Book.epub'))
    args=parser.parse_args()
    print('PASS:',check(args.epub))
    print('Internal structural check only; independent EPUBCheck is a separate release gate.')
