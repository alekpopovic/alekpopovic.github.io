#!/usr/bin/env python3
"""Structural readiness gate. Missing manuscript is expected in a new pack."""
from pathlib import Path
import argparse,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--strict',action='store_true');args=parser.parse_args()
outline=json.loads((ROOT/'editorial/book-outline.json').read_text());errors=[];warnings=[];words=0
required={'claim_id','statement','classification','source_path','source_sha','line_start','line_end','associated_commits','validation','evidence_log','limitations'}
classifications={'runtime-integrated','implemented package','partial integration','design only','teaching extension','future work'}
statuses={'expected_only','inspected','executed','blocked'}
if not (ROOT/'manuscript/00-preface.md').is_file():errors.append('Missing canonical preface')
for ch in outline['chapters']:
    path=ROOT/ch['chapter_path']
    if not path.is_file():errors.append('Missing chapter '+ch['id']);continue
    text=path.read_text();prose=re.sub(r'```.*?```','',text,flags=re.S)
    expected=f"# Chapter {int(ch['id'])} - {ch['title']}"
    if next((line for line in text.splitlines() if line.startswith('# ')),'')!=expected:errors.append('Incorrect native chapter H1 '+ch['id'])
    count=len(re.findall(r'\b[\w-]+\b',prose));words+=count
    if count<1800:errors.append(f"Chapter {ch['id']} has only {count} approximate narrative words")
    if len(re.findall(r'^```',text,re.M))%2:errors.append('Unclosed code fence: '+ch['id'])
    if re.search(r'https://github\.com/alekpopovic/orch/blob/(main|master)/',text):errors.append('Moving source link: '+ch['id'])
    if re.search(r'\b(TODO|TBD|PLACEHOLDER)\b',prose):errors.append('Unresolved draft placeholder: '+ch['id'])
    ep=ROOT/f"validation/evidence/ch{ch['id']}.json"
    if not ep.exists():errors.append('Missing claim ledger '+ch['id'])
    else:
        try:
            records=json.loads(ep.read_text());records=records.get('claims',[]) if isinstance(records,dict) else records
            if not isinstance(records,list) or not records:raise ValueError('No claims')
            for r in records:
                if not required.issubset(r):errors.append('Incomplete claim '+str(r.get('claim_id')))
                if r.get('classification') not in classifications or r.get('validation') not in statuses:errors.append('Invalid claim classification/status')
                if r.get('validation')=='executed' and not r.get('evidence_log'):errors.append('Executed claim lacks a log')
        except (ValueError,TypeError):errors.append('Invalid claim ledger '+ch['id'])
    if not (ROOT/f"manuscript/solutions/ch{ch['id']}.md").exists():errors.append('Missing solutions '+ch['id'])
for ap in outline['appendices']:
    if not (ROOT/ap['appendix_path']).is_file():errors.append('Missing appendix '+ap['id'])
    else:
        atext=(ROOT/ap['appendix_path']).read_text()
        if next((line for line in atext.splitlines() if line.startswith('# ')),'')!=f"# Appendix {ap['id']} - {ap['title']}":errors.append('Incorrect native appendix H1 '+ap['id'])
for n in range(1,9):
    if not list((ROOT/'labs').glob(f'{n:02d}-*/README.md')):errors.append(f'Missing lab {n:02d}')
if not (ROOT/'validation/RELEASE_GATE.md').exists():warnings.append('Final human/execution/publication gate not yet present')
print(json.dumps({'status':'incomplete' if errors else 'structure_ready','scope':'Structural only; source truth, actual experiments and visual publication review remain separate gates','approximate_narrative_words':words,'errors':errors,'warnings':warnings},indent=2))
sys.exit(1 if args.strict and errors else 0)
