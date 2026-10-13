#!/usr/bin/env python3
"""Check this author batch without certifying technical truth or other chapters."""
from pathlib import Path
import datetime,hashlib,json,re,sys
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';lock=json.loads((B/'evidence/source-lock.json').read_text());SHA=lock['baseline_sha'];outline=json.loads((B/'editorial/book-outline.json').read_text());commits={c['sha'] for c in json.loads((B/'evidence/commits.json').read_text())};errors=[];chapters=[]
required={'claim_id','statement','classification','source_path','source_sha','line_start','line_end','associated_commits','validation','evidence_log','limitations'}
for f in lock['files']:
 if hashlib.sha256((S/f['path']).read_bytes()).hexdigest()!=f['sha256']:errors.append('Immutable hash mismatch: '+f['path'])
for n in range(1,9):
 ch=f'{n:02d}';item=outline['chapters'][n-1];text=(B/item['chapter_path']).read_text()
 assert text.splitlines()[0]==f"# Chapter {n} - {item['title']}"
 prose=re.sub(r'```.*?```','',text,flags=re.S);prose=re.sub(r'\[([^\]]+)\]\([^\)]+\)',r'\1',prose);words=len(re.findall(r'\b[\w-]+\b',prose))
 if not 1800<=words<=2500:errors.append(f'ch{ch} word count{words}')
 if re.search(r'\]\[|\{\{EXCERPT|\[\[[^|\n]+\|\d',text):errors.append(f'ch{ch} malformed/unresolved link')
 sources=[]
 for m in re.finditer(r'https://github.com/alekpopovic/orch/blob/([^/]+)/([^\s)#]+)(?:#L(\d+)(?:-L(\d+))?)?',text):
  sha,path,start,end=m.groups();file=S/path;start=int(start or 1);end=int(end or start)
  if sha!=SHA or not file.is_file() or not 1<=start<=end<=len(file.read_text().splitlines()):errors.append(f'ch{ch} bad source '+m.group())
  sources.append(dict(path=path,start=start,end=end))
 for sha in re.findall(r'https://github.com/alekpopovic/orch/commit/([0-9a-f]+)',text):
  if sha not in commits:errors.append(f'ch{ch} unknown historical SHA{sha}')
 registry=json.loads((B/f'examples/source-excerpts/ch{ch}/registry.json').read_text())
 for excerpt in registry:
  raw=(S/excerpt['source_path']).read_bytes();exact=b''.join(raw.splitlines(keepends=True)[excerpt['start_line']-1:excerpt['end_line']]);copied=(B/excerpt['output']).read_bytes()
  if exact!=copied or hashlib.sha256(copied).hexdigest()!=excerpt['sha256']:errors.append(f'ch{ch} excerpt differs')
 ledger=json.loads((B/f'validation/evidence/ch{ch}.json').read_text())
 for claim in ledger['claims']:
  file=S/claim['source_path']
  if not required.issubset(claim) or claim['source_sha']!=SHA or not file.is_file() or not 1<=claim['line_start']<=claim['line_end']<=len(file.read_text().splitlines()):errors.append(f'ch{ch} invalid claim{claim.get("claim_id")}')
  if any(sha not in commits for sha in claim['associated_commits']):errors.append(f'ch{ch} unknown claim commit')
  if claim['validation']=='executed' and not (B/claim['evidence_log']).is_file():errors.append(f'ch{ch} missing executed evidence')
 if not (B/f'manuscript/solutions/ch{ch}.md').is_file():errors.append(f'ch{ch} missing solutions')
 chapters.append(dict(chapter=ch,words_excluding_fences_and_url_destinations=words,source_links=len(sources),excerpts=len(registry),claims=len(ledger['claims'])))
report=dict(source_sha=SHA,checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command='python3 books/inside-orch/scripts/check_chapters_01_08.py',scope='Batch-only structural/source/word/excerpt/hash verification. Semantic source review and actual named execution records remain distinct.',chapters=chapters,errors=errors,status='failed' if errors else 'passed')
(B/'validation/reviews/chapters-01-08.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(bool(errors))
