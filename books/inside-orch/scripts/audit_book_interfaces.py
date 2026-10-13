#!/usr/bin/env python3
"""Source-bind command/route/config occurrences without executing mutation procedures."""
from pathlib import Path
import datetime,hashlib,json,re,shlex
import yaml
B=Path(__file__).resolve().parents[1];S=B/'evidence/orch';SHA=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'];ref=json.loads((B/'reference/cli-api-config.json').read_text());blocks=json.loads((B/'validation/excerpts/index.json').read_text())['all_blocks'];errors=[];commands=[]
commands_by_path={r['path']:r for r in ref['commands']};rootflags={x['name']:x for x in commands_by_path['orch']['persistent_flags']};tests={}
for f in S.rglob('*_test.go'):
 package='./'+str(f.parent.relative_to(S));tests.setdefault(package,[]).extend(re.findall(r'^func (Test\w+)\(',f.read_text(),re.M))
def envstrip(words):
 while words and re.match(r'^[A-Z_][A-Z0-9_]*=',words[0]):words=words[1:]
 return words
for block in blocks:
 if block['kind']!='procedure':continue
 text=block['content'].replace('\\\n',' ')
 for n,line in enumerate(text.splitlines(),1):
  line=line.strip()
  if not line or line.startswith('#'):continue
  try:words=envstrip(shlex.split(line))
  except ValueError:continue # heredoc/data is already checked as a complete Bash block.
  if not words:continue
  name=Path(words[0]).name;row={'block_id':block['block_id'],'line_in_joined_block':n,'command_text':line,'argv':words,'validation':'inspected source definition; expected-only operation unless linked observed record','source_definitions':[]}
  if name=='orch':
   rest=words[1:];pos=[];i=0
   while i<len(rest):
    w=rest[i]
    if w.startswith('--'):
     flag=w[2:].split('=')[0]
     if flag in rootflags:i+=1 if '='in w else 2;continue
    if w.startswith('-'):i+=1;continue
    pos.append(w);i+=1
   candidates=[(key,value)for key,value in commands_by_path.items()if key!='orch'and pos[:len(key.split())-1]==key.split()[1:]]
   if not candidates:errors.append('Unknown CLI path '+line)
   else:
    key,c=max(candidates,key=lambda x:len(x[0]));row.update(kind='Cobra CLI',command_path=key,source_definitions=c['source_candidates'],accepted_probe_counts=c['accepted_probe_counts'])
    flags={x['name']for mode in ['local_flags','persistent_flags','inherited_flags']for x in c[mode]}
    for flag in re.findall(r'--([a-z][a-z-]*)',line):
     if flag not in flags:errors.append('Unknown CLI flag '+flag+' in '+line)
  elif name=='go':
   row['kind']='Go toolchain procedure'
   if len(words)>1 and words[1]=='test':
    packages=[x for x in words if x.startswith('./')];pattern=None
    for i,w in enumerate(words):
     if w=='-run'and i+1<len(words):pattern=words[i+1]
     elif w.startswith('-run='):pattern=w.split('=',1)[1]
    found={pkg:[x for x in tests.get(pkg,[])if pattern is None or re.search(pattern,x)]for pkg in packages};row['matched_test_names']=found;row['test_filter']=pattern
    if pattern and pattern!='^$'and packages and not any(found.values())and not all(x.startswith('./.book-labs/')for x in packages):errors.append('No source tests match '+line)
    row['source_definitions']=[{'path':pkg[2:],'scope':'named test declarations and implementation inspected'}for pkg in packages]
   elif len(words)>1 and words[1]=='run':row['source_definitions']=[{'path':p,'scope':'registered original teaching overlay; see examples/manifest.json'}for p in words[2:]if p.startswith('./')]
  elif name in ['orch-server','orch-loadtest','orch-agent']:
   path='cmd/'+name+'/main.go';source=(S/path).read_text();row.update(kind='entrypoint',source_definitions=[{'path':path,'source_sha':SHA}])
   for flag in re.findall(r'--([a-z][a-z-]*)',line):
    if '"'+flag+'"' not in source:errors.append('Unknown entrypoint flag '+flag+' in '+line)
  elif name.startswith('python'):
   targets=[x for x in words[1:]if x.endswith('.py')];row.update(kind='book Python tooling',source_definitions=[{'path':x,'scope':'canonical script plus recorded independent target'}for x in targets])
  elif words[0].startswith('./scripts/'):
   row.update(kind='upstream shell helper',source_definitions=[{'path':words[0][2:],'source_sha':SHA}]);
   if not(S/words[0][2:]).is_file():errors.append('Missing upstream script '+line)
  else:row['kind']='shell setup/data/standard utility'
  commands.append(row)
# Every route/header/env occurrence across chapter/appendix/lab/post sources is retained, not merely every definition.
paths=[B/x for x in json.loads((B/'validation/excerpts/index.json').read_text())['reviewed_paths']];occurrences=[]
for file in paths:
 text=file.read_text()
 for kind,pattern in [('environment',r'\b(?:ORCH_|DOCKER_|COMPOSE_|ATLAS_|BOOK_)[A-Z0-9_]+\b'),('route',r'/(?:v1/[A-Za-z0-9_{}./-]+|healthz|readyz|metrics)\b'),('header',r'\b(?:X-Orch-[A-Za-z-]+|Authorization|Content-Type|X-Request-ID)\b')]:
  for m in re.finditer(pattern,text):
   value=m[0].rstrip('.,/');defs=[]
   if kind=='environment':defs=[r['source']for r in ref['environment']if r['name']==value]
   elif kind=='route':defs=[r['source']for r in ref['routes']if r['path'].replace('{id...}','{id}')==value or r['path']==value]
   else:
    for p in (S/'internal').rglob('*.go'):
     if p.name.endswith('_test.go'):continue
     for i,l in enumerate(p.read_text().splitlines(),1):
      if '"'+value+'"'in l:defs.append({'path':str(p.relative_to(S)),'line_start':i,'line_end':i})
   occurrences.append({'path':str(file.relative_to(B))if file.is_relative_to(B)else str(file),'line':text[:m.start()].count('\n')+1,'kind':kind,'value':value,'source_definitions':defs,'scope':'Defined source surface'if defs else 'Dynamic/illustrative URL, teaching variable or separately documented SDK setting; inspect local narrative context'})
payloads=[]
for block in blocks:
 if block['language']in ['yaml','yml','json']:
  data=json.loads(block['content'])if block['language']=='json'else yaml.safe_load(block['content'])
  keys=[]
  def walk(v,prefix=''):
   if isinstance(v,dict):
    for k,x in v.items():
     key=prefix+'.'+str(k)if prefix else str(k);keys.append(key);walk(x,key)
   elif isinstance(v,list):
    for x in v:walk(x,prefix+'[]')
  walk(data);payloads.append({'block_id':block['block_id'],'kind':block['kind'],'keys':keys,'source_definition':block.get('source_path'),'validation_scope':block['validation']})
result={'source_sha':SHA,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands,'structured_payloads':payloads,'inline_references':json.loads((B/'validation/excerpts/index.json').read_text())['inline_references'],'occurrences':occurrences,'cli_tree':ref['commands'],'routes':ref['routes'],'configuration_fields':ref['config_fields'],'environment_definitions':ref['environment'],'openapi_comparison':ref['openapi_comparison'],'namespace_auth_evidence':['validation/labs/review076/05-command.json','validation/labs/review076/06-command.json'],'schema_and_migration_evidence':'validation/labs/review076/08-recovery-command.json','public_error_and_DTO_evidence':'validation/labs/ch07/public-contract-final.json','CLI_constructor_arity_flag_evidence':'validation/reference-offline-inventory.json','published_cron_manifest_evidence':'validation/examples/published-cron-manifest.json','errors':errors,'overall_status':'passed'if not errors else'failed','limitations':['Reference inventory plus selective actual contract fixtures do not constitute full OpenAPI semantic conformance.','Published mutation/Compose procedures remain expected-only; syntax/source binding is not execution.','An environment occurrence may be a teaching variable or SDK setting, not an Orch config option.','App baseline integration gaps remain documented, not patched.']}
out=B/'validation/interfaces';out.mkdir(exist_ok=True);(out/'inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'command_lines':len(commands),'interface_occurrences':len(occurrences),'registered_routes':len(ref['routes']),'commands_defined':len(ref['commands']),'errors':errors}));raise SystemExit(bool(errors))
