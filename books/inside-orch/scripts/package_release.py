#!/usr/bin/env python3
"""Package frozen local reader/source editions; never fetch, deploy or run labs."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import io
import json
import platform
import re
import stat
import zipfile
import zlib
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
DIST = BOOK / 'dist'
DATE = (2026, 10, 13, 0, 0, 0)
EXTENSIONS = {'.md', '.txt', '.json', '.csv', '.go', '.py', '.sh', '.yaml', '.yml', '.css', '.html', '.svg', '.png', '.ttf', '.cjs', '.xml', '.patch'}
SOURCE_DIRS = ('manuscript', 'examples', 'labs', 'exercises', 'scripts', 'tests', 'templates', 'editorial', 'reference', 'runbooks')
EVIDENCE_FILES = ('source-lock.json', 'commits.json', 'commits.csv', 'COMMIT_INDEX.md', 'prompt-commit-map.json', 'releases.json', 'link-lock.json')
PUBLICATION_FILES = ('REPRODUCE.md', 'RIGHTS.md', 'NOTICE.md', 'DESIGN_SYSTEM.md', 'style-tokens.json', 'print.css', 'offline.css', 'cover.svg', 'cover.png', 'book-metadata.json', 'CATALOG.md', 'catalog.json')
FORBIDDEN_PATH = re.compile(r'(^|/)(\.git|\.env(?:\..*)?|__pycache__|node_modules|prompts|credentials?)(/|$)|\.(dump|sql|pem|key|p12|pfx)$', re.I)
SECRET_PATTERNS = [re.compile(rb'-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----'), re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'), re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'), re.compile(rb'postgres(?:ql)?://[^\s"/]+:[^\s"@]+@')]
# Reviewed public CI/sample literals, never captured credentials. Bind exceptions
# to whole-file hashes so a changed password or surrounding content is rejected.
PUBLIC_FIXTURE_EXCEPTIONS = {
    'examples/source-excerpts/ch40-source-anchor.md': '251c2256f28f5fffb78f9fcb62996bb6e5807830fc70d69ac4ddeb98b0550084',
    'examples/source-excerpts/ch40-source-anchor.yaml': 'cffc82040c130216cdcecc708472a3e52d1e362b5e092ab6a0597932b8f53868',
    'tests/test_lab_database_guard.py': '89c91916a96c31b1ecd50bd883b4220de46095ed3a8566efd2dd5e129e2a9ce6',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def add_file(entries, name, path):
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(BOOK):
        raise ValueError('Not a regular book-owned file: ' + str(path))
    if FORBIDDEN_PATH.search(name) or name.startswith('/') or '..' in Path(name).parts:
        raise ValueError('Forbidden archive path: ' + name)
    data = path.read_bytes()
    if path.suffix.lower() in EXTENSIONS and path.suffix.lower() not in {'.png', '.ttf'}:
        if any(pattern.search(data) for pattern in SECRET_PATTERNS) and PUBLIC_FIXTURE_EXCEPTIONS.get(path.relative_to(BOOK).as_posix()) != digest(data):
            raise ValueError('Credential-like content; inspect without printing value: ' + name)
    if name in entries:
        raise ValueError('Duplicate archive path: ' + name)
    entries[name] = data

def add_tree(entries, prefix, directory, *, metadata_only=False):
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in selected tree: ' + str(path))
        if not path.is_file() or any(part.startswith('.') or part == '__pycache__' for part in path.relative_to(directory).parts):
            continue
        if path.suffix.lower() not in EXTENSIONS:
            continue
        rel = path.relative_to(BOOK).as_posix()
        if metadata_only and path.suffix.lower() not in {'.json', '.md', '.csv'}:
            continue
        # Packaging proof is outside its own input closure to avoid self-reference.
        if metadata_only and ('release-packag' in path.name or '095-package' in path.name or '095-checksum' in path.name):
            continue
        add_file(entries, prefix + rel, path)

def archive_bytes(entries, label, source_sha):
    manifest = {'schema_version': 1, 'package': label, 'source_sha': source_sha,
                'timestamp_utc': '2026-10-13T00:00:00Z', 'rights': 'All rights reserved; third-party materials retain their notices.',
                'files': {name: {'sha256': digest(data), 'bytes': len(data)} for name, data in sorted(entries.items())}}
    prefix = 'inside-orch/' if label == 'reader' else 'books/inside-orch/'
    entries = dict(entries)
    entries[prefix + 'PACKAGE-MANIFEST.json'] = (json.dumps(manifest, sort_keys=True, indent=2) + '\n').encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, DATE)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(info, data, compresslevel=9)
    return buffer.getvalue(), manifest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='validation/publication/release-packaging.json')
    args = parser.parse_args()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    meta = json.loads((BOOK / 'book.json').read_text())
    for gate in ('site-quality.json', 'native-site-acceptance.json', 'offline-reader.json'):
        if json.loads((BOOK / 'validation/publication' / gate).read_text())['status'] != 'passed':
            raise ValueError('Prerequisite gate has not passed: ' + gate)
    audit = json.loads((BOOK / 'validation/publication/material-audit.json').read_text())
    if digest((BOOK / 'publication/NOTICE.md').read_bytes()) != audit['notice_sha256']:
        raise ValueError('NOTICE differs from actual material audit')
    reader = {}
    for path in sorted((DIST / 'online').rglob('*')):
        if path.is_file():
            add_file(reader, 'inside-orch/reader/' + path.relative_to(DIST / 'online').as_posix(), path)
    for directory in ('examples', 'labs', 'exercises'):
        add_tree(reader, 'inside-orch/', BOOK / directory)
    for path in sorted((BOOK / 'manuscript/solutions').glob('*.md')):
        add_file(reader, 'inside-orch/answers/' + path.name, path)
    for name in EVIDENCE_FILES:
        add_file(reader, 'inside-orch/reference/' + name, BOOK / 'evidence' / name)
    for name in ('RIGHTS.md', 'NOTICE.md', 'REPRODUCE.md'):
        add_file(reader, 'inside-orch/' + name, BOOK / 'publication' / name)
    add_file(reader, 'inside-orch/book.json', BOOK / 'book.json')
    reader['inside-orch/OPEN-BOOK.txt'] = b'Open reader/index.html in a browser. All47sections and worked answers navigate without JavaScript or a server. PDFs/EPUB are under reader/downloads. External source/commit references require internet. SeeREPRODUCE.md for scoped reproduction.\n'

    source = {}
    for directory in SOURCE_DIRS:
        add_tree(source, 'books/inside-orch/', BOOK / directory)
    for name in ('book.json', 'BOOK_SPEC.md', 'SITE_WORKSPACE.md', 'AGENTS.md', '.gitignore'):
        add_file(source, 'books/inside-orch/' + name, BOOK / name)
    for name in EVIDENCE_FILES:
        add_file(source, 'books/inside-orch/evidence/' + name, BOOK / 'evidence' / name)
    for name in PUBLICATION_FILES:
        add_file(source, 'books/inside-orch/publication/' + name, BOOK / 'publication' / name)
    add_tree(source, 'books/inside-orch/', BOOK / 'publication/fonts')
    add_tree(source, 'books/inside-orch/', BOOK / 'publication/site-adapter')
    add_tree(source, 'books/inside-orch/', BOOK / 'validation', metadata_only=True)
    # These four already-published synthetic lab transcripts are linked by the
    # canonical text. Preserve their exact bytes so the source publisher works.
    for name in ('validation/labs/lab08-fixed-seed-fake-load.stdout.txt', 'validation/labs/lab05-security-local-probes.stdout.txt',
                 'validation/labs/lab04-rollout-observed.stdout.txt', 'validation/intake/docker-complete-flow-log-guard.stdout.txt'):
        add_file(source, 'books/inside-orch/' + name, BOOK / name)
    results = {}
    for label, entries, filename in [('reader', reader, 'inside-orch-offline.zip'), ('sources', source, 'inside-orch-sources.zip')]:
        data, manifest = archive_bytes(entries, label, meta['source_sha'])
        repeat, _ = archive_bytes(entries, label, meta['source_sha'])
        if data != repeat:
            raise ValueError('Repeated deterministic archive differs')
        with zipfile.ZipFile(io.BytesIO(data)) as check:
            if check.testzip() is not None:
                raise ValueError('Archive CRC failed')
            for name, values in manifest['files'].items():
                if digest(check.read(name)) != values['sha256']:
                    raise ValueError('Archive input hash mismatch: ' + name)
        (DIST / filename).write_bytes(data)
        results[filename] = {'sha256': digest(data), 'bytes': len(data), 'files': len(manifest['files']) + 1,
                             'repeat_bytes_identical': True, 'crc_and_member_hashes_passed': True,
                             'input_sha256': {name: digest(content) for name, content in sorted(entries.items())}}
    files = ['inside-orch.pdf', 'inside-orch.epub', 'inside-orch-offline.zip', 'inside-orch-sources.zip']
    (DIST / 'SHA256SUMS.txt').write_text(''.join(digest((DIST / name).read_bytes()) + '  ' + name + '\n' for name in files))
    evidence = {'status': 'passed', 'source_sha': meta['source_sha'], 'started_at_utc': started,
                'finished_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'command_scope': __doc__,
                'python': platform.python_version(), 'zlib_runtime': zlib.ZLIB_RUNTIME_VERSION,
                'archive_timestamp_utc': '2026-10-13T00:00:00Z', 'packages': results,
                'notice_sha256': audit['notice_sha256'], 'script_sha256': digest(Path(__file__).read_bytes()),
                'reviewed_public_fixture_exceptions': PUBLIC_FIXTURE_EXCEPTIONS,
                'exclusions': ['Immutable application/site snapshots and original prompts', 'Raw infrastructure dumps, all unselected terminal stdout/stderr/logs', 'Git/auth/environment configuration, dependency caches, binaries, unrelated site files', 'Self-referential packaging proof; later release/review stages are separate snapshots'],
                'credential_check_scope': 'Strict path/extension allowlists, no symlinks; private keys, common GitHub tokens and password-bearing PostgreSQL URI patterns rejected. Not an assertion of mathematically exhaustive secret detection.',
                'nondeterminism': 'Fixed archive input bytes produce identical ZIP bytes in this Python/zlib runtime. Re-running labs changes timestamps/timings; PDF producers/tool versions and platform font rasterization can change exported bytes.'}
    destination = (BOOK / args.output).resolve()
    if not destination.is_relative_to(BOOK / 'validation'):
        raise ValueError('Evidence destination must remain under validation')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'packages': {name: {k: v for k, v in values.items() if k != 'input_sha256'} for name, values in results.items()}}, indent=2))

if __name__ == '__main__':
    main()
