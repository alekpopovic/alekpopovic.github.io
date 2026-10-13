#!/usr/bin/env python3
"""Join canonical teaching additions to actual retained command evidence; execute no app mutation."""
from pathlib import Path
import ast,datetime,hashlib,json
B=Path(__file__).resolve().parents[1];SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];errors=[]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entries=json.loads((B/'validation/intake/lab-foundation-example-entries.json').read_text())['examples']
for e in entries:e['input_sha256']={p:h(B/p)for p in e['paths']};e['go_version']='1.25.0'if any(p.endswith('.go')for p in e['paths'])else None
mapping=[
('ch05-parser',['examples/teaching-extensions/ch05/check_manifests.py',*['examples/teaching-extensions/ch05/'+x.name for x in (B/'examples/teaching-extensions/ch05').glob('*.yaml')]],'validation/labs/ch05/parser-manifests.json','Actual CLI strict parser acceptance/rejection; no runtime deployment'),
('ch06-combined-restart',['examples/teaching-extensions/ch06/observe_container_restart.py'],'validation/labs/ch06/combined-restart-command.json','Fresh real binary plus manually associated owned Docker container; no claimed adoption'),
('ch07-public-contract',['examples/teaching-extensions/ch07/contract_test.go'],'validation/labs/ch07/public-contract-final.json','Actual in-process API and public client/lifecycle/error behavior; no TCP or daemon'),
('ch07-route-comparison',['examples/teaching-extensions/ch07/compare_routes.py'],'validation/labs/ch07/openapi-routes.json','Registered method/path versus OpenAPI structural comparison, not full semantic conformance'),
('ch08-cli',['examples/teaching-extensions/ch08/exercise_cli.py','examples/teaching-extensions/ch08/atlas_status.py'],'validation/labs/ch08/exact-cli-identities.json','Owned fresh binary endpoint and actual CLI identities; no Docker placement claim'),
('ch08-semantic-status',['examples/teaching-extensions/ch08/test_status.py','examples/teaching-extensions/ch08/atlas_status.py'],'validation/labs/ch08/status-semantics.json','Eight response semantic fixtures; no connected host'),
('ch33-adapter',['examples/teaching-extensions/ch33/adapter_contract_test.go'],'validation/labs/ch33/adapter-contract.json','FakeRuntime replay/cancellation plus proposed supplied-handshake validation; no external plugin protocol'),
('ch35-preflight',['examples/teaching-extensions/ch35/preflight_test.go'],'validation/labs/ch35/controlled-preflight-corrected.json','Actual unchanged Cobra decision with supplied version/node fixture; no cluster'),
('ch38-metrics',['examples/teaching-extensions/ch38/metrics_contract_test.go'],'validation/labs/ch38/failed-pull-emission.json','Actual adapter wrapper instrumentation and Prometheus exposition under FakeRuntime failure; no scrape server'),
('ch39-summary',['examples/teaching-extensions/ch39/summarize_benchmark.py'],'validation/examples/075-benchmark-summary.json','Mechanical summary of three retained bounded Plan benchmark samples; no new benchmark run'),
('ch40-dossier',['examples/teaching-extensions/ch40/verify_dossier.py'],'validation/labs/ch40/dossier-integrity-corrected.json','Checks actual evidence inventory integrity; never production readiness'),
('lab01-process',['scripts/observe_process_restart.py'],'validation/labs/review076/01-fresh-process-command.json','Actual fresh processes on owned ephemeral loopback ports; no Docker in this command'),
('lab01-docker',['examples/teaching-extensions/docker-boundary/main.go'],'validation/labs/review076/01-docker-flow-command.json','Guarded real Docker adapter/agent/API flow, captured exact IDs and cleanup; no Compose'),
('lab02',['examples/teaching-extensions/lab02/main.go','scripts/verify_scheduler_lab.py'],'validation/labs/review076/02-model-and-permutations.json','24 distinct node permutations/6candidates plus separate actual concurrent claim tests; no SQL in this command'),
('lab03',['examples/teaching-extensions/lab03/agent_contract_test.go','examples/teaching-extensions/lab03/reconciler_contract_test.go','scripts/run_drift_lab.py'],'validation/labs/review076/03-command.json','15 actual FakeRuntime/MemoryService/reconciler cases; expected rejection preserved; no daemon'),
('lab04',['examples/teaching-extensions/rollout/main.go','scripts/verify_rollout_security_labs.py'],'validation/labs/review076/04-command.json','Actual controller/memory fixtures7checkpoints and pending-stop success boundary; no daemon'),
('lab05',['examples/teaching-extensions/security/main.go'],'validation/labs/review076/05-command.json','Actual in-process API plus owned local probes and synthetic canary; no external service'),
('lab08-store',['examples/teaching-extensions/full-schema/main.go','scripts/observe_database_recovery.py'],'validation/labs/review076/08-recovery-command.json','Owned PostgreSQL16migrations/restore/canary/advisory lock boundary; no default binary persistence'),
('review-published-cron',['examples/teaching-extensions/review-interfaces/cron_manifest_test.go','examples/teaching-extensions/review-interfaces/published-cron.yaml'],'validation/examples/published-cron-manifest.json','Actual published Chapter31 YAML through unchanged Cobra parser into captured CronJobClient; no server/jobs/Docker'),
]
for id,paths,record,scope in mapping:
 r=json.loads((B/record).read_text());status='passed'if r.get('exit_code')==0 else r.get('status','unknown');
 if status!='passed':errors.append('Not observed successful '+record)
 entries.append(dict(id=id,classification='teaching extension',source_sha=SHA,paths=paths,input_sha256={p:h(B/p)for p in paths},command=r['command'],cwd=r['cwd'],evidence_log=record,status=status,scope=scope,validation_target=record,go_version='1.25.0'if any(p.endswith('.go')for p in paths)else None))
# Add current fresh records for the lab agent programs without misrepresenting earlier evidence.
for e,record in [(x,'validation/labs/review076/'+('06'if x['id']=='lab06'else'07')+'-command.json')for x in entries if x['id']in ['lab06','lab07']]:
 r=json.loads((B/record).read_text());assert r['exit_code']==0;e.update(command=r['command'],cwd=r['cwd'],evidence_log=record,validation_target=record)
# Diagram generation is checked in an isolated output tree by the075 utility test.
entries.append(dict(id='task-lifecycle-diagram',classification='teaching extension',source_sha=SHA,paths=['examples/diagrams/generate_task_lifecycle.py','examples/diagrams/task-lifecycle.svg','examples/diagrams/task-lifecycle.png','examples/diagrams/task-lifecycle.json'],input_sha256={str(p.relative_to(B)):h(p)for p in (B/'examples/diagrams').iterdir()if p.is_file()},command=['python3','books/inside-orch/scripts/check_example_utilities.py'],cwd=str(B.parents[1]),evidence_log='validation/examples/075-utilities.json',status='passed',scope='Isolated deterministic SVG regeneration equality; PNG viewed separately, no runtime guarantee',validation_target='validation/examples/075-utilities.json'))
entries.append(dict(id='ch34-ha-adr',classification='design only',source_sha=SHA,paths=['examples/teaching-extensions/ch34/ADR-durable-composition.md'],input_sha256={'examples/teaching-extensions/ch34/ADR-durable-composition.md':h(B/'examples/teaching-extensions/ch34/ADR-durable-composition.md')},status='inspected',validation_target=None,scope='Proposed durable composition, not runnable code or shipped capability'))
registered={p for e in entries for p in e['paths']};canonical={str(p.relative_to(B))for p in (B/'examples/teaching-extensions').rglob('*')if p.is_file()and p.suffix in ['.go','.py','.yaml']}
missing=canonical-registered
if missing:errors.append('Unregistered canonical additions: '+str(sorted(missing)))
for e in entries:
 for p in e['paths']:
  if p.endswith('.py'):ast.parse((B/p).read_text(),filename=p)
 r=e.get('evidence_log')
 if r and not(B/r).is_file():errors.append('Missing evidence '+r)
 elif r:
  actual=json.loads((B/r).read_text())
  if actual.get('exit_code')!=0:errors.append('Evidence is not an actual success '+r)
  for key in ['stdout','stderr']:
   if isinstance(actual.get(key),str)and not(B/actual[key]).is_file():errors.append('Missing raw log '+actual[key])
result=dict(schema_version=1,source_sha=SHA,checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),examples=entries,errors=errors,note='Complete original additions registry. Exact source fragments have separate registry/index; optional reader procedures remain expected-only. Canonical hashes frozen here; actual commands retain precise runtime scope.');(B/'examples/manifest.json').write_text(json.dumps(result,indent=2)+'\n')
index=json.loads((B/'validation/excerpts/index.json').read_text());out=dict(result,blocks=index['all_blocks'],matrix_scope='All formal manuscript, lab, example guide and inside-orch post fenced blocks.80exact/historical fragments use containing package context; original runnable additions each have actual execution target. Optional shell procedures have syntax validation and expected-only operational scope.');(B/'validation/examples/manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'registered_examples':len(entries),'canonical_program_fixture_files':len(canonical),'blocks':len(index['all_blocks']),'errors':errors}));raise SystemExit(bool(errors))
