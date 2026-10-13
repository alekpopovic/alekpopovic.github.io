from pathlib import Path
import json,re,html,textwrap,math
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,KeepTogether,Flowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

PACK=Path(__file__).resolve().parents[1];ROOT=PACK
OUT=PACK/'publication/Inside-Orch-Book-Blueprint.pdf'
F=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,str(F/file)))
INK=colors.HexColor('#0f172a');BLUE=colors.HexColor('#2374e1');CYAN=colors.HexColor('#22d3ee');VIOLET=colors.HexColor('#8b5cf6');LIGHT=colors.HexColor('#f1f5f9');MUTED=colors.HexColor('#475569')
styles={
'body':ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=15.2,textColor=INK,spaceAfter=8,allowWidows=0,allowOrphans=0),
'outline':ParagraphStyle('outline',fontName='Sans',fontSize=9.2,leading=13.2,textColor=INK,spaceAfter=5),
'question':ParagraphStyle('question',fontName='Body',fontSize=10.2,leading=15.2,textColor=INK,spaceAfter=8,keepWithNext=True,allowWidows=0,allowOrphans=0),
'small':ParagraphStyle('small',fontName='Sans',fontSize=8.6,leading=12.4,textColor=MUTED,spaceAfter=6),
'h1':ParagraphStyle('h1',fontName='SansBold',fontSize=23,leading=28,textColor=INK,spaceAfter=14,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=15,leading=20,textColor=BLUE,spaceBefore=13,spaceAfter=8,keepWithNext=True),
'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11.5,leading=16,textColor=INK,spaceBefore=10,spaceAfter=6,keepWithNext=True),
'code':ParagraphStyle('code',fontName='Mono',fontSize=8.3,leading=11.4,textColor=INK,backColor=LIGHT,borderPadding=7,spaceBefore=5,spaceAfter=10),
'table':ParagraphStyle('table',fontName='Sans',fontSize=8.5,leading=12,textColor=INK),
'tablehead':ParagraphStyle('tablehead',fontName='SansBold',fontSize=8.5,leading=12,textColor=colors.white),
}
def clean(s):return s.replace('—',' - ').replace('–','-').replace('\u00a0',' ').replace('\u2011','-')
def mdinline(s):
    s=clean(s);s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^ )]+)\)',lambda m:'<link href="'+html.escape(html.unescape(m[2]),quote=True)+'" color="#2374e1">'+m[1]+'</link>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Mono" size="8.8">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    return s
story=[]
def p(text,style='body'):story.append(Paragraph(mdinline(text),styles[style]))
def heading(text,level=1):p(text,'h'+str(level))
def table(headers,rows,widths):
    data=[[Paragraph(html.escape(clean(x)),styles['tablehead']) for x in headers]]+[[Paragraph(mdinline(str(x)),styles['table']) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('LINEBELOW',(0,-1),(-1,-1),0.4,colors.HexColor('#cbd5e1'))]))
    story.extend([t,Spacer(1,10)])
def page():story.append(PageBreak())

class Cover(Flowable):
    def __init__(self):
        super().__init__();self.width=490;self.height=680
    def wrap(self,availWidth,availHeight):
        return self.width,self.height
    def draw(self):
        c=self.canv;c.setFillColor(INK);c.roundRect(0,0,490,680,12,stroke=0,fill=1)
        c.setStrokeColor(CYAN);c.setLineWidth(3);c.ellipse(42,470,173,601,stroke=1,fill=0)
        for angle,col in [(25,BLUE),(145,VIOLET),(265,CYAN)]:
            x=107+66*math.cos(math.radians(angle));y=535+66*math.sin(math.radians(angle));c.setFillColor(col);c.roundRect(x-12,y-12,24,24,5,fill=1,stroke=0)
        c.setFillColor(CYAN);c.setFont('SansBold',10);c.drawString(42,642,'SOURCE-BASED ENGINEERING / BOOK GENERATION PACK')
        c.setFillColor(colors.white);c.setFont('SansBold',49);c.drawString(42,398,'Inside orch')
        c.setFont('Sans',21)
        for i,line in enumerate(['Building and Operating','a Docker Orchestrator in Go']):c.drawString(42,352-i*31,line)
        c.setStrokeColor(CYAN);c.setLineWidth(1);c.line(42,261,444,261)
        c.setFont('SansBold',14);c.drawString(42,226,'Aleksandar Popovic')
        c.setFont('Sans',11);c.drawString(42,202,'alekpopovic.com')
        c.setFillColor(colors.HexColor('#cbd5e1'));c.setFont('Sans',11)
        for i,line in enumerate(['100 book-production prompts / 40 chapters','6 appendices / 8 progressive laboratories','Verified source history + one sample chapter']):c.drawString(42,135-i*23,line)
        c.setFillColor(CYAN);c.setFont('SansBold',10);c.drawString(42,37,'BLUEPRINT AND SAMPLE - THE FULL MANUSCRIPT IS PENDING')

class Doc(BaseDocTemplate):
    def afterFlowable(self,flow):
        if isinstance(flow,Paragraph) and flow.style.name in ['h1','h2']:
            title=flow.getPlainText();key='b'+str(getattr(self,'bookmark_count',0));self.bookmark_count=getattr(self,'bookmark_count',0)+1
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=0 if flow.style.name=='h1' else 1,closed=False)
def footer(c,doc):
    if doc.page==1:return
    c.setStrokeColor(colors.HexColor('#cbd5e1'));c.setLineWidth(.4);c.line(48,48,547,48)
    c.setFillColor(MUTED);c.setFont('Sans',8);c.drawString(48,33,'Inside orch / Blueprint and sample / Aleksandar Popovic');c.drawRightString(547,33,str(doc.page))
    c.setTitle('Inside orch - Book Blueprint and Sample');c.setAuthor('Aleksandar Popovic');c.setSubject('Complete Codex generation pack: source evidence, editorial plan and sample chapter')

story.append(Cover());page()
heading('A book grounded in executable behavior')
p('This document accompanies the complete Codex generation pack for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by **Aleksandar Popovic**. It gives the editorial plan, evidence boundaries, execution sequence and a finished source-based sample chapter.')
p('The full 40-chapter manuscript is not included yet. The package contains the complete 100-prompt workflow that produces it, along with the locked source corpus and quality gates. Future PDF, EPUB and online editions are outputs of that workflow.')
heading('The intended readers',2)
table(['Reader','What the book should enable'],[
['Developer','Trace APIs and lifecycle transitions; reason about planner/reconciler invariants; test runtime side effects and integration seams.'],
['DevOps engineer','Deploy an isolated lab, inspect actual runtime behavior, diagnose failures, validate recovery, and explain operational limits.'],
['Architect','Evaluate state ownership, durability, concurrency, leases, fencing, isolation and capacity from mechanisms and evidence.']],[114,376])
heading('A distinctive teaching contract',2)
p('Every chapter connects development intent, actual source changes, current code, an invariant, a failure window and observable evidence. Exact code excerpts have immutable links. Teaching extensions are visibly separate from upstream implementation. Exercises have worked answers.')
p('The target is 85,000-110,000 meaningful words, excluding source listings and command output. This is an editorial target. The final page count will be measured after typesetting. Length cannot substitute for correct mechanisms, useful examples or tested procedures.')
p('Every prompt executes from alekpopovic/alekpopovic.github.io repository root. The inspected Jekyll + Tailwind site has a native publisher, catalog, reader and completeness checks. Canonical book work lives under books/inside-orch; the pack preserves that contract and prepares local integration without publishing the live site.','small')
page();heading('The immutable source edition')
lock=json.loads((PACK/'evidence/source-lock.json').read_text())
p('[Source repository](https://github.com/alekpopovic/orch) - Docker-first orchestration for small clusters.')
p('Pinned HEAD: `'+lock['baseline_sha']+'`. This is a documentation update after the published 0.3.0 tag. Current code citations use this HEAD; historical explanations use the relevant historical commit.')
table(['Evidence','Measured inventory'],[['Tracked orch source files','361 files with byte sizes and SHA-256 checksums'],['Native website contract','20 selected source files, separately pinned at SHA 80801c8d3d97a4d8ff78e0fe69f3f902beda00c0'],['Development prompts','91 original prompts numbered 00-90'],['Reachable commits','105, with author/committer dates and exported diffs'],['Associated implementation/design commits','66 distinct SHAs in the prompt crosswalk'],['Migrations','16 up/down pairs'],['Book-production prompts','100 full prompts numbered 000-099'],['Source links checked in prompts','508 immutable source/commit URLs']],[190,300])
heading('History requires careful attribution',2)
p('The first 29 original prompt files were added after their June implementation. Their linked commits are retrospective topical associations, not proof of literal prompt execution at that date. Later changes batch several prompts in one commit. The original execution tracker is navigation evidence; it does not establish every requested guarantee.')
releases=json.loads((PACK/'evidence/releases.json').read_text())
table(['Release','Published UTC','Evidence'],[[r['tag_name'],r['published_at'],f"[GitHub release]({r['html_url']})"] for r in reversed(releases)],[82,180,228])
p('Tag 0.3.0 points to `79d616acb679f237513b86eafe8c535983973579`; HEAD is `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. No 0.2.0 tag was present in the inspected repository. Release publication time and implementation commit time are different facts.','small')
page();heading('What the book must explain honestly')
p('The strongest material comes from the gap between a capable package and the executable that actually uses it. These are source-reviewed boundaries; runtime experiments remain tasks for the generated book.')
table(['Topic','Source-based boundary'],[
['Durability','Default orch-server constructs MemoryService. PostgreSQL stores and migrations do not persist its live domain state.'],
['Placement','MemoryService normally creates already assigned service tasks through its immediate reconciliation path. The standalone scheduler planner has a separate path.'],
['Resource enforcement','The Docker adapter supports limits, but the active agent assignment/create path does not populate ContainerSpec.Resources.'],
['Reconciliation','The standalone reconciler package is implemented; default startup instead relies on MemoryService reconciliation for normal services.'],
['HA and autoscaling','Leadership and autoscaling packages exist; default server composition does not activate them as the claimed complete platform mechanisms.'],
['Restart tests','The named rollout restart test reuses the same memory state. It demonstrates controller reconstruction, not whole-process durable recovery.'],
['Partition recovery','Node timeout/replacement is different from fencing a still-live isolated workload.'],
['Workload/platform scope','Local volume claims, partial GitOps applies, job/cron semantics, digest parsing and design-only features need precise boundaries.']],[110,380])
heading('Capability labels',2)
p('Use runtime-integrated, implemented package, partial integration, design only, teaching extension and future work consistently. A package can be well-tested without being wired into a binary. Source inspection and executed validation are recorded separately.')
page();heading('The complete writing sequence')
table(['Prompt range','Concrete output'],[['000-019','Research, source inventory, integration ledger, history, reader paths, lab environment and editorial foundation'],['020-059','All 40 chapters, examples, worked answers and chapter evidence ledgers'],['060-065','Six appendices with field/state/history/exercise/operator/glossary reference'],['066-073','Eight progressive laboratories and actual execution records'],['074-085','Code, source, lab, architecture, developer, operations, security and editorial reviews'],['086-095','Metadata, cover, PDF, EPUB, native Jekyll adapter, three posts, glossary and site checks'],['096-099','Release gate, independent review, archives/checksums and publication handoff']],[94,396])
heading('Execute from the website repository root',2)
p('Extract the ZIP into alekpopovic/alekpopovic.github.io so books/inside-orch/ exists. Open the website repository root in Codex. Read root AGENTS.md, books/inside-orch/AGENTS.md, BOOK_SPEC.md and SITE_WORKSPACE.md. Execute books/inside-orch/prompts/000-workspace-and-baseline.md. Never replace the site root instructions or scripts. Original orch prompts 00-90 are evidence; do not rerun them as book-writing tasks.')
story.append(Preformatted('python3 books/inside-orch/scripts/verify_pack.py\npython3 books/inside-orch/scripts/next_prompt.py --show',styles['code']))
p('The tracker begins pending for all 100 future book-production tasks. The provided source audits are seeds for verification. A done entry requires concrete evidence; blocked prerequisites and unrun experiments must stay visible.')
heading('What has actually been checked',2)
p('Orch and native-site source hashes, all 100 site-root execution bindings, prompt coverage, mapped commit objects, source paths and immutable links have been checked. Website builds have not been executed by this pack. The sample lab passes Bash syntax validation and was statically compared with flags, routes and configuration. Go is unavailable here, so the application build, Go tests, Docker/PostgreSQL labs and benchmarks have not been run. Expected sample observations are labeled accordingly.')
page();heading('Forty chapters with distinct purposes')
outline=json.loads((PACK/'editorial/book-outline.json').read_text())
part=None
for c in outline['chapters']:
    entry_start=len(story)
    if c['part']!=part:
        part=c['part'];heading(part,2)
    heading(c['id']+'. '+c['title'],3)
    p(c['focus'],'outline')
    p('**Lab / analysis:** '+c['lab'],'small')
    p('**Original prompts:** '+', '.join(f'{n:02d}' for n in c['original_prompts'])+'. **Writing task:** '+str(int(c['id'])+19).zfill(3)+'.','small')
    chunk=story[entry_start:];del story[entry_start:];story.append(KeepTogether(chunk))
page();heading('Appendices and progressive laboratories')
p('The native reader has 47 sections: a separate preface first, then 40 numbered chapters and six appendices. Canonical selection follows books/inside-orch/manuscript/Book.txt. Chapter titles use Chapter N - Title; appendices use Appendix A - Title, matching the existing classifier.')
for a in outline['appendices']:
    heading(a['id']+'. '+a['title'],3);p(a['focus'])
heading('Eight laboratory stages',2)
table(['Lab','Question to resolve'],[['01','What survives a fresh default-server process, and what is lost?'],['02','What does the standalone planner/claim path guarantee under fit and concurrency conflicts?'],['03','How do repeated reconciliation and Docker adoption behave after drift or a lost report?'],['04','Which health/surge/availability conditions advance rollout and rollback?'],['05','Where do credentials, encrypted secrets and health probes cross trust boundaries?'],['06','What do namespace boundaries and quota decisions enforce in actual call paths?'],['07','How do GitOps partial failure and finite/time-based workloads converge?'],['08','What do migration/backup/load experiments prove, and what remains outside durable runtime recovery?']],[43,447])
page();heading('The quality gate is part of the book')
p('Every future chapter needs source evidence, a distinct engineering problem, a specific failure window, a safe experiment and worked answers. Mechanical checks catch changed corpus bytes and missing artifacts; independent review checks the meaning. Neither a tracker nor a word count establishes correctness.')
table(['Review','Required result'],[['Source fidelity','Exact source listings regenerated; historical/current SHAs and renamed paths correct.'],['Execution','Actual commands, versions, UTC timestamps, exit codes and sanitized logs; all skipped external checks visible.'],['Claims','No false durability, fencing, atomicity, resource-enforcement or HA promise.'],['Readers','Developer, DevOps and architect reviews with concrete source-backed findings resolved.'],['Publication','All-page PDF render review; EPUB structure/reader checks; complete accessible online navigation and verified downloads.'],['Release','Measured metadata, chosen rights, reproducible sources, exact final hashes and a reviewable site patch.']],[96,394])
heading('Rights and publication',2)
p('The author is Aleksandar Popovic. This pack has not selected a new public manuscript license or relabeled the source repository. No source license metadata was observed at the baseline. Rights, attribution and reused asset notices are reviewed explicitly before a public edition.')
p('The pack targets scripts/book_catalog.py and scripts/build-books.py in the actual website. Final integration includes three original posts about different chapters, an inside-orch glossary and stable updates entry. Generated book-pages/inside-orch, assets/books/inside-orch and _data/books.json stay ignored. The native build checks completeness and actual download formats. Live publication remains a separate authorized action; no application or website repository was changed by this delivery.')
page();heading('Sample chapter')
p('The following is a finished source-based specimen of the intended writing standard. It belongs to the early runtime-boundary material. It is not a substitute for the planned 40-chapter manuscript. Its code excerpts are unchanged; its shell experiment is a labeled teaching addition with expected, unexecuted observations.','small')

sample=(PACK/'samples/runtime-boundary.md').read_text()
code=False;lines=[];para=[]
def flushpara():
    if para:
        text=' '.join(para);p(text,'question' if re.match(r'^\*\*[1-4]\.',text) else 'body');para.clear()
def flushcode():
    raw='\n'.join(lines);visual=[]
    wrapped=False
    for line in clean(raw).expandtabs(4).splitlines():
        if len(line)>88:
            wrapped=True
            visual.extend(textwrap.wrap(line,width=88,subsequent_indent='    ',break_long_words=True,break_on_hyphens=False,replace_whitespace=False,drop_whitespace=False))
        else:visual.append(line)
    if wrapped:p('Print presentation wraps long lines; the companion Markdown and script preserve the copyable source.','small')
    story.append(Preformatted('\n'.join(visual),styles['code']));lines.clear()
for line in sample.splitlines():
    if line.startswith('```'):
        if code:flushcode();code=False
        else:flushpara();code=True
    elif code:lines.append(line)
    elif not line.strip():flushpara()
    elif line.startswith('# '):flushpara();heading(line[2:],1)
    elif line.startswith('## '):flushpara();heading(line[3:],2)
    elif line.startswith('### '):flushpara();heading(line[4:],3)
    else:para.append(line)
flushpara()
heading('The supplied package at a glance')
table(['Path','Purpose'],[['START_HERE.md','English site-root quick start and exact first task'],['SITE_WORKSPACE.md','Native Jekyll paths, ownership and publisher/check contract'],['ALL_100_PROMPTS.md','All full prompt texts in one file'],['prompts/','100 individually executable book-production tasks'],['editorial/','Outline, history and technical seeds, claim/source policy and quality gates'],['evidence/','Immutable orch snapshot/history plus 20 pinned native-site contract files'],['samples/','Source-based sample chapter and Bash teaching lab'],['examples/source-excerpts/','Six exact excerpt seeds with checksums and pinned line links'],['scripts/','Corpus validation, excerpt extraction, tracker management and future manuscript structure checks'],['state/','Machine-readable prompt index, all-pending tracker and pack verification result'],['publication/','Consistent author/title/edition metadata']],[160,330])
p('All paths above are under books/inside-orch. Start prompt 000 from the website repository root, keep both source locks immutable, and retain real validation as the book grows. The final artifact should let readers inspect the code, reproduce the lesson and understand exactly where its guarantees stop.')

doc=Doc(str(OUT),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=63,title='Inside orch - Book Blueprint and Sample',author='Aleksandar Popovic')
doc.addPageTemplates([PageTemplate(id='normal',frames=[Frame(48,63,499,728,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer)])
doc.build(story)
print(OUT)
