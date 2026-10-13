#!/usr/bin/env python3
"""Compile each current canonical Go teaching addition in a fresh owned module overlay."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
B=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--source-copy',required=True);p.add_argument('--go-root',required=True);a=p.parse_args();source=Path(a.source_copy).resolve()
if B/'evidence' in source.parents:raise SystemExit('Never execute inside immutable source')
lock=json.loads((B/'evidence/source-lock.json').read_text())
for x in lock['files']:
 if hashlib.sha256((source/x['path']).read_bytes()).hexdigest()!=x['sha256']:raise SystemExit('Source changed: '+x['path'])
paths=sorted(set(q for e in json.loads((B/'examples/manifest.json').read_text())['examples']for q in e['paths']if q.endswith('.go')));groups={};observations=[]
for rel in paths:
 f=B/rel
 if '/lab03/'in rel:continue # Private-copy actual compile+execution already in fresh07603, with explicit input hashes.
 key=f.parent.name;target=source/'.book-labs/review075'/key;target.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target/f.name);groups[key]=target;observations.append({'canonical':rel,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'overlay':str(target/f.name)})
env=dict(os.environ,GOROOT=a.go_root,GOTOOLCHAIN='local',GOPATH='/tmp/inside-orch-gopath',GOMODCACHE='/tmp/inside-orch-gomod',GOCACHE='/tmp/inside-orch-gocache',GOFLAGS='-buildvcs=false',GOMAXPROCS='2')
cmd=[str(Path(a.go_root)/'bin/go'),'test','-count=1','-run','^$',*[ './'+str(x.relative_to(source))for x in groups.values()]];r=subprocess.run(cmd,cwd=source,env=env,text=True,capture_output=True);print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr);print(json.dumps({'canonical_inputs':observations,'command':cmd,'scope':'Compile-only current canonical additions; focused semantic executions joined separately in manifest. Lab03 excluded here because private-source overlays have fresh076 actual compile+execution.'},indent=2));sys.exit(r.returncode)
