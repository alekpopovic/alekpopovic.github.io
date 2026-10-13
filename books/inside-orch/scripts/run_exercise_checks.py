#!/usr/bin/env python3
"""Run eight offline existing-test exercises in an explicit disposable module."""
from pathlib import Path
import argparse,os,json,datetime,subprocess
p=argparse.ArgumentParser();p.add_argument('--module',required=True);p.add_argument('--go-root',required=True);p.add_argument('--module-cache',required=True);a=p.parse_args();B=Path(__file__).resolve().parents[1];src=Path(a.module).resolve();assert not src.is_relative_to(B/'evidence');D=json.loads((B/'exercises/catalog.json').read_text());logs=B/'validation/exercises';logs.mkdir(exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith(('ORCH_','DOCKER_','DATABASE_URL'))};env.update(GOROOT=a.go_root,GOTOOLCHAIN='local',GOENV='off',GOPROXY='off',GOFLAGS='-mod=readonly',GOMODCACHE=a.module_cache,GOCACHE='/tmp/inside-orch-reference-cbfc94ade5b5/gocache',GOPATH='/tmp/inside-orch-reference-cbfc94ade5b5/gopath');results=[]
for x in D['exercises']:
 if not x['executable']:continue
 command=[a.go_root+'/bin/go']+x['command'][1:];command.insert(2,'-json');start=datetime.datetime.now(datetime.timezone.utc).isoformat();run=subprocess.run(command,cwd=src,env=env,capture_output=True,text=True);output=logs/(x['id'].lower()+'.stdout.jsonl');output.write_text(run.stdout);(logs/(x['id'].lower()+'.stderr.txt')).write_text(run.stderr);passed=[]
 for line in run.stdout.splitlines():
  item=json.loads(line)
  if item.get('Action')=='pass' and 'Test' in item:passed.append(item['Test'])
 expected=set(x['test_filter'].split('|'));found=set(t.split('/')[0] for t in passed);results.append({'id':x['id'],'command':command,'cwd':str(src),'source_sha':D['source_sha'],'started_at_utc':start,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':run.returncode,'passed_tests':passed,'exact_requested_tests_ran':expected<=found,'stdout':str(output.relative_to(B)),'scope':'Actual pinned package tests with fakes/local temporary Git only; not Docker/DB/remote-host execution.'})
report={'source_sha':D['source_sha'],'go_version':subprocess.run([a.go_root+'/bin/go','version'],env=env,capture_output=True,text=True,check=True).stdout.strip(),'runs':results,'all_passed':all(r['exit_code']==0 and r['exact_requested_tests_ran'] for r in results)};(B/'validation/exercises/offline-runs.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'executable_entries':len(results),'all_passed':report['all_passed'],'test_passes':sum(len(r['passed_tests']) for r in results)}));raise SystemExit(not report['all_passed'])
