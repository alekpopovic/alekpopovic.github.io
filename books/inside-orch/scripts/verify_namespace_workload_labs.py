#!/usr/bin/env python3
"""Check retained observed lab results and frozen canonical input hashes offline."""
import argparse
import hashlib
import json
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--lab', choices=['06', '07'], required=True)
a = p.parse_args()
check = json.loads((BOOK / f'validation/labs/{a.lab}-check.json').read_text())
lock = json.loads((BOOK / 'evidence/source-lock.json').read_text())['baseline_sha']
assert check['source_sha'] == lock
for path, digest in check['inputs'].items():
    assert hashlib.sha256((BOOK / path).read_bytes()).hexdigest() == digest, path
run = json.loads((BOOK / check['run_record']).read_text())
assert run['source_sha'] == lock and run['exit_code'] == 0 and run['status'] == 'passed'
assert not Path(run['cwd']).resolve().is_relative_to((BOOK / 'evidence/orch').resolve())
for path, digest in check['output_hashes'].items():
    assert hashlib.sha256((BOOK / path).read_bytes()).hexdigest() == digest, path
observed = json.loads((BOOK / run['stdout']).read_text())
assert observed['source_sha'] == lock
cases = {c['id']: c for c in observed['cases']}
assert len(cases) == observed['case_count'] == len(check['cases'])
assert all(c['passed'] is True for c in cases.values())
if a.lab == '06':
    required = {'duplicate-local-name', 'cross-id-hidden', 'secret-reference-isolation',
                'zero-is-unlimited', 'concurrent-final-slot', 'denied-scale-atomic',
                'header-precedes-query', 'query-fallback', 'history-blocks-namespace-delete',
                'independent-servers-no-shared-state'}
    assert required <= cases.keys() and len(cases) >= 10
    for c in cases.values():
        assert {'tenant','actor','source_route','initial_quota','requested_delta',
                'expected_response','observed_response','final_usage'} <= c.keys()
    usage = cases['concurrent-final-slot']['final_usage']
    assert (usage['services'], usage['replicas'], usage['cpu_millicores'], usage['memory_bytes'], usage['public_ports']) == (2, 3, 300, 3 * 64 * 1024**2, 1)
    assert observed['postgresql_quota_test'].startswith('not executed')
    output = (BOOK / run['stdout']).read_text()
    for secret in ['non-sensitive-fixture', 'non-sensitive-password', 'non-sensitive-book-payments', 'non-sensitive-book-observability']:
        assert secret not in output
else:
    required = {'unchanged-sync-no-new-version','failed-fetch-no-prune','prune-preserves-unrelated',
                'partial-apply-not-atomic','job-exit-zero','job-limit-terminal',
                'latest-attempt-log-selection','cron-forbid-active','cron-replace-active',
                'cron-resume-catches-backlog','dst-spring-missing-local-0230',
                'dst-fall-repeated-local-0230','cron-cli-manifest','job-cli-success-manifest'}
    assert required <= cases.keys() and len(cases) >= 12
    assert len(observed['fixture_revisions']) == 3
    assert all(re.fullmatch('[0-9a-f]{40}', s) for s in observed['fixture_revisions'])
    assert observed['job_attempts'] == 2 and observed['job_statuses'] == ['succeeded','failed']
    assert observed['clock_instants']['spring_next'] == '2026-03-30T00:30:00Z'
    assert observed['clock_instants']['fall_due'] == ['2026-10-25T02:30:00+02:00','2026-10-25T02:30:00+01:00']
    assert cases['prune-preserves-unrelated']['observed'] == {'manual':'active','worker':'deleted'}
print(json.dumps({'lab': a.lab, 'source_sha': lock, 'case_count': len(cases), 'status':'passed',
                  'scope':'offline validation of retained scoped execution; not a fresh experiment'}))
