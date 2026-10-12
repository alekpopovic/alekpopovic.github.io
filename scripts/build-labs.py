#!/usr/bin/env python3
"""Package original, local-only workshops reproducibly; no network requests."""
from pathlib import Path
import hashlib
import json
import zipfile

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
