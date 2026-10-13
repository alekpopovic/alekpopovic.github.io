from pathlib import Path
from xml.sax.saxutils import escape
B=Path(__file__).resolve().parents[2];out=B/'examples/diagrams/task-lifecycle.svg'
nodes=[('pending',210,44,False),('assigned',210,106,False),('pulling',210,168,False),('created',210,230,False),('running',210,292,False),('healthy',210,365,False),('unhealthy',530,365,False),('stopped',210,438,True),('failed',530,292,True),('removed',530,438,True)]
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="780" height="650" viewBox="0 0 780 650" role="img" aria-labelledby="title desc">
<title id="title">Selected task lifecycle transitions and their owners</title>
<desc id="desc">Server assigns pending to assigned. Accepted agent reports progress assigned to pulling, pulling to created, created to running, running to healthy, healthy to unhealthy and unhealthy to healthy. Healthy can stop, running can fail, and stopped or failed can be removed subject to desired-state checks. Removed accepts duplicate removed acknowledgements. Stopped, failed and removed are terminal for execution. This is a selection, not the full transition graph.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#334155"/></marker></defs>
<rect width="780" height="650" fill="#ffffff"/>
<g fill="none" stroke="#334155" stroke-width="2" marker-end="url(#arrow)">''']
for a,b in [(44,106),(106,168),(168,230),(230,292),(292,365),(365,438)]:s.append(f'<path d="M210 {a+18}V{b-20}"/>')
s+=['<path d="M282 292H456"/>','<path d="M282 350Q370 320 456 350"/>','<path d="M458 380Q370 410 284 380"/>','<path d="M282 438H456"/>','<path d="M602 292H720V428H604"/>','<path d="M602 450C690 480 690 520 600 520H530V458"/>','</g>']
for label,x,y,terminal in nodes:
 fill='#eef2ff' if not terminal else '#e2e8f0';stroke='#6366f1' if not terminal else '#0f172a'
 s.append(f'<rect x="{x-72}" y="{y-18}" width="144" height="36" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 s.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="sans-serif" font-size="22" fill="#0f172a">{escape(label)}</text>')
s+=['<g font-family="sans-serif" font-size="20" fill="#334155">','<text x="298" y="80">server assignment</text>','<text x="298" y="154">accepted agent reports</text>','<text x="298" y="216">accepted agent reports</text>','<text x="340" y="278">failure</text>','<text x="340" y="332">health</text>','<text x="340" y="372">recovery</text>','<text x="26" y="409">cleanup report</text>','<text x="318" y="460">cleanup *</text>','<text x="625" y="350">cleanup *</text>','<text x="470" y="549">duplicate acknowledgement</text>','<text x="26" y="584">* Cleanup to removed depends on desired-state checks.</text>','<text x="26" y="613">Gray states are terminal for execution.</text><text x="26" y="642">Selected legal edges; other valid transitions are omitted.</text>','</g></svg>']
out.write_text('\n'.join(s)+'\n')
