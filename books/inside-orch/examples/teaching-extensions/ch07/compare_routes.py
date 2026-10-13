#!/usr/bin/env python3
"""Static route-method comparison; YAML parsing is not semantic OpenAPI validation."""
from pathlib import Path
import json,re,yaml
B=Path(__file__).resolve().parents[3];S=B/'evidence/orch'
doc=yaml.safe_load((S/'api/openapi.yaml').read_text())
missing=[];internal=[];public=[]
normalize=lambda path: re.sub(r'\{[^}]+\}','{}',path)
for line,text in enumerate((S/'internal/api/api.go').read_text().splitlines(),1):
 match=re.search(r'HandleFunc\("(GET|POST|PUT|DELETE|PATCH) ([^"]+)',text)
 if not match: continue
 method,path=match.groups();entry=dict(method=method,path=path,line=line)
 if path.startswith('/v1/agent/'):
  internal.append(entry);continue
 if path=='/metrics':continue
 public.append(entry)
 operations=next((v for k,v in doc['paths'].items() if normalize(k)==normalize(path)),{})
 if method.lower() not in operations:missing.append(entry)
expected={'/v1/discovery/services','/v1/discovery/services/{name}','/v1/integrations/traefik/config'}
assert {item['path'] for item in missing}==expected,missing
assert all(not path.startswith('/v1/agent/') for path in doc['paths'])
print(json.dumps(dict(source_sha=json.loads((B/'evidence/source-lock.json').read_text())['baseline_sha'],scope='Registered method/path coverage only; agent paths intentionally internal; no schema or live response validation.',public_methods=len(public),internal_agent_methods=len(internal),missing_public_methods=missing),indent=2))
