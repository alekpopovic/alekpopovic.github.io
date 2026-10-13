#!/usr/bin/env python3
"""Apply only narrow prose spacing repairs; preserve fences, code and destinations."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--through', type=int, required=True)
p.add_argument('--record', required=True, help='New book-relative review JSON')
a = p.parse_args()
out = (BOOK / a.record).resolve()
if not out.is_relative_to(BOOK) or out.exists():
    p.error('Use a new book-relative evidence file')
changes = []
paths = [p for p in sorted((BOOK / 'manuscript/chapters').glob('*.md')) if int(p.name[:2]) <= a.through]
joined = re.compile(r'\b(all|Go|Python|Chapter|chapter|Chapters|chapters|prompt|prompts|Prompts|migration|migrations|with|and|for|port|requests|requesting|using|has|a|SQLSTATE|threshold|schema|version|numeric|remains|by|replicas|trim|margins|inside|outside|top|bottom|Body|body|minimum|Reading|contains|in|CPU|memory|TCP|UDP)(?=\d)')
for path in paths:
    old = path.read_text()
    fence = False
    lines = []
    for n, line in enumerate(old.splitlines(keepends=True), 1):
        if re.match(r'^\s*(```|~~~)', line):
            fence = not fence
        new = line
        if not fence and not re.match(r'^\s*(```|~~~)', line):
            parts = re.split(r'(`+[^`]*`+|\]\([^)]*\)|\[[a-f0-9]{7,40}\]|[a-f0-9]{40})', line)
            for i in range(0, len(parts), 2):
                parts[i] = joined.sub(r'\1 ', parts[i])
                parts[i] = re.sub(r'\b(schedulers?|and|task|token|pool|key|node|container|pass|[Hh]andler)([A-Z])\b', r'\1 \2', parts[i])
                parts[i] = re.sub(r"'s(?=\d)", "'s ", parts[i])
                parts[i] = re.sub(r'\b([Nn]ode)([abc])\b', r'\1 \2', parts[i])
                parts[i] = re.sub(r'(?<=[A-Za-z]),(?=\d)', ', ', parts[i])
                parts[i] = re.sub(r'\b(\d+)second\b', r'\1-second', parts[i])
            new = ''.join(parts)
        lines.append(new)
        if new != line:
            changes.append({'path': str(path.relative_to(BOOK)), 'line': n, 'before': line.rstrip(), 'after': new.rstrip()})
    updated = ''.join(lines)
    if updated != old:
        old_fences = re.findall(r'```.*?```', old, re.S)
        new_fences = re.findall(r'```.*?```', updated, re.S)
        assert old_fences == new_fences
        path.write_text(updated)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'status': 'applied', 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                           'scope': 'Narrow spacing copyedit only; no semantic or source-listing changes. Final whole-book copyedit remains separate.',
                           'changes': changes, 'reviewed_paths': [str(p.relative_to(BOOK)) for p in paths],
                           'final_hashes': {str(p.relative_to(BOOK)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}, indent=2) + '\n')
print(json.dumps({'changed_lines': len(changes), 'reviewed_chapters': len(paths)}))
