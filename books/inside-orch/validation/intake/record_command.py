#!/usr/bin/env python3
"""Capture this intake's actual local commands; no application tests run here."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

SITE = Path('/home/popac/alekpopovic.github.io')
BOOK = SITE / 'books/inside-orch'
OUT = BOOK / 'validation/intake'
OUT.mkdir(parents=True, exist_ok=True)
RECORDS = OUT / 'commands.jsonl'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(key, args, timeout=60, env=None):
    record = dict(id=key, command=args, cwd=str(SITE), started_at_utc=utc())
    start = time.monotonic()
    effective_env = dict(os.environ)
    effective_env.update(env or {})
    if env:
        record['environment_overrides'] = env
    try:
        result = subprocess.run(args, cwd=SITE, env=effective_env, capture_output=True,
                                text=True, timeout=timeout)
        record.update(exit_code=result.returncode, status='executed')
        stdout, stderr = result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        record.update(exit_code=None, status='timed_out')
        stdout = (exc.stdout or b'').decode() if isinstance(exc.stdout, bytes) else (exc.stdout or '')
        stderr = (exc.stderr or b'').decode() if isinstance(exc.stderr, bytes) else (exc.stderr or '')
    except OSError as exc:
        record.update(exit_code=None, status='unavailable')
        stdout, stderr = '', str(exc)
    record.update(finished_at_utc=utc(), duration_seconds=round(time.monotonic()-start, 3))
    for stream, contents in [('stdout', stdout), ('stderr', stderr)]:
        path = OUT / f'{key}.{stream}.txt'
        path.write_text(contents)
        record[stream] = str(path.relative_to(BOOK))
    with RECORDS.open('a') as handle:
        handle.write(json.dumps(record) + '\n')
    print(json.dumps(record), flush=True)
    return record

def inventory():
    records = []
    for path in sorted((BOOK / 'evidence/orch').rglob('*')):
        if path.is_file():
            raw = path.read_bytes()
            records.append(dict(path=str(path.relative_to(BOOK / 'evidence/orch')),
                                bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    return records

def initial():
    target = OUT / 'source-before.json'
    if target.exists():
        raise SystemExit('Refusing to replace an earlier intake inventory')
    target.write_text(json.dumps(dict(recorded_at_utc=utc(), files=inventory()), indent=2)+'\n')
    (OUT / 'pack-before.json').write_text(json.dumps({
        str(p.relative_to(BOOK)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(BOOK.rglob('*')) if p.is_file() and OUT not in p.parents
    }, indent=2)+'\n')
    run('git-status-initial', ['git','status','--porcelain=v1','--untracked-files=normal'])
    run('site-revision', ['git','rev-parse','HEAD'])
    run('site-branch', ['git','branch','--show-current'])
    run('site-origin', ['git','remote','get-url','origin'])
    run('generated-ignore-rules', ['git','check-ignore','-v',
        'book-pages/inside-orch/index.md',
        'assets/books/inside-orch/downloads/inside-orch.pdf', '_data/books.json'])
    run('verify-pack-initial', ['python3','books/inside-orch/scripts/verify_pack.py'])
    tools = [
        ('python','python3',['--version']), ('git','git',['--version']),
        ('go','go',['version']), ('docker','docker',['--version']),
        ('postgres-client','psql',['--version']),
        ('postgres-server','postgres',['--version']),
        ('postgres-readiness','pg_isready',['--version']),
        ('pandoc','pandoc',['--version']), ('weasyprint','weasyprint',['--version']),
        ('pdflatex','pdflatex',['--version']), ('xelatex','xelatex',['--version']),
        ('lualatex','lualatex',['--version']), ('pdfinfo','pdfinfo',['-v']),
        ('pdftoppm','pdftoppm',['-v']), ('epubcheck','epubcheck',['--version']),
        ('java','java',['-version']), ('ruby','ruby',['--version']),
        ('bundler','bundle',['--version']), ('node','node',['--version']),
        ('npm','npm',['--version']),
    ]
    capabilities = []
    for key, executable, arguments in tools:
        resolved = shutil.which(executable)
        item = dict(tool=key, executable=executable, path=resolved)
        if resolved:
            record=run('tool-'+key, [executable,*arguments], timeout=20,
                       env={'GOTOOLCHAIN':'local'} if key=='go' else None)
            item.update(status='version_checked' if record['exit_code']==0 else 'version_check_failed',
                        evidence=record['stdout'], stderr=record['stderr'])
        else:
            item.update(status='missing', reason='Executable not found on PATH; command not run.')
        capabilities.append(item)
    run('site-jekyll-version', ['bundle','exec','jekyll','--version'], timeout=30)
    run('python-publication-modules', [str(SITE/'.venv/bin/python'),'-c',
        'import importlib.metadata as m; print("\\n".join(f"{p} {m.version(p)}" for p in ["PyYAML", "Pillow", "Markdown", "weasyprint"]))'], timeout=30)
    if shutil.which('docker'):
        run('docker-daemon', ['docker','info','--format','{{.ServerVersion}}'], timeout=10)
        run('docker-compose-version', ['docker','compose','version'], timeout=10)
    if shutil.which('pg_isready'):
        run('postgres-local-readiness',['pg_isready','-h','127.0.0.1','-p','5432','-t','2'],timeout=5)
    (OUT/'tool-capabilities.json').write_text(json.dumps(dict(recorded_at_utc=utc(),tools=capabilities),indent=2)+'\n')

if __name__=='__main__':
    if sys.argv[1:] == ['initial']:
        initial()
    else:
        key, *args = sys.argv[1:]
        result = run(key, args, timeout=1800)
        sys.exit(result['exit_code'] if result['exit_code'] is not None else 1)
