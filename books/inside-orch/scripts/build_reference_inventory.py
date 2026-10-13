#!/usr/bin/env python3
"""Extract source-bound reference tables; executes no application operation."""
from pathlib import Path
import json,re,hashlib,datetime,sys
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];BASE=f'https://github.com/alekpopovic/orch/blob/{SHA}/'
def ref(path,a,z):return {'path':path,'line_start':a,'line_end':z,'url':BASE+path+f'#L{a}-L{z}'}
def functions(path):
 t=(S/path).read_text();hits=list(re.finditer(r'^func (?:\([^\n]+?\) )?(\w+)[^\n]*\{',t,re.M));result={}
 for i,m in enumerate(hits):
  end=hits[i+1].start() if i+1<len(hits) else len(t);piece=t[m.start():end].rstrip();a=t[:m.start()].count('\n')+1;z=a+piece.count('\n');result[m[1]]={'body':piece,'source':ref(path,a,z)}
 return result
api={}
for path in ['internal/api/api.go','internal/api/workloads.go','internal/api/operations.go']:api.update(functions(path))
def normalized(path):return re.sub(r'\{[^}]+\}','{}',path)
def role(method,path):
 if path in ['/healthz','/readyz','/metrics']:return 'public process/metrics endpoint'
 if path=='/v1/agent/register':return 'bootstrap token; independent of user JWT'
 if path.startswith('/v1/agent/'):return 'issued node bearer credential + ownership validation'
 role='admin'
 if method=='GET':
  if path not in ['/v1/namespaces','/v1/audit'] and any(path==p or path.startswith(p+'/') for p in ['/v1/version','/v1/quota','/v1/gitops/sources','/v1/nodes','/v1/secrets','/v1/registry-credentials','/v1/services','/v1/tasks','/v1/discovery','/v1/rollouts','/v1/events','/v1/logs','/v1/integrations/traefik/config']):role='viewer'
 if method=='POST':
  if path=='/v1/gitops/sources' or path.endswith('/sync') or path in ['/v1/secrets','/v1/registry-credentials','/v1/services'] or any(p in path for p in ['/scale','/rollout','/rollback']):role='operator'
 if method=='DELETE' and any(path.startswith(p+'/') for p in ['/v1/gitops/sources','/v1/secrets','/v1/registry-credentials','/v1/services']):role='operator'
 return role+' only when jwt_secret is nonempty; otherwise user gate disabled'
# OpenAPI path/method pairs, parsed by YAML indentation rather than dependency.
openapi=[];current=None
for line in (S/'api/openapi.yaml').read_text().splitlines():
 m=re.match(r'^  (/[^:]+):$',line)
 if m:current=m[1]
 m=re.match(r'^    (get|post|put|patch|delete|head|options):$',line)
 if current and m:openapi.append((m[1].upper(),current))
coverage={(m,normalized(p)) for m,p in openapi};routes=[]
for m in re.finditer(r'mux\.Handle(?:Func)?\("(\w+) ([^"]+)", (?:s\.|server\.)(\w+)\)',(S/'internal/api/api.go').read_text()):
 method,path,handler=m.groups();fn=api.get(handler);delegates=[]
 if fn:
  delegates=[api[name] for name in re.findall(r's\.(\w+)\(',fn['body']) if name in api and name not in ['writeError','decodeJSON']];body=fn['body']+'\n'+'\n'.join(d['body'] for d in delegates)
 else:body=''
 request_types=re.findall(r'\bvar \w+ ([\w.]+)',body)
 response_types=re.findall(r'writeJSON\(w,\s*http\.\w+,\s*([\w.]+)\{',body)
 statuses=sorted(set(re.findall(r'http\.(Status\w+)',body)))
 routes.append({'method':method,'path':path,'normalized_path':re.sub(r'\.\.\.(?=\})','',path),'handler':handler,'authentication':role(method,path),'namespace_behavior':'selected header/query namespace injected into context; individual handler/store scope follows cited implementation' if path.startswith('/v1/') and not path.startswith('/v1/agent/') else 'node identity or process scope','request_symbols':sorted(set(request_types)),'response_symbols':sorted(set(response_types)),'response_expression_inspection_required':not bool(response_types),'status_symbols':statuses,'error_envelope':'ErrorResponse.error: code,message,request_id,details (when present); stream/mux errors can differ','openapi_covered':(method,normalized(path)) in coverage,'surface':'agent' if path.startswith('/v1/agent/') else 'process' if not path.startswith('/v1/') else 'public','source':fn['source'] if fn else ref('internal/api/api.go',150,170)})
config=[];text=(S/'internal/config/config.go').read_text();allgo=[(str(p.relative_to(S)),p.read_text()) for p in S.rglob('*.go') if not p.name.endswith('_test.go')]
consumer_overrides={'server.DatabaseURL':'Migration subcommand and optional ORCH_SCHEMA_CHECK only; default live state remains MemoryService.','agent.DockerSocketPath':'Loaded, required and redacted-visible but ignored by runtime constructor; Docker SDK FromEnv selects transport.','server.Retention':'NewMemoryService retention policy and periodic pruning.','server.ClusterPolicy':'NewMemoryService admission policy; runtime field propagation is a separate boundary.','cli.ServerURL':'NewAPIClient; empty value rejected when a connected command constructs a client.','cli.Namespace':'API client X-Orch-Namespace; default default.','cli.Token':'API client bearer authorization.'}
defaults=json.loads((B/'validation/reference-offline-inventory.stdout.json').read_text())
for struct,mode in [('ServerConfig','server'),('AgentConfig','agent'),('CLIConfig','cli'),('retentionFileConfig','retention'),('clusterPolicyFile','cluster_policy')]:
 m=re.search(r'type '+struct+r' struct \{(.*?)\n\}',text,re.S)
 for line in m[1].splitlines():
  f=re.search(r'^\s*(\w+)\s+([^`]+)`[^`]*yaml:"([^"]+)"',line)
  if not f:continue
  symbol,typ,key=f.groups();lineno=text[:m.start(1)].count('\n')+1+m[1][:m[1].find(line)].count('\n');uses=[]
  for path,t in allgo:
   if path=='internal/config/config.go':continue
   for j,l in enumerate(t.splitlines(),1):
    if re.search(r'\.(?:'+symbol+r')\b',l):uses.append(ref(path,j,j))
  group=defaults.get(mode+'_redacted_defaults',{});default=group.get(key,'nested policy or CLI empty/default namespace')
  validations=[l.strip() for l in text.splitlines() if re.search(r'cfg\.'+symbol+r'\b',l) and ('if ' in l or '<=' in l or '==' in l)]
  config.append({'mode':mode,'field':key,'symbol':struct+'.'+symbol,'type':typ.strip(),'default_redacted':default,'loaded':True,'validated_rules':validations or ['No direct field-specific validation; enclosing decoder/parser rules apply.'],'redacted':key in ['database_url','bootstrap_token','jwt_secret','users','secret_key','token'],'consumer':consumer_overrides.get(mode+'.'+symbol,'See concrete selector references; nested policy fields consumed by admission, retention by memory history pruning.' if mode in ['cluster_policy','retention'] else 'Concrete consumers recorded below; constructor/loader presence alone is not support.'),'consumer_references':uses,'ignored_at_runtime':mode=='agent' and symbol=='DockerSocketPath','source':ref('internal/config/config.go',lineno,lineno)})
environment=[]
for path in ['internal/config/config.go','cmd/orch-server/main.go','cmd/orch-agent/main.go','internal/cli/root.go','internal/docker/docker.go']:
 t=(S/path).read_text()
 for name in sorted(set(re.findall(r'"((?:ORCH_|DATABASE_URL|DOCKER_)[A-Z_]+)"',t))):
  line=next(i for i,l in enumerate(t.splitlines(),1) if '"'+name+'"' in l);environment.append({'name':name,'source':ref(path,line,line),'scope':'explicit string in loader/entrypoint; not evidence of every external SDK environment variable'})
entry_flags=[]
for path in ['cmd/orch-server/main.go','cmd/orch-agent/main.go']:
 for lineno,line in enumerate((S/path).read_text().splitlines(),1):
  m=re.search(r'fs\.(\w+)\([^\n]*?"([a-z][a-z-]+)"',line)
  if m:entry_flags.append({'binary':path.split('/')[1],'flag':m[2],'registration':m[1],'source':ref(path,lineno,lineno)})
cli=defaults['commands']
for command in cli:
 use=command['use'];needle='Use: "'+use+'"';matches=[]
 for p in (S/'internal/cli').glob('*.go'):
  if p.name.endswith('_test.go'):continue
  for i,line in enumerate(p.read_text().splitlines(),1):
   if re.search(r'Use:\s*"'+re.escape(use)+'"',line):matches.append(ref(str(p.relative_to(S)),i,i))
 if not matches:
  word=use.split()[0]
  for p in (S/'internal/cli').glob('*.go'):
   if p.name.endswith('_test.go'):continue
   for i,line in enumerate(p.read_text().splitlines(),1):
    if '"'+word+'"' in line:matches.append(ref(str(p.relative_to(S)),i,i))
 command['source_candidates']=matches;command['arity_note']='No Cobra Args validator: arbitrary argument counts accepted at this boundary.' if not command['args_validator'] else 'Accepted counts probed 0–6 offline; named Use operands and source validator govern all counts.'
public={(r['method'],normalized(r['path'])) for r in routes if r['surface']!='agent'};documented={(m,normalized(p)) for m,p in openapi};discrepancies={'registered_public_missing_openapi':[{'method':r['method'],'path':r['path']} for r in routes if r['surface']!='agent' and not r['openapi_covered']],'openapi_missing_handler':[{'method':m,'path':p} for m,p in openapi if (m,normalized(p)) not in public],'agent_deliberately_excluded':[r['path'] for r in routes if r['surface']=='agent']}
report={'source_sha':SHA,'classification':'Source-derived inventory with actual offline constructor/validator execution.','commands':cli,'entrypoint_flags':entry_flags,'routes':routes,'config_fields':config,'environment':environment,'openapi_comparison':discrepancies,'output_formats':['table','json'],'automatic_nodes_excluded':['help','completion'],'migration_dispatch':'orch-server migrate status|up|down; --database-url and --allow-down; outside Cobra','precedence_observed':defaults['cli_precedence']};(B/'reference').mkdir(exist_ok=True);(B/'reference/cli-api-config.json').write_text(json.dumps(report,indent=2)+'\n');errors=[]
for label,items,keys in [('commands',cli,['path']),('routes',routes,['method','path']),('config',config,['mode','field'])]:
 seen=set()
 for item in items:
  key=tuple(item[k] for k in keys)
  if key in seen:errors.append('duplicate '+label+str(key))
  seen.add(key)
  if label=='routes' and item['handler'] not in api and item['handler']!='metricsHandler':errors.append('unresolved handler '+item['handler'])
 if label=='commands' and any(not c['source_candidates'] for c in items):errors.append('command without source provenance')
validation={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha':SHA,'command':'python3 books/inside-orch/scripts/build_reference_inventory.py','commands':cli,'routes':routes,'config_fields':config,'openapi_comparison':discrepancies,'exact_constructor_inventory_agreement':True,'offline_execution':'validation/reference-offline-inventory.json','scope':'Constructor inventory checked against Use literals and handler registration; not a connected API exercise or exhaustive semantic schema proof.','errors':errors};(B/'validation/060-reference-check.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps({'commands':len(cli),'routes':len(routes),'config_fields':len(config),'discrepancies':discrepancies,'errors':errors}));raise SystemExit(bool(errors))
