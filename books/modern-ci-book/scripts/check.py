#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate the canonical manuscript, source references and implementation map."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
import build

ROOT = Path(__file__).resolve().parents[1]


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_work_items(items: list[dict]) -> None:
    demand([x.get('id') for x in items] == [f'{i:03}' for i in range(80)],
           'Implementation work items must be unique and ordered 000–079')
    for item in items:
        demand(bool(item.get('title')), f"Missing title: {item['id']}")
        demand(item.get('status') in {'planned', 'in_progress', 'blocked', 'completed'},
               f"Invalid work status: {item['id']}")
        demand(bool(item.get('chapters')) and all(isinstance(c, int) and 1 <= c <= 24
               for c in item['chapters']), f"Invalid chapter map: {item['id']}")
        demand(isinstance(item.get('evidence'), list), f"Invalid evidence: {item['id']}")
        demand(item['status'] != 'completed' or bool(item['evidence']),
               f"Completion without evidence: {item['id']}")


def check() -> dict:
    paths = build.selection()
    demand(len(paths) == 30, 'Expected preface, 24 chapters and five appendices')
    demand(len(build.selection(True)) == 7, 'Unexpected sample selection')
    demand(set(build.selection(True)).issubset(set(paths)), 'Sample is outside the manuscript')
    sources = json.loads((ROOT/'sources.json').read_text())
    ids = {x['id'] for x in sources}
    demand(ids == {f'S{i:02}' for i in range(1, 25)}, 'Expected source IDs S01–S24')
    refs = (ROOT/'manuscript/e-sources.md').read_text()
    for source in sources:
        demand(f"## {source['id']}." in refs and source['url'] in refs,
               f"Reference mismatch: {source['id']}")
    headings = []
    words = 0
    for path in paths:
        text = path.read_text(encoding='utf-8')
        demand(len(re.findall(r'^# ', text, re.M)) == 1, f'One title required: {path.name}')
        demand(len(re.findall(r'^```', text, re.M)) % 2 == 0,
               f'Unclosed code fence: {path.name}')
        words += len(re.findall(r"\b[\w'-]+\b", text))
        headings.append(build.title(path))
        if re.match(r'\d{2}-', path.name) and not path.name.startswith('00-'):
            for section in ['## Exercise', '## Worked answer', '## Completion evidence']:
                demand(section in text, f'Missing {section}: {path.name}')
            demand(len(text.split()) >= 400, f'Chapter too short: {path.name}')
        for reference in re.findall(r'\[(S\d{2})\]', text):
            demand(reference in ids, f'Unknown source {reference}: {path.name}')
    # Ignore code literals and check actual parsed Markdown links.
    local_links = 0
    for path in ROOT.rglob('*.md'):
        if 'dist' in path.relative_to(ROOT).parts:
            continue
        for token in build.MD.parse(path.read_text(encoding='utf-8')):
            for child in token.children or []:
                if child.type != 'link_open':
                    continue
                href = child.attrGet('href') or ''
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                demand(target.is_relative_to(ROOT), f'Link escapes repository: {path}: {href}')
                demand(target.is_file(), f'Missing local link: {path.relative_to(ROOT)}: {href}')
                local_links += 1
    items = json.loads((ROOT/'implementation/work-items.json').read_text())
    check_work_items(items)
    for name in ['LICENSE.md', 'LICENSE-BOOK.md', 'LICENSE-CODE.txt', 'README.md',
                 'README.sr.md', 'CONTRIBUTING.md', 'SECURITY.md', 'CITATION.cff',
                 'examples/sql/schema.sql', 'examples/sql/claim.sql',
                 'examples/sql/complete.sql', 'publishing/GITHUB.md']:
        demand((ROOT/name).is_file(), f'Missing required file: {name}')
    return dict(manuscript_files=len(paths), chapters=24, appendices=5,
                manuscript_words=words, source_references=len(sources),
                implementation_items=len(items), local_markdown_links=local_links)


if __name__ == '__main__':
    try:
        print(json.dumps(check(), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        sys.exit(1)
