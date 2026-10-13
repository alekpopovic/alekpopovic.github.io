#!/usr/bin/env python3
"""Verify the book's exported history against explicitly supplied Git objects."""
from pathlib import Path
import argparse,subprocess,json,re,csv,hashlib,datetime
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);a=p.parse_args();B=Path(__file__).resolve().parents[1];SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];U='https://github.com/alekpopovic/orch/';G=['git','--git-dir='+a.git_dir]
def git(*args):return subprocess.run(G+list(args),capture_output=True,check=True).stdout.decode()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();tree=git('rev-parse',SHA+'^{tree}').strip();shas=git('rev-list','--reverse','--topo-order',SHA).splitlines();exported=json.loads((B/'evidence/commits.json').read_text());expected={c['sha'] for c in exported};errors=[];commits=[]
for sha in shas:
 parts=git('show','-s','--format=%H%x00%P%x00%aI%x00%cI%x00%s%x00%an',sha).strip().split('\0');paths=git('diff-tree','--root','--no-commit-id','--name-only','-r','-m',sha).splitlines();commits.append({'sha':sha,'parents':parts[1].split(),'authored_at':parts[2],'committed_at':parts[3],'subject':parts[4],'author_name':parts[5],'changed_paths':sorted(set(paths)),'url':U+'commit/'+sha})
 for parent in parts[1].split():
  if parent not in set(shas):errors.append('parent outside reachable set '+parent)
if set(shas)!=expected:errors.append('Git/exported reachable sets differ')
if len(shas)!=105:errors.append('expected105 reachable commits')
originals=json.loads((B/'evidence/original-prompts.json').read_text());mappings=json.loads((B/'evidence/prompt-commit-map.json').read_text())['mapping'];outline=json.loads((B/'editorial/book-outline.json').read_text())['chapters'];prompts=[];unresolved=[]
for original in originals:
 ident=original['id'];path=original['path'];mapping=next(x for x in mappings if int(x['prompt_id'])==ident);adds=git('log','--reverse','--topo-order','--format=%H','--diff-filter=A',SHA,'--',path).splitlines();first=adds[0] if adds else None
 if not first:errors.append('no first-containing addition '+path)
 else:git('cat-file','-e',first+':'+path)
 associations=[]
 for sha in [mapping['commit_sha']]:
  paths=[]
  for historical_path in mapping['evidence_paths']:
   try:git('cat-file','-e',sha+':'+historical_path);paths.append(historical_path)
   except subprocess.CalledProcessError:errors.append('missing historical path '+sha+':'+historical_path)
  design=ident in [54,56,63,68,69,72,75,77,79];grade='partial relationship' if design else 'strong path/diff correspondence';associations.append({'sha':sha,'grade':grade,'paths':paths,'note':mapping['note'],'causality':'Topical source association, not a transcript proving this prompt executed.'})
 chapter_ids=[c['id'] for c in outline if ident in c['original_prompts']];prompts.append({'id':f'{ident:02d}','filename':path,'immutable_blob_link':original['source_url'],'first_containing_commit':first,'first_containing_blob_oid':git('rev-parse',first+':'+path).strip() if first else None,'addition_commits':adds,'thematic_chapters':chapter_ids,'associations':associations,'scope':'Addition commit establishes file presence. Earlier implementation association may predate prompt text.'})
 if grade=='partial relationship':unresolved.append({'id':f'{ident:02d}','missing_evidence':'Design file/path correspondence exists, but no prompt execution transcript or complete runtime wiring establishes delivery of the requested architecture.'})
if [int(x['id']) for x in prompts]!=list(range(91)):errors.append('prompt IDs are not00–90 exactly once')
# Twelve checkpoints, with historical bytes retrieved from the corresponding object.
selected=[(1,'cmd/orch-server/main.go','func run'),(2,'pkg/types/types.go','type ServiceSpec'),(3,'internal/store/postgres.go','func NewPostgresStore'),(7,'internal/agent/agent.go','func (r *Runner) Run'),(9,'internal/scheduler/scheduler.go','func (s *Scheduler) RunOnce'),(10,'internal/reconciler/reconciler.go','func (r *Reconciler) ReconcileOnce'),(14,'internal/rollout/rollout.go','func (c *Controller) RunOnce'),(19,'internal/auth/agent.go','func NewTokenAgentCredentialIssuer'),(66,'internal/gitops/gitops.go','func (controller *Controller) Sync'),(73,'internal/controlplane/workloads.go','func (s *MemoryService) CreateJob'),(81,'internal/maintenance/maintenance.go','func Validate'),(None,'README.md','#')]
snippets=[]
for n,path,needle in selected:
 sha=SHA if n is None else next(x for x in mappings if int(x['prompt_id'])==n)['commit_sha'];raw=git('show',sha+':'+path);lines=raw.splitlines();matches=[i for i,l in enumerate(lines) if needle in l];idx=matches[0] if matches else next((i for i,l in enumerate(lines) if l.startswith(('func ','type '))),0);end=min(idx+6,len(lines));excerpt='\n'.join(lines[idx:end])+'\n';oid=git('rev-parse',sha+':'+path).strip();snippets.append({'checkpoint':len(snippets)+1,'prompt_association':n,'commit_sha':sha,'historical_path':path,'source_object_oid':oid,'line_start':idx+1,'line_end':end,'exact_excerpt':excerpt,'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),'source_url':U+'blob/'+sha+'/'+path+f'#L{idx+1}-L{end}','symbol_selection':needle,'selection_fallback':not bool(matches),'scope':'Historical Git object content, not present-day code shown as earlier.'})
report={'source_sha':SHA,'tree_sha':tree,'count_definitions':{'commits':'All commits reachable from locked SHA, including merged side parents; not only first-parent history.','prompts':'Committed source prompts with distinct numeric filename prefixes00–90; book prompts000–099 are a separate workflow.','first_containing':'Earliest topological addition returned by Git log --diff-filter=A; blob existence checked in that commit.'},'commits':commits,'prompts':prompts,'checkpoints':snippets,'unresolved_causality':unresolved,'scope':'Exact source objects and topical correspondence, not execution transcripts.'};(B/'reference/history.json').write_text(json.dumps(report,indent=2)+'\n');(B/'validation/history-snippets.json').write_text(json.dumps({'source_sha':SHA,'snippets':snippets},indent=2)+'\n')
with (B/'reference/prompt-commit-map.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['prompt_id','filename','immutable_blob_link','first_containing_commit','associated_commit','evidence_grade','thematic_chapters'])
 for row in prompts:
  for association in row['associations']:w.writerow([row['id'],row['filename'],row['immutable_blob_link'],row['first_containing_commit'],association['sha'],association['grade'],','.join(row['thematic_chapters'])])
validation={'command':G+['rev-list','--reverse','--topo-order',SHA],'cwd':str(Path.cwd()),'source_sha':SHA,'started_at_utc':start,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':0 if not errors else 1,'observed_commits':len(commits),'observed_prompts':len(prompts),'parent_completeness':not any('parent ' in x for x in errors),'duplicates':len(shas)-len(set(shas)),'missing_numbers':sorted(set(range(91))-{int(r['id']) for r in prompts}),'historical_paths_checked':sum(len(a['paths']) for p in prompts for a in p['associations']),'historical_snippets':len(snippets),'exported_set_matches':set(shas)==expected,'tree_matches_lock':tree==json.loads((B/'evidence/source-lock.json').read_text())['tree_sha'],'immutable_permalinks':'Full SHA and actual blob existence verified locally; HTTP status not required for Git objects.','errors':errors};(B/'validation/062-history-check.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation));raise SystemExit(bool(errors))
