#!/usr/bin/env python3
"""Regenerate exact contiguous excerpts from the source lock."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'evidence/source-lock.json').read_text())
registered={f['path']:f for f in lock['files']}
registry_path=ROOT/'examples/source-excerpts/registry.json'
registry=json.loads(registry_path.read_text())
for item in registry:
    rel=item['source_path']
    if rel not in registered:raise ValueError('Unknown source path: '+rel)
    if item['source_sha']!=lock['baseline_sha']:raise ValueError('Only baseline extraction supported; use a separately verified historical checkout')
    source=ROOT/'evidence/orch'/rel
    raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=registered[rel]['sha256']:raise ValueError('Source changed: '+rel)
    lines=raw.decode('utf-8').splitlines(keepends=True)
    start,end=item['line_start'],item['line_end']
    if not 1<=start<=end<=len(lines):raise ValueError('Invalid interval: '+item['id'])
    excerpt=''.join(lines[start-1:end])
    item['sha256']=hashlib.sha256(excerpt.encode()).hexdigest()
    item['source_url']=f"https://github.com/alekpopovic/orch/blob/{item['source_sha']}/{rel}#L{start}-L{end}"
    extension={'go':'go','sql':'sql','yaml':'yaml'}.get(item['language'],'txt')
    target=ROOT/'examples/source-excerpts'/(item['id']+'.'+extension)
    target.write_text(excerpt)
    (target.with_suffix('.md')).write_text(f"# {item['id']}\n\n{item['purpose']}\n\nUnchanged, contiguous source excerpt: [{rel}, lines {start}–{end}]({item['source_url']}).\n\n```{item['language']}\n{excerpt.rstrip()}\n```\n\nSHA-256: `{item['sha256']}`. This excerpt is not an independently compilable program.\n")
registry_path.write_text(json.dumps(registry,indent=2)+'\n')
print(json.dumps({'status':'passed','exact_excerpts':len(registry),'source_sha':lock['baseline_sha']}))
