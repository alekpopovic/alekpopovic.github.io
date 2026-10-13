#!/usr/bin/env python3
"""Run original drift fixtures against byte-identical source overlays, without Docker."""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys
BOOK=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source-copy',required=True);p.add_argument('--go-root',required=True);p.add_argument('--output-prefix',required=True);a=p.parse_args()
source=pathlib.Path(a.source_copy).resolve();output=(BOOK/a.output_prefix).resolve()
if BOOK/'evidence' in source.parents or not source.is_dir():p.error('Use a disposable source copy')
if BOOK not in output.parents or any(output.parent.glob(output.name+'*.json')):p.error('Use a fresh book-relative output prefix')
output.parent.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,GOROOT=a.go_root,GOTOOLCHAIN='local',GOPATH='/tmp/inside-orch-gopath',GOMODCACHE='/tmp/inside-orch-gomod',GOCACHE='/tmp/inside-orch-gocache',GOFLAGS='-buildvcs=false',GOMAXPROCS='2',ORCH_BOOK_LAB03_OUTPUT=str(output))
inputs={};overlays=[]
lock=json.loads((BOOK/'evidence/source-lock.json').read_text())
for item in lock['files']:
 f=source/item['path']
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=item['sha256']:raise SystemExit('Disposable source baseline mismatch: '+item['path'])
fixture=BOOK/'labs/03-reconciler-drift/fixtures/cases.json'
inputs[str(fixture.relative_to(BOOK))]=hashlib.sha256(fixture.read_bytes()).hexdigest()
for package in ('agent','reconciler'):
 target=source/'.book-labs'/('lab03'+package);target.mkdir(parents=True,exist_ok=True);overlays.append('./'+str(target.relative_to(source)))
 origin=BOOK/'evidence/orch/internal'/package
 # All baseline package/test files are copied unchanged; only TestBook* is executed.
 for f in origin.glob('*.go'):
  dest=target/f.name;shutil.copyfile(f,dest);inputs[str(f.relative_to(BOOK))]=hashlib.sha256(f.read_bytes()).hexdigest()
 for f in (BOOK/'examples/teaching-extensions/lab03').glob(package+'_contract_test.go'):
  shutil.copyfile(f,target/f.name);inputs[str(f.relative_to(BOOK))]=hashlib.sha256(f.read_bytes()).hexdigest()
cmd=[str(pathlib.Path(a.go_root)/'bin/go'),'test','-count=1','-v','-run','^TestBook',*overlays]
r=subprocess.run(cmd,cwd=source,env=env,text=True,capture_output=True);print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
if r.returncode:sys.exit(r.returncode)
cases=[]
for owner in ('agent','reconciler'):cases+=json.loads(pathlib.Path(str(output)+'-'+owner+'.json').read_text())
fixture_cases=json.loads(fixture.read_text())
if {c['id'] for c in cases}!=set(fixture_cases['store_cases']+fixture_cases['agent_cases']) or not all(c.get('passed') for c in cases):raise SystemExit('Incomplete case set')
check={'status':'passed','source_sha':json.loads((BOOK/'evidence/source-lock.json').read_text())['baseline_sha'],'runtime_mode':'FakeRuntime and in-process MemoryService lifecycle; separate store-backed reconciler test double; no Docker, HTTP or PostgreSQL','cwd':str(source),'go_command':cmd,'input_sha256':inputs,'cases':cases,'limitations':['Copied private package access, no behavior changes to baseline sources.','FakeRuntime does not establish Docker daemon behavior.','Store-backed reconciler is not the shipped server MemoryService loop.','Expected lifecycle rejection is a passing assertion, not successful recreation.']}
pathlib.Path(str(output)+'.json').write_text(json.dumps(check,indent=2)+'\n')
print(json.dumps({'case_count':len(cases),'check':str(output)+'.json','status':'passed'}))
