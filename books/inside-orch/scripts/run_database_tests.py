#!/usr/bin/env python3
"""Run destructive store tests only against an identified lab-owned PostgreSQL container."""
import argparse, hashlib, json, os, re, subprocess
from pathlib import Path
from urllib.parse import urlparse
BOOK=Path(__file__).resolve().parents[1]

def validate_target(url, container):
    u=urlparse(url)
    if u.scheme not in ('postgres','postgresql') or u.hostname not in ('127.0.0.1','localhost'):
        raise ValueError('Database URL must address a loopback PostgreSQL endpoint')
    database=u.path.removeprefix('/')
    if not re.fullmatch(r'inside_orch_lab_[a-z0-9_]+',database):
        raise ValueError('Database name must start inside_orch_lab_ and have a unique lab suffix')
    labels=container.get('Config',{}).get('Labels') or {}
    if labels.get('inside-orch.lab')!='true' or not labels.get('inside-orch.run'):
        raise ValueError('Container lacks explicit inside-orch ownership labels')
    env=dict(x.split('=',1) for x in container['Config'].get('Env',[]) if '=' in x)
    if env.get('POSTGRES_DB')!=database:
        raise ValueError('URL database differs from lab container POSTGRES_DB')
    ports=container.get('NetworkSettings',{}).get('Ports',{}).get('5432/tcp') or []
    if not any(p.get('HostIp')=='127.0.0.1' and p.get('HostPort')==str(u.port or 5432) for p in ports):
        raise ValueError('URL port is not the owned container loopback-only PostgreSQL binding')
    if not container.get('State',{}).get('Running'):
        raise ValueError('Owned container is not running')
    return database

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--container',required=True); p.add_argument('--working-copy',type=Path,required=True)
    p.add_argument('--go',default='go'); p.add_argument('--database-url-env',default='INSIDE_ORCH_LAB_DATABASE_URL')
    p.add_argument('--check-only',action='store_true')
    a=p.parse_args(); url=os.environ.get(a.database_url_env,'')
    if not url: p.error('Designated database URL environment variable is empty')
    try:
        c=json.loads(subprocess.check_output(['docker','inspect',a.container],text=True))[0]
        database=validate_target(url,c)
        work=a.working_copy.resolve()
        if work==BOOK/'evidence/orch' or BOOK in work.parents: raise ValueError('Working copy must be outside canonical book')
        lock=json.loads((BOOK/'evidence/source-lock.json').read_text())
        for f in lock['files']:
            if hashlib.sha256((work/f['path']).read_bytes()).hexdigest()!=f['sha256']:
                raise ValueError('Working copy differs from baseline: '+f['path'])
        print(json.dumps({'guard':'passed','database':database,'container_id':c['Id'],'working_directory':str(work),'source_sha':lock['baseline_sha']}),flush=True)
        if a.check_only:return 0
        env=dict(os.environ,GOTOOLCHAIN='local',GOFLAGS='-buildvcs=false',ORCH_INTEGRATION_DATABASE_URL=url)
        env.pop('ORCH_E2E_DATABASE_URL',None)
        return subprocess.run([a.go,'test','./internal/store','-run','^TestPostgresStore','-count=1','-v'],cwd=work,env=env).returncode
    except (ValueError,KeyError,OSError,subprocess.CalledProcessError) as e:
        print('Database guard refused: '+str(e));return 2
if __name__=='__main__':raise SystemExit(main())
