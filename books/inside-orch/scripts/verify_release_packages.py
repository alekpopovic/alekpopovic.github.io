#!/usr/bin/env python3
"""Independently inspect ZIP inventories, hashes and frozen reader byte equality."""
import datetime
import hashlib
import json
import re
from pathlib import Path
import zipfile

BOOK = Path(__file__).resolve().parents[1]
DIST = BOOK / 'dist'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    results = {}
    for name, prefix in [('inside-orch-offline.zip', 'inside-orch/'), ('inside-orch-sources.zip', 'books/inside-orch/')]:
        with zipfile.ZipFile(DIST / name) as archive:
            names = archive.namelist()
            assert names == sorted(names), 'Archive names are not sorted'
            assert len(names) == len(set(names)), 'Duplicate ZIP entries'
            assert archive.testzip() is None, 'CRC failure'
            assert all(n.startswith(prefix) and '..' not in Path(n).parts for n in names), 'Unsafe path'
            assert all(i.date_time == (2026, 10, 13, 0, 0, 0) for i in archive.infolist()), 'Timestamp differs'
            manifest = json.loads(archive.read(prefix + 'PACKAGE-MANIFEST.json'))
            assert set(manifest['files']) == set(names) - {prefix + 'PACKAGE-MANIFEST.json'}, 'Manifest inventory differs'
            for member, expected in manifest['files'].items():
                content = archive.read(member)
                assert sha(content) == expected['sha256'] and len(content) == expected['bytes'], 'Member hash differs: ' + member
            if name == 'inside-orch-offline.zip':
                reader_files = [n for n in names if n.startswith(prefix + 'reader/')]
                for member in reader_files:
                    rel = member.removeprefix(prefix + 'reader/')
                    assert archive.read(member) == (DIST / 'online' / rel).read_bytes(), 'Browser-tested export differs'
                chapters = [n for n in reader_files if n.endswith('.html') and n.count('/') == 2 and not n.endswith('/index.html')]
                assert len(chapters) == 47, 'Incomplete reader sections'
                assert archive.read(prefix + 'reader/downloads/inside-orch.pdf') == (DIST / 'inside-orch.pdf').read_bytes()
                assert archive.read(prefix + 'reader/downloads/inside-orch.epub') == (DIST / 'inside-orch.epub').read_bytes()
                assert len([n for n in names if re.fullmatch(re.escape(prefix) + r'answers/ch\d\d\.md', n)]) == 40
                results[name] = {'reader_files_exactly_match_tested_export': len(reader_files), 'sections': len(chapters), 'numbered_chapter_answers': 40, 'appendix_answers': 1}
            else:
                assert not any('/evidence/orch/' in n or '/evidence/site/' in n or '/prompts/' in n or n.endswith(('.dump', '.sql', '.pem', '.key')) for n in names)
                assert len([n for n in names if '/manuscript/chapters/' in n and n.endswith('.md')]) == 40
                assert len([n for n in names if '/manuscript/appendices/' in n and n.endswith('.md')]) == 6
                assert len([n for n in names if re.search(r'/manuscript/solutions/ch\d\d\.md$', n)]) == 40
                assert len([n for n in names if '/labs/' in n and n.endswith('/lab.json') and '/validation/' not in n]) == 8
                assert prefix + 'scripts/package_release.py' in names
                results[name] = {'chapters': 40, 'appendices': 6, 'answers': 40, 'labs': 8, 'excluded_application_snapshot': True}
            results[name].update(member_hashes_verified=len(manifest['files']), crc_passed=True, sorted_order=True, fixed_timestamps=True, sha256=sha((DIST / name).read_bytes()))
    record = {'status': 'passed', 'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Separate standard-library ZIP reader verifies inventory/CRC/member hashes/path structure and exact browser-tested export bytes. System sha256sum verifies external checksum file separately.',
              'script_sha256': sha(Path(__file__).read_bytes()), 'packages': results}
    (BOOK / 'validation/publication/release-package-verification.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
