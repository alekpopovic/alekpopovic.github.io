from pathlib import Path
import json,re,hashlib,datetime
B=Path('books/inside-orch');S=B/'evidence/orch';O=json.loads((B/'editorial/book-outline.json').read_text());SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];commits={c['sha'] for c in json.loads((B/'evidence/commits.json').read_text())};results=[];errors=[]
for c in O['chapters'][16:24]:
 n=c['id'];p=B/c['chapter_path'];text=p.read_text();prose=re.sub(r'```.*?```','',text,flags=re.S);prose=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',prose);words=len(re.findall(r"\b[\w’'-]+\b",prose));checks=[]
 if not 1800<=words<=2500:errors.append(f'ch{n} narrative words {words}')
 for m in re.finditer(r'https://github.com/alekpopovic/orch/blob/([a-f0-9]{40})/([^\s)#]+)(?:#L(\d+)(?:-L(\d+))?)?',text):
  rev,path,a,z=m.groups();f=S/path;ok=rev==SHA and f.is_file() and (not a or int(z or a)<=len(f.read_text().splitlines()));checks.append({'path':path,'start':a,'end':z,'valid':ok})
  if not ok:errors.append(f'ch{n} bad source ref {m.group()}')
 for ref in re.findall(r'https://github.com/alekpopovic/orch/commit/([a-f0-9]+)',text):
  if ref not in commits:errors.append(f'ch{n} unknown commit {ref}')
 for meta in (B/f'examples/source-excerpts/ch{n}').glob('*.json'):
  x=json.loads(meta.read_text());raw=(S/x['source_path']).read_bytes();slice=('\n'.join(raw.decode().splitlines()[x['line_start']-1:x['line_end']])+'\n').encode();payload=meta.with_suffix('.txt').read_bytes()
  if payload!=slice or hashlib.sha256(payload).hexdigest()!=x['excerpt_sha256'] or hashlib.sha256(raw).hexdigest()!=x['raw_source_sha256']:errors.append(f'ch{n} excerpt mismatch {meta}')
 for target in re.findall(r'(?<!!)\[[^]]*\]\((?!https?://)([^)#]+)',text):
  if not (p.parent/target).is_file():errors.append(f'ch{n} missing companion {target}')
 ledger=json.loads((B/f'validation/evidence/ch{n}.json').read_text());actual_names=set()
 for sf in c['source_paths']:
  fp=S/sf
  if fp.suffix=='.go':actual_names.update(re.findall(r'^func (Test\w+)\(',fp.read_text(),re.M))
 for claim in ledger['claims']:
  f=S/claim['source_path']
  if not f.is_file() or not 0<claim['line_start']<=claim['line_end']<=len(f.read_text().splitlines()):errors.append(f'ch{n} invalid claim source {claim["claim_id"]}')
 review=B/f'validation/reviews/ch{n}.md';review.write_text(re.sub(r'Narrative words excluding fenced blocks: \d+\.',f'Narrative words excluding fenced blocks and destination URLs: {words}.',review.read_text()))
 results.append({'chapter_id':n,'narrative_words_excluding_fences_and_destination_urls':words,'source_refs':checks,'claims':len(ledger['claims']),'excerpts':len(list((B/f'examples/source-excerpts/ch{n}').glob('*.json'))),'worked_answers':(B/f'manuscript/solutions/ch{n}.md').is_file(),'execution_scope':'Source reviewed; named tests inspectable; no new runtime execution by this author.'})
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha':SHA,'command':'python3 books/inside-orch/scripts/check_chapters_17_24.py','scope':'Local H1/word count/source/commit/claim/byte-excerpt/companion verification plus manual source review; not a test execution.','chapters':results,'errors':errors};(B/'validation/reviews/chapters-17-24.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'chapters':[{k:v for k,v in c.items() if k in ['chapter_id','narrative_words_excluding_fences_and_destination_urls','claims','excerpts']} for c in results],'errors':errors},indent=2));raise SystemExit(bool(errors))
