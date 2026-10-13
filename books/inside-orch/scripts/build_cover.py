#!/usr/bin/env python3
"""Draw the original vector-derived cover with local OFL font outlines."""
from pathlib import Path
import html,json,re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg
BOOK=Path(__file__).resolve().parents[1];SITE=BOOK.parents[1]

def text_paths(text,fontfile,size,x,y,fill):
 font=TTFont(fontfile);glyphs=font.getGlyphSet();cmap=font.getBestCmap();scale=size/font['head'].unitsPerEm;result=[]
 for ch in text:
  name=cmap.get(ord(ch),'.notdef');pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
  result.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale:.6f} {-scale:.6f})" fill="{fill}"/>')
  x+=glyphs[name].width*scale
 font.close();return ''.join(result)
def main():
 display=BOOK/'publication/fonts/passion-one-bold.ttf';body=BOOK/'publication/fonts/dm-sans.ttf'
 mark=(BOOK/'evidence/orch/docs/assets/orch-mark.svg').read_text();inner=re.sub(r'^.*?<svg[^>]*>|</svg>\s*$','',mark,flags=re.S)
 title='Inside orch — Building and Operating a Docker Orchestrator in Go'
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1700 2400" role="img" aria-labelledby="cover-title cover-description"><title id="cover-title">{html.escape(title)}</title><desc id="cover-description">Aleksandar Popovic. A source-based engineering study. Cyan, blue and violet orbit mark on deep navy, with a deliberate typographic hierarchy.</desc><defs><linearGradient id="cover-gradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#020617"/><stop offset="1" stop-color="#101e36"/></linearGradient></defs><rect width="1700" height="2400" fill="url(#cover-gradient)"/><circle cx="1520" cy="220" r="650" fill="none" stroke="#22d3ee" stroke-opacity=".13" stroke-width="3"/><circle cx="1520" cy="220" r="830" fill="none" stroke="#8b5cf6" stroke-opacity=".15" stroke-width="3"/><path d="M120 480H1580" stroke="#22d3ee" stroke-width="4"/><g transform="translate(1210 130) scale(1.35)">{inner}</g>'''
 svg+=text_paths('THE ENGINEERING SERIES',body,31,125,190,'#a7f3d0')
 svg+=text_paths('INSIDE',display,258,115,830,'#f8fafc')
 svg+=text_paths('orch',display,480,110,1235,'#22d3ee')
 for line,y in [('Building and Operating a',1450),('Docker Orchestrator in Go',1540)]:svg+=text_paths(line,body,63,125,y,'#f8fafc')
 svg+='<path d="M125 1740H580" stroke="#8b5cf6" stroke-width="9"/>'
 for line,y in [('Desired state. Runtime boundaries.',1850),('Failures you can explain.',1920)]:svg+=text_paths(line,body,42,125,y,'#cbd5e1')
 svg+=text_paths('Aleksandar Popovic',body,62,125,2160,'#ffffff')
 svg+=text_paths('SOURCE-BASED ENGINEERING EDITION',body,27,125,2260,'#a7f3d0')
 svg+='</svg>'
 out=BOOK/'publication/cover.svg';out.write_text(svg);cairosvg.svg2png(bytestring=svg.encode(),write_to=str(BOOK/'publication/cover.png'),output_width=1700,output_height=2400)
 from PIL import Image
 with Image.open(BOOK/'publication/cover.png') as im:im.resize((340,480)).save(BOOK/'publication/cover-card-preview.png')
 print(json.dumps({'svg':str(out),'png':[1700,2400],'card_preview':[340,480],'fonts':'Local Passion One and DM Sans, OFL; outlined vectors','brand':'Pinned unchanged Orch mark embedded'}))
if __name__=='__main__':main()
