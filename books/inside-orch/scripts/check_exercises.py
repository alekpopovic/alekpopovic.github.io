#!/usr/bin/env python3
from pathlib import Path
import json,collections,datetime,copy,re
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';D=json.loads((B/'exercises/catalog.json').read_text());entries=D['exercises'];errors=[];pending=[];ids=[x['id'] for x in entries];counts=collections.Counter(x['audience'] for x in entries);negative=[]
if len(ids)!=24 or len(set(ids))!=24:errors.append('expected24 unique exercises')
if counts!={'developer':8,'devops':8,'architect':8}:errors.append('audience counts differ')
for x in entries:
 for k in ['prerequisites','estimated_minutes','source','question','required_artifact','rubric','hints','worked_solution','chapter_ids']:
  if not x.get(k):errors.append(x['id']+' missing '+k)
 if not (S/x['source']['path']).is_file():errors.append(x['id']+' unknown source')
 if sum(r['points'] for r in x['rubric'])!=6:errors.append(x['id']+' rubric mismatch')
 if x['executable']:
  expected=x['expected_artifact'];wrong=copy.deepcopy(expected);key=next(iter(wrong));wrong[key]=not wrong[key] if isinstance(wrong[key],bool) else wrong[key]+1 if isinstance(wrong[key],int) else 'specified wrong outcome'
  grade=lambda artifact:artifact==expected
  negative.append({'id':x['id'],'expected_artifact':expected,'specified_incorrect_artifact':wrong,'reference_accepted':grade(expected),'incorrect_rejected':not grade(wrong),'scope':'Artifact grading discrimination only; upstream test assertions separately inspected and actually executed.'})
 if x['executable'] and (not x.get('trace',{}).get('initial_state') or not x.get('trace',{}).get('expected_transition_sequence')):errors.append(x['id']+' missing serialized trace')
 for c in x['chapter_ids']:
  if not any((B/'manuscript/chapters').glob(c+'-*.md')):pending.append('chapter'+c+' not finalized')
sol=(B/'manuscript/solutions/appendix-d.md').read_text()
for ident in ids:
 if '\n## '+ident+'\n' not in sol:errors.append('missing worked solution '+ident)
chapter_answers=[]
for n in range(1,41):
 p=B/f'manuscript/solutions/ch{n:02d}.md';chapter_answers.append({'chapter_id':f'{n:02d}','exists':p.is_file()})
 if not p.is_file():pending.append(f'chapter{n:02d} worked answers not finalized')
runs=json.loads((B/'validation/exercises/offline-runs.json').read_text());run_ids={x['id'] for x in runs['runs']}
if run_ids!={x['id'] for x in entries if x['executable']}:errors.append('offline run coverage mismatch')
if not runs['all_passed']:errors.append('offline execution failed')
mutants=json.loads((B/'validation/exercises/mutation-runs.json').read_text())
if not mutants['all_rejected'] or {x['id'] for x in mutants['runs']}!=run_ids:errors.append('specified incorrect implementation behavior not rejected')
report={'source_sha':D['source_sha'],'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python3 books/inside-orch/scripts/check_exercises.py','unique_ids':len(set(ids)),'audience_counts':dict(counts),'executable_entries':len(negative),'actual_tests':'validation/exercises/offline-runs.json','actual_mutant_rejection':'validation/exercises/mutation-runs.json','grading_checks':negative,'chapter_answers':chapter_answers,'questions_second_pass':'Source author reread stated prerequisites and corrected chapter mappings; independent review belongs to prompt084. No independent-review claim here.','scope':'Catalog/link/serialized-trace checks plus eight actual offline baseline tests and eight specified implementation mutations rejected by those tests; no Docker/DB or exhaustive mutation claim.','errors':errors,'pending_dependencies':sorted(set(pending)),'status':'failed' if errors else 'review_needed' if pending else 'passed'};(B/'validation/063-exercise-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['unique_ids','audience_counts','executable_entries','errors','pending_dependencies','status']}));raise SystemExit(bool(errors))
