#!/usr/bin/env python3
"""Inspect exact PDF/EPUB structure and canonical section completeness."""
import hashlib,importlib.util,json,re,subprocess,unicodedata,zipfile
from datetime import datetime,timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from pypdf import PdfReader
BOOK=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('publisher',BOOK/'scripts/build.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub)
paths=pub.selection();pdf=BOOK/'dist/inside-orch.pdf';epub=BOOK/'dist/inside-orch.epub';reader=PdfReader(pdf)
def norm(x):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',x)).strip()
text=norm(' '.join(p.extract_text() for p in reader.pages));errors=[]
section_checks=[]
for path in paths:
 title=pub.title(path);present=norm(title) in text
 section_checks.append(dict(title=title,pdf_present=present))
 if not present:errors.append('PDF missing title: '+title)
assert (BOOK/'dist/inside-orch.md').read_text()==pub.assemble(),'stale assembled manuscript'
outline=[]
def walk(items):
 for item in items:
  if isinstance(item,list):walk(item)
  else:outline.append(str(item.title))
walk(reader.outline)
for path in paths:
 if pub.title(path) not in outline:errors.append('Missing PDF bookmark: '+pub.title(path))
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
if any(' no ' in line for line in fonts.splitlines()[2:]):errors.append('Unembedded font')
fontnames=[line.split()[0].split('+')[-1] for line in fonts.splitlines()[2:]]
for name in fontnames:
 if not name.startswith(('DM','BookMono','BookEmoji')):errors.append('Unbundled fallback font: '+name)
metadata=reader.metadata
if metadata.author!=pub.meta()['author']:errors.append('PDF author metadata')
with zipfile.ZipFile(epub) as z:
 entries=z.infolist()
 if entries[0].filename!='mimetype' or entries[0].compress_type!=zipfile.ZIP_STORED or z.read('mimetype')!=b'application/epub+zip':errors.append('EPUB mimetype/order')
 for p in paths:
  doc=ET.fromstring(z.read('EPUB/text/'+p.stem+'.xhtml'));hs=doc.findall('.//{http://www.w3.org/1999/xhtml}h1')
  if len(hs)!=1 or ''.join(hs[0].itertext())!=pub.title(p):errors.append('EPUB section mismatch: '+p.stem)
 opf=ET.fromstring(z.read('EPUB/package.opf'))
 creators=[x.text for x in opf.findall('.//{http://purl.org/dc/elements/1.1/}creator')]
 if pub.meta()['author'] not in creators:errors.append('EPUB author metadata')
 cover=z.read('EPUB/media/cover.png')
 if cover!=(BOOK/'publication/cover.png').read_bytes():errors.append('EPUB cover differs')
 epub_count=sum(x.filename.startswith('EPUB/text/') and x.filename.endswith('.xhtml') for x in entries)
r=dict(status='passed' if not errors else 'failed',source_sha=pub.meta()['source_sha'],checked_at_utc=datetime.now(timezone.utc).isoformat(),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),epub_sha256=hashlib.sha256(epub.read_bytes()).hexdigest(),pdf_pages=len(reader.pages),pdf_bookmarks=len(outline),pdf_fonts=fontnames,pdf_author=metadata.author,reading_sections=len(paths),epub_text_documents=epub_count,section_checks=section_checks,errors=errors,scope='Structural/extracted text and embedded-font checks; all-page visual and real EPUB preview remain separate.')
(BOOK/'validation/publication/format-structure.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='section_checks'}));raise SystemExit(bool(errors))
