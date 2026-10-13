#!/usr/bin/env python3
"""Measure prose in the canonical reading order and separate worked answers."""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('orch_measure_publisher', BOOK / 'scripts/build.py')
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)

def words(path):
    # Markdown inline tokens omit URL destinations and fenced source/output blocks.
    # Keep technical identifiers and explanatory table cells as ordinary prose.
    text = []
    for token in publisher.MD.parse(path.read_text()):
        if token.type == 'inline':
            text.extend(child.content for child in token.children or []
                        if child.type in {'text', 'code_inline'})
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", ' '.join(text)))

ordered = publisher.selection()
answers = sorted((BOOK / 'manuscript/solutions').glob('*.md'))
assert len(answers) == 41, 'Forty chapter answers plus Appendix D answers required'
groups = {'reading_sections': ordered, 'worked_answers': answers,
          'separate_lab_guides': sorted((BOOK / 'labs').glob('[0-9][0-9]-*/README.md'))}
counts = {name: {p.relative_to(BOOK).as_posix(): words(p) for p in paths}
          for name, paths in groups.items()}
totals = {name: sum(values.values()) for name, values in counts.items()}
meaningful = totals['reading_sections'] + totals['worked_answers']
result = {'source_sha': publisher.meta()['source_sha'],
          'measured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'method': 'Markdown inline text and technical identifiers; no fenced code/output, URL destinations, build metadata or duplicated unified export. Separate lab guides reported but excluded from the editorial target.',
          'counts': counts, 'totals': totals, 'meaningful_manuscript_words': meaningful,
          'target': [85000, 110000], 'target_met': 85000 <= meaningful <= 110000,
          'inputs': {p.relative_to(BOOK).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                     for paths in groups.values() for p in paths}}
out = BOOK / 'validation/publication/manuscript-measurement.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'meaningful_manuscript_words': meaningful, 'totals': totals,
                  'target_met': result['target_met']}))
if not result['target_met']:
    raise SystemExit('Editorial word target not met')
