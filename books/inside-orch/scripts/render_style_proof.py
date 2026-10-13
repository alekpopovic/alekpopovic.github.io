#!/usr/bin/env python3
"""Typeset three real completed chapters as an explicit non-final design proof."""
import importlib.util
import hashlib
import json
from pathlib import Path
from weasyprint import HTML
from pypdf import PdfReader

BOOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('orch_proof_publisher', BOOK / 'scripts/build.py')
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)
paths = sorted((BOOK / 'manuscript/chapters').glob('*.md'))
chosen = [next(p for p in paths if p.name.startswith(n + '-')) for n in ['04', '09', '17']]
css = (BOOK / 'publication/print.css').read_text().replace('../../../assets/fonts/dm-sans.ttf', (BOOK / 'publication/fonts/dm-sans.ttf').as_uri()).replace('fonts/dejavu-sans-mono.ttf', (BOOK / 'publication/fonts/dejavu-sans-mono.ttf').as_uri())
body = '<section><h1>Typesetting proof</h1><p>Three completed chapters only. This is a design inspection artifact, not the complete edition or its release PDF.</p></section>'
body += ''.join('<section class="chapter">' + pub.render(p, 'print', paths) + '</section>' for p in chosen)
folder = BOOK / 'validation/publication/style-proof'
folder.mkdir(parents=True, exist_ok=True)
source = folder / 'proof.html'
source.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Inside orch · Typesetting proof</title><style>' + css + '</style></head><body>' + body + '</body></html>')
out = folder / 'proof.pdf'
HTML(filename=str(source)).write_pdf(out)
record = {'scope': 'Provisional typesetting proof of three actual chapters; not a complete-book build or final acceptance.', 'pages': len(PdfReader(out).pages), 'chapters': [p.name for p in chosen], 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest()}
(folder / 'build.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
