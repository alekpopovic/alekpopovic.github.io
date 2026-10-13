from pathlib import Path
import sys,json,hashlib,datetime,zipfile,re,collections
B=Path(__file__).resolve().parents[2];S=B.parents[1];sys.path.insert(0,str(S/'scripts'))
from book_catalog import orch_publication as p
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat();meta=json.loads((B/'book.json').read_text());selected=p.companions();assert len(selected)==152
assert B/'publication/NOTICE.md' not in selected
items=[]
for f in sorted(selected):
 rel=f.relative_to(B).as_posix()
 if rel.startswith('manuscript/solutions/'):cls='original_worked_answers'
 elif rel.startswith(('labs/','exercises/')) and f.suffix=='.md':cls='original_lab_and_exercise_guidance'
 elif rel.startswith('examples/teaching-extensions/') and f.suffix in {'.go','.py'}:cls='original_or_explicitly_adapted_teaching_code'
 elif rel.startswith(('scripts/','tests/')):cls='original_book_execution_helper'
 elif rel.startswith('examples/source-excerpts/'):cls='pinned_source_attribution_metadata'
 elif f.suffix=='.png':cls='original_source_checked_diagram'
 elif rel.startswith(('validation/','exercises/')):cls='bounded_execution_or_claim_record'
 elif f.suffix=='.md':cls='original_design_note'
 else:cls='original_fixture'
 items.append({'path':rel,'bytes':f.stat().st_size,'sha256':sha(f),'material_class':cls,'origin':'Inside orch canonical book source; pinned Orch API/source associations retained where applicable.','rights':'Original book material retains the owner’s all-rights-reserved decision. Exact upstream snippets or adapted behavior references preserve their source attribution; no application or dependency relicense.','published_by':'Explicit source-reference traversal; not an implicit snapshot or module copy.'})
fonts=[];notices={}
for f in meta['typesetting_fonts']:
 fp=B/f['path'];np=B/f['notice_path'];assert sha(fp)==f['sha256']
 text=np.read_text()
 if np.name.endswith('OFL.txt'):assert 'SIL OPEN FONT LICENSE' in text and ('Copyright' in text or 'copyright' in text)
 else:assert 'Bitstream' in text and 'Permission is hereby granted' in text and 'DejaVu changes are in public domain' in text
 notices[f['notice_path']]={'path':f['notice_path'],'bytes':np.stat().st_size,'sha256':sha(np),'license':'SIL Open Font License 1.1' if 'OFL' in np.name else 'Retained Bitstream Vera license; DejaVu changes public domain','verified_against':'Actual retained notice text, not go.sum or inferred dependency metadata.'}
 fonts.append({'path':f['path'],'sha256':sha(fp),'bytes':fp.stat().st_size,'notice_path':f['notice_path'],'scope':f['scope']})
assert len(fonts)==5 and len(notices)==4
mark=B/'evidence/orch/docs/assets/orch-mark.svg';inner=re.sub(r'^.*?<svg[^>]*>|</svg>\s*$','',mark.read_text(),flags=re.S);assert inner in (B/'publication/cover.svg').read_text()
fontlog=B/'validation/publication/material-pdf-fonts-notice-command.stdout.txt';fontrows=[]
for line in fontlog.read_text().splitlines()[2:]:
 if not line.strip():continue
 fields=line.split();assert fields[-5:-2]==['yes','yes','yes'],fields
 fontrows.append({'postscript_subset_name':fields[0],'embedded':True,'subset':True,'unicode_map':True})
assert len(fontrows)==17
with zipfile.ZipFile(B/'dist/inside-orch.epub') as z:
 media=[{'path':n,'bytes':len(z.read(n)),'sha256':hashlib.sha256(z.read(n)).hexdigest()} for n in z.namelist() if '/media/' in n]
 assert {x['path'] for x in media}=={'EPUB/media/cover.png','EPUB/media/examples/diagrams/task-lifecycle.png'}
 assert z.read('EPUB/media/cover.png')==(B/'publication/cover.png').read_bytes()
 assert z.read('EPUB/media/examples/diagrams/task-lifecycle.png')==(B/'examples/diagrams/task-lifecycle.png').read_bytes()
 assert not any(n.endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
 forbidden_parts={'vendor','node_modules','.git','.book-labs','GOMODCACHE'};scanned=[];violations=[]
for root in [S/'assets/books/inside-orch',B/'dist']:
 for f in sorted(root.rglob('*')):
  if not f.is_file():continue
  scanned.append(str(f.relative_to(S)))
  data=f.read_bytes();parts=set(f.relative_to(root).parts)
  if forbidden_parts&parts or f.suffix in {'.exe','.so','.a','.o'} or data.startswith((b'\x7fELF',b'MZ',b'\xca\xfe\xba\xbe')):violations.append(str(f.relative_to(S)))
assert not violations,violations
source_licenses=[str(f.relative_to(B/'evidence/orch')) for f in (B/'evidence/orch').rglob('*') if f.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE)',f.name,re.I)]
assert not source_licenses
addendum='''\n## Completed local-edition material audit — October 13, 2026\n\nThe final local candidate’s distributed material was inspected in `validation/publication/material-audit.json`. Its explicit companion traversal contains 152 files: original worked answers, laboratory/exercise guidance and teaching helpers, source-attribution metadata, bounded execution/claim records, fixtures and one source-checked lifecycle diagram. These files do not include vendored Go modules, node modules, compiled application executables or the immutable research snapshot. Teaching programs call pinned application APIs; importing a dependency does not redistribute that dependency’s source or grant its license. Exact source listings retain their immutable source/line attribution.\n\nFive locally bundled publication font files retain four verified notice texts: DM Sans and Passion One under their SIL OFL notices; regular and bold DejaVu Sans Mono under the retained Bitstream Vera/DejaVu notice; and Noto Color Emoji under its SIL OFL notice. The final PDF reports 17 embedded Unicode-mapped font subsets from DM, DM-Bold, BookMono, BookMono-Bold and BookEmoji. Passion One cover lettering is outlined rather than an added PDF font substitution. The EPUB embeds the exact catalog cover PNG and checked lifecycle PNG; it contains no font software. Its reflowable text uses reader-selected fonts.\n\nThe existing Orch mark is embedded unchanged from `docs/assets/orch-mark.svg` at source revision `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`; surrounding cover geometry and outlined book typography are original book composition. The final PDF and EPUB hashes, actual media members, font/notice hashes and every referenced companion are retained in the material audit.\n\nNo LICENSE/COPYING/NOTICE file was observed in the pinned application snapshot. The owner’s all-rights-reserved instruction covers original manuscript material and adds no new public license to Orch, its contributors’ material or its dependencies. This completed local material audit resolves the earlier pending inventory for the files actually included; it does not claim a vendored transitive-dependency license audit, rights over omitted dependency software, a legal certification, or permission to publish a different bundle. Live deployment remains outside this local candidate.\n'''
notice=B/'publication/NOTICE.md';text=notice.read_text();heading='\n## Completed local-edition material audit — October 13, 2026\n'
if heading not in text:notice.write_text(text.rstrip()+'\n'+addendum)
report={'status':'passed_for_actual_local_materials','reviewed_at_utc':now,'source_sha':meta['source_sha'],'pdf_sha256':sha(B/'dist/inside-orch.pdf'),'epub_sha256':sha(B/'dist/inside-orch.epub'),'companion_count':len(items),'companions':items,'material_class_counts':dict(collections.Counter(x['material_class'] for x in items)),'fonts':fonts,'verified_notices':list(notices.values()),'cover_identity':{'pinned_path':'docs/assets/orch-mark.svg','source_sha':meta['source_sha'],'mark_sha256':sha(mark),'unchanged_inner_svg_bytes_present':True,'cover_svg_sha256':sha(B/'publication/cover.svg'),'cover_png_sha256':sha(B/'publication/cover.png'),'composition':'Original outlined book typography/orbit composition around the unchanged source mark.'},'pdf_embedded_fonts':{'actual_command':'validation/publication/material-pdf-fonts-notice-command.json','actual_stdout':'validation/publication/material-pdf-fonts-notice-command.stdout.txt','font_subsets':fontrows,'source_font_notices_checked':True},'epub_media':media,'epub_embedded_font_software':False,'distribution_scan':{'scoped_roots':['assets/books/inside-orch','books/inside-orch/dist'],'scanned_file_count':len(scanned),'vendored_modules_or_application_binaries':violations,'scope':'File/member paths and executable magic checked; fonts/PDF/images/EPUB are intended non-application binary assets. No claim that omitted dependency code has been audited.'},'source_license_files_observed':source_licenses,'rights':'Original manuscript All rights reserved by explicit owner selection. No new public license is applied to application, excerpts, contributors or dependencies.','notice_path':'publication/NOTICE.md','notice_sha256':sha(notice),'limitations':['Archives created after this audit must reuse this exact NOTICE and explicitly bounded file selection; packaging agent validates archive members separately.','Source availability and module hashes do not constitute a dependency permission grant. No transitive vendored license audit is claimed because no modules or application executables are included.','The completed audit records the local candidate, not a live deployment or legal certification.']}
(B/'validation/publication/material-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':report['status'],'companions':len(items),'fonts':len(fonts),'notices':len(notices),'pdf_embedded_subsets':len(fontrows),'epub_media':len(media),'notice_sha256':sha(notice)}))
