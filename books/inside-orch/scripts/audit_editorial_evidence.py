#!/usr/bin/env python3
"""Offline evidence/schema, reader exercise navigation and sensitive-material inventory."""
from pathlib import Path
import json,re,hashlib,datetime,subprocess,argparse
p=argparse.ArgumentParser();p.add_argument('--git-dir');a=p.parse_args();B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();errors=[];pending=[];claims=[];reviewed=[]
known={x['sha'] for x in json.loads((B/'evidence/commits.json').read_text())};schema=['claim_id','statement','classification','source_path','source_sha','line_start','line_end','associated_commits','validation','evidence_log','limitations'];classes={'runtime-integrated','implemented package','partial integration','design only','teaching extension','future work'}
for f in sorted((B/'validation/evidence').glob('*.json')):
 d=json.loads(f.read_text())
 for c in d.get('claims',[]):
  for k in schema:
   if k not in c:errors.append(str(f.relative_to(B))+':missing '+k)
  if c.get('classification')not in classes or c.get('validation')not in {'expected_only','inspected','executed','blocked'}:errors.append(c.get('claim_id','?')+' invalid labels')
  if c.get('source_sha')not in known:errors.append(c['claim_id']+' unknown SHA')
  if c['source_sha']==SHA:
   source=S/c['source_path']
   if not source.exists():errors.append(c['claim_id']+' unknown source')
   elif not 1<=c['line_start']<=c['line_end']<=len(source.read_text().splitlines()):errors.append(c['claim_id']+' invalid lines')
  elif a.git_dir:
   r=subprocess.run(['git','--git-dir='+a.git_dir,'show',c['source_sha']+':'+c['source_path']],capture_output=True,text=True)
   if r.returncode or c['line_end']>len(r.stdout.splitlines()):errors.append(c['claim_id']+' invalid historical source interval')
  else:pending.append(c['claim_id']+' historical object not rechecked')
  if any(sha not in known for sha in c['associated_commits']):errors.append(c['claim_id']+' unknown associated history')
  if c['validation']=='executed' and (not c['evidence_log'] or not(B/c['evidence_log']).is_file()):errors.append(c['claim_id']+' missing execution record')
  claims.append(dict(c,record_path=str(f.relative_to(B))))
ids=[c['claim_id'] for c in claims]
if len(ids)!=len(set(ids)):errors.append('duplicate claim IDs')
exercises=[];independent=[n for n in range(1,41) if n not in range(17,25)]
for n in range(1,41):
 files=list((B/'manuscript/chapters').glob(f'{n:02d}-*.md'));answer=B/f'manuscript/solutions/ch{n:02d}.md'
 if len(files)!=1 or not answer.exists():pending.append(f'chapter{n:02d} or answers unavailable');continue
 f=files[0];text=f.read_text();solution=answer.read_text();section=text.split('## Exercises',1)[-1];questions=re.findall(r'^(\d+)\. (.+)$',section,re.M);answers=re.findall(r'^## (\d+)\. (.+)$',solution,re.M)
 if not 3<=len(questions)<=5 or {q[0]for q in questions}!={q[0]for q in answers}:errors.append(f'chapter{n:02d} question/answer mismatch')
 if '../solutions/ch'+f'{n:02d}'+'.md'not in section:errors.append(f'chapter{n:02d} missing answer navigation')
 if '../chapters/'+f.name not in solution:errors.append(f'chapter{n:02d} missing reciprocal chapter navigation')
 for ident,question in questions:exercises.append({'exercise_id':f'ch{n:02d}.ex{ident}','chapter_path':str(f.relative_to(B)),'question':question,'solution_path':str(answer.relative_to(B)),'answer_heading':next((h for i,h in answers if i==ident),None),'verification':'independent source/argument review' if n in independent else 'author review; independent cross-review delegated to source_foundation','evidence_record':'validation/reviews/exercises-solutions.json'})
 reviewed.append({'path':str(f.relative_to(B)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'independence':n in independent})
# Scan authored and captured text. Do not copy matched values into this report.
patterns={'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----','github_token':r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}','aws_access_key':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b','jwt_literal':r'\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\b','private_author_email':r'(?i)\balek(?:sandar)?[._-]?popovic[^\s@]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'};hits=[];scanned=[]
for tree in ['manuscript','examples','validation','reference','publication','runbooks','exercises']:
 for f in sorted((B/tree).rglob('*')):
  if not f.is_file() or f.suffix.lower()not in{'.md','.json','.jsonl','.txt','.go','.py','.yaml','.yml','.html','.csv','.sh','.svg'} or f.name=='redaction-scan.json':continue
  text=f.read_text(errors='replace');scanned.append(str(f.relative_to(B)))
  for typ,pattern in patterns.items():
   for m in re.finditer(pattern,text):hits.append({'path':str(f.relative_to(B)),'line':text[:m.start()].count('\n')+1,'pattern':typ,'value':'omitted from report'})
finish=datetime.datetime.now(datetime.timezone.utc).isoformat();record={'source_sha':SHA,'command':'python3 books/inside-orch/scripts/audit_editorial_evidence.py'+(' --git-dir '+a.git_dir if a.git_dir else ''),'cwd':str(B.parents[1]),'prerequisites':['Python3','locked source bytes']+(['local historical Git objects']if a.git_dir else []),'started_at_utc':start,'finished_at_utc':finish,'exit_code':int(bool(errors)),'claims':len(claims),'reviewed_paths':reviewed,'errors':errors,'pending_dependencies':pending,'status':'failed'if errors else'review_needed'if pending else'passed'}
(B/'validation/claims/index.json').write_text(json.dumps({'source_sha':SHA,'claims':claims,'scope':'Explicit technical claim records plus detailed appendix inventories with individual source provenance; citation presence is not semantic certification.','appendix_detail_inventories':['reference/cli-api-config.json','reference/lifecycle.json','reference/invariants.json','reference/history.json','exercises/catalog.json','reference/measurement-contracts.json','reference/glossary.json','reference/bibliography.json']},indent=2)+'\n')
(B/'validation/exercises/index.json').write_text(json.dumps({'source_sha':SHA,'chapter_exercises':exercises,'additional_practice_catalog':'exercises/catalog.json','independent_chapters':independent,'author_chapters_require_cross_review':list(range(17,25)),'appendix_d_independent_review':'delegated to source_foundation; not self-certified','actual_offline_checks':'validation/exercises/offline-runs.json','specified_incorrect_behavior_rejection':'validation/exercises/mutation-runs.json','pending_dependencies':pending},indent=2)+'\n')
(B/'validation/security/redaction-scan.json').write_text(json.dumps({'source_sha':SHA,'command':record['command'],'cwd':record['cwd'],'prerequisites':['Python3','authored and captured text'],'started_at_utc':start,'finished_at_utc':finish,'exit_code':int(bool(hits)),'scanned_files':len(scanned),'patterns':list(patterns),'findings':hits,'limitations':['Static high-signal pattern scan is not a proof arbitrary passwords or canaries cannot appear.','Manual source-to-channel review separately traces authorized plaintext and synthetic fixture use.','Immutable source corpus excluded from mutation; output records never include matched sensitive values.'],'status':'review_needed'if hits else'passed'},indent=2)+'\n')
(B/'validation/reviews/editorial-evidence-audit.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'claims':len(claims),'chapter_exercises':len(exercises),'redaction_files':len(scanned),'high_signal_hits':len(hits),'errors':errors,'pending':pending}));raise SystemExit(bool(errors))
