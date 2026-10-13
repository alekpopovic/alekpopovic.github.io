#!/usr/bin/env python3
"""Give granular, source-backed reference assertions stable claim identities."""
from pathlib import Path
import json,re,hashlib
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';A=json.loads((B/'reference/cli-api-config.json').read_text());SHA=A['source_sha'];out=[]
def add(ident,statement,path,a,z,classification='runtime-integrated',validation='inspected',evidence=None,limitations=None):
 out.append({'claim_id':ident,'statement':statement,'classification':classification,'source_path':path,'source_sha':SHA,'line_start':a,'line_end':z,'associated_commits':[],'validation':validation,'evidence_log':evidence,'limitations':limitations or ['Exact reference assertion at the locked source; does not establish broader system integration or production fitness.']})
for x in A['commands']:
 r=x['source_candidates'][0];ident='reference.cli.'+x['path'].replace(' ','-');add(ident,'Cobra constructs '+x['path']+' with Use '+repr(x['use'])+'; the offline constructor inventory records its exact flags and arity probes.',r['path'],r['line_start'],r['line_end'],validation='executed',evidence='validation/reference-offline-inventory.json',limitations=['Constructor execution and local help only; no connected operation or application side effect inferred.','The inventory uses an explicit privacy override for the machine-specific default config path.'])
router=(S/'internal/api/api.go').read_text().splitlines()
for x in A['routes']:
 line=next(i for i,t in enumerate(router,1)if '"'+x['method']+' '+x['path']+'"'in t);ident='reference.api.'+hashlib.sha256((x['method']+' '+x['path']).encode()).hexdigest()[:12];add(ident,x['method']+' '+x['path']+' is registered to '+x['handler']+'.','internal/api/api.go',line,line,limitations=['Registration does not establish every DTO/status schema; companion inventory separately traces handlers, role middleware and OpenAPI coverage.'])
for x in A['config_fields']:
 r=x['source'];add('reference.config.'+x['mode']+'.'+x['field'],x['symbol']+' declares YAML field '+repr(x['field'])+' with Go type '+x['type']+'.',r['path'],r['line_start'],r['line_end'],limitations=['Declaration does not prove validation, consumption or runtime enforcement; companion explicitly records ignored DockerSocketPath and inactive live DatabaseURL semantics.'])
M=json.loads((B/'reference/measurement-contracts.json').read_text())
for x in M['registered_metrics']:
 a=int(x['source'].split('#L')[1]);add('reference.metric.'+x['name'],x['name']+' is registered as '+x['collector']+' with labels '+repr(x['labels'])+'.','internal/metrics/prometheus.go',max(1,a-1),min(a+5,len((S/'internal/metrics/prometheus.go').read_text().splitlines())),limitations=['Collector declaration is not proof an unwired controller emits samples, that a scrape ran, or that an alert fired.'])
L=json.loads((B/'reference/lifecycle.json').read_text());text=(S/'pkg/types/lifecycle.go').read_text();symbols={'task_actual':'ValidateTaskTransition','task_desired':'ValidateTaskDesiredTransition','service':'ValidateServiceTransition','node':'ValidateNodeTransition','deployment':'ValidateDeploymentTransition'}
for domain,matrix in L['matrices'].items():
 idx=text.index('func '+symbols[domain]);a=text[:idx].count('\n')+1;nextfunc=re.search(r'^func ',text[idx+5:],re.M);z=text[:idx+5+nextfunc.start()].count('\n')if nextfunc else len(text.splitlines())
 for state,successors in matrix.items():add('reference.lifecycle.'+domain+'.'+state,'Generic '+domain+' validator accepts '+state+' → '+', '.join(successors)+'.','pkg/types/lifecycle.go',a,z,validation='executed',evidence='validation/reference-offline-inventory.json',limitations=['Generic state edge only; authenticated agent report guard, current desired intent, service policy and physical side effects remain separate.'])
(B/'validation/evidence/reference-detail.json').write_text(json.dumps({'source_sha':SHA,'claims':out,'scope':'Granular appendix reference assertions; stable IDs derived from interface identity, not mutable line numbers.'},indent=2)+'\n');print(json.dumps({'reference_claims':len(out)}))
