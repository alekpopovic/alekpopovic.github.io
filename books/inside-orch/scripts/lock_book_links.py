#!/usr/bin/env python3
"""Inventory book links offline; validate pinned Git objects and rendered anchors.

Network status remains not_checked_offline unless separately retained retrieval
records establish it. Local object proof never implies HTTP reachability.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,re,subprocess,posixpath,zipfile
from xml.etree import ElementTree as ET
from pathlib import Path
from urllib.parse import unquote,urlsplit
from markdown_it import MarkdownIt
B=Path(__file__).resolve().parents[1];SITE=B.parents[1]
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);p.add_argument('--output',default='evidence/link-lock.json');p.add_argument('--final',action='store_true');a=p.parse_args()
G=Path(a.git_dir).resolve();lock=json.loads((B/'evidence/source-lock.json').read_text());SHA=lock['baseline_sha'];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
head=subprocess.check_output(['git','--git-dir='+str(G),'rev-parse','HEAD'],text=True).strip();assert head==SHA
md=MarkdownIt('commonmark',{'html':False}).enable('table');cache={};errors=[];entries=[]
retrieved={r['url']:r for r in json.loads((B/'validation/intake/reference-register.json').read_text())['external_references']}
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-') or 'section'
def anchors(path):
 toks=md.parse(path.read_text());seen={};result=set()
 for i,t in enumerate(toks):
  if t.type=='heading_open':
   base=path.stem if t.tag=='h1' else slug(toks[i+1].content);n=seen.get(base,0);seen[base]=n+1;result.add(base if not n else f'{base}-{n}')
 return result
paths=sorted(set([*B.glob('manuscript/**/*.md'),*B.glob('publication/*.md'),*B.glob('publication/*.json'),*B.glob('publication/*.svg'),B/'book.json',B/'editorial/REFERENCES.md',B/'evidence/prompt-commit-map.json',*B.glob('examples/source-excerpts/**/*.json')]))
paths += [x for x in (SITE/'_posts').glob('*.md') if re.search(r'book_id:\s*[\"\']?inside-orch',x.read_text())]
for path in paths:
 text=path.read_text();links=[]
 if path.suffix=='.md':
  for t in md.parse(text):
   for c in t.children or []:
    key='href' if c.type=='link_open' else 'src' if c.type=='image' else None
    if key and c.attrGet(key):links.append(c.attrGet(key))
 # Raw URLs include editorial evidence URLs in JSON and code; do not miss them.
 links += [m[0].rstrip('.,;') for m in re.finditer(r'https?://[^\s<>"\x27`\)\]]+',text)]
 for target in sorted(set(links)):
  u=urlsplit(target);row=dict(origin=str(path.relative_to(SITE)),destination=target,type='external_primary_or_reference',sha=None,line_start=None,line_end=None,local_verification='not_applicable',network_status='not_checked_offline',checked_at_utc=now)
  if target in retrieved:
   row.update(network_status='previous_primary_retrieval_recorded',retrieved_at_date=retrieved[target]['retrieved_at_date'],retrieval_evidence='validation/intake/reference-register.json',retrieval_scope=retrieved[target]['claim_scope'])
  if u.netloc=='github.com' and u.path.startswith('/alekpopovic/orch/'):
   parts=u.path.split('/');kind=parts[3] if len(parts)>3 else ''
   if kind in ['blob','tree','commit']:
    sha=parts[4] if len(parts)>4 else '';row['sha']=sha;row['type']='pinned_source' if kind=='blob' else 'associated_commit' if kind=='commit' else 'pinned_tree'
    if not re.fullmatch('[0-9a-f]{40}',sha):row['local_verification']='failed_mutable_or_abbreviated_sha'
    else:
     obj=sha+(':'+unquote('/'.join(parts[5:])) if kind in ['blob','tree'] else '^{commit}');key=(kind,obj)
     if key not in cache:
      r=subprocess.run(['git','--git-dir='+str(G),'show',obj] if kind=='blob' else ['git','--git-dir='+str(G),'cat-file','-e',obj],capture_output=True)
      cache[key]=(r.returncode,r.stdout)
     code,data=cache[key];row['local_verification']='passed_git_object' if code==0 else 'failed_missing_git_object'
     if kind=='blob' and not code:
      row['source_path']=unquote('/'.join(parts[5:]));row['source_kind']='locked_current' if sha==SHA else 'historical';row['content_sha256']=hashlib.sha256(data).hexdigest()
      if u.fragment:
       m=re.fullmatch(r'L(\d+)(?:-L(\d+))?',u.fragment)
       if not m:row['local_verification']='failed_unknown_line_anchor'
       else:
        low=int(m[1]);high=int(m[2] or low);row.update(line_start=low,line_end=high)
        row['local_verification']='passed_git_lines' if 1<=low<=high<=len(data.splitlines()) else 'failed_line_interval'
  elif not u.scheme and not u.netloc:
   row['network_status']='not_applicable';row['type']='internal_cross_reference'
   dest=(SITE/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path)) if u.path else path
   if u.path.startswith('/books/inside-orch/'):
    generated=SITE/'book-pages/inside-orch'/u.path.removeprefix('/books/inside-orch/')
    if generated.is_file():dest=generated
   dest=dest.resolve()
   if dest.is_file():
    row['local_verification']='passed_file'
    if u.fragment and dest.suffix=='.md':row['local_verification']='passed_rendered_anchor' if unquote(u.fragment) in anchors(dest) else 'failed_rendered_anchor'
   else:row['local_verification']='blocked_missing_local_output' if u.path.startswith(('/books/inside-orch/','/assets/books/inside-orch/')) else 'failed_missing_file'
  if '/assets/books/inside-orch/' in u.path or (u.path.endswith(('.pdf','.epub')) and 'inside-orch' in u.path):
   row['type']='publication_download'
   candidate=B/'dist'/Path(u.path).name
   if candidate.is_file():row.update(local_verification='passed_built_download',artifact_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
   else:row['local_verification']='blocked_download_not_built'
  entries.append(row)
  if row['local_verification'].startswith(('failed','blocked')):errors.append(row)
mapdata=json.loads((B/'evidence/prompt-commit-map.json').read_text());mapping=mapdata['mapping'];ids=[int(x['prompt_id']) for x in mapping];assert sorted(ids)==list(range(91)) and len(set(ids))==91
tags={}
for line in subprocess.check_output(['git','--git-dir='+str(G),'show-ref','--tags'],text=True).splitlines():
 commit,ref=line.split();tags[ref.removeprefix('refs/tags/')]=subprocess.check_output(['git','--git-dir='+str(G),'rev-parse',ref+'^{commit}'],text=True).strip()
assert tags==mapdata['metadata']['tags'] and '0.2.0' not in tags and tags['0.3.0']!=SHA
known_commits={r['sha'] for r in json.loads((B/'evidence/commits.json').read_text())};assert all(r['commit_sha'] in known_commits for r in mapping)
# Verify exact excerpts against the actual historical/current Git bytes, not only URLs.
excerpt_checks=[]
def records(value):
 if isinstance(value,list):
  for item in value:yield from records(item)
 elif isinstance(value,dict):
  if {'source_path','source_sha','line_start','line_end'} <= value.keys():yield value
  else:
   for item in value.values():yield from records(item)
for metadata in sorted((B/'examples/source-excerpts').rglob('*.json')):
 for item in records(json.loads(metadata.read_text())):
  sha=item['source_sha'];rel=item['source_path'];low=item['line_start'];high=item['line_end']
  source=subprocess.check_output(['git','--git-dir='+str(G),'show',sha+':'+rel])
  raw=b''.join(source.splitlines(keepends=True)[low-1:high]);digest=hashlib.sha256(raw).hexdigest()
  target=item.get('output',item.get('excerpt_path',item.get('path')))
  if target:out=B/target
  elif metadata.parent==B/'examples/source-excerpts' and 'id' in item:out=metadata.parent/(item['id']+'.'+{'go':'go','sql':'sql','yaml':'yaml'}.get(item.get('language'),'txt'))
  else:out=metadata.with_suffix('.txt')
  declared=item.get('excerpt_sha256',item.get('sha256'));ok=declared==digest and out.is_file() and out.read_bytes()==raw
  excerpt_checks.append(dict(metadata=str(metadata.relative_to(B)),path=str(out.relative_to(B)),source_sha=sha,line_start=low,line_end=high,passed=ok))
  if not ok:errors.append(dict(origin=str(metadata.relative_to(B)),destination=str(out.relative_to(B)),local_verification='failed_exact_excerpt'))
if a.final:
 for ext in ['pdf','epub']:
  artifact=B/'dist'/('inside-orch.'+ext);public=SITE/'assets/books/inside-orch/downloads'/artifact.name
  ok=artifact.is_file() and public.is_file() and hashlib.sha256(artifact.read_bytes()).digest()==hashlib.sha256(public.read_bytes()).digest()
  entries.append(dict(origin='final publication artifacts',destination=str(public.relative_to(SITE)),type='publication_download',sha=None,line_start=None,line_end=None,local_verification='passed_exact_public_copy' if ok else 'blocked_download_not_built',network_status='not_checked_offline',checked_at_utc=now,artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest() if artifact.is_file() else None))
  if not ok:errors.append(entries[-1])
 epub=B/'dist/inside-orch.epub'
 if epub.is_file():
  with zipfile.ZipFile(epub) as z:
   names=set(z.namelist());docs={n:ET.fromstring(z.read(n)) for n in names if n.endswith('.xhtml')};epub_ids={n:{x.attrib['id'] for x in root.iter() if 'id' in x.attrib} for n,root in docs.items()}
   for name,root in docs.items():
    for node in root.iter():
     for attr in ['href','src']:
      target=node.attrib.get(attr)
      if not target:continue
      u=urlsplit(target)
      if u.scheme or u.netloc:continue
      destination=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(u.path))) if u.path else name
      ok=destination in names and (not u.fragment or unquote(u.fragment) in epub_ids.get(destination,set()))
      row=dict(origin='dist/inside-orch.epub:'+name,destination=target,type='epub_cross_reference',sha=None,line_start=None,line_end=None,local_verification='passed_epub_target_anchor' if ok else 'failed_epub_target_anchor',network_status='not_applicable',checked_at_utc=now)
      entries.append(row)
      if not ok:errors.append(row)
 pdf=B/'dist/inside-orch.pdf'
 if pdf.is_file():
  from pypdf import PdfReader
  reader=PdfReader(pdf)
  for number,page in enumerate(reader.pages,1):
   for annotation in page.get('/Annots',[]):
    obj=annotation.get_object();action=obj.get('/A',{});uri=action.get('/URI')
    if uri:entries.append(dict(origin=f'dist/inside-orch.pdf:page{number}',destination=str(uri),type='pdf_clickable_uri',sha=None,line_start=None,line_end=None,local_verification='passed_pdf_uri_annotation',network_status='not_checked_offline',checked_at_utc=now))
result=dict(source_sha=SHA,checked_at_utc=now,git_object_database=str(G),scope=('Complete manuscript, appendix, solution, publication metadata and original book-post link inventory; exact public PDF/EPUB copies, EPUB internal anchors and PDF URI annotations checked.' if a.final else 'Complete selected manuscript/appendix/solution/publication metadata and original book-post link inventory; final generated artifacts require a later rerun.'),offline_behavior='No HTTP requests; local Git object checks do not establish network reachability.',inventory_paths=[str(x.relative_to(SITE)) for x in paths],input_sha256={str(x.relative_to(SITE)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},provenance=dict(verified_tag_targets=tags,release_dates='Captured releases.jsonmetadata is historical; not re-fetched by offlinechecker.',prompt_ids=ids,unique_prompt_count=91,unique_associated_commits=len(set(x['commit_sha'] for x in mapping)),design_prompt_numbers=mapdata['metadata']['design_prompt_numbers'],early_prompts='00–28 retrospective; associations do not prove execution',late_prompts='62–90 diff-supported batches'),counts=dict(links=len(entries),errors=len(errors),pinned=sum(x['type']=='pinned_source' for x in entries),network_not_checked=sum(x['network_status']=='not_checked_offline' for x in entries)),links=entries,exact_excerpt_checks=excerpt_checks,errors=errors,status='passed_offline' if not errors else 'review_needed')
result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
if a.final:
 result['artifact_sha256']={ext:hashlib.sha256((B/'dist'/('inside-orch.'+ext)).read_bytes()).hexdigest() for ext in ['pdf','epub'] if (B/'dist'/('inside-orch.'+ext)).is_file()}
out=(B/a.output).resolve();assert out.is_relative_to(B) and not out.is_relative_to(B/'evidence/orch');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'counts':result['counts'],'error_destinations':[(x['origin'],x['destination'],x['local_verification']) for x in errors]}));raise SystemExit(bool(errors))
