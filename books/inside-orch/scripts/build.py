#!/usr/bin/env python3
"""Publish the canonical Inside orch manuscript locally. No network or deployment."""
from __future__ import annotations
import argparse,hashlib,html,json,os,re,shutil,zipfile
from pathlib import Path
from urllib.parse import unquote,urlsplit
from xml.etree import ElementTree as ET
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT.parents[1]
DIST=ROOT/'dist'
NAME='inside-orch'
MD=MarkdownIt('commonmark',{'html':False,'xhtmlOut':True}).enable('table')

def meta():return json.loads((ROOT/'book.json').read_text())
def selection(manuscript=None):
 base=(manuscript or ROOT/'manuscript').resolve();result=[]
 for entry in (base/'Book.txt').read_text().splitlines():
  if not entry.strip():continue
  p=(base/entry.strip()).resolve()
  if not p.is_relative_to(base) or p.suffix!='.md' or not p.is_file():raise ValueError('Invalid manuscript entry: '+entry)
  if p.parent not in (base,base/'chapters',base/'appendices'):raise ValueError('Unsupported manuscript directory: '+entry)
  result.append(p)
 if len(result)!=47 or len({p.stem for p in result})!=47:raise ValueError('Expected 47 unique source stems')
 if title(result[0])!='Preface':raise ValueError('Preface must be first')
 for n,p in enumerate(result[1:41],1):
  if not title(p).startswith(f'Chapter {n} - '):raise ValueError('Incorrect chapter order/title: '+str(p))
 for letter,p in zip('ABCDEF',result[41:]):
  if not title(p).startswith(f'Appendix {letter} - '):raise ValueError('Incorrect appendix order/title: '+str(p))
 return result

def title(path):
 headings=re.findall(r'^# (.+)$',path.read_text(),re.M)
 if len(headings)!=1:raise ValueError('Exactly one H1 required: '+str(path))
 return headings[0]
def slug(text):return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-') or 'section'
def assemble():return '\n\n'.join(p.read_text().rstrip() for p in selection())+'\n'
def epub_sections():return {p.stem:['EPUB/text/'+p.stem+'.xhtml'] for p in selection()}
def source_reference(origin,target):
 u=urlsplit(target)
 if u.scheme or u.netloc or not u.path:return None
 p=(origin.parent/unquote(u.path)).resolve()
 if not p.is_relative_to(ROOT) or not p.is_file():raise ValueError(f'Broken/escaped book reference {origin}: {target}')
 return p

def permitted_companion(path):
 rel=path.relative_to(ROOT).as_posix()
 # Never traverse the pack, source corpus, credentials or raw infrastructure exports.
 if rel.startswith(('prompts/','evidence/','state/','dist/')):return False
 if path.suffix.lower() not in {'.md','.json','.txt','.go','.py','.sh','.yaml','.yml','.svg','.png','.csv'}:return False
 if path.name.startswith('.') or any(x in path.name.lower() for x in ('credential','private-key','.env')):return False
 if rel in {'scripts/observe_database_recovery.py','scripts/observe_process_restart.py','scripts/run_database_tests.py','scripts/verify_lab_records.py','scripts/verify_rollout_security_labs.py','scripts/run_recorded.py','tests/test_recovery_targets.py'}:return True
 return rel.startswith(('manuscript/solutions/','exercises/','validation/exercises/','examples/','labs/','validation/evidence/','validation/labs/','validation/intake/')) or rel in ('validation/reviews/ch17-24-source-tests.json','validation/reviews/ch17-24-fresh-source-tests.json','publication/RIGHTS.md','publication/NOTICE.md','editorial/REFERENCES.md')

def references(path):
 result=[]
 for t in MD.parse(path.read_text()):
  for c in t.children or []:
   attr='href' if c.type=='link_open' else 'src' if c.type=='image' else None
   if attr and (p:=source_reference(path,c.attrGet(attr) or '')) is not None:result.append(p)
 return result

def companions():
 selected=selection();seen=set(selected);pending=list(selected);found=[]
 while pending:
  origin=pending.pop()
  for p in references(origin):
   if p in seen:continue
   if not permitted_companion(p):raise ValueError('Unapproved public companion: '+str(p.relative_to(ROOT)))
   seen.add(p);found.append(p)
   if p.suffix=='.md':pending.append(p)
 return found

def target_reference(origin,target,mode,paths):
 u=urlsplit(target)
 if u.scheme or u.netloc:return target
 if not u.path:
  root=origin.stem if origin in paths else 'companion-'+slug(origin.relative_to(ROOT).as_posix())
  return '#'+root+'-'+u.fragment if mode=='print' and u.fragment and u.fragment!=origin.stem else ('#'+root if mode=='print' and u.fragment==origin.stem else target)
 p=source_reference(origin,target)
 suffix=('?'+u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
 if p in paths:
  if mode=='print':return '#'+(p.stem+'-'+u.fragment if u.fragment and u.fragment!=p.stem else p.stem)
  if mode=='offline':return offline_relative(origin,Path(p.stem+'.html'),paths)+suffix
  return p.stem+'.xhtml'+suffix if mode=='epub' else '/books/inside-orch/'+p.stem+'.html'+suffix
 rel=p.relative_to(ROOT).as_posix()
 if not permitted_companion(p):raise ValueError('Unapproved public reference: '+rel)
 if mode=='offline':
  destination=Path('companion')/Path(rel).with_suffix('.html') if p.suffix=='.md' else Path('assets')/rel
  return offline_relative(origin,destination,paths)+suffix
 if mode=='site':
  return ('/books/inside-orch/companion/'+str(Path(rel).with_suffix('.html')) if p.suffix=='.md' else '/assets/books/inside-orch/'+rel)+suffix
 if mode=='epub':
  return ('../media/'+rel if p.suffix in {'.png','.svg'} else 'companion-'+slug(rel)+'.xhtml')+suffix
 if p.suffix=='.md':return '#companion-'+slug(rel)+(('-'+u.fragment) if u.fragment else '')
 return 'https://www.alekpopovic.com/assets/books/inside-orch/'+rel+suffix

def offline_location(path,paths):
 return Path(path.stem+'.html') if path in paths else Path('companion')/path.relative_to(ROOT).with_suffix('.html')

def offline_relative(origin,destination,paths):
 return Path(os.path.relpath(destination,offline_location(origin,paths).parent)).as_posix()

def render(path,mode='site',paths=None):
 paths=paths or selection();tokens=MD.parse(path.read_text());used={}
 for i,t in enumerate(tokens):
  if mode=='print' and t.type=='table_open':
   if path.name.startswith('a-cli-api'):t.attrSet('class','cli-reference')
   elif path.name.startswith('b-lifecycle'):
    # Count only this table's header, not subsequent tables in the appendix.
    header_end=next(j for j in range(i+1,len(tokens)) if tokens[j].type=='thead_close')
    header_columns=sum(token.type=='th_open' for token in tokens[i+1:header_end])
    t.attrSet('class','invariant-reference' if header_columns==4 else 'lifecycle-reference')
   elif path.name.startswith('f-glossary'):t.attrSet('class','glossary-reference')
  if mode=='print' and t.type=='paragraph_open' and i+3<len(tokens) and tokens[i+3].type=='fence':
   t.attrSet('class','code-introduction')
  if t.type=='heading_open':
   base=path.stem if t.tag=='h1' else slug(tokens[i+1].content)
   if mode=='print':
    root=path.stem if path in paths else 'companion-'+slug(path.relative_to(ROOT).as_posix())
    base=root if t.tag=='h1' else root+'-'+base
   n=used.get(base,0);used[base]=n+1;t.attrSet('id',base if not n else f'{base}-{n}')
  for c in t.children or []:
   attr='href' if c.type=='link_open' else 'src' if c.type=='image' else None
   if attr:
    target=c.attrGet(attr) or '';resolved=source_reference(path,target)
    if c.type=='image' and resolved is None and mode=='print':raise ValueError('Print images must be local approved assets: '+target)
    if c.type=='image' and resolved is not None and mode=='site' and resolved.suffix.lower()=='.png':
     from PIL import Image
     with Image.open(resolved) as image:
      c.attrSet('width',str(image.width));c.attrSet('height',str(image.height))
    if c.type=='image' and resolved is not None and mode=='print':
     if not permitted_companion(resolved):raise ValueError('Unapproved image: '+str(resolved))
     c.attrSet(attr,resolved.as_uri())
    else:c.attrSet(attr,target_reference(path,target,mode,paths))
 return MD.renderer.render(tokens,MD.options,{})

def hashes(paths):return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
def evidence(name,data):
 p=ROOT/'validation/publication'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')

def print_html():
 m=meta();paths=selection();extra=[p for p in companions() if p.suffix=='.md']
 contents=''.join('<section class="chapter">'+render(p,'print',paths)+'</section>' for p in paths)
 answers=''.join('<section class="chapter companion">'+render(p,'print',paths)+'</section>' for p in extra)
 toc='<nav class="toc"><h1>Contents</h1><ol>'+''.join(f'<li><a href="#{p.stem}">{html.escape(title(p))}</a></li>' for p in paths)+'</ol></nav>'
 rights=html.escape(m.get('copyright','Copyright © 2026 Aleksandar Popovic. All rights reserved.'))
 css=(ROOT/'publication/print.css').read_text().replace('../../../assets/fonts/dm-sans.ttf',(ROOT/'publication/fonts/dm-sans.ttf').as_uri())
 for font in ('dejavu-sans-mono.ttf','dejavu-sans-mono-bold.ttf','noto-color-emoji.ttf'):
  css=css.replace('fonts/'+font,(ROOT/'publication/fonts'/font).as_uri())
 css+='\nhtml{font-family:DM,BookEmoji,sans-serif}pre{font-family:BookMono,BookEmoji,monospace}code{font-family:BookMono,BookEmoji,monospace}'
 doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(m['title']+': '+m['subtitle'])}</title><meta name="author" content="{html.escape(m['author'])}"><meta name="dcterms.created" content="2026-10-13"><style>{css}</style></head><body><section class="cover"><img alt="Inside orch — Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic" src="{(ROOT/'publication/cover.png').as_uri()}"></section><section class="rights"><h1>{html.escape(m['title'])}</h1><p>{html.escape(m['subtitle'])}</p><p>{html.escape(m['author'])}</p><p>{rights}</p><p>Source-based engineering edition · {html.escape(m['edition'])}</p><p>Source revision <code>{m['source_sha']}</code>. Observations describe the inspected and tested boundaries; no production certification is implied.</p></section>{toc}{contents}{answers}</body></html>'''
 out=ROOT/'publication/pdf-build/inside-orch.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(doc);return out

def pdf():
 from weasyprint import HTML
 doc=print_html();out=DIST/(NAME+'.pdf');DIST.mkdir(exist_ok=True)
 HTML(filename=str(doc)).write_pdf(out,pdf_identifier=b'inside-orch-1.0-cbfc94ade5b5')
 from pypdf import PdfReader
 import weasyprint
 r=PdfReader(out);evidence('pdf-build.json',{'status':'built_visual_review_pending','pages':len(r.pages),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'inputs':hashes(selection()+companions()+[ROOT/'book.json',ROOT/'scripts/build.py',ROOT/'publication/cover.png',ROOT/'publication/print.css']+sorted((ROOT/'publication/fonts').glob('*'))),'tool':'WeasyPrint','tool_version':weasyprint.__version__,'author':meta()['author']});return out

EPUB_CSS='''html{color-scheme:light dark}body{font-family:serif;line-height:1.55;margin:5%;overflow-wrap:anywhere;}h1,h2,h3{font-family:sans-serif;line-height:1.2;break-after:avoid}h1{font-size:1.7em}a{color:#2374e1}pre{font-size:.88em;white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid #718096;padding:.6em}code{font-family:monospace}table{border-collapse:collapse;width:100%;table-layout:fixed;font-size:.9em}th,td{border:1px solid #718096;padding:.35em;text-align:left;overflow-wrap:anywhere}img,svg{max-width:100%;height:auto}blockquote{border-left:.2em solid #2374e1;padding-left:1em}@media(prefers-color-scheme:dark){a{color:#73c7ff}}'''
def xhtml(name,body):return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>'+html.escape(name)+'</title><link rel="stylesheet" type="text/css" href="../styles/book.css" /></head><body>'+body+'</body></html>'
def epub():
 m=meta();paths=selection();extra=companions();documents={p.stem+'.xhtml':(title(p),render(p,'epub',paths)) for p in paths}
 for p in extra:
  name='companion-'+slug(p.relative_to(ROOT).as_posix())+'.xhtml'
  if name in documents:raise ValueError('EPUB companion filename collision: '+name)
  if p.suffix=='.md':documents[name]=(title(p),render(p,'epub',paths))
  elif p.suffix not in {'.png','.svg'}:documents[name]=(p.name,'<h1>'+html.escape(p.name)+'</h1><pre>'+html.escape(p.read_text())+'</pre>')
 manifest=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="css" href="styles/book.css" media-type="text/css"/>','<item id="cover-image" href="media/cover.png" media-type="image/png" properties="cover-image"/>','<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>'];spine=['<itemref idref="cover"/>']
 files={'EPUB/styles/book.css':EPUB_CSS.encode(),'EPUB/media/cover.png':(ROOT/'publication/cover.png').read_bytes(),'EPUB/text/cover.xhtml':xhtml('Cover','<section epub:type="cover"><img src="../media/cover.png" alt="'+html.escape(m['title']+': '+m['subtitle']+' — '+m['author'],quote=True)+'" /></section>').encode()}
 for n,(filename,(name,body)) in enumerate(documents.items()):
  ident='doc-'+str(n);manifest.append(f'<item id="{ident}" href="text/{filename}" media-type="application/xhtml+xml"/>');spine.append(f'<itemref idref="{ident}"/>');files['EPUB/text/'+filename]=xhtml(name,body).encode()
 mime={'.png':'image/png','.svg':'image/svg+xml','.json':'application/json','.txt':'text/plain','.go':'text/plain','.py':'text/plain','.sh':'text/plain','.yaml':'text/plain','.yml':'text/plain','.csv':'text/csv'}
 for n,p in enumerate(p for p in extra if p.suffix in {'.png','.svg'}):
  rel=p.relative_to(ROOT).as_posix();manifest.append(f'<item id="asset-{n}" href="media/{rel}" media-type="{mime[p.suffix]}"/>');files['EPUB/media/'+rel]=p.read_bytes()
 navlinks=''.join(f'<li><a href="text/{p.stem}.xhtml">{html.escape(title(p))}</a></li>' for p in paths)
 files['EPUB/nav.xhtml']=('''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>Contents</title></head><body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'''+navlinks+'''</ol></nav><nav epub:type="landmarks"><h2>Landmarks</h2><ol><li><a epub:type="cover" href="text/cover.xhtml">Cover</a></li><li><a epub:type="bodymatter" href="text/00-preface.xhtml">Start reading</a></li></ol></nav></body></html>''').encode()
 files['EPUB/package.opf']=('''<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">urn:inside-orch:1.0:cbfc94ade5b57e449d6b73bf1485b1c5b1647022</dc:identifier><dc:title>'''+html.escape(m['title']+': '+m['subtitle'])+'</dc:title><dc:creator>'+html.escape(m['author'])+'</dc:creator><dc:language>en</dc:language><dc:rights>'+html.escape(m['copyright'])+'</dc:rights><meta property="dcterms:modified">2026-10-13T00:00:00Z</meta></metadata><manifest>'+''.join(manifest)+'</manifest><spine>'+''.join(spine)+'</spine></package>').encode()
 files['META-INF/container.xml']=b'<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
 for path,data in files.items():
  if path.endswith(('.opf','.xhtml','.xml')):ET.fromstring(data)
 DIST.mkdir(exist_ok=True);out=DIST/(NAME+'.epub')
 with zipfile.ZipFile(out,'w') as z:
  info=zipfile.ZipInfo('mimetype',(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_STORED;z.writestr(info,b'application/epub+zip')
  for path,data in sorted(files.items()):
   info=zipfile.ZipInfo(path,(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 evidence('epub-build.json',{'status':'built_validation_pending','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'reading_sections':len(paths),'companion_documents':len(documents)-len(paths),'epub_chapters':epub_sections(),'inputs':hashes(paths+extra+[ROOT/'publication/cover.png']),'files':sorted(files)});return out

def build():
 DIST.mkdir(exist_ok=True);(DIST/(NAME+'.md')).write_text(assemble());pdf();epub()

def offline():
 """Explicit downloadable edition; never alters the site's service worker."""
 paths=selection();extra=companions();m=meta();out=DIST/'online'
 if out.exists():shutil.rmtree(out)
 out.mkdir(parents=True)
 css=(ROOT/'publication/offline.css').read_text()
 (out/'assets').mkdir();(out/'assets/reader.css').write_text(css)
 for font in (ROOT/'publication/fonts').iterdir():
  dest=out/'assets/fonts'/font.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(font,dest)
 for p in extra:
  if p.suffix!='.md':
   dest=out/'assets'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 for origin in paths+[p for p in extra if p.suffix=='.md']:
  location=offline_location(origin,paths);dest=out/location;dest.parent.mkdir(parents=True,exist_ok=True)
  def relative(p):return Path(os.path.relpath(p,location.parent)).as_posix()
  links=''.join('<li><a '+('aria-current="page" ' if p==origin else '')+'href="'+html.escape(relative(Path(p.stem+'.html')),quote=True)+'">'+html.escape(title(p))+'</a></li>' for p in paths)
  pager=''
  if origin in paths:
   i=paths.index(origin)
   for label,j in [('Previous',i-1),('Next',i+1)]:
    if 0<=j<len(paths):pager+='<a rel="'+('prev' if label=='Previous' else 'next')+'" href="'+relative(Path(paths[j].stem+'.html'))+'">'+label+': '+html.escape(title(paths[j]))+'</a>'
  body=render(origin,'offline',paths)
  page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="'+html.escape(m['author'],quote=True)+'"><title>'+html.escape(title(origin)+' · '+m['title'])+'</title><link rel="stylesheet" href="'+relative(Path('assets/reader.css'))+'"></head><body><a class="skip" href="#reading">Skip to reading</a><header><a href="'+relative(Path('index.html'))+'">Inside orch</a><span>Offline engineering edition · Aleksandar Popovic</span></header><div class="reader"><nav aria-label="Book contents"><details open><summary>Contents · 47 sections</summary><ol>'+links+'</ol></details></nav><main id="reading" tabindex="-1">'+body+'<nav class="pager" aria-label="Reading navigation">'+pager+'</nav><footer><p>Source revision <code>'+m['source_sha']+'</code>.</p><p>'+html.escape(m['copyright'])+'</p><p>External source links require an internet connection. Reading and navigation require no JavaScript.</p></footer></main></div></body></html>'
  dest.write_text(page)
 cover=out/'assets/cover.png';shutil.copy2(ROOT/'publication/cover.png',cover)
 (out/'downloads').mkdir()
 for ext in ['pdf','epub']:shutil.copy2(DIST/(NAME+'.'+ext),out/'downloads'/(NAME+'.'+ext))
 (out/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Inside orch · Offline edition</title><link rel="stylesheet" href="assets/reader.css"></head><body><main class="landing"><img class="cover" src="assets/cover.png" alt="Inside orch book cover"><h1>Inside orch</h1><p>'+html.escape(m['subtitle'])+'</p><p>By '+html.escape(m['author'])+'</p><p>47 complete reading sections, worked answers and selected companions. External repository references require internet access.</p><p><a href="00-preface.html">Start reading</a> · <a href="downloads/inside-orch.pdf">PDF</a> · <a href="downloads/inside-orch.epub">EPUB</a></p><p>'+html.escape(m['copyright'])+'</p></main></body></html>')
 files={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
 evidence('offline-export.json',{'status':'exported_validation_pending','source_sha':m['source_sha'],'sections':len(paths),'files':files,'scope':'Explicit publisher offline export; no live worker or analytics changes.'})
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('format',choices=['all','pdf','epub','markdown','offline','check'],default='all',nargs='?');a=p.parse_args()
 if a.format=='all':build()
 elif a.format=='pdf':print(pdf())
 elif a.format=='epub':print(epub())
 elif a.format=='offline':print(offline())
 elif a.format=='markdown':DIST.mkdir(exist_ok=True);(DIST/(NAME+'.md')).write_text(assemble())
 else:print(json.dumps({'sections':len(selection()),'companions':len(companions()),'metadata':meta()},indent=2))
