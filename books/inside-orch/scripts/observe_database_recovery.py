#!/usr/bin/env python3
"""Full-schema experiment and restore only in fresh databases of an owned lab container."""
import argparse,hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse,urlunparse
from run_database_tests import validate_target
BOOK=Path(__file__).resolve().parents[1]
def utc():return datetime.now(timezone.utc).isoformat()
def validate_recovery_names(source,target):
 if source==target:raise ValueError("Restore source and target must differ")
 if not all(re.fullmatch(r"inside_orch_lab_[a-z0-9_]+_test",n or "") for n in (source,target)):raise ValueError("Both database identities must be explicit owned lab names")
 return True
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--container',required=True);p.add_argument('--working-copy',type=Path,required=True);p.add_argument('--go',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 c=json.loads(subprocess.check_output(['docker','inspect',a.container],text=True))[0]
 base=os.environ.get('INSIDE_ORCH_LAB_DATABASE_URL','');dbname=validate_target(base,c);u=urlparse(base)
 suffix=dbname.removeprefix('inside_orch_lab_').removesuffix('_test')
 source='inside_orch_lab_'+suffix+'_recovery_test';target='inside_orch_lab_'+suffix+'_restored_test'
 validate_recovery_names(source,target)
 work=a.working_copy.resolve();assert BOOK not in work.parents
 lock=json.loads((BOOK/'evidence/source-lock.json').read_text())
 for f in lock['files']:assert hashlib.sha256((work/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
 out=(BOOK/a.output).resolve();assert BOOK in out.parents and not out.exists();out.parent.mkdir(parents=True,exist_ok=True)
 record={'source_sha':lock['baseline_sha'],'started_at_utc':utc(),'container_id':c['Id'],'container_image':c['Image'],'databases':{'source':source,'target':target},'working_directory':str(work),'commands':[]}
 owned=[]
 def run(argv,**kw):
  result=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kw)
  record['commands'].append({'argv':argv,'exit_code':result.returncode,'stdout':result.stdout.decode(errors='replace') if isinstance(result.stdout,bytes) else result.stdout,'stderr':result.stderr.decode(errors='replace') if isinstance(result.stderr,bytes) else result.stderr})
  if result.returncode:raise RuntimeError('Command failed: '+repr(argv))
  return result.stdout
 def sql(statement):return run(['docker','exec',a.container,'psql','-U','postgres','-d','postgres','-At','-v','ON_ERROR_STOP=1','-c',statement]).decode().strip()
 def bookgo(database,mode):
  env=dict(os.environ,INSIDE_ORCH_LAB_DATABASE_URL=urlunparse(u._replace(path='/'+database)))
  data=run([a.go,'run','./.book-labs/full-schema',mode],cwd=work,env=env)
  return json.loads(data)
 try:
  for name in (source,target):
   if sql("SELECT count(*) FROM pg_database WHERE datname='"+name+"'")!='0':raise ValueError('Refusing existing database '+name)
   sql('CREATE DATABASE '+name);owned.append(name)
  prepared=bookgo(source,'prepare')
  dump=subprocess.run(['docker','exec',a.container,'pg_dump','-U','postgres','--format=custom','--no-owner','--no-privileges',source],capture_output=True)
  record['commands'].append({'argv':dump.args,'exit_code':dump.returncode,'binary_stdout':'dump retained under validation; not embedded','stderr':dump.stderr.decode()})
  assert dump.returncode==0
  dump_path=out.with_suffix('.dump');dump_path.write_bytes(dump.stdout)
  run(['docker','exec','-i',a.container,'pg_restore','-U','postgres','--no-owner','--no-privileges','--dbname',target],input=dump.stdout)
  verified=bookgo(target,'verify');assert prepared['canary_sha256']==verified['canary_sha256'],'canary roundtrip'
  record.update(status='passed',prepare=prepared,restored=verified,backup={'path':str(dump_path.relative_to(BOOK)),'bytes':len(dump.stdout),'sha256':hashlib.sha256(dump.stdout).hexdigest()},boundaries=['Only PostgreSQL package rows restored; default server MemoryService maps are separate','No host production database was touched','Source scripts inspected; pg_dump/pg_restore executed directly inside lab container'])
 except Exception as e:
  record.update(status='failed',error=type(e).__name__+': '+str(e));raise
 finally:
  for name in reversed(owned):sql('DROP DATABASE '+name+' WITH (FORCE)')
  record['cleanup']={'created_databases_removed':owned};record['finished_at_utc']=utc();out.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'status':record['status'],'record':str(out.relative_to(BOOK))}))
if __name__=='__main__':main()
