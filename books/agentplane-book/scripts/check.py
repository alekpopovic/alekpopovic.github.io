#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline source validation. Does not prove integration or deployment security."""
from __future__ import annotations
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from build import ROOT, markdown

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag=='a' and attrs.get('href'):self.links.append(attrs['href'])
        if tag=='img' and attrs.get('src'):self.links.append(attrs['src'])

def main() -> None:
    ignore={'.venv','.git','_site','.build','__pycache__','dist'}
    docs=[p for p in ROOT.rglob('*.md') if not any(x in ignore for x in p.relative_to(ROOT).parts)]
    parsed={};errors=[]
    for p in docs:
        text=p.read_text(encoding='utf-8')
        parser=Links();parser.feed(markdown(text));parsed[p.resolve()]=parser
        fences=[line.strip() for line in text.splitlines() if line.startswith('```')]
        if len(fences)%2:errors.append(f'{p.relative_to(ROOT)}: unbalanced code fences')
    for p,parser in parsed.items():
        for link in parser.links:
            url=urlsplit(link)
            if url.scheme or link.startswith('//'):continue
            target=(p.parent/unquote(url.path)).resolve() if url.path else p
            if not target.is_relative_to(ROOT):
                errors.append(f'{p.relative_to(ROOT)}: path escapes repository: {link}');continue
            if not target.exists():errors.append(f'{p.relative_to(ROOT)}: missing {link}')
            elif url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:
                errors.append(f'{p.relative_to(ROOT)}: missing fragment {link}')
    meta=json.loads((ROOT/'book/book.json').read_text())
    if len(meta['chapters'])!=28:errors.append('expected 28 chapters')
    prompts=list((ROOT/'prompts').glob('[0-9][0-9]-*.md'))
    if len(prompts)!=45:errors.append('expected 45 implementation prompts')
    for c in meta['chapters']:
        if len((ROOT/c['path']).read_text().split())<350:errors.append(f'chapter unexpectedly short: {c["path"]}')
    for p in ROOT.rglob('*'):
        if p.is_file() and not any(x in ignore for x in p.relative_to(ROOT).parts):
            if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.key','.p12','.kubeconfig'}:
                errors.append(f'prohibited distributed file: {p.relative_to(ROOT)}')
    if errors:
        print('\n'.join(errors),file=sys.stderr);raise SystemExit(1)
    print(f'PASS: {len(docs)} Markdown files, 28 chapters, 45 prompts; local links, fragments and fence checks.')
    print('External URLs, SQL execution and Kubernetes behavior are not checked by this command.')
if __name__=='__main__':main()
