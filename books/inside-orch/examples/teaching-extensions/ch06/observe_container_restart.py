#!/usr/bin/env python3
"""Observe a fresh default server process; never connect to a pre-existing endpoint."""
import argparse, contextlib, hashlib, json, os, signal, socket, subprocess, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
BOOK=Path(__file__).resolve().parents[3]

def utc(): return datetime.now(timezone.utc).isoformat()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--working-copy',type=Path,required=True)
    ap.add_argument('--server',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    work=a.working_copy.resolve(); out=(BOOK/a.output).resolve()
    if BOOK not in out.parents or out.exists(): ap.error('Output must be a new book-relative file')
    if BOOK in work.parents: ap.error('Execute only in a disposable copy outside the book')
    lock=json.loads((BOOK/'evidence/source-lock.json').read_text())
    for f in lock['files']:
        if hashlib.sha256((work/f['path']).read_bytes()).hexdigest()!=f['sha256']: ap.error('Source hash mismatch: '+f['path'])
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    origin='http://127.0.0.1:'+str(port)
    # Allowlist environment: no owner ORCH_*, Docker, database or credential settings.
    env={k:v for k,v in os.environ.items() if k in ('PATH','LANG','LC_ALL','TZ')}
    env.update(ORCH_SERVER_ADDR='127.0.0.1:'+str(port),ORCH_JWT_SECRET='',ORCH_USERS='',ORCH_AGENT_REGISTRATION_TOKEN='book-only-registration-token',ORCH_SCHEMA_CHECK='false',ORCH_SECRET_KEY='book-only-disposable-key',DATABASE_URL='postgres://unused@127.0.0.1:1/inside_orch_lab_unused_test?sslmode=disable')
    result={'source_sha':lock['baseline_sha'],'started_at_utc':utc(),'working_directory':str(work),'origin':origin,'mode':'actual fresh orch-server processes plus manually created owned Docker container; manually authenticated task report, no agent Runner adoption','observations':[]}
    out.parent.mkdir(parents=True,exist_ok=True)
    def request(path,body=None,token=None):
        data=json.dumps(body).encode() if body is not None else None
        headers={'Content-Type':'application/json','X-Orch-Bootstrap-Token':'book-only-registration-token'}
        if token: headers['Authorization']='Bearer '+token
        req=urllib.request.Request(origin+path,data=data,headers=headers)
        with urllib.request.urlopen(req,timeout=2) as r: return json.load(r)
    @contextlib.contextmanager
    def server(n):
        logpath=out.with_name(out.stem+'-process-'+str(n)+'.log')
        with logpath.open('wb') as log:
            p=subprocess.Popen([str(a.server.resolve())],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
            try:
                for attempt in range(100):
                    if p.poll() is not None: raise RuntimeError('Server exited early; see '+str(logpath))
                    try:
                        request('/readyz'); break
                    except (OSError,ValueError): time.sleep(.05)
                else: raise RuntimeError('Ready deadline exceeded')
                result['observations'].append({'event':'ready','process':n,'pid':p.pid,'at_utc':utc()})
                yield
            finally:
                if p.poll() is None:
                    p.send_signal(signal.SIGTERM)
                    try:p.wait(timeout=12)
                    except subprocess.TimeoutExpired:p.kill();p.wait()
                result['observations'].append({'event':'stopped','process':n,'exit_code':p.returncode,'at_utc':utc()})
    def snapshot():
        return {name:request('/v1/'+name).get(name) for name in ('services','tasks','nodes','namespaces')}
    container_id=None
    def docker(*args):
        command=['docker',*args]
        r=subprocess.run(command,capture_output=True,text=True,timeout=30)
        if r.returncode: raise RuntimeError('Docker command failed: '+str(command)+': '+r.stderr)
        return r.stdout.strip()
    try:
        # Cached image only; no pull, no published host ports, no host volumes.
        image_id=docker('image','inspect','nginx:1.27-alpine','--format','{{.Id}}')
        container_id=docker('create','--label','inside-orch.book=ch06-owned-restart','--network','none','nginx:1.27-alpine')
        if len(container_id)!=64 or any(c not in '0123456789abcdef' for c in container_id): raise RuntimeError('Invalid captured container ID')
        docker('start',container_id)
        result['docker']={'image_id':image_id,'container_id':container_id,'relationship':'Manually created, then explicitly reported as this task container by the harness; not created or adopted by an upstream Runner.','before':json.loads(docker('inspect',container_id))[0]['State']}
        assert result['docker']['before']['Running']
        with server(1):
            version=request('/v1/version'); request('/v1/namespaces',{'name':'book-payments'})
            registration=request('/v1/agent/register',{'node_name':'book-http-node','advertise_address':'http://127.0.0.1:1','capacity':{'cpu':4000,'memory':1073741824},'allocatable':{'cpu':4000,'memory':1073741824},'agent_version':'0.3.0'})
            node=registration['node']
            service=request('/v1/services',{'spec':{'name':'book-http','image':'nginx:1.27-alpine','replicas':1}})['service']
            assigned=snapshot()['tasks'][0]
            reported=request('/v1/agent/tasks/'+assigned['id']+'/status',{'node_id':node['id'],'status':'running','container_id':container_id},registration['credential']['token'])['task']
            assert reported['container_id']==container_id and reported['actual_status']=='running'
            before=snapshot(); assert len(before['services'])==1 and len(before['nodes'])==1
            assert any(x['name']=='book-payments' for x in before['namespaces'])
            result.update(version=version,before=before,captured_ids={'node':node['id'],'service':service['id'],'tasks':[x['id'] for x in before['tasks']]})
        with server(2):
            result['docker']['after']=json.loads(docker('inspect',container_id))[0]['State']
            assert result['docker']['after']['Running']
            after=snapshot(); assert not after['services'] and not after['tasks'] and not after['nodes']
            assert not any(x['name']=='book-payments' for x in after['namespaces'])
            result.update(after=after,assertions={'new_process_ready':True,'owned_container_still_running':True,'services_lost':True,'tasks_lost':True,'nodes_lost':True,'custom_namespace_lost':True,'default_namespace_recreated':any(x['name']=='default' for x in after['namespaces'])},status='passed')
    except Exception as e:
        result.update(status='failed',error=type(e).__name__+': '+str(e)); raise
    finally:
        if container_id:
            try:
                docker('rm','-f',container_id)
                probe=subprocess.run(['docker','inspect',container_id],capture_output=True,text=True,timeout=10)
                result['cleanup']={'exact_container_id':container_id,'removed':probe.returncode!=0,'inspect_exit_code':probe.returncode}
                assert result['cleanup']['removed']
            except Exception as cleanup_error:
                result.update(status='failed',cleanup_error=str(cleanup_error))
        result['finished_at_utc']=utc();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'record':str(out.relative_to(BOOK)),'captured_ids':result['captured_ids']}))
if __name__=='__main__':main()
