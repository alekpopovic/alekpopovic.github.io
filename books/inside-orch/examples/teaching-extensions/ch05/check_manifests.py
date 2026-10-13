#!/usr/bin/env python3
"""Teaching harness: execute upstream local parser, preserving each real outcome."""
from pathlib import Path
import json, subprocess, sys
cli=Path(sys.argv[1]).resolve(); here=Path(__file__).resolve().parent
cases=[('valid',0,'is valid'),('invalid-cpu',1,'invalid CPU'),('invalid-memory',1,'invalid memory'),('invalid-port',1,'container must be between'),('invalid-field',1,'field replica not found')]
results=[]
for name,want,text in cases:
 command=[str(cli),'validate',str(here/f'atlas-{name}.yaml')]
 result=subprocess.run(command,capture_output=True,text=True)
 results.append(dict(case=name,command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
 assert (result.returncode==0)==(want==0),results[-1]
 assert text in result.stdout+result.stderr,results[-1]
print(json.dumps({'scope':'Actual upstream CLI parser only; no deployment, placement or Docker claim.','cases':results},indent=2))
