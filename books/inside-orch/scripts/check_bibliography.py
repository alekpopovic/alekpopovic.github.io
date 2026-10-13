#!/usr/bin/env python3
"""Resolve final formal manuscript citations to precise bibliography entries."""
from pathlib import Path
import json,re,hashlib,datetime,subprocess,urllib.parse,argparse
p=argparse.ArgumentParser();p.add_argument('--git-dir');a=p.parse_args();B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';lock=json.loads((B/'evidence/source-lock.json').read_text());SHA=lock['baseline_sha'];data=json.loads((B/'reference/bibliography.json').read_text());entries=[x for x in data['entries'] if x.get('evidence_class')=='primary external context, not Orch implementation evidence'];by_url={urllib.parse.urldefrag(x['url'])[0]:x for x in entries};known_commits={x['sha'] for x in json.loads((B/'evidence/commits.json').read_text())};citations=[];errors=[];pending=[];historical_checks=0
for file in sorted((B/'manuscript').rglob('*.md')):
 text=re.sub(r'```.*?```','',file.read_text(),flags=re.S)
 for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',text):
  label,url=m.groups();base,fragment=urllib.parse.urldefrag(url);row=by_url.get(base)
  match=re.match(r'https://github.com/alekpopovic/orch/(blob|commit)/([a-f0-9]{40})(?:/(.*))?$',base)
  if match:
   kind,sha,path=match.groups()
   if sha not in known_commits:errors.append('unknown source commit '+sha)
   if kind=='blob':
    if sha==SHA:
     f=S/path
     if not f.is_file():errors.append('missing baseline source '+path)
     line=re.match(r'L(\d+)(?:-L(\d+))?',fragment)
     if line and f.is_file() and (int(line[1])<1 or int(line[2] or line[1])>len(f.read_text().splitlines())):errors.append('invalid source interval '+url)
    elif a.git_dir:
     r=subprocess.run(['git','--git-dir='+a.git_dir,'cat-file','-e',sha+':'+path],capture_output=True)
     historical_checks+=1
     if r.returncode:errors.append('missing historical blob '+base)
    else:pending.append('Historical object not locally rechecked: '+base)
   if row is None:
    row={'id':'source-'+hashlib.sha256(base.encode()).hexdigest()[:16],'title':path if kind=='blob' else 'Orch commit '+sha,'authors_or_owner':'alekpopovic/orch repository contributors','version':sha,'url':base,'group':'Source code/history','annotation':'Immutable source object cited in this edition; interpret baseline implementation and historical context separately.','accessed_at':'2026-10-13','url_outcome':'Actual local source bytes or historical Git object verified; HTTP fetch not required.','evidence_class':'repository source evidence'};entries.append(row);by_url[base]=row
  elif row is None:
   row={'id':'external-'+hashlib.sha256(base.encode()).hexdigest()[:16],'title':label,'authors_or_owner':urllib.parse.urlsplit(base).netloc,'version':'Unversioned; not independently accessed in this bibliography pass','url':base,'group':'Unresolved external references','annotation':'Formal manuscript link retained with explicit unresolved access; no technical behavior inferred.','accessed_at':None,'url_outcome':'unresolved: URL not among the eight actually retrieved primary sources','evidence_class':'unresolved external context'};entries.append(row);by_url[base]=row
  citations.append({'manuscript_path':str(file.relative_to(B)),'label':label,'url':url,'bibliography_id':row['id']})
gloss=json.loads((B/'reference/glossary.json').read_text())['terms'];ids={x['id'] for x in gloss}
if len(gloss)<60:errors.append('fewer than60 glossary terms')
if len(ids)!=len(gloss):errors.append('duplicate glossary IDs')
for x in gloss:
 if not (B/x['chapter_path']).is_file():pending.append('Glossary chapter not finalized '+x['chapter_id'])
 if any(r not in ids for r in x['related']):errors.append('dangling glossary relationship '+x['id'])
 if x['definition'].strip().lower()==x['term'].strip().lower():errors.append('circular undefined term '+x['id'])
 if x['source'].split('/'+SHA+'/',1)[-1] not in {f['path'] for f in lock['files']}:errors.append('glossary source outside inventory '+x['id'])
for x in entries:
 for field in ['id','title','authors_or_owner','version','url','group','annotation','url_outcome','evidence_class']:
  if not x.get(field):errors.append('bibliography missing '+field+' '+x.get('id','unknown'))
data.update(entries=entries,citations=citations,repository_entries='Explicit expanded entries with full immutable URLs; no wildcard citation resolution.',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(B/'reference/bibliography.json').write_text(json.dumps(data,indent=2)+'\n');report={'source_sha':SHA,'command':'python3 books/inside-orch/scripts/check_bibliography.py'+(' --git-dir '+a.git_dir if a.git_dir else ''),'glossary_count':len(gloss),'glossary_duplicate_ids':len(gloss)-len(ids),'bibliography_entries':len(entries),'citations_resolved':len(citations),'historical_blob_checks':historical_checks,'external_access_outcomes':data['access_outcomes'],'unresolved_external':[x for x in entries if x['evidence_class']=='unresolved external context'],'errors':errors,'pending_dependencies':sorted(set(pending)),'scope':'Formal Markdown citations, immutable source/commit membership and term links. External page retrieval recorded separately; no claim that a reachable URL proves behavior.','status':'failed' if errors else 'review_needed' if pending else 'passed'};(B/'validation/065-reference-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['glossary_count','bibliography_entries','citations_resolved','historical_blob_checks','errors','pending_dependencies','status']}));print(json.dumps({'unresolved_external_urls':[x['url'] for x in report['unresolved_external']]}));raise SystemExit(bool(errors))
