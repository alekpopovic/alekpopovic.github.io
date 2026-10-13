#!/usr/bin/env python3
"""Validate an evidence inventory, never certify production readiness."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[3]
SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha']
entries=[
 ('build','validation/intake/orch-build-isolated-root.json','Built binaries from locked disposable source, not deployment.'),
 ('baseline-tests','validation/intake/orch-baseline-tests.json','Ungated suite, with explicit Docker/PostgreSQL skips.'),
 ('race','validation/intake/orch-race-tests.json','Reached race-detector paths only; same gated integrations absent.'),
 ('real-docker-flow','validation/intake/docker-complete-flow-log-guard.json','Guarded handler/Runner/engine flow, not upstream Compose deployment.'),
 ('resource-boundary','validation/intake/docker-resource-boundary-corrected.json','Normal-path zero limits versus supplied direct-adapter limits.'),
 ('fresh-server','validation/labs/ch06/combined-restart.json','Actual process restart loses memory records; manually associated container survives.'),
 ('database-restore','validation/intake/full-schema-recovery-corrected.json','Full-schema owned store/backup restore, not default server persistence.'),
 ('upgrade-preflight','validation/labs/ch35/controlled-preflight-corrected.json','Real Cobra command, controlled node inputs, no live cluster.'),
 ('retention-maintenance','validation/labs/ch35/operations-tests.json','Deterministic memory fixtures and migration helper tests.'),
 ('bounded-performance','validation/labs/ch39/bounded-benchmarks.json','Short shared-host samples; no capacity promise.')]
rows=[]
for topic,path,scope in entries:
 p=B/path;d=json.loads(p.read_text());assert d['source_sha']==SHA;assert d['status']=='passed',(path,d.get('status'))
 for k in ['stdout','stderr']:
  if isinstance(d.get(k),str):assert(B/d[k]).is_file()
 rows.append(dict(topic=topic,path=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),observed_status=d['status'],scope=scope))
print(json.dumps(dict(source_sha=SHA,status='passed',meaning='Evidence inventory exists and matched selected observed success records; not production certification.',entries=rows,production_decision='not approved',unresolved=['Default active state is MemoryService','PostgreSQL composition and transactional parity incomplete','Leadership not wired; cancellation can retain advisory session lock','Ordinary agent task path drops runtime resource limits','Autoscaler provider/controller not composed','No complete node mTLS or cluster fencing','No complete cross-node networking/stateful recovery','Live alert evaluation and production-shaped capacity not demonstrated']),indent=2))
