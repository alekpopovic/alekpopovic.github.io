#!/usr/bin/env python3
"""Verify source or recorded author-run lab evidence; never rerun infrastructure implicitly."""
import argparse,hashlib,json,os,platform,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
BOOK=Path(__file__).resolve().parents[1]
def read(path):return json.loads((BOOK/path).read_text())
def passed(path):
 d=read(path);assert d['status']=='passed' and d['exit_code']==0,path;return d

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lab',choices=['01','08'],required=True);p.add_argument('--mode',choices=['inspection','recorded'],required=True);a=p.parse_args()
 lock=read('evidence/source-lock.json');source=BOOK/'evidence/orch'
 for f in lock['files']:assert hashlib.sha256((source/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
 composition=(source/'cmd/orch-server/main.go').read_text();assert 'controlplane.NewMemoryService(' in composition
 pairs=[]
 for up in sorted((source/'migrations').glob('*.up.sql')):
  down=up.with_name(up.name.replace('.up.sql','.down.sql'));assert down.is_file();pairs.append({'up':str(up.relative_to(source)),'down':str(down.relative_to(source)),'up_sha256':hashlib.sha256(up.read_bytes()).hexdigest(),'down_sha256':hashlib.sha256(down.read_bytes()).hexdigest()})
 assert len(pairs)==16
 version=(source/'internal/version/version.go').read_text();assert re.search(r'Schema\s*=\s*16',version)
 result={'source_sha':lock['baseline_sha'],'checked_at_utc':datetime.now(timezone.utc).isoformat(),'lab':a.lab,'mode':a.mode,'validation':'inspected' if a.mode=='inspection' else 'executed','scope':'Source/hash inspection and verification of existing recorded runs; infrastructure experiments are NOT implicitly repeated','inspection':{'source_files':len(lock['files']),'memory_constructor':True,'migration_pairs':len(pairs)},'status':'passed'}
 if a.mode=='recorded' and a.lab=='01':
  commands={name:passed('validation/labs/'+name+'.json') for name in ('lab01-version','lab01-help','lab01-redacted-config','lab01-manifest-cli-format')}
  config=(BOOK/commands['lab01-redacted-config']['stdout']).read_text();assert "secret_key: '[REDACTED]'" in config and "database_url: '[REDACTED]'" in config
  restart=read('validation/intake/fresh-server-restart-authenticated.json');assert restart['status']=='passed' and all(restart['assertions'].values())
  ids=restart['captured_ids'];assert ids['service'] and ids['node'] and len(ids['tasks'])==1
  command=passed('validation/intake/docker-complete-flow-log-guard.json');flow=read(command['stdout'])
  assert flow['status']=='passed' and flow['http_probe']['welcome_matched'] and flow['logs']['nginx_matched']
  assert [(x['active'],x['removed']) for x in flow['flow']]==[(1,0),(2,0),(1,1),(0,2)]
  combined=read('validation/labs/ch06/combined-restart.json');assert combined['status']=='passed' and all(combined['assertions'].values()) and combined['cleanup']['removed']
  cleanup=read('validation/intake/docker-complete-flow-cleanup.json');assert cleanup['status']=='passed' and len(cleanup['checks'])==3 and all(x['absent'] for x in cleanup['checks'])
  result['combined_container_survival_record']='validation/labs/ch06/combined-restart.json';result['docker_cleanup_record']='validation/intake/docker-complete-flow-cleanup.json'
  result.update(tracks={'inspection':'passed','offline_commands':'passed','fresh_binary_process_restart':'passed','docker_package_integration':'passed'},commands=list(commands.values()),restart={'record':'validation/intake/fresh-server-restart-authenticated.json','before':restart['before'],'after':restart['after'],'captured_ids':ids},docker={'command_record':'validation/intake/docker-complete-flow-log-guard.json','observed':flow},database_status_record='validation/intake/full-schema-recovery-corrected.json')
 elif a.mode=='recorded' and a.lab=='08':
  rec=read('validation/intake/full-schema-recovery-corrected.json');assert rec['status']=='passed'
  before=rec['prepare']['schema_before'];after=rec['prepare']['schema_after'];twice=rec['prepare']['schema_after_second_up']
  assert len(before['pending'])==16 and after['current']=='000016' and not after['pending'] and twice==after
  assert rec['prepare']['down_without_allow_rejected'] and rec['restored']['wrong_key_rejected']
  assert rec['prepare']['canary_sha256']==rec['restored']['canary_sha256']
  names=rec['databases'];assert names['source']!=names['target'] and set(rec['cleanup']['created_databases_removed'])==set(names.values())
  dump=rec['backup'];assert hashlib.sha256((BOOK/dump['path']).read_bytes()).hexdigest()==dump['sha256']
  guard=passed('validation/labs/recovery-target-guards.json');load=passed('validation/labs/lab08-fixed-seed-fake-load.json');raw=(BOOK/load['stdout']).read_text()
  assert '--seed' in load['command'] and '20261013' in load['command'] and 'tasks_created' in raw
  tool=read('validation/intake/go125-toolchain-network.json')
  result.update(tracks={'inspection':'passed','postgres_artifact_restore':'passed','fake_agent_load':'passed','live_orchestration_recovery':'unsupported_default_runtime'},migration_pairs=pairs,recovery=rec,load={'command_record':'validation/labs/lab08-fixed-seed-fake-load.json','command':load['command'],'raw_output':raw,'host':{'architecture':platform.machine(),'platform':platform.platform(),'available_cpu_count':os.cpu_count()},'go_record':'validation/intake/go125-toolchain-network.json','measurement_scope':'in-process MemoryService and simulated task transitions, not Docker or PostgreSQL capacity'},target_guards=guard)
 path=BOOK/'validation/labs'/f'{a.lab}-check{ "-inspection" if a.mode=="inspection" else ""}.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'mode':a.mode,'record':str(path.relative_to(BOOK))}))
if __name__=='__main__':main()
