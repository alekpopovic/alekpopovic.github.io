#!/usr/bin/env python3
"""Verify persisted author-run results; does not rerun the source application."""
import argparse
import csv
import datetime
import hashlib
import json
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--lab', choices=['04', '05'], required=True)
a = p.parse_args()
def read(rel):
    return json.loads((BOOK / rel).read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
checks = []
def check(name, ok):
    checks.append({'name': name, 'passed': bool(ok)})
    if not ok:
        raise SystemExit('Failed: ' + name)
if a.lab == '04':
    command = 'validation/labs/lab04-rollout-observed.json'
    r = read(command)
    observation = r['stdout']
    x = read(observation)
    rows = list(csv.DictReader((BOOK / 'validation/labs/04-timeline.csv').open()))
    check('actual command exit zero', r['exit_code'] == 0 and x['status'] == 'passed')
    check('at least six observed checkpoints', len(rows) == len(x['timeline']) >= 6)
    previous_old = 3
    for row, c in zip(rows, x['timeline']):
        check('CSV stage and captured deployment match', row['stage'] == c['stage'] and row['deployment_id'] == c['deployment']['id'])
        old, target, healthy = (int(row[k]) for k in ['old_active', 'target_active', 'target_healthy'])
        check('modeled surge <= replicas + one', old + target <= 4)
        check('modeled availability >= three', int(row['modeled_available']) >= 3)
        if old < previous_old:
            check('old stops have healthy replacement coverage', healthy >= 3 - old)
        previous_old = old
    by_stage = {c['stage']: c for c in x['timeline']}
    check('exhausted placement remains pending', any(t['actual_status'] == 'pending' for t in by_stage['capacity-exhausted']['tasks'] if t['version'] == 2))
    check('running target cannot stop old replica', by_stage['running-but-not-healthy']['old_active'] == 3 and by_stage['running-but-not-healthy']['pending_stops'] == 0)
    check('at least three negative operations', len(x['negative_cases']) >= 3)
    check('no duplicate work on repeated passes', x['identical_rollout_idempotent'] and x['repeated_pass_did_not_duplicate'])
    check('failed history survives separate rollback', x['failed_deployment'] == x['preserved_failed_history'] and x['rollback_deployment']['id'] != x['failed_deployment']['id'] and x['rollback_deployment']['to_version'] == 1)
    check('terminal revival and stale update refused', all(k in x['negative_cases'] for k in ['terminal_revival', 'stale_deployment_status', 'late_healthy_report', 'no_previous_version']))
    check('delete canceled active work', x['delete_canceled_deployment']['status'] == 'failed')
    check('model completion does not imply acknowledged final stop', x['timeline'][-1]['deployment']['status'] == 'succeeded' and x['timeline'][-1]['pending_stops'] == 1)
else:
    command = 'validation/labs/lab05-security-local-probes.json'
    r = read(command)
    observation = r['stdout']
    x = read(observation)
    check('actual command exit zero', r['exit_code'] == 0 and x['status'] == 'passed')
    check('at least twelve actual boundary cases', len(x['cases']) >= 12)
    cases = {c['id']: c for c in x['cases']}
    for c in x['cases']:
        if 'expected_http' in c:
            check('HTTP ' + c['id'], c['expected_http'] == c['actual_http'])
        if 'expected_healthy' in c:
            check('probe ' + c['id'], c['expected_healthy'] == c['actual_healthy'])
            check('only local probe destination', c['destination'].startswith(('http://127.0.0.1:', 'http://[::1]:')))
    check('wrong node refused without mutation', cases['wrong-node-credential']['actual_http'] == 401 and x['wrong_node_unchanged_task'])
    check('rotated old credential rejected', cases['rotated-old-token-denied']['actual_http'] == 401)
    check('cross-origin target never contacted', x['cross_origin_destination_requests'] == 0 and not cases['cross-origin-blocked']['actual_healthy'])
    check('permitted plaintext verified separately', x['assigned_agent_plaintext_permitted'])
    check('envelope roundtrip and key loss boundaries', x['same_key_roundtrip'] and x['wrong_key_rejected'] and not x['ciphertext_contains_plaintext'])
    base = BOOK / 'validation/labs/05-forbidden-channels'
    for f in x['scanned_forbidden_channels']:
        path = (base / f['file']).resolve()
        check('scanned channel stays inside owned directory', path.parent == base.resolve())
        check('scanned bytes unchanged: ' + f['file'], sha(path) == f['sha256'] and path.stat().st_size == f['bytes'] and not f['canary_found'])
    check('logs, errors, metadata and audits scanned', {'captured-logs.txt', 'wrong-envelope-error.txt', 'secret-get-metadata.txt', 'secret-audit-redacted.txt', 'missing-secret-error.txt'} <= {f['file'] for f in x['scanned_forbidden_channels']})
result = {'status': 'passed', 'source_sha': r['source_sha'], 'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'Verification of persisted author-run records and their byte integrity; no new application execution.',
          'command_record': command, 'observation_record': observation, 'observation_sha256': sha(BOOK / observation), 'checks': checks}
out = BOOK / f'validation/labs/{a.lab}-check.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'passed', 'lab': a.lab, 'checks': len(checks), 'output': str(out.relative_to(BOOK))}))
