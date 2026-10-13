#!/usr/bin/env python3
"""Render an exact edition for all-page visual review; images are internal QA."""
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfReader
BOOK=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pdf=BOOK/'dist/inside-orch.pdf';digest=hashlib.sha256(pdf.read_bytes()).hexdigest();out=a.output.resolve()
if out.exists():raise SystemExit('Use a new render directory')
out.mkdir(parents=True)
subprocess.run(['pdftoppm','-r','110','-png',str(pdf),str(out/'page')],check=True)
images=sorted(out.glob('page-*.png'));count=len(PdfReader(pdf).pages)
assert len(images)==count
contacts=[]
for start in range(0,count,12):
    sheet=Image.new('RGB',(1120,2180),'#cbd5e1');draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(images[start:start+12]):
        with Image.open(path) as im:
            im.thumbnail((360,510));x=10+(j%3)*370;y=25+(j//3)*540
            sheet.paste(im,(x,y));draw.text((x,y-18),f'PDF page {start+j+1}',fill='black')
    target=out/f'contact-{start//12+1:03d}.png';sheet.save(target)
    contacts.append({'path':str(target),'first_page':start+1,'last_page':min(start+12,count),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
r={'status':'rendered_visual_inspection_pending','pdf_sha256':digest,'page_count':count,'render_directory':str(out),'dpi':110,'tool':subprocess.check_output(['pdftoppm','-v'],stderr=subprocess.STDOUT,text=True).splitlines()[0],'pages':[{'page':i+1,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for i,path in enumerate(images)],'contact_sheets':contacts,'scope':'Internal QA images; contact-sheet review and full-size suspect inspection are separate recorded steps.'}
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==digest,'PDF changed during rendering'
(BOOK/'validation/publication/pdf-pages.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'page_count':count,'sha256':digest,'contact_sheets':len(contacts)}))
