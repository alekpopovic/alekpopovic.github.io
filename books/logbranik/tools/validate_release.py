"""Structural validation; does not pretend to run unavailable production services."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    meta=json.loads((ROOT/'publishing/book-metadata.json').read_text())
    def check(ok,name):
        if not ok:raise ValueError(name)
        checks.append(name)
    check(meta['author']=='Aleksandar Popovic' and meta['author_profile']=='https://github.com/alekpopovic','author attribution')
    check(meta['open_source'] and meta['content_license']=='CC-BY-4.0' and meta['code_license']=='MIT','open license metadata')
    for license_file in ['LICENSE.md','LICENSE-CODE','LICENSE-CONTENT.md','CONTENT_RIGHTS.md']:
        check('Aleksandar Popovic' in (ROOT/license_file).read_text(),license_file+' attribution')
    files=sorted((ROOT/'lessons').glob('*.md'))
    check(len(files)==24,'preface + twenty lessons + three appendices')
    book=(ROOT/'manuscript/Book.txt').read_text().splitlines()
    sample=(ROOT/'manuscript/Sample.txt').read_text().splitlines()
    check(book==[p.with_suffix('.txt').name for p in files],'Leanpub order complete')
    check(sample==book[:5],'sample selection deterministic')
    for p in files:
        content=p.read_text()
        check(content==(ROOT/'manuscript'/p.with_suffix('.txt').name).read_text(),p.name+' export equality')
        check(content.count('```')%2==0,p.name+' balanced code fences')
        if re.match(r'^(0[1-9]|1\d|20)-',p.name):
            check('## Exercise' in content and '## Answer' in content,p.name+' exercise and answer')
        for resource in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',content):
            check((ROOT/'lessons'/resource).is_file(),p.name+' image resource')
    mapping=json.loads((ROOT/'publishing/prompt-lesson-map.json').read_text())
    check([p['prompt_id'] for p in mapping]==[f'{i:03}' for i in range(60)],'all sixty source tasks mapped')
    for p in (ROOT/'companion').rglob('*.py'):
        ast.parse(p.read_text(),filename=str(p))
    check(True,'companion Python syntax')
    for name in ['nginx-log-security','nginx-log-security-sample']:
        pdf=PdfReader(ROOT/'output'/(name+'.pdf'))
        check(pdf.metadata.author==meta['author'],name+' PDF author metadata')
        texts=[p.extract_text() or '' for p in pdf.pages]
        check('Copyright and open licenses' in '\n'.join(texts),name+' license section')
        check(len(pdf.pages)>10,name+' PDF page count')
        check(all(text.strip() for text in texts[1:]),name+' no blank reading pages')
        check('AI transparency' in '\n'.join(texts),name+' disclosure present')
        with zipfile.ZipFile(ROOT/'output'/(name+'.epub')) as z:
            check(z.read('mimetype')==b'application/epub+zip',name+' EPUB MIME')
            opf=ET.fromstring(z.read(next(item for item in z.namelist() if item.endswith('.opf'))))
            ns={'dc':'http://purl.org/dc/elements/1.1/'}
            check(any(n.text==meta['author'] for n in opf.findall('.//dc:creator',ns)),name+' EPUB author metadata')
            check(any('CC BY 4.0' in (n.text or '') and 'MIT' in (n.text or '') for n in opf.findall('.//dc:rights',ns)),name+' EPUB rights metadata')
            for item in z.namelist():
                if item.endswith(('.xml','.opf','.xhtml','.ncx')):ET.fromstring(z.read(item))
            check(any('cover' in item and item.endswith('.png') for item in z.namelist()),name+' embedded cover')
            check(any('architecture' in item or item.endswith('file0.png') for item in z.namelist()),name+' embedded figure')
    for p in (ROOT/'branding').glob('*.svg'):ET.fromstring(p.read_text())
    check(True,'SVG assets well formed')
    check(not list(ROOT.rglob('signing.key')) and not list(ROOT.rglob('*.sqlite3')),'no generated credentials or lab data')
    result={'status':'passed','checks':checks,'scope':'structure, source/export equality, PDF text, EPUB XML/assets, Python syntax',
      'does_not_verify':['Leanpub hosted generator','Nginx runtime','Vector runtime','PostgreSQL runtime','Go agent implementation',
                        'independent human editorial review','trademark clearance']}
    (ROOT/'verification/release-checks.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'passed','check_count':len(checks)}))


if __name__=='__main__':main()
