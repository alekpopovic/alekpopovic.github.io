#!/usr/bin/env python3
"""Exhaustive fenced-block/source synchronization and syntax inventory; never runs published procedures."""
from pathlib import Path
import argparse,ast,datetime,hashlib,json,re,subprocess,textwrap
from markdown_it import MarkdownIt
import yaml
B=Path(__file__).resolve().parents[1];SITE=B.parents[1]
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);a=p.parse_args();G=a.git_dir
SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];md=MarkdownIt();errors=[];sources={};metadata=[]
def digest(v):return hashlib.sha256(v).hexdigest()
def records(v):
 if isinstance(v,list):
  for x in v:yield from records(x)
 elif isinstance(v,dict):
  if {'source_path','source_sha','line_start','line_end'}<=v.keys():yield v
  else:
   for x in v.values():yield from records(x)
def source(sha,path):
 key=(sha,path)
 if key not in sources:sources[key]=subprocess.check_output(['git','--git-dir='+G,'show',sha+':'+path])
 return sources[key]
for file in sorted((B/'examples/source-excerpts').rglob('*.json')):
 for r in records(json.loads(file.read_text())):
  raw=b''.join(source(r['source_sha'],r['source_path']).splitlines(keepends=True)[r['line_start']-1:r['line_end']]);metadata.append(dict(r,metadata_path=str(file.relative_to(B)),raw=raw))
paths=sorted(set([*B.glob('manuscript/**/*.md'),*B.glob('labs/**/README.md'),*B.glob('examples/**/README.md')]))
paths += [x for x in (SITE/'_posts').glob('*.md') if re.search(r'book_id:\s*["\']?inside-orch',x.read_text())]
blocks=[];exact=[];inline=[];syntax=[]
for file in paths:
 text=file.read_text();lines=text.splitlines(keepends=True);tokens=md.parse(text);fences=[x for x in tokens if x.type=='fence']
 rel=str(file.relative_to(B)) if file.is_relative_to(B) else '../../'+str(file.relative_to(SITE))
 for n,t in enumerate(fences,1):
  start,end=t.map;code=t.content;lang=t.info.split()[0]if t.info else '';row=dict(path=rel,chapter=file.stem[:2] if file.parent.name=='chapters'else file.stem,block_id=f'{rel}#block-{n:03}',language=lang,line_start=start+1,line_end=end,displayed_sha256=digest(code.encode()),content=code,context=''.join(lines[max(0,start-5):min(len(lines),end+5)]))
  matches=[r for r in metadata if r['raw'].decode().rstrip('\n')==code.rstrip('\n') or textwrap.dedent(r['raw'].decode()).rstrip('\n')==code.rstrip('\n')]
  if matches:
   nearby=''.join(lines[max(0,start-7):min(len(lines),end+6)])
   pinned=[r for r in matches if r['source_sha']+'/'+r['source_path'] in nearby]
   r=(pinned or matches)[0];raw=r['raw'];trans='normalize final newline only'if raw.decode().rstrip('\n')==code.rstrip('\n')else 'dedent common whitespace and normalize final newline'
   row.update(kind='historical source'if r['source_sha']!=SHA else'exact source',source_sha=r['source_sha'],source_path=r['source_path'],source_line_start=r['line_start'],source_line_end=r['line_end'],raw_sha256=digest(raw),checked_transform=trans,metadata_path=r['metadata_path'],source_url=f"https://github.com/alekpopovic/orch/blob/{r['source_sha']}/{r['source_path']}#L{r['line_start']}-L{r['line_end']}",validation='passed byte comparison',fragment_context={'package_and_imports':'Use surrounding pinned source file; listing is not a complete separate module.','setup':'Compile/test the unchanged package in a disposable locked Go module; historical fragment is archival, not current runnable program.'})
   if not pinned:errors.append('Source block lacks nearby matching immutable attribution: '+row['block_id'])
   exact.append({k:v for k,v in row.items()if k not in ['content','context']})
  elif lang in ['sh','bash']:
   r=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True);row.update(kind='procedure',validation='shell syntax checked; operation not executed by this audit',execution_status='expected_only unless linked actual command record establishes the exact procedure',syntax_exit_code=r.returncode)
   syntax.append({'block_id':row['block_id'],'command':['bash','-n'],'exit_code':r.returncode,'stderr':r.stderr})
   if r.returncode:errors.append('Invalid shell syntax '+row['block_id']+': '+r.stderr)
  elif lang in ['yaml','yml']:
   try:yaml.safe_load(code);row.update(kind='teaching configuration',validation='YAML syntax parsed; semantic caller validation recorded separately')
   except Exception as e:errors.append('YAML parse '+row['block_id']+str(e))
  elif lang=='json':
   try:json.loads(code);row.update(kind='illustrative response',validation='JSON syntax parsed; illustrative example-only request ID, not observed transcript')
   except Exception as e:errors.append('JSON parse '+row['block_id']+str(e))
  else:
   row.update(kind='unmatched fragment',validation='review needed');errors.append('Unclassified fragment '+row['block_id'])
  blocks.append(row)
 # Inline tokens inventory includes every code span; symbols can be paths, env names, quantities or command pieces.
 for t in tokens:
  for c in t.children or []:
   if c.type=='code_inline':inline.append({'path':rel,'value':c.content,'kind':'inline reference; resolve by source inventory/command tree or explicit narrative context'})
# Source metadata consistency is exhaustive independently of whether its seed appears in manuscript.
seed_checks=[]
for r in metadata:
 declared=r.get('excerpt_sha256',r.get('sha256'));ok=declared==digest(r['raw']);seed_checks.append({'metadata':r['metadata_path'],'source_sha':r['source_sha'],'source_path':r['source_path'],'line_start':r['line_start'],'line_end':r['line_end'],'raw_sha256':digest(r['raw']),'passed':ok})
 if not ok:errors.append('Stale excerpt metadata '+r['metadata_path'])
now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=B/'validation/excerpts';out.mkdir(exist_ok=True)
index={'source_sha':SHA,'checked_at_utc':now,'command':['.venv/bin/python','books/inside-orch/scripts/audit_book_examples.py','--git-dir',G],'reviewed_paths':[str(f.relative_to(B))if f.is_relative_to(B)else'../../'+str(f.relative_to(SITE))for f in paths],'input_sha256':{str(f):digest(f.read_bytes())for f in paths},'excerpts':exact,'all_blocks':blocks,'inline_references':inline,'seed_checks':seed_checks,'shell_syntax_checks':syntax,'errors':errors,'status':'passed'if not errors else'failed','limitations':['Syntax checking never executes published shell procedures.','Exact fragment equality is not independent compilation or runtime wiring.','Inline reference inventory does not infer guarantees from symbol occurrence.']}
(out/'index.json').write_text(json.dumps(index,indent=2)+'\n')
print(json.dumps({'blocks':len(blocks),'exact_or_historical':len(exact),'seed_checks':len(seed_checks),'inline_references':len(inline),'errors':errors,'status':index['status']}));raise SystemExit(bool(errors))
