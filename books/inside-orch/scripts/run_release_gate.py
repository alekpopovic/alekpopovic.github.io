#!/usr/bin/env python3
"""Join real edition evidence and verify its frozen inputs; never publish."""
import argparse, csv, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

BOOK=Path(__file__).resolve().parents[1]
SITE=BOOK.parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--complete-tracker',action='store_true')
a=p.parse_args()
errors=[]
checks=[]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads((BOOK/path).read_text())
def demand(ok,message):
    if not ok: errors.append(message)
def record(path):
    data=load(path)
    status=data.get('status',data.get('overall_status',''))
    demand(status.startswith('passed'),path+': '+status)
    checks.append({'path':path,'sha256':sha(BOOK/path),'status':status})
    return data

lock=load('evidence/source-lock.json')
for entry in lock['files']:
    path=BOOK/'evidence/orch'/entry['path']
    demand(path.is_file() and sha(path)==entry['sha256'],'Immutable source changed: '+entry['path'])
rows=list(csv.DictReader((BOOK/'state/execution-tracker.csv').open()))
demand(len(rows)==100 and [r['id'] for r in rows]==[f'{i:03d}' for i in range(100)],'Tracker sequence')
tracker=[]
for row in rows:
    required=a.complete_tracker or int(row['id'])<96
    if required: demand(row['status']=='done','Unfinished prerequisite '+row['id'])
    if row['status']=='done':
        evidence=[x.strip() for x in row['evidence'].split(';') if x.strip()]
        demand(bool(evidence),'Missing evidence list '+row['id'])
        for name in evidence:
            path=(BOOK/name).resolve()
            demand(path.is_relative_to(BOOK) and path.is_file(),'Missing or unsafe evidence '+row['id']+': '+name)
        tracker.append({'id':row['id'],'evidence':evidence})

formats={ext:sha(BOOK/f'dist/inside-orch.{ext}') for ext in ['pdf','epub']}
for ext,digest in formats.items():
    for base in [SITE/'assets/books/inside-orch/downloads',SITE/'_site/assets/books/inside-orch/downloads',BOOK/'dist/online/downloads']:
        demand(sha(base/f'inside-orch.{ext}')==digest,'Different public/offline '+ext)
for name in ['pdf-build','epub-build']:
    build=load('validation/publication/'+name+'.json')
    for path,digest in build['inputs'].items():
        demand(sha(BOOK/path)==digest,'Changed export input '+path)
measurement=load('validation/publication/manuscript-measurement.json')
for path,digest in measurement['inputs'].items(): demand(sha(BOOK/path)==digest,'Changed measured manuscript '+path)
demand(measurement['target_met'] and measurement['meaningful_manuscript_words']==101211,'Word measurement')

for name in ['excerpt-sync','code-compilation','lab-execution','architect-review','developer-review','devops-review','security-review','claim-guarantee-audit','command-api-fidelity','copyedit','exercises-solutions','evidence-link-lock']:
    record('validation/reviews/'+name+'.json')
for name in ['metadata-cover-catalog-review','pdf-typesetting-acceptance','pdf-visual-review','epub-publication-acceptance','epub-reading-preview','native-adapter-acceptance','native-publisher-acceptance','site-integration-acceptance','site-quality','native-site-acceptance','material-audit','offline-reader','release-packaging']:
    data=record('validation/publication/'+name+'.json')
    if name in ['pdf-visual-review','pdf-typesetting-acceptance','native-adapter-acceptance','native-publisher-acceptance','site-integration-acceptance','material-audit']:
        demand(data['pdf_sha256']==formats['pdf'],'Stale final PDF acceptance '+name)
    if name=='epub-reading-preview': demand(data['epub_sha256']==formats['epub'],'Stale EPUB preview')
structure=record('validation/publication/format-structure.json')
demand(structure['pdf_sha256']==formats['pdf'] and structure['epub_sha256']==formats['epub'],'Stale format structure')
demand(structure['pdf_pages']==546 and structure['reading_sections']==47,'Measured final format count')
labs=load('validation/labs/summary.json')['ordered_labs']
demand(len(labs)==8 and all(x['status']=='passed' for x in labs),'Eight executed mandatory labs')
for lab in labs: demand((BOOK/lab['result']).is_file(),'Missing actual lab '+lab['lab_id'])
for name in ['final-notice-site-build','final-notice-jekyll-build','notice-rebuild-books-check','notice-rebuild-site-check','final-content-check','workspace-six-books-ui','final-performance','notice-rebuild-native-site-check','invariant-table-publisher-tests']:
    data=record('validation/publication/'+name+'.json')
    demand(data['exit_code']==0,'Nonzero final check '+name)
demand(load('validation/labs/owned-postgres-cleanup.json')['exit_code']==0,'Owned database cleanup failed')
absence=load('validation/labs/owned-postgres-absence.json')
demand(absence['exit_code']==0 and not (BOOK/absence['stdout']).read_text().strip(),'Owned database remains')
checksum=subprocess.run(['sha256sum','-c','SHA256SUMS.txt'],cwd=BOOK/'dist',capture_output=True,text=True)
demand(checksum.returncode==0,'Archive checksum mismatch')
commands=[]
for command in [[sys.executable,str(BOOK/'scripts/verify_pack.py')],[sys.executable,str(BOOK/'scripts/check_manuscript.py'),'--strict']]:
    result=subprocess.run(command,cwd=SITE,capture_output=True,text=True)
    commands.append({'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    demand(result.returncode==0,'Structural/corpus command failed')
boundaries=[
 'Default MemoryService is process-local; PostgreSQL schema/store is not the active server state owner.',
 'Ordinary assignment is distinct from optional scheduler.Plan/store reconciler; task CAS is not a global resource fence.',
 'Ordinary resource values do not reach AgentTask/ContainerSpec/HostConfig; direct adapter limits and volume eligibility are distinct.',
 'Desired stop accounting, rollout success and drain completion can precede physical stop; partitions have no network fencing.',
 'HA advisory-lock cancellation can retain a pooled-session lock; HA/autoscaler packages are not wired default leadership.',
 'GitOps applies are partial; logical namespaces/local volumes are not hostile kernel isolation/distributed storage.',
 'Image digest parsing is not enforced supply-chain verification; plugins/billing/overlay designs remain proposals.',
 'The original PostgreSQL fixture still has two failures from its fourteen-migration setup; the separately labelled full-sixteen-schema extension passed.',
 'Baseline six external skips, fake-load measurements and optional unrun procedures remain explicitly scoped.'
]
limitations=[
 'Local reviewable edition only: no push, PR, default-branch publication, live deployment or production fitness certification.',
 'Source/engineering/visual review was performed by AI agents with independent lenses; no external human endorsement is invented. Owner review remains the publication handoff.',
 'Browser evidence is actual installed Chrome on Linux; no proprietary e-reader or Safari/Firefox hardware compatibility claim.',
 'Full UI run had151passes/one stale five-book assertion; corrected six-book test passed separately. This is152distinct test coverage, not a fabricated zero-exit full rerun.',
 'All546 final PDF rasters match the actually reviewed edition; rebuilt PDF byte hash differs. No bit-for-bit PDF rebuild promise.',
 'Source/reader archive validation metadata is a timestamped snapshot; later gate/review records are carried separately in the final handoff.'
]
report={'status':'failed' if errors else 'passed_local_edition_gate','checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'source_sha':lock['baseline_sha'],'source_files_verified':len(lock['files']),'artifacts':formats,
 'meaningful_words':measurement['meaningful_manuscript_words'],'pdf_pages':structure['pdf_pages'],
 'reading_sections':47,'numbered_chapters':40,'appendices':6,'mandatory_labs':8,
 'tracker_audit':tracker,'complete_tracker_requested':a.complete_tracker,'evidence':checks,'commands':commands,
 'checksum_stdout':checksum.stdout,'critical_boundaries':boundaries,'blockers':errors,'limitations':limitations,
 'decision':'Ready for independent skeptical-reader review097 and a local release handoff; no deployment authorization.'}
(BOOK/'validation/release-gate.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Inside orch — exact local edition gate','',report['status']+' at '+report['checked_at_utc']+'.','',
 'Source `'+lock['baseline_sha']+'`;40chapters,6appendices,preface;101,211meaningfulwords;546PDFpages;8actuallyexecutedboundedlaboratories.','',
 'PDF SHA256 `'+formats['pdf']+'`; EPUB SHA256 `'+formats['epub']+'`.','',
 'The machine record [release-gate.json](release-gate.json) records every joined evidence hash, tracker-evidence path, exact export-input check, executed corpus/strict command and archive checksum result. A done tracker value was never accepted as sole proof.','',
 '## Critical boundaries','']+['- '+x for x in boundaries]+['','## Remaining limitations and publication boundary','']+['- '+x for x in limitations]+['','## Decision','',report['decision'],'','Blocking findings: '+('none.' if not errors else '; '.join(errors)), '']
(BOOK/'validation/RELEASE_GATE.md').write_text('\n'.join(lines))
print(json.dumps({'status':report['status'],'blockers':errors,'pdf_pages':546,'words':101211}))
raise SystemExit(bool(errors))
