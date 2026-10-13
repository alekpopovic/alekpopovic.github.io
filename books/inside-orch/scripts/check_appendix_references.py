#!/usr/bin/env python3
"""Recheck source inventories, lifecycle matrices and operational references offline."""
from pathlib import Path
import json,re,datetime,hashlib
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';load=lambda p:json.loads((B/p).read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();errors=[]
A=load('reference/cli-api-config.json');actual=load('validation/reference-offline-inventory.stdout.json');L=load('reference/lifecycle.json');I=load('reference/invariants.json');M=load('reference/measurement-contracts.json');R=load('runbooks/index.json')
if A['commands']!=actual['commands']:
 # Source anchors are additional authored metadata; constructor fields must still match.
 for row,got in zip(A['commands'],actual['commands']):
  if any(row.get(k)!=v for k,v in got.items()):errors.append('command metadata differs '+got['path'])
if len(A['commands'])!=len(actual['commands']):errors.append('command count mismatch')
if L['matrices']!=actual['transition_matrices']:errors.append('lifecycle matrix differs from executed validators')
if L['agent_report_checks']!=actual['agent_report_checks']:errors.append('agent guard cases differ')
for x in I['invariants']:
 for field in ['enforcing_symbol','test']:
  ref=x[field];text=(S/ref['path']).read_text()
  if not re.search(r'\b'+re.escape(ref['symbol'])+r'\b',text):errors.append(x['id']+' unknown '+field)
# Parse complete constructor call, balancing parentheses outside string literals.
t=(S/'internal/metrics/prometheus.go').read_text();metrics=[]
for m in re.finditer(r'prometheus\.New(CounterVec|HistogramVec|GaugeVec|Counter|Histogram|Gauge)\(',t):
 i=m.end();depth=1;quoted=False;escape=False
 while depth:
  ch=t[i];i+=1
  if quoted:
   if escape:escape=False
   elif ch=='\\':escape=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':depth+=1
  elif ch==')':depth-=1
 piece=t[m.end():i];name=re.search(r'Name:\s*"([^"]+)"',piece)
 if not name:continue
 labels=re.search(r'\[\]string\{([^}]+)\}',piece);metrics.append({'name':name[1],'collector':m[1],'labels':re.findall(r'"([^"]+)"',labels[1]) if labels else []})
expected=[{k:x[k] for k in ['name','collector','labels']} for x in M['registered_metrics']]
if metrics!=expected:errors.append('metric names/types/labels differ from actual constructors')
commands={x['path'] for x in A['commands']}
for x in R['playbooks']:
 for key in ['trigger','observation_command_paths','triage_order','decision_points','bounded_action','verification','rollback_or_stop_condition','supported_mode','architecture_boundary','evidence_class']:
  if not x.get(key):errors.append(x['id']+' missing '+key)
 for cmd in x['observation_command_paths']:
  if cmd not in commands:errors.append(x['id']+' unknown command '+cmd)
for x in M['contracts']:
 for key in ['unit','numerator','denominator','start_stop_events','timestamp_source','sampling','missing_data','workload_size','warmup','limitations','evidence_class']:
  if not x.get(key):errors.append(x['id']+' missing '+key)
if len(R['playbooks'])!=10 or len(M['contracts'])!=9 or len(metrics)!=30:errors.append('reference count mismatch')
for row in load('examples/source-excerpts/appendix-c-registry.json')['excerpts']:
 if hashlib.sha256((B/row['path']).read_bytes()).hexdigest()!=row['excerpt_sha256']:errors.append('historical excerpt hash mismatch '+row['id'])
(B/'validation/061-transition-check.json').write_text(json.dumps({'source_sha':L['source_sha'],'checked_at_utc':now,'command':'python3 books/inside-orch/scripts/check_appendix_references.py','state_sets':{k:sorted(v) for k,v in L['matrices'].items()},'matrix':L['matrices'],'terminal':L['terminal'],'owners':L['owners'],'checks':{'actual_validator_matrix_equal':L['matrices']==actual['transition_matrices'],'actual_agent_guards_equal':L['agent_report_checks']==actual['agent_report_checks']},'invariant_count':len(I['invariants']),'test_gaps':[x['id'] for x in I['invariants'] if x.get('test_gap')],'execution':'validation/reference-offline-inventory.json','scope':'Rechecks actual offline validator results and source symbols; no distributed proof.','errors':errors,'passed':not errors},indent=2)+'\n')
(B/'validation/064-ops-contract-check.json').write_text(json.dumps({'source_sha':M['source_sha'],'checked_at_utc':now,'command':'python3 books/inside-orch/scripts/check_appendix_references.py','playbooks':len(R['playbooks']),'measurement_contracts':len(M['contracts']),'registered_metrics':len(metrics),'command_paths_resolve':not errors,'verification_and_stop_complete':not errors,'actual_fake_load':'validation/ops-fake-load.json','metrics_and_labels':'Exact constructor names, types and label keys re-parsed from immutable source.','errors':errors,'passed':not errors},indent=2)+'\n')
print(json.dumps({'commands':len(commands),'invariants':len(I['invariants']),'metrics':len(metrics),'errors':errors}));raise SystemExit(bool(errors))
