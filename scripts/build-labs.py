#!/usr/bin/env python3
"""Package original, local-only workshops reproducibly; no network requests."""
from pathlib import Path
import hashlib
import json
import zipfile
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'labs/ai-workshops'
destination = ROOT / 'assets/labs'
destination.mkdir(parents=True, exist_ok=True)
target = destination / 'ai-workshops.zip'
with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(source.rglob('*')):
        if not path.is_file() or path.suffix not in {'.md', '.mjs', '.json'}:
            continue
        entry = zipfile.ZipInfo('ai-workshops/' + path.relative_to(source).as_posix(), (2026, 10, 12, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o644 << 16
        archive.writestr(entry, path.read_bytes())
(destination / 'manifest.json').write_text(json.dumps({'file': target.name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'bytes': target.stat().st_size}, indent=2) + '\n')
print(f'Built local workshop archive ({target.stat().st_size} bytes).')

# Adapt only the Node imports. Acceptance assertions stay canonical.
workshops = yaml.safe_load((ROOT / '_data/workshops.yml').read_text())
for workshop in workshops:
    folder = source / workshop['id']
    tests = (folder / 'test.mjs').read_text()
    browser = tests.replace("import test from 'node:test';\n", '').replace("import assert from 'node:assert/strict';\n", '')
    browser, count = re.subn(r"await import\(process\.env\.LAB_SOLUTION === '1' \? './solution.mjs' : './app.mjs'\)", 'await import(applicationUrl)', browser)
    if count != 1 or 'node:' in browser or 'process.env' in browser:
        raise ValueError(f"Unsupported browser test adapter: {workshop['id']}")
    workshop.update(starter=(folder / 'app.mjs').read_text(), solution=(folder / 'solution.mjs').read_text(), tests=browser, display_tests=tests)
(destination / 'browser-workshops.json').write_text(json.dumps(workshops, ensure_ascii=False) + '\n')
