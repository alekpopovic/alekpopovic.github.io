#!/usr/bin/env python3
"""Read-only host capability report; no installs, starts, migrations or resets."""
import argparse, datetime, json, os, re, shutil, subprocess
from pathlib import Path

def probe(argv, timeout=8):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return {'command': argv, 'exit_code': p.returncode, 'output': (p.stdout+p.stderr).strip()[:2000]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'command': argv, 'exit_code': None, 'error': str(e)}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--go', default='go', help='Existing Go binary; never downloads a toolchain')
    a.add_argument('--probe-docker', action='store_true', help='Read Docker server version; privileged socket access')
    a.add_argument('--output', type=Path)
    args=a.parse_args()
    os.environ['GOTOOLCHAIN']='local'
    report={'schema_version':1,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope':'read-only capability probes, not application test results','working_directory':str(Path.cwd()),'capabilities':{}}
    for name,cmd in [('go',[args.go,'version']),('docker_cli',['docker','--version']),('compose',['docker','compose','version']),('psql',['psql','--version']),('pandoc',['pandoc','--version']),('java',['java','-version'])]:
        report['capabilities'][name]=probe(cmd)
    go=report['capabilities']['go']; m=re.search(r'go(\d+)\.(\d+)',go.get('output',''))
    report['source_only_ready']=bool(m and (int(m[1]),int(m[2])) >= (1,25))
    if args.probe_docker:
        report['capabilities']['docker_daemon']=probe(['docker','version','--format','{{.Server.Version}}'])
    else:
        report['capabilities']['docker_daemon']={'status':'not_probed','reason':'Pass --probe-docker to authorize a read-only daemon request.'}
    report['database_experiments']={'status':'not_run','reason':'Require independently provisioned throwaway container and scripts/run_database_tests.py guard.'}
    report['missing_tools']=[k for k,v in report['capabilities'].items() if v.get('exit_code') not in (None,0) or 'error' in v]
    raw=json.dumps(report,indent=2)+'\n'
    if args.output: args.output.write_text(raw)
    print(raw,end='')
    return 0
if __name__=='__main__': raise SystemExit(main())
