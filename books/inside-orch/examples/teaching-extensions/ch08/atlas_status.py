#!/usr/bin/env python3
"""Teaching extension: check server-reported current Atlas replicas, not live health."""
import argparse,json,subprocess,sys

def evaluate(service,tasks):
 if not isinstance(service,dict) or not isinstance(tasks,list):raise ValueError('Unexpected CLI JSON shape')
 spec=service.get('spec');sid=service.get('id');version=service.get('deployment_version')
 if not isinstance(spec,dict) or not isinstance(sid,str) or not sid or type(version) is not int:raise ValueError('Missing service identity/version')
 replicas=spec.get('replicas')
 if type(replicas) is not int or replicas<0:raise ValueError('Invalid replica count')
 current=[];seen=set()
 for task in tasks:
  if not isinstance(task,dict) or not all(key in task for key in ('id','service_id','desired_status','actual_status','version')):raise ValueError('Missing task contract fields')
  if not isinstance(task['id'],str) or not task['id'] or task['id'] in seen:raise ValueError('Missing or duplicate task identity')
  seen.add(task['id'])
  if task['service_id']!=sid:raise ValueError('Task belongs to another service')
  if task['desired_status']=='running' and task['version']==version:current.append(task)
 available=sum(task['actual_status'] in ('running','healthy') for task in current)
 ok=service.get('status')=='active' and len(current)==replicas and available==replicas
 return ok,dict(service=spec.get('name'),version=version,desired_replicas=replicas,current_tasks=len(current),reported_available=available,scope='server observation only; no fresh host probe')

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--cli',required=True);p.add_argument('--server',required=True)
 p.add_argument('--service',default='atlas-api');p.add_argument('--namespace',default='default');p.add_argument('--config')
 a=p.parse_args();base=[a.cli,'--server',a.server,'--namespace',a.namespace,'--output','json']
 if a.config:base+=['--config',a.config]
 def query(*args):
  r=subprocess.run([*base,*args],capture_output=True,text=True,timeout=35)
  if r.returncode:raise RuntimeError('CLI request failed; check server reachability, selected namespace and credential configuration')
  return json.loads(r.stdout)
 try:
  ok,result=evaluate(query('service','inspect',a.service),query('service','ps',a.service))
 except (OSError,subprocess.TimeoutExpired,RuntimeError):
  print('Atlas status unavailable: check CLI path, server reachability, namespace and credential configuration.',file=sys.stderr);return 2
 except (ValueError,TypeError):
  print('Atlas status incompatible: inspect the current CLI JSON contract before retrying.',file=sys.stderr);return 3
 print(json.dumps(result,sort_keys=True))
 if not ok:print('Atlas has not converged: inspect service ps and events for assigned, failed or old-version tasks.',file=sys.stderr)
 return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
