#!/usr/bin/env python3
"""Run exact CLI/status commands against one owned fresh binary; no Docker/database."""
import contextlib,hashlib,json,os,signal,socket,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
B=Path(__file__).resolve().parents[3];cli=Path(sys.argv[1]).resolve();server=Path(sys.argv[2]).resolve();work=Path(sys.argv[3]).resolve()
for f in json.loads((B/'evidence/source-lock.json').read_text())['files']:assert hashlib.sha256((work/f['path']).read_bytes()).hexdigest()==f['sha256']
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
origin='http://127.0.0.1:'+str(port);results=[]
env={k:v for k,v in os.environ.items() if k in ('PATH','LANG','LC_ALL','TZ')}
env.update(ORCH_SERVER_ADDR='127.0.0.1:'+str(port),ORCH_JWT_SECRET='',ORCH_USERS='',ORCH_AGENT_REGISTRATION_TOKEN='book-ch08-only',ORCH_SCHEMA_CHECK='false',ORCH_SECRET_KEY='book-ch08-local-key',DATABASE_URL='postgres://unused@127.0.0.1:1/book_unused_test?sslmode=disable')
def request(path,body=None,token=None):
 headers={'Content-Type':'application/json','X-Orch-Bootstrap-Token':'book-ch08-only'}
 if token:headers['Authorization']='Bearer '+token
 req=urllib.request.Request(origin+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
 with urllib.request.urlopen(req,timeout=2) as r:return json.load(r)
def run(name,command,want=0,extra=None):
 childenv=dict(env);childenv.update(extra or {})
 r=subprocess.run(command,cwd=work,env=childenv,capture_output=True,text=True,timeout=40)
 results.append(dict(case=name,command=[str(x) for x in command],environment_overrides=list((extra or {}).keys()),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
 assert r.returncode==want,results[-1]
 return r
with tempfile.TemporaryDirectory(prefix='inside-orch-ch08-') as temp:
 temp=Path(temp);cfg=temp/'config.yaml';cfg.write_text('server_url: http://127.0.0.1:1\nnamespace: absent-config\n')
 with (temp/'server.log').open('wb') as log:
  process=subprocess.Popen([str(server)],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
  try:
   for attempt in range(100):
    if process.poll() is not None:raise RuntimeError('Owned server exited')
    try:request('/readyz');break
    except OSError:time.sleep(.05)
   else:raise RuntimeError('Owned server deadline')
   command=[str(cli),'--config',str(cfg),'--server',origin,'--namespace','default','--output','json','service','ls']
   run('flag-over-env-over-file',command,extra={'ORCH_SERVER_URL':'http://127.0.0.1:1','ORCH_NAMESPACE':'absent-env'})
   run('env-over-file',[str(cli),'--config',str(cfg),'--output','json','service','ls'],extra={'ORCH_SERVER_URL':origin,'ORCH_NAMESPACE':'default'})
   cfg.write_text('server_url: '+origin+'\nnamespace: default\n')
   run('file-only',[str(cli),'--config',str(cfg),'--output','json','service','ls'])
   empty=temp/'empty.yaml';empty.write_text('{}\n')
   run('missing-server',[str(cli),'--config',str(empty),'service','ls'],want=1)
   fixture=B/'examples/teaching-extensions/ch05/atlas-valid.yaml'
   run('local-validation',[str(cli),'validate',str(fixture)])
   run('deploy',[str(cli),'--server',origin,'--config',str(empty),'--output','json','deploy',str(fixture)])
   status=[sys.executable,str(B/'examples/teaching-extensions/ch08/atlas_status.py'),'--cli',str(cli),'--server',origin,'--config',str(empty)]
   run('not-converged-before-node',status,want=1)
   registration=request('/v1/agent/register',{'node_name':'ch08-node','advertise_address':'http://127.0.0.1:1','labels':{'role':'worker'},'capacity':{'cpu':4000,'memory':1073741824},'allocatable':{'cpu':4000,'memory':1073741824},'agent_version':'0.3.0'})
   tasks=request('/v1/tasks')['tasks'];assert len(tasks)==3
   for task in tasks:request('/v1/agent/tasks/'+task['id']+'/status',{'node_id':registration['node']['id'],'status':'running'},registration['credential']['token'])
   run('converged-server-reports',status)
   run('inspect',[str(cli),'--server',origin,'--config',str(empty),'--output','json','service','inspect','atlas-api'])
   run('ps',[str(cli),'--server',origin,'--config',str(empty),'--output','json','service','ps','atlas-api'])
   run('bad-service',[*status,'--service','missing-atlas'],want=2)
   run('connection-refused',[sys.executable,str(B/'examples/teaching-extensions/ch08/atlas_status.py'),'--cli',str(cli),'--server','http://127.0.0.1:1','--config',str(empty)],want=2)
  finally:
   if process.poll() is None:
    process.send_signal(signal.SIGTERM)
    try:process.wait(timeout=12)
    except subprocess.TimeoutExpired:process.kill();process.wait()
   assert process.poll() is not None
print(json.dumps(dict(scope='Actual CLI and fresh server process; manually authenticated running reports, no Docker containers or host health observations.',origin=origin,commands=results,cleanup='owned process stopped; temporary configuration directory removed'),indent=2))
