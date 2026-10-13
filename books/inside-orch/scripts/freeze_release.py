#!/usr/bin/env python3
"""Freeze already-reviewed files in a local release ZIP; no build or deployment."""
import hashlib, importlib.metadata, importlib.util, io, json, platform, stat, zipfile
from datetime import datetime, timezone
from pathlib import Path

BOOK=Path(__file__).resolve().parents[1]
DIST=BOOK/'dist'
def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads((BOOK/path).read_text())
gate=load('validation/release-gate.json')
assert gate['status']=='passed_local_edition_gate' and not gate['blockers']
review=load('validation/reviews/final-findings.json')
assert review['status']=='passed' and not review['remaining_blockers']
assert review['gate_sha256']==sha((BOOK/'validation/release-gate.json').read_bytes())
for lens in review['lenses']:
    assert sha((BOOK/lens['report']).read_bytes())==lens['sha256']
    assert sha((BOOK/lens['narrative_report']).read_bytes())==lens['narrative_sha256']
measurement=load('validation/publication/manuscript-measurement.json')
assert measurement['meaningful_manuscript_words']==gate['meaningful_words']
for name,digest in measurement['inputs'].items():
    assert sha((BOOK/name).read_bytes())==digest,name
spec=importlib.util.spec_from_file_location('inside_orch_publisher',BOOK/'scripts/build.py')
publisher=importlib.util.module_from_spec(spec);spec.loader.exec_module(publisher)
assert (DIST/'inside-orch.md').read_text()==publisher.assemble()
for ext,digest in gate['artifacts'].items(): assert sha((DIST/f'inside-orch.{ext}').read_bytes())==digest
for name,record in load('validation/publication/release-package-verification.json')['packages'].items():
    assert sha((DIST/name).read_bytes())==record['sha256'], name
files={}
for name in ['inside-orch.pdf','inside-orch.epub','inside-orch.md','inside-orch-offline.zip','inside-orch-sources.zip']:
    assert (DIST/name).is_file() and not (DIST/name).is_symlink(),name
    files[name]=(DIST/name).read_bytes()
extras=[
 'book.json','publication/cover.png','publication/RIGHTS.md','publication/NOTICE.md',
 'publication/REPRODUCE.md','publication/RELEASE_NOTES.md','publication/HANDOFF.md',
 'publication/site-adapter/changes.patch','publication/site-adapter/source-generated-manifest.json',
 'validation/RELEASE_GATE.md','validation/release-gate.json',
 'validation/reviews/final-independent-review.md','validation/reviews/final-findings.json',
 'validation/reviews/final-reader-developer.json','validation/reviews/final-reader-devops.json',
 'validation/reviews/final-reader-developer.md','validation/reviews/final-reader-devops.md',
 'validation/reviews/final-reader-architect.md',
 'validation/reviews/final-reader-architect.json','validation/publication/pdf-rebuild-equivalence.json',
 'validation/publication/pdf-visual-review.json','validation/publication/pdf-range-report-history.json',
 'validation/publication/pdf-visual-source-review.json','validation/publication/pdf-visual-lab-review.json',
 'validation/publication/epub-validation.json','validation/publication/epub-validation.md',
 'validation/publication/manuscript-measurement.json',
 'validation/publication/site-quality.json','validation/publication/release-package-verification.json',
 'scripts/freeze_release.py','state/execution-tracker.csv']
for name in extras:
    path=BOOK/name
    assert path.is_file() and not path.is_symlink(), name
    files['edition/'+name]=path.read_bytes()
versions={'python':platform.python_version()}
for name in ['weasyprint','pypdf','markdown-it-py','Pillow']:
    versions[name]=importlib.metadata.version(name)
manifest={
 'schema_version':1,'edition':'1.0','edition_date':'2026-10-13','author':'Aleksandar Popovic',
 'title':'Inside orch: Building and Operating a Docker Orchestrator in Go',
 'status':'complete_local_reviewed_edition','source_sha':gate['source_sha'],
 'website_baseline_sha':'80801c8d3d97a4d8ff78e0fe69f3f902beda00c0',
 'frozen_at_utc':datetime.now(timezone.utc).isoformat(),
 'manuscript_sha256':sha(files['inside-orch.md']),
 'meaningful_words':gate['meaningful_words'],'word_measurement':measurement['method'],
 'word_count_breakdown':measurement['totals'],
 'pdf_pages':gate['pdf_pages'],'reading_sections':gate['reading_sections'],
 'numbered_chapters':gate['numbered_chapters'],'appendices':gate['appendices'],'executed_labs':gate['mandatory_labs'],
 'rights':'All rights reserved; exact source and bundled third-party assets retain their original rights/notices.',
 'tool_versions':versions,'release_gate_sha256':sha(files['edition/validation/release-gate.json']),
 'independent_review_sha256':sha(files['edition/validation/reviews/final-findings.json']),
 'source_package_snapshot':'Prompt 095 editable inputs and validation metadata frozen before later 096–099 steps. Later gate/review/handoff and freeze tool are separate edition members.',
 'tracker_snapshot':'Actual tracker at archive assembly: completed preceding tasks; 098/099 may still be in progress/pending. Final author-facing tracker remains canonical outside this frozen archive.',
 'nondeterminism':'Same archive input bytes use fixed ordered ZIP metadata; rebuilding PDF can change its bytes even with 546 identical raster pages. Preserve the reviewed exports.',
 'deployment':'None; local branch and patch only.',
 'files':{name:{'sha256':sha(data),'bytes':len(data)} for name,data in sorted(files.items())}}
(BOOK/'publication/edition-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
files['EDITION-MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
def encode():
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo('inside-orch-1.0/'+name,(2026,10,13,0,0,0))
            info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data,compresslevel=9)
    return stream.getvalue()
data=encode();assert data==encode()
path=DIST/'inside-orch-release.zip';path.write_bytes(data)
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    for name,content in files.items(): assert z.read('inside-orch-1.0/'+name)==content
names=['inside-orch.pdf','inside-orch.epub','inside-orch-offline.zip','inside-orch-sources.zip','inside-orch-release.zip']
(DIST/'SHA256SUMS.txt').write_text(''.join(sha((DIST/name).read_bytes())+'  '+name+'\n' for name in names))
result={'status':'passed','frozen_at_utc':manifest['frozen_at_utc'],'source_sha':gate['source_sha'],
 'release_zip_sha256':sha(data),'release_zip_bytes':len(data),'members':len(files),
 'repeated_encoding_identical':True,'crc_and_exact_member_bytes_passed':True,
 'edition_manifest_sha256':sha((BOOK/'publication/edition-manifest.json').read_bytes()),
 'scope':'Archive assembly of existing exact reviewed exports; no regeneration or deployment.'}
(BOOK/'validation/publication/final-release-archive.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
