from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parents[2];S=B.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();pdfsha=sha(B/'dist/inside-orch.pdf');epubsha=sha(B/'dist/inside-orch.epub')
assert pdfsha=='a734dd82a27fde589fd81cf9755693401f8b1abbe9a055d1ebe2e482916caee3';assert epubsha=='e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b'
eqpath=B/'validation/publication/pdf-rebuild-equivalence.json';eq=json.loads(eqpath.read_text());assert eq['status']=='passed' and eq['final_pdf_sha256']==pdfsha and len(eq['pages'])==546
mapping={'invariant-table-site-build':'final-notice-site-build','invariant-table-jekyll-build':'final-notice-jekyll-build','invariant-table-format-check':'notice-rebuild-format-check','invariant-table-books-check':'notice-rebuild-books-check','invariant-table-site-check':'notice-rebuild-site-check'}
changed=[]
for rel in ['validation/publication/pdf-typesetting-acceptance.json','validation/publication/epub-publication-acceptance.json','validation/publication/native-adapter-acceptance.json','validation/publication/native-publisher-acceptance.json','validation/publication/site-integration-acceptance.json','publication/site-adapter/adapter-contract.json','validation/publication/pdf-visual-source-review.json']:
 p=B/rel;d=json.loads(p.read_text());d['pdf_sha256']=pdfsha;d['epub_sha256']=epubsha;d['reviewed_at_utc']=now;d['notice_rebuild_rebind']={'prior_pdf_sha256':eq['previous_reviewed_pdf_sha256'],'prior_record':'validation/publication/prior-notice-rebuild/'+rel,'equivalence_record':'validation/publication/pdf-rebuild-equivalence.json','equivalence_record_sha256':sha(eqpath),'scope':'All 546 text/content streams and raster images equal the reviewed prior edition. Fresh build/check records retained; no new visual views or format builds claimed.'}
 for c in d.get('checks',[]):
  if 'record' not in c:continue # Visual observations are descriptive checks, not command records.
  stem=Path(c['record']).stem
  if stem not in mapping:continue
  record='validation/publication/'+mapping[stem]+'.json';r=json.loads((B/record).read_text());assert r['status']=='passed' and r['exit_code']==0
  c.update({'record':record,'record_sha256':sha(B/record),'command':r['command'],'working_directory':r['cwd'],'started_at_utc':r['started_at_utc'],'finished_at_utc':r['finished_at_utc'],'exit_code':r['exit_code'],'stdout':r['stdout'],'stderr':r['stderr'],'scope':r['scope']})
 p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');changed.append(rel)
p=B/'publication/catalog.json';d=json.loads(p.read_text());d['formats']['pdf']['sha256']=pdfsha;d['measured_at_utc']=now;p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
p=B/'validation/publication/site-build.md';s=p.read_text().replace(eq['previous_reviewed_pdf_sha256'],pdfsha)
for a,z in mapping.items():s=s.replace(a,z)
s+='\nThe final NOTICE copy triggered a PDF container-identifier change. `validation/publication/pdf-rebuild-equivalence.json` records identical text/content streams and all 546 rendered page images, binding earlier actual visual coverage to this exact final hash. Prior hash-bearing acceptance records remain under `validation/publication/prior-notice-rebuild/`.\n';p.write_text(s)
for ext in ['pdf','epub']:
 for root in [S/'assets/books/inside-orch/downloads',S/'_site/assets/books/inside-orch/downloads']:assert (root/('inside-orch.'+ext)).read_bytes()==(B/('dist/inside-orch.'+ext)).read_bytes()
assert (S/'assets/books/inside-orch/publication/NOTICE.md').read_bytes()==(B/'publication/NOTICE.md').read_bytes()==(S/'_site/assets/books/inside-orch/publication/NOTICE.md').read_bytes()
print(json.dumps({'status':'passed','formal_records_rebound':changed,'final_pdf_sha256':pdfsha,'epub_sha256':epubsha,'canonical_public_downloads_equal':True,'notice_copies_equal':True,'patch_manifest':'Final refresh deferred until packaging documentation freeze.'}))
