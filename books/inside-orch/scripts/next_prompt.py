#!/usr/bin/env python3
from pathlib import Path
import csv,argparse,sys
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description='Print the next unfinished task; does not execute it.')
p.add_argument('--show',action='store_true',help='Print the complete prompt')
p.add_argument('--id',help='Choose a specific three-digit ID')
a=p.parse_args()
rows=list(csv.DictReader((ROOT/'state/execution-tracker.csv').open()))
row=next((r for r in rows if (r['id']==a.id if a.id else r['status']!='done')),None)
if row is None:print('No matching unfinished task. Review the release evidence before publication.');sys.exit(0)
print(f"{row['id']} [{row['status']}] {row['title']}\nbooks/inside-orch/{row['prompt_path']}")
if a.show:print('\n'+(ROOT/row['prompt_path']).read_text())
