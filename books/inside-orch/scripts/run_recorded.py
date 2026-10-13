#!/usr/bin/env python3
"""Run one explicit verification command and retain sanitized UTC evidence."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BOOK = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--id', required=True)
p.add_argument('--cwd', required=True)
p.add_argument('--output', required=True, help='Book-relative result JSON path')
p.add_argument('--env', action='append', default=[])
p.add_argument('--timeout', type=int, default=600)
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
target = (BOOK / a.output).resolve()
if BOOK not in target.parents or target.exists():
    p.error('Use a new evidence path inside the book')
cwd = Path(a.cwd).resolve()
if cwd == BOOK / 'evidence/orch' or BOOK / 'evidence/orch' in cwd.parents:
    p.error('Immutable source cannot be an execution working directory')
cmd = a.command[1:] if a.command[:1] == ['--'] else a.command
if not cmd:
    p.error('Missing command')
env = dict(os.environ)
keys = []
for entry in a.env:
    key, value = entry.split('=', 1)
    env[key] = value
    keys.append(key)
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
record = dict(id=a.id, command=cmd, cwd=str(cwd), environment_keys=keys,
              source_sha=json.loads((BOOK/'evidence/source-lock.json').read_text())['baseline_sha'],
              started_at_utc=utc(), scope='Only the command and environment recorded here were executed.')
start = time.monotonic()
try:
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=a.timeout)
    stdout, stderr = r.stdout, r.stderr
    record.update(exit_code=r.returncode, status='passed' if r.returncode == 0 else 'failed')
except (OSError, subprocess.TimeoutExpired) as exc:
    stdout, stderr = '', str(exc)
    record.update(exit_code=None, status='blocked' if isinstance(exc, OSError) else 'timed_out')
record.update(finished_at_utc=utc(), duration_seconds=round(time.monotonic()-start, 3))
target.parent.mkdir(parents=True, exist_ok=True)
for key, output in [('stdout', stdout), ('stderr', stderr)]:
    path = target.with_suffix('.'+key+'.txt')
    path.write_text(output)
    record[key] = str(path.relative_to(BOOK))
target.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
sys.exit(record['exit_code'] if record['exit_code'] is not None else 1)
