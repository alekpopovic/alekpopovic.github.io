import sys, importlib.util, json, hashlib
from pathlib import Path
site=Path(__file__).resolve().parents[3];sys.path.insert(0,str(site/'scripts'))
from book_catalog import catalog,orch_publication,render,resolve_reference,public_reference,section
book=next(b for b in catalog() if b['id']=='inside-orch')
paths=book['paths']; assert len(paths)==47
assert sum(section(book,p,i)[0]=='Chapters' for i,p in enumerate(paths))==40
assert sum(section(book,p,i)[0]=='Appendices' for i,p in enumerate(paths))==6
for p in paths:
    text=render(book,p); assert '/books/modern-ci/' not in text
    for target in orch_publication.references(p):
        assert target in paths or orch_publication.permitted_companion(target)
spec=importlib.util.spec_from_file_location('native_builder',site/'scripts/build-books.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
# Build only this source to exercise the actual shared adapter. Final npm build runs all publishers.
orch_publication.build()
data=builder.build_book(book,__import__('book_catalog').publication,render)
assert data['chapter_count']==40 and data['appendix_count']==6
for ext in ('pdf','epub'):
    assert (book['files']/'downloads'/('inside-orch.'+ext)).read_bytes()==(book['editions']/('inside-orch.'+ext)).read_bytes()
report={'status':'passed','sections':47,'numbered_chapters':40,'appendices':6,'companion_count':len(orch_publication.companions()),'epub_chapters':book['epub_chapters'],'cover_sha256':hashlib.sha256((book['source']/book['cover']).read_bytes()).hexdigest(),'implementation':['scripts/book_catalog.py','scripts/build-books.py','books/inside-orch/scripts/build.py'],'scope':'Actual native build_book integration for Inside orch; full site gates remain separate.'}
(book['source']/'publication/site-adapter/adapter-contract.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='epub_chapters'}))
