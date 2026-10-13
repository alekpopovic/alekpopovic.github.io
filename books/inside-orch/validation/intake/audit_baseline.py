#!/usr/bin/env python3
"""Read-only intake audit. No Git database or application execution is required."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

BOOK = Path(__file__).resolve().parents[2]
SITE = BOOK.parents[1]
SOURCE = BOOK / 'evidence/orch'
lock = json.loads((BOOK / 'evidence/source-lock.json').read_text())
site_lock = json.loads((BOOK / 'evidence/site-lock.json').read_text())
commits = json.loads((BOOK / 'evidence/commits.json').read_text())
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=SITE, text=True).strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected = {f['path']: f for f in lock['files']}
actual = {str(p.relative_to(SOURCE)): p for p in SOURCE.rglob('*') if p.is_file()}
require(set(expected) == set(actual), 'Snapshot file membership differs from the source lock')
for name, record in expected.items():
    path = SOURCE / name
    require(path.is_file(), 'Missing source: ' + name)
    if path.is_file():
        require(path.stat().st_size == record['bytes'], 'Source size changed: ' + name)
        require(digest(path) == record['sha256'], 'Source hash changed: ' + name)
require(not (SOURCE / '.git').exists(), 'Evidence snapshot must not contain a Git database')

# The ZIP exports file bytes without executable bits. Recover Git file modes
# from the ordered, supplied commit diffs without chmod or git init in evidence.
modes = {}
for commit in commits:
    patch_path = BOOK / 'evidence/commit-diffs' / (commit['sha'] + '.patch')
    require(patch_path.is_file(), 'Missing commit diff: ' + commit['sha'])
    if not patch_path.is_file():
        continue
    patch = patch_path.read_text()
    for section in re.split(r'(?=^diff --git )', patch, flags=re.M):
        header = re.match(r'diff --git a/(.+) b/(.+)\n', section)
        if not header:
            continue
        old, new = header.groups()
        previous = re.search(r'^old mode ([0-9]+)$', section, re.M)
        if previous:
            modes.setdefault(old, previous.group(1))
        if old != new and old in modes:
            modes[new] = modes.pop(old)
        replacement = re.search(r'^(?:new file mode|new mode) ([0-9]+)$', section, re.M)
        if replacement:
            modes[new] = replacement.group(1)
        if re.search(r'^deleted file mode ', section, re.M):
            modes.pop(old, None)

def object_sha(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).digest()

tree = {}
for name, path in actual.items():
    node = tree
    parts = name.split('/')
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = (modes.get(name, '100644'), object_sha('blob', path.read_bytes()))

def tree_sha(node):
    entries = []
    for name, value in node.items():
        mode, sha = ('40000', tree_sha(value)) if isinstance(value, dict) else value
        order = (name + ('/' if mode == '40000' else '')).encode()
        entries.append((order, mode.encode() + b' ' + name.encode() + b'\0' + sha))
    return object_sha('tree', b''.join(raw for _, raw in sorted(entries)))

reconstructed_tree_sha = tree_sha(tree).hex()
require(reconstructed_tree_sha == lock['tree_sha'], 'Reconstructed Git tree differs from the source lock')
require(len(commits) == lock['reachable_commit_count'] == 105, 'Expected 105 commit records')
require(lock['baseline_sha'] in {c['sha'] for c in commits}, 'Locked commit absent from history records')
originals = json.loads((BOOK / 'evidence/original-prompts.json').read_text())
require([p['id'] for p in originals] == list(range(91)), 'Expected development prompts 00–90')
require(all((SOURCE / p['path']).is_file() for p in originals), 'Missing original prompt')
migrations = sorted((SOURCE / 'migrations').glob('*.up.sql'))
require(len(migrations) == 16, 'Expected 16 migration pairs')
require(all(p.with_name(p.name.replace('.up.sql', '.down.sql')).is_file() for p in migrations),
        'Missing down migration')

before = json.loads((BOOK / 'validation/intake/source-before.json').read_text())
before_files = {p['path']: p['sha256'] for p in before['files']}
require(before_files == {name: digest(p) for name, p in actual.items()}, 'Immutable evidence changed during intake')
supplied = json.loads((BOOK / 'validation/intake/pack-before.json').read_text())
changed_supplied = [name for name, sha in supplied.items() if not (BOOK/name).is_file() or digest(BOOK/name) != sha]
require(not set(changed_supplied) - {'state/execution-tracker.csv'}, 'Existing supplied pack files overwritten')

site_comparison = []
for record in site_lock['files']:
    name = record['path']
    snapshot = BOOK / 'evidence/site' / name
    require(snapshot.is_file() and digest(snapshot) == record['sha256'], 'Site evidence changed: '+name)
    current = SITE / name
    unchanged = current.is_file() and digest(current) == record['sha256']
    site_comparison.append(dict(path=name, matches_locked_snapshot=unchanged))
    require(unchanged or name == '_config.yml', 'Unexpected site contract change: '+name)

head = git('rev-parse', 'HEAD')
require(head == site_lock['baseline_sha'], 'Current site revision differs from inspected revision')
require(git('remote', 'get-url', 'origin') in {
    'git@github.com:alekpopovic/alekpopovic.github.io.git',
    'https://github.com/alekpopovic/alekpopovic.github.io.git',
    'https://github.com/alekpopovic/alekpopovic.github.io'}, 'Incorrect website origin')
config_before = (BOOK / 'evidence/site/_config.yml').read_text()
config_after = (SITE / '_config.yml').read_text()
require(config_after == config_before.replace('  - books/universal-tracking-technical-book\n',
    '  - books/universal-tracking-technical-book\n  - books/inside-orch\n'),
    'Configuration differs beyond the canonical book exclusion')
for rel in ['book-pages/inside-orch/index.md', 'assets/books/inside-orch/downloads/inside-orch.pdf', '_data/books.json']:
    result = subprocess.run(['git','check-ignore','-q',rel], cwd=SITE)
    require(result.returncode == 0, 'Generated path is not ignored: ' + rel)
require('inside-orch' not in (SITE / 'scripts/book_catalog.py').read_text(), 'Incomplete book was registered')
metadata = json.loads((BOOK / 'book.json').read_text())
require(metadata['author'] == 'Aleksandar Popovic' and metadata['language'] == 'en', 'Incorrect canonical metadata')
require(metadata['edition'] == '1.0 planned' and metadata['status'] == 'generation_pack', 'Premature edition status')
workspace = json.loads((BOOK / 'state/workspace.json').read_text())
lab_root = Path(workspace['paths']['lab_working_root'])
require(lab_root.is_dir() and not lab_root.is_relative_to(SITE), 'Lab directory is not isolated')
for rel in ['manuscript/chapters', 'manuscript/appendices', 'manuscript/solutions',
            'examples/teaching-extensions', 'validation/labs', 'validation/evidence', 'dist']:
    require((BOOK / rel).is_dir(), 'Missing canonical directory: ' + rel)
require((BOOK / 'manuscript/README.md').is_file(), 'Missing manuscript scope note')
require((SITE / '_site').is_dir(), 'Site build has not produced an output directory')
require(not (SITE / '_site/books/inside-orch').exists(), 'Raw canonical pack leaked into site output')
require(not (SITE / '_site/assets/books/inside-orch').exists(), 'Incomplete book has public generated files')
generated_catalog = json.loads((SITE / '_data/books.json').read_text())
require('inside-orch' not in {b['id'] for b in generated_catalog}, 'Incomplete book present in generated catalog')

result = dict(
    status='failed' if errors else 'passed', checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='Intake integrity and site binding only; no orch builds, tests, labs, or book releases executed.',
    source_sha=lock['baseline_sha'], locked_tree_sha=lock['tree_sha'], reconstructed_tree_sha=reconstructed_tree_sha,
    tree_method='Git blob/tree SHA-1 from snapshot bytes; file modes recovered from supplied chronological commit diffs.',
    source_files_checked=len(actual), source_snapshot_unchanged=before_files=={name:digest(p) for name,p in actual.items()},
    original_prompts_available=len(originals), commit_records_available=len(commits),
    commit_diffs_available=len(list((BOOK/'evidence/commit-diffs').glob('*.patch'))),
    migration_pairs=len(migrations), tags_recorded_from_source_lock=lock['tags'],
    site_sha=head, site_branch=git('branch','--show-current'), site_contract=site_comparison,
    supplied_pack_changes=changed_supplied, source_git_database_present=False,
    canonical_pack_absent_from_site_output=not (SITE / '_site/books/inside-orch').exists(),
    generated_catalog_ids=[b['id'] for b in generated_catalog],
    lab_working_directory=str(lab_root),
    source_commit_provenance='Commit SHA is in supplied lock/history records; no local commit object database is available.',
    errors=errors)
(BOOK/'validation/intake/baseline-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(1 if errors else 0)
