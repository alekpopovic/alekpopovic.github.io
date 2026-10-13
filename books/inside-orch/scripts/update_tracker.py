#!/usr/bin/env python3
from pathlib import Path
import csv,argparse,datetime,os
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description='Update one book-production task after verification.')
p.add_argument('--id',required=True);p.add_argument('--status',required=True,choices=['pending','in_progress','blocked','review_needed','done'])
p.add_argument('--evidence',default='');p.add_argument('--outputs',default='');p.add_argument('--note',default='');p.add_argument('--commit',default='')
a=p.parse_args();path=ROOT/'state/execution-tracker.csv'
with path.open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
row=next((r for r in rows if r['id']==a.id),None)
if row is None:raise SystemExit('Unknown three-digit task ID')
if a.status=='done' and not a.evidence:raise SystemExit('A done task requires concrete evidence paths')
for rel in filter(None,a.evidence.split(';')):
    target=(ROOT/rel).resolve()
    if ROOT not in target.parents:raise SystemExit('Evidence must be inside the book workspace')
    if not target.exists():raise SystemExit('Evidence path missing: '+rel)
row.update(status=a.status,evidence=a.evidence,outputs=a.outputs,note=a.note,local_commit=a.commit,updated_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
tmp=path.with_suffix('.csv.tmp')
with tmp.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
os.replace(tmp,path);print(f"Updated {a.id} to {a.status}; evidence presence checked, semantic truth still requires review.")
