"""Export one Markdown source set to Leanpub, PDF, EPUB and review HTML."""
from pathlib import Path
import html
import hashlib
import json
import re
import shutil
import subprocess
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
                               Paragraph, Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
META=json.loads((ROOT/'publishing/book-metadata.json').read_text())
WIDTH,HEIGHT=432,648
MARGIN=42
TEXT_WIDTH=WIDTH-2*MARGIN
NAVY=colors.HexColor('#101D33'); TEAL=colors.HexColor('#36D6C2')
FONT=Path('/usr/share/fonts/truetype/dejavu')


def fonts():
    for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),
                      ('Head','DejaVuSans.ttf'),('HeadBold','DejaVuSans-Bold.ttf'),
                      ('Code','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    pdfmetrics.registerFontFamily('Head',normal='Head',bold='HeadBold',italic='Head',boldItalic='HeadBold')
    pdfmetrics.registerFontFamily('Code',normal='Code',bold='Code',italic='Code',boldItalic='Code')


STYLES={}
def styles():
    STYLES.update({
        'body':ParagraphStyle('BodyStyle',fontName='Body',fontSize=9.8,leading=14,spaceAfter=7,
                              textColor=NAVY,splitLongWords=True,allowWidows=0,allowOrphans=0),
        'h1':ParagraphStyle('Chapter',fontName='HeadBold',fontSize=21,leading=26,spaceAfter=19,keepWithNext=True,
                            textColor=NAVY),
        'h2':ParagraphStyle('Section',fontName='HeadBold',fontSize=12.3,leading=16.5,spaceBefore=8,
                            spaceAfter=6,keepWithNext=True,textColor=NAVY),
        'cell':ParagraphStyle('Cell',fontName='Head',fontSize=7.7,leading=10.5,textColor=NAVY,
                              splitLongWords=True),
        'code':ParagraphStyle('CodeStyle',fontName='Code',fontSize=7.9,leading=10.7,spaceBefore=4,
                              spaceAfter=8,leftIndent=8,rightIndent=8,backColor=colors.HexColor('#F0F3F7')),
        'toc':ParagraphStyle('TOCLine',fontName='Head',fontSize=9,leading=14,spaceBefore=5,
                             leftIndent=0,rightIndent=20),
        'bullet':ParagraphStyle('Bullet',fontName='Body',fontSize=9.8,leading=14.7,leftIndent=12,
                                firstLineIndent=-10,spaceAfter=6,textColor=NAVY),
    })


def inline(text):
    snippets=[]
    def code(match):
        snippets.append('<font name="Code" size="8.2">'+html.escape(match.group(1))+'</font>')
        return f'ZZCODE{len(snippets)-1}ZZ'
    text=re.sub(r'`([^`]+)`',code,text)
    text=html.escape(text)
    text=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#16756C">\1</link>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'\*([^*]+)\*',r'<i>\1</i>',text)
    for i,value in enumerate(snippets):text=text.replace(f'ZZCODE{i}ZZ',value)
    return text


class BookDoc(BaseDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name=='Chapter':
            title=flowable.getPlainText()
            key='chapter-'+hashlib.sha256(title.encode()).hexdigest()[:16]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)
            self.notify('TOCEntry',(0,title,self.page,key))


def page(canvas,doc):
    if doc.page==1:
        canvas.drawImage(str(ROOT/'branding/book-cover.png'),0,0,width=WIDTH,height=HEIGHT)
        return
    canvas.saveState()
    canvas.setStrokeColor(TEAL);canvas.setLineWidth(1.1)
    canvas.line(MARGIN,HEIGHT-29,WIDTH-MARGIN,HEIGHT-29)
    canvas.setFont('Head',7);canvas.setFillColor(NAVY)
    canvas.drawString(MARGIN,HEIGHT-22,'LOGBRANIK  /  NGINX LOG SECURITY')
    canvas.drawString(MARGIN,22,'CC BY 4.0 / code MIT - candidate '+META['edition'])
    canvas.drawRightString(WIDTH-MARGIN,22,str(doc.page))
    canvas.restoreState()


def parse_markdown(text):
    result=[];lines=text.splitlines();i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            i+=1;code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                source=lines[i].expandtabs(4)
                if len(source)>68:
                    code.extend(textwrap.wrap(source,width=68,replace_whitespace=False,
                                              drop_whitespace=False,subsequent_indent='    ',break_on_hyphens=False))
                else:code.append(source)
                i+=1
            i+=1
            blocks=[]
            for start in range(0,len(code),20):
                blocks.append(Preformatted('\n'.join(code[start:start+20]),STYLES['code']))
            result.append(KeepTogether(blocks))
            continue
        if line.startswith('!['):
            match=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
            if match:
                path=ROOT/'lessons'/match.group(2)
                from PIL import Image as PILImage
                with PILImage.open(path) as im:w,h=im.size
                result.append(Image(str(path),width=TEXT_WIDTH,height=TEXT_WIDTH*h/w))
                result.append(Paragraph(inline(match.group(1)),STYLES['cell']))
                result.append(Spacer(1,8))
            i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',x) for x in cells):
                    rows.append([Paragraph(inline(x),STYLES['cell']) for x in cells])
                i+=1
            columns=len(rows[0]);widths=[TEXT_WIDTH/columns]*columns
            if columns==2:widths=[TEXT_WIDTH*0.35,TEXT_WIDTH*0.65]
            if columns==3 and rows[0][0].getPlainText()=='ID':widths=[32,TEXT_WIDTH-80,48]
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#D9EEE9')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F7FA')]),
                ('LINEBELOW',(0,0),(-1,0),0.7,NAVY),('LEFTPADDING',(0,0),(-1,-1),6),
                ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            result.extend([table,Spacer(1,10)]);continue
        if line.startswith('# '):
            result.append(Paragraph(inline(line[2:]),STYLES['h1']));i+=1;continue
        if line.startswith('## '):
            result.append(Paragraph(inline(line[3:]),STYLES['h2']));i+=1;continue
        if re.match(r'^[-*] ',line):
            result.append(Paragraph('&#8226; '+inline(line[2:]),STYLES['bullet']));i+=1;continue
        if re.match(r'^\d+\. ',line):
            result.append(Paragraph(inline(line),STYLES['bullet']));i+=1;continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||!\[|[-*] |\d+\. )',lines[i]):
            paragraph.append(lines[i]);i+=1
        result.append(Paragraph(inline(' '.join(paragraph)),STYLES['body']))
    return result


def pdf(files,destination):
    doc=BookDoc(str(destination),pagesize=(WIDTH,HEIGHT),leftMargin=MARGIN,rightMargin=MARGIN,
                topMargin=47,bottomMargin=42,title=META['title'],author=META['author'],
                subject='Open book: CC BY 4.0; original code: MIT',
                allowSplitting=True)
    doc.addPageTemplates(PageTemplate('Reading',frames=[Frame(MARGIN,42,TEXT_WIDTH,HEIGHT-89,
                        leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page))
    toc=TableOfContents();toc.levelStyles=[STYLES['toc']]
    toc_title=ParagraphStyle('ContentsTitle',parent=STYLES['h1'])
    story=[Spacer(1,1),PageBreak(),Paragraph('Contents',toc_title),toc,PageBreak()]
    for number,file in enumerate(files):
        if number:story.append(PageBreak())
        story.extend(parse_markdown(file.read_text()))
    doc.multiBuild(story)


def main():
    OUT.mkdir(exist_ok=True);fonts();styles()
    files=sorted((ROOT/'lessons').glob('*.md'))
    sample=files[:5]
    for p in files:(ROOT/'manuscript'/p.with_suffix('.txt').name).write_text(p.read_text())
    (ROOT/'manuscript/Book.txt').write_text('\n'.join(p.with_suffix('.txt').name for p in files)+'\n')
    (ROOT/'manuscript/Sample.txt').write_text('\n'.join(p.with_suffix('.txt').name for p in sample)+'\n')
    all_text='\n\n'.join(p.read_text() for p in files)
    (OUT/'nginx-log-security.md').write_text(all_text)
    (OUT/'nginx-log-security-sample.md').write_text('\n\n'.join(p.read_text() for p in sample))
    pdf(files,OUT/'nginx-log-security.pdf');pdf(sample,OUT/'nginx-log-security-sample.pdf')
    css=ROOT/'tools/epub.css'
    if shutil.which('pandoc'):
        for stem in ['nginx-log-security','nginx-log-security-sample']:
            subprocess.run(['pandoc',str(OUT/(stem+'.md')),'-o',str(OUT/(stem+'.epub')),
              '--from=markdown','--to=epub3','--toc','--split-level=1','--resource-path='+str(ROOT/'lessons'),
              '--epub-cover-image='+str(ROOT/'branding/book-cover.png'),'--css='+str(css),
              '-M','title='+META['title'],'-M','author='+META['author'],
              '-M','rights=Copyright 2026 '+META['author']+'; text and original visuals CC BY 4.0; original code MIT',
              '-M','lang=en','-M','date=2026-10-10'],check=True)
        subprocess.run(['pandoc',str(OUT/'nginx-log-security.md'),'-o',str(OUT/'nginx-log-security.html'),
            '--standalone','--toc','--embed-resources','--resource-path='+str(ROOT/'lessons'),
            '-M','title='+META['title'],'-M','author='+META['author']],check=True)
    stats={'lesson_files':len(files),'main_lessons':20,'words_whitespace':len(all_text.split()),
           'edition':META['edition']+' publication candidate','author_finalized':bool(META['author']),
           'author':META['author'],'content_license':'CC-BY-4.0','code_license':'MIT',
           'leanpub_generator_executed':False}
    from pypdf import PdfReader
    stats['pdf_pages']=len(PdfReader(OUT/'nginx-log-security.pdf').pages)
    stats['sample_pdf_pages']=len(PdfReader(OUT/'nginx-log-security-sample.pdf').pages)
    (OUT/'book-statistics.json').write_text(json.dumps(stats,indent=2))
    print(json.dumps(stats))


if __name__=='__main__':main()
