#!/usr/bin/env python3
"""Prove eight existing tests reject specified incorrect behavior in disposable copies."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,datetime,hashlib
p=argparse.ArgumentParser();p.add_argument('--go-root',required=True);p.add_argument('--module-cache',required=True);a=p.parse_args();B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';D=json.loads((B/'exercises/catalog.json').read_text());root=Path('/tmp/inside-orch-exercise-mutants');root.mkdir(exist_ok=True)
mutations=[
('DEV-01','internal/scheduler/scheduler.go','return Assignment{}, false, nil\n\t}\n\tif err != nil {','return Assignment{}, true, nil\n\t}\n\tif err != nil {','Misreport stale conflict as successful assignment.'),
('DEV-02','internal/controlplane/controlplane.go','status = types.TaskFailed\n\t\t\teventType = events.TypeTaskHealthFailed','status = types.TaskUnhealthy\n\t\t\teventType = events.TypeTaskHealthFailed','Keep restartable unhealthy task unhealthy instead of marking failed.'),
('DEV-03','pkg/types/lifecycle.go','return status == TaskStopped || status == TaskRemoved || status == TaskFailed','return status == TaskStopped || status == TaskFailed','Deny removed report during cleanup intent.'),
('DEV-04','internal/rollout/rollout.go','if state.oldActive == 0 && state.newHealthy >= service.Spec.Replicas {','if false && state.oldActive == 0 && state.newHealthy >= service.Spec.Replicas {','Never complete otherwise successful rollout.'),
('DEV-05','internal/controlplane/controlplane.go','service, ok := s.services[id]\n\tif !ok || !namespace.Matches(ctx, service.Namespace) {\n\t\treturn types.Service{}, store.ErrNotFound','service, ok := s.services[id]\n\tif !ok {\n\t\treturn types.Service{}, store.ErrNotFound','Allow GetService to return a foreign namespace record.'),
('DEV-06','internal/controlplane/controlplane.go','if err := quota.Check(s.quotaLocked(service.Namespace), usage); err != nil {','if err := quota.Check(s.quotaLocked(service.Namespace), usage); err != nil && false {','Ignore quota denial in ScaleService.'),
('DEV-07','internal/gitops/gitops.go','if source.Prune {','if source.Prune && false {','Disable requested GitOps prune.'),
('DEV-08','internal/cronjobs/cronjobs.go','case types.ConcurrencyForbid:\n\t\t\tif len(active) > 0 {','case types.ConcurrencyForbid:\n\t\t\tif len(active) > 0 && false {','Allow a due occurrence despite Forbid overlap.')]
env={k:v for k,v in os.environ.items() if not k.startswith(('ORCH_','DOCKER_','DATABASE_URL'))};env.update(GOROOT=a.go_root,GOTOOLCHAIN='local',GOENV='off',GOPROXY='off',GOFLAGS='-mod=readonly',GOMODCACHE=a.module_cache,GOCACHE=str(root/'gocache'),GOPATH=str(root/'gopath'));results=[]
for ident,path,old,new,behavior in mutations:
 target=root/ident.lower();assert not target.is_relative_to(S)
 if target.exists():shutil.rmtree(target)
 shutil.copytree(S,target);f=target/path;text=f.read_text();assert text.count(old)>=1,(ident,text.count(old));f.write_text(text.replace(old,new));exercise=next(x for x in D['exercises'] if x['id']==ident);cmd=[a.go_root+'/bin/go','test','-json']+exercise['command'][2:];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,cwd=target,env=env,capture_output=True,text=True,timeout=180);out=B/'validation/exercises'/(ident.lower()+'.mutant.stdout.jsonl');out.write_text(r.stdout);err=out.with_name(ident.lower()+'.mutant.stderr.txt');err.write_text(r.stderr);fails=[]
 for line in r.stdout.splitlines():
  x=json.loads(line)
  if x.get('Action')=='fail' and x.get('Test'):fails.append(x['Test'])
 results.append({'id':ident,'source_sha':D['source_sha'],'mutation_path':path,'baseline_sha256':hashlib.sha256((S/path).read_bytes()).hexdigest(),'old':old,'new':new,'specified_incorrect_behavior':behavior,'command':cmd,'cwd':str(target),'prerequisites':['Go1.25.0','cached dependencies','Git for DEV-07'],'started_at_utc':start,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'failing_tests':fails,'incorrect_behavior_rejected':r.returncode!=0 and bool(fails),'stdout':str(out.relative_to(B)),'stderr':str(err.relative_to(B))})
 print(ident,r.returncode,fails,flush=True)
report={'source_sha':D['source_sha'],'scope':'Eight specified one-line teaching mutations in disposable copies; actual existing-test rejection, not a claim of exhaustive mutation coverage. Immutable snapshot unchanged.','runs':results,'all_rejected':all(x['incorrect_behavior_rejected'] for x in results)};(B/'validation/exercises/mutation-runs.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(not report['all_rejected'])
