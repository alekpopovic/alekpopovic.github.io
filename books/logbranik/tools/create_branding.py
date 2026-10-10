"""Deterministic vector identity and typographic cover; no model-generated art."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BRAND=ROOT/'branding'
META=json.loads((ROOT/'publishing/book-metadata.json').read_text())
NAVY='#101D33'; TEAL='#36D6C2'; AMBER='#F4B860'; INK='#243247'; PAPER='#F5F7FA'
FONT=Path('/usr/share/fonts/truetype/dejavu')


def font(size,bold=False):
    return ImageFont.truetype(str(FONT/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)


def icon_svg(color=TEAL):
    return f'''<g fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<path d="M20 40H66M20 75H66M20 110H66M66 40L93 75M66 110L93 75M66 75H104"/>
<path d="M120 30L170 48V85C170 118 148 140 120 151C92 140 70 118 70 85"/>
<path d="M104 88L118 102L148 68"/></g>'''


def logo(background,text_color,filename):
    back=f'<rect width="640" height="180" fill="{background}"/>' if background else ''
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="180" viewBox="0 0 640 180">
<title>LogBranik wordmark</title>{back}{icon_svg()}
<text x="198" y="109" font-family="DejaVu Sans, sans-serif" font-size="59" font-weight="700" fill="{text_color}">LogBranik</text></svg>'''
    (BRAND/filename).write_text(svg)


def cover():
    image=Image.new('RGB',(1600,2560),NAVY); draw=ImageDraw.Draw(image)
    draw.rectangle((0,0,32,2560),fill=TEAL)
    draw.text((128,118),'LOGBRANIK',font=font(46,True),fill=TEAL)
    draw.text((130,189),'FROM LOGS TO CONTROLLED ACTION',font=font(24),fill=PAPER)
    for n,line in enumerate(['NGINX','LOG','SECURITY']):
        draw.text((116,360+n*172),line,font=font(145,True),fill=PAPER)
    draw.rectangle((128,975,745,987),fill=TEAL)
    for n,line in enumerate(['Build a local IP guard,','signed policies, and a','reliable analysis pipeline']):
        draw.text((128,1062+n*76),line,font=font(48),fill=PAPER)
    # Own geometric mark: observation paths converge into a bounded policy shield.
    draw.rounded_rectangle((128,1430,1472,2200),radius=28,fill='#162A44')
    for y in [1620,1815,2010]:
        draw.line((245,y,620,y),fill=TEAL,width=12)
        draw.ellipse((230,y-16,262,y+16),fill=TEAL)
    draw.line((620,1620,800,1815),fill=TEAL,width=12)
    draw.line((620,2010,800,1815),fill=TEAL,width=12)
    draw.line((620,1815,885,1815),fill=TEAL,width=12)
    shield=[(1060,1535),(1320,1640),(1320,1855),(1270,1990),(1170,2075),(1060,2135),(950,2075),(850,1990),(800,1855),(800,1640)]
    draw.polygon(shield,fill=NAVY)
    draw.line(shield+[shield[0]],fill=TEAL,width=13,joint='curve')
    draw.line([(932,1820),(1030,1920),(1200,1700)],fill=AMBER,width=24,joint='curve')
    draw.text((128,2260),META['author'],font=font(44,True),fill=PAPER)
    draw.text((128,2370),'NGINX OPEN SOURCE  /  PYTHON LAB',font=font(28,True),fill=TEAL)
    draw.text((128,2450),'OPEN BOOK: CC BY 4.0  /  CODE: MIT',font=font(24),fill=PAPER)
    image.save(BRAND/'book-cover.png')


def architecture():
    image=Image.new('RGB',(1500,1000),PAPER); draw=ImageDraw.Draw(image)
    draw.text((65,40),'Two paths, separate responsibilities',font=font(45,True),fill=NAVY)
    draw.text((65,103),'Local request checks remain independent of central analysis.',font=font(27),fill=INK)
    def box(x,y,w,h,title,sub,fill=NAVY):
        draw.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=fill)
        draw.text((x+25,y+22),title,font=font(29,True),fill=PAPER)
        draw.text((x+25,y+68),sub,font=font(22),fill=TEAL)
    def arrow(points,color=INK):
        draw.line(points,fill=color,width=5)
        x,y=points[-1]; ax,ay=points[-2]
        if x>ax: p=[(x,y),(x-15,y-9),(x-15,y+9)]
        elif x<ax: p=[(x,y),(x+15,y-9),(x+15,y+9)]
        elif y>ay: p=[(x,y),(x-9,y-15),(x+9,y-15)]
        else: p=[(x,y),(x-9,y+15),(x+9,y+15)]
        draw.polygon(p,fill=color)
    draw.text((70,190),'EDGE HOST',font=font(24,True),fill=INK)
    draw.text((1020,190),'CENTRAL HOST',font=font(24,True),fill=INK)
    box(70,250,300,130,'Nginx OSS','Resolved IP + site')
    box(540,250,330,130,'Protected app','Allowed requests')
    box(70,500,300,130,'Local agent','204 / 403 / unavailable')
    box(540,500,330,130,'Collector','Completed log events')
    box(1020,500,410,130,'Ingestion + store','Identity + deduplication')
    box(1020,760,410,130,'Detector + delivery','Signed full policy')
    arrow([(370,310),(540,310)]); draw.text((380,272),'allow',font=font(22),fill=INK)
    arrow([(150,380),(150,500)]); draw.text((175,420),'local check',font=font(22),fill=INK)
    arrow([(95,500),(95,380)],TEAL)
    arrow([(370,350),(435,350),(435,565),(540,565)])
    draw.text((445,422),'logs',font=font(22),fill=INK)
    arrow([(870,565),(1020,565)]); draw.text((900,526),'mTLS',font=font(22),fill=INK)
    arrow([(1220,630),(1220,760)])
    arrow([(1020,825),(220,825),(220,630)],TEAL)
    draw.text((360,850),'mTLS + signature + revision + original TTL',font=font(25,True),fill=INK)
    draw.text((70,935),'Deployment design; the compact lab substitutes Python/SQLite and finite captures.',font=font(23),fill=INK)
    image.save(BRAND/'architecture.png')
    for sub in ['lessons/resources','manuscript/resources']:
        p=ROOT/sub;p.mkdir(parents=True,exist_ok=True);image.save(p/'architecture.png')


def main():
    BRAND.mkdir(exist_ok=True)
    logo(None,NAVY,'logo-light.svg');logo(NAVY,PAPER,'logo-dark.svg')
    (BRAND/'symbol.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180"><title>LogBranik symbol</title>{icon_svg()}</svg>')
    (BRAND/'symbol-monochrome.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180"><title>LogBranik monochrome symbol</title>{icon_svg(NAVY)}</svg>')
    (BRAND/'tokens.json').write_text(json.dumps({'brand':'LogBranik','status':'proposed, not trademark-cleared',
      'colors':{'navy':NAVY,'teal':TEAL,'amber':AMBER,'ink':INK,'paper':PAPER},
      'fonts':{'heading':'DejaVu Sans','body':'DejaVu Serif','code':'DejaVu Sans Mono'},
      'tagline':'From logs to controlled action', 'author':META['author'], 'license':'CC-BY-4.0'},indent=2))
    cover();architecture()
    (ROOT/'manuscript/resources/cover.png').write_bytes((BRAND/'book-cover.png').read_bytes())


if __name__=='__main__':main()
