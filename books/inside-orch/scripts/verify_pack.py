#!/usr/bin/env python3
"""Validate the shipped corpus and workflow structure, not engineering claims."""
from pathlib import Path
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def require(value,message):
    if not value: errors.append(message)
def main():
    lock=json.loads((ROOT/'evidence/source-lock.json').read_text())
    commits=json.loads((ROOT/'evidence/commits.json').read_text())
    known={x['sha'] for x in commits}
    require(len(commits)==105,'Commit count differs from the inspected edition')
    require(lock['baseline_sha'] in known,'Baseline absent from commit corpus')
    site=json.loads((ROOT/'evidence/site-lock.json').read_text())
    require(site['repository']=='https://github.com/alekpopovic/alekpopovic.github.io','Incorrect execution repository')
    require(site['book_root']=='books/inside-orch' and site['total_sections']==47,'Incorrect native site contract')
    for sf in site['files']:
        sp=ROOT/'evidence/site'/sf['path']
        require(sp.is_file(),'Missing site-contract source '+sf['path'])
        if sp.is_file():require(hashlib.sha256(sp.read_bytes()).hexdigest()==sf['sha256'],'Changed site-contract source '+sf['path'])
    checked=0
    for f in lock['files']:
        p=ROOT/'evidence/orch'/f['path']
        require(p.is_file(),'Missing source: '+f['path'])
        if p.is_file():
            raw=p.read_bytes();checked+=1
            require(len(raw)==f['bytes'],'Changed source size: '+f['path'])
            require(hashlib.sha256(raw).hexdigest()==f['sha256'],'Changed source hash: '+f['path'])
    prompts=sorted((ROOT/'prompts').glob('[0-9][0-9][0-9]-*.md'))
    ids=[int(p.name[:3]) for p in prompts]
    require(ids==list(range(100)),'Expected unique sequential prompts 000–099')
    outline=json.loads((ROOT/'editorial/book-outline.json').read_text())
    require([c['id'] for c in outline['chapters']]==[f'{n:02}' for n in range(1,41)],'Expected chapters 01–40')
    require([a['id'] for a in outline['appendices']]==list('ABCDEF'),'Expected appendices A–F')
    mapping=json.loads((ROOT/'evidence/prompt-commit-map.json').read_text())['mapping']
    require([int(x['prompt_id']) for x in mapping]==list(range(91)),'Expected development prompt map 00–90')
    for x in mapping:
        require(x['commit_sha'] in known,'Unknown mapped commit: '+x['commit_sha'])
        p=ROOT/'evidence/orch'/x['path']
        require(p.exists(),'Missing original prompt: '+x['path'])
        if p.exists():require(hashlib.sha256(p.read_bytes()).hexdigest()==x['prompt_sha256'],'Original prompt checksum mismatch: '+x['path'])
        require((ROOT/'evidence/commit-diffs'/(x['commit_sha']+'.patch')).exists(),'Missing diff for mapped commit')
    require(set(n for c in outline['chapters'] for n in c['original_prompts'])==set(range(91)),'Chapter map misses an original prompt')
    links=0
    for p in prompts:
        body=p.read_text()
        require(len(body.split())>=300,'Prompt unexpectedly short: '+p.name)
        require('BOOK_SPEC.md' in body and 'source-lock.json' in body,'Missing execution contract: '+p.name)
        require('execution-tracker.csv' in body,'Missing progress rule: '+p.name)
        require('## Mandatory execution context' in body and 'alekpopovic.github.io' in body and 'books/inside-orch/' in body,'Missing site-root execution binding: '+p.name)
        for sha,rel in re.findall(r'https://github\.com/alekpopovic/orch/blob/([0-9a-f]{40})/([^\s)\]>]+)',body):
            links+=1
            require(sha in known,'Unknown source SHA in '+p.name)
            rel=rel.split('#')[0]
            if sha==lock['baseline_sha']:
                require((ROOT/'evidence/orch'/rel).is_file(),'Bad baseline source link '+rel+' in '+p.name)
        for sha in re.findall(r'https://github\.com/alekpopovic/orch/commit/([0-9a-f]{40})',body):
            links+=1;require(sha in known,'Unknown commit link in '+p.name)
        require(not re.search(r'/orch/blob/(main|master)/',body),'Moving source link in '+p.name)
    index=json.loads((ROOT/'state/prompt-index.json').read_text())
    require(len(index)==100,'Prompt index count mismatch')
    for item in index:require((ROOT/item['path']).is_file(),'Prompt index missing '+item['path'])
    order=(ROOT/'manuscript/Book.txt').read_text().splitlines()
    require(len(order)==47 and len(set(order))==47 and order[0]=='00-preface.md','Incorrect 47-section reading order')
    result={'status':'failed' if errors else 'passed','scope':'Corpus integrity and workflow structure only; website/application/labs/manuscript not executed','source_sha':lock['baseline_sha'],'site_sha':site['baseline_sha'],'source_files_checked':checked,'site_contract_files_checked':len(site['files']),'book_prompts_checked':len(prompts),'original_prompts_mapped':len(mapping),'commits_checked':len(commits),'chapters':len(outline['chapters']),'appendices':len(outline['appendices']),'planned_reader_sections':len(order),'immutable_links_checked':links,'errors':errors}
    print(json.dumps(result,indent=2))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
