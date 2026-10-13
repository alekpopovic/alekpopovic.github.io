#!/usr/bin/env python3
"""Summarize only explicit scheduler benchmark samples; never estimate production capacity."""
import hashlib,json,re,statistics,sys
from pathlib import Path
book=Path(__file__).resolve().parents[3]
record=json.loads((book/'validation/labs/ch39/bounded-benchmarks.json').read_text())
raw=(book/record['stdout']).read_text()
rows=[dict(iterations=int(m[1]),ns_per_op=int(m[2]),bytes_per_op=int(m[3]),allocations_per_op=int(m[4])) for m in re.finditer(r'^BenchmarkSchedulerScoring-2\s+(\d+)\s+(\d+) ns/op\s+(\d+) B/op\s+(\d+) allocs/op$',raw,re.M)]
assert len(rows)==3
cpu=re.search(r'^cpu: (.+)$',raw,re.M).group(1).strip()
print(json.dumps(dict(source_sha=record['source_sha'],command=record['command'],started_at_utc=record['started_at_utc'],finished_at_utc=record['finished_at_utc'],go='1.25.0',goos='linux',goarch='amd64',cpu=cpu,gomaxprocs=2,workload=dict(ready_nodes=100,pending_tasks=1000,cpu_per_task_millicores=100,memory_per_task_bytes=64<<20,random_seed=None),samples=rows,median_ns_per_op=statistics.median(x['ns_per_op'] for x in rows),range_ns_per_op=[min(x['ns_per_op'] for x in rows),max(x['ns_per_op'] for x in rows)],raw_stdout_sha256=hashlib.sha256(raw.encode()).hexdigest(),limitations=['Three short samples on a shared host; no statistical confidence interval inferred.','Pure Plan only: no HTTP, database, Docker or container startup.','API benchmark raw logs interleave with result labels; not automatically attributed here.']),indent=2))
