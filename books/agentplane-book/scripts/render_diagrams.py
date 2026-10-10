#!/usr/bin/env python3
# Diagram prose/artwork: CC BY-SA 4.0. Rendering program: MIT.
"""Regenerate original diagrams. Requires the optional CairoSVG dependency."""
from pathlib import Path
from html import escape
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'book/assets'

class Drawing:
    def __init__(self,height=640):
        self.height=height
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="920" height="{height}" viewBox="0 0 920 {height}">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0L8,4L0,8Z" fill="#426c77"/></marker></defs>',
        '<rect width="920" height="'+str(height)+'" fill="white"/>']
    def box(self,x,y,w,h,lines,warn=False):
        fill,stroke=('#fcf1df','#a7793e') if warn else ('#eef6f6','#477b83')
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        first=y+h/2-(len(lines)-1)*13
        for i,line in enumerate(lines):
            self.parts.append(f'<text x="{x+w/2}" y="{first+i*26}" text-anchor="middle" dominant-baseline="middle" font-family="DejaVu Sans,sans-serif" font-size="19" fill="#183e49">{escape(line)}</text>')
    def path(self,d,both=False,dashed=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="#426c77" stroke-width="2.5" marker-end="url(#arrow)"'+(' marker-start="url(#arrow)"' if both else '')+(' stroke-dasharray="7 5"' if dashed else '')+'/>')
    def text(self,x,y,text,size=16):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="#34636e">{escape(text)}</text>')
    def save(self,name):
        s='\n'.join(self.parts+['</svg>']);(OUT/(name+'.svg')).write_text(s)
        cairosvg.svg2png(bytestring=s.encode(),write_to=str(OUT/(name+'.png')),scale=1.5)

# System context: two trust zones; no crowded crossing through the nodes.
d=Drawing(610)
d.box(300,10,320,60,['Browser / SDK / CLI'])
for x,label in [(20,'SAAS CONTROL PLANE'),(480,'CUSTOMER CLUSTER')]:
    d.parts.append(f'<rect x="{x}" y="105" width="420" height="425" rx="12" fill="white" stroke="#9bb8bd" stroke-width="2"/>')
    d.text(x+210,135,label,18)
left=[['API','Identity + tenant authorization'],['PostgreSQL','Intent + audit + outbox'],['Worker','Durable command transport'],['Connector gateway','Authenticated stream']]
right=[['Outbound connector','Customer-owned policy bounds'],['Operator + upstream adapter','Constrained local reconciliation'],['Agent Sandbox + runtime','Workspace + limited identity'],['Governed tool gateway','Policy + approval enforcement']]
for idx,lines in enumerate(left):
    y=155+idx*90;d.box(50,y,360,65,lines)
    if idx<3:d.path(f'M230 {y+65}V{y+90}')
for idx,lines in enumerate(right):
    y=155+idx*90;d.box(510,y,360,65,lines)
    if idx<3:d.path(f'M690 {y+65}V{y+90}')
d.path('M420 70V90H35V187H50')
d.path('M410 457H458V187H510',both=True)
d.text(460,562,'The connector initiates mTLS; the channel still carries remote authority.',17)
d.text(460,588,'Local policy bounds must reject requests outside the customer envelope.',17)
d.save('system-context')

positions=[(35,20),(515,20),(515,175),(35,175),(35,330),(515,330),(515,485),(35,485)]
def connect(d,i,j):
    x,y=positions[i];xx,yy=positions[j];w,h=370,90
    if yy==y:
        if xx>x:d.path(f'M{x+w} {y+h/2}H{xx}')
        else:d.path(f'M{x} {y+h/2}H{xx+w}')
    elif x==xx:d.path(f'M{x+w/2} {y+h}V{yy}')
    else:d.path(f'M{x+w/2} {y+h}L{xx+w/2} {yy}')

def flow(name,nodes,links,height=615,warnings=()):
    d=Drawing(height)
    for i,lines in enumerate(nodes):
        x,y=positions[i];d.box(x,y,370,90,lines,i in warnings)
    for i,j in links:connect(d,i,j)
    d.save(name)
flow('enrollment',[
 ['01  Authorize enrollment','Short-lived, scoped token'],
 ['02  Generate key locally','Private key never leaves cluster'],
 ['03  Submit CSR over TLS','Bind proof and token identity'],
 ['04  Validate and consume token','Atomic single-use boundary'],
 ['05  Sign certificate externally','Short-lived cluster identity'],
 ['06  Protect local key storage','No key material in SaaS logs'],
 ['07  Authenticate the stream','Check current certificate status'],
 ['08  Rotate and revoke','Reject stale or revoked authority']],[(i,i+1) for i in range(7)])
flow('command-flow',[
 ['01  Authorize operation','Scope + stable request identity'],
 ['02  Commit one transaction','Intent + audit + outbox'],
 ['03  Publish durable event','Retry without changing identity'],
 ['04  Deliver through JetStream','Duplicates remain possible'],
 ['05  Check local command','Scope + expiry + epoch + bounds'],
 ['06  Record and perform effect','Recipient-side operation identity'],
 ['07  Persist and reconcile result','Report a verified outcome'],
 ['UNKNOWN OUTCOME','Effect occurred; result was lost']],[(i,i+1) for i in range(6)]+[(5,7)],warnings=(7,))
flow('lifecycle',[
 ['Requested','Versioned desired state'],
 ['Provisioning','Observed resource creation'],
 ['Ready','Runtime + policy + identity'],
 ['Termination requested','Work may still be running'],
 ['Removal confirmed','Cleanup and retention recorded'],
 ['Disconnected / stale','Keep observation age and quota']],[(0,1),(1,2),(2,3),(3,4),(2,5),(5,3)],height=445,warnings=(5,))
flow('approval',[
 ['01  Authenticate request','Exact scope + operation'],
 ['02  Evaluate effective policy','Deny by default'],
 ['03  Bind pending approval','Actor + tool + input + revision'],
 ['04  Obtain human decision','Authorized approver + expiry'],
 ['05  Consume approval atomically','Single use; exact binding'],
 ['06  Invoke downstream tool','Separate effect idempotency'],
 ['REJECT','Changed input / expiry / replay']],[(0,1),(1,2),(2,3),(3,4),(4,5),(4,6)],warnings=(6,))
cover=(OUT/'cover.svg').read_bytes()
cairosvg.svg2png(bytestring=cover,write_to=str(OUT/'cover.png'))
print('Rendered five SVG/PNG diagrams and EPUB cover.')
