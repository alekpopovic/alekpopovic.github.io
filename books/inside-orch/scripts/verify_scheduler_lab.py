#!/usr/bin/env python3
"""Check recorded finite planner observations, exact fixture hashes and test scope."""
from pathlib import Path
import datetime
import hashlib
import json

BOOK = Path(__file__).resolve().parents[1]
SOURCE = 'cbfc94ade5b57e449d6b73bf1485b1c5b1647022'
inputs = ['examples/teaching-extensions/lab02/main.go',
          'labs/02-scheduler-placement/fixtures/plan.json']
input_hashes = {p: hashlib.sha256((BOOK / p).read_bytes()).hexdigest() for p in inputs}
metadata = json.loads((BOOK / 'labs/02-scheduler-placement/lab.json').read_text())
assert metadata['inputs'] == input_hashes
model_record = json.loads((BOOK / 'validation/labs/lab02-model-and-permutations.json').read_text())
assert model_record['exit_code'] == 0 and model_record['source_sha'] == SOURCE
observed = json.loads((BOOK / model_record['stdout']).read_text())
assert observed['status'] == 'passed' and observed['source_sha'] == SOURCE
orders = observed['distinct_input_permutations']
assert observed['permutations_checked'] == 24
assert len({json.dumps(o, sort_keys=True) for o in orders}) == 24
assignments = observed['assignments']
expected = [('atlas-01', 'c', 31080), ('atlas-02', 'b', 30000), ('atlas-03', 'c', 30000)]
actual = [(a['task_id'], a['node_id'], a['ports'][0]['published_port']) for a in assignments]
assert actual == expected
assert observed['pending_no_fit'] == ['atlas-04', 'atlas-05', 'atlas-06']
assert observed['lexical_tie_node'] == 'b'
assert observed['actual_stopping_desired_running_counted']
assert observed['desired_stopped_before_actual_ack_excluded']
assert observed['accounted_resources'] == {'b': {'cpu': 500, 'memory': 192 * 1048576},
                                         'c': {'cpu': 800, 'memory': 256 * 1048576}}
assert observed['memory_path']['ordinary_task_resource_requirements_absent']
assert observed['memory_path']['declared_requests']['cpu'] > observed['memory_path']['advertised_allocatable']['cpu']
assert observed['memory_path']['actual_task_status'] == 'assigned'
test_record = json.loads((BOOK / 'validation/labs/lab02-concurrent-claims.json').read_text())
assert test_record['exit_code'] == 0
events = [json.loads(line) for line in (BOOK / test_record['stdout']).read_text().splitlines()]
required = {'TestConcurrentSchedulerAttemptsAssignTaskOnce',
            'TestConcurrentRunOnceAssignsTaskOnceAcrossSchedulers',
            'TestRunOnceAccountsForNonTerminalAssignedTasks'}
passed = {e.get('Test') for e in events if e.get('Action') == 'pass'}
assert required <= passed
assert not any(e.get('Action') in {'fail', 'skip'} for e in events)
pg = json.loads((BOOK / 'validation/intake/full-schema-recovery-corrected.json').read_text())
assert pg['status'] == 'passed' and pg['prepare']['claims'] == {'winners': 1, 'conflicts': 1}
result = {'status': 'passed', 'source_sha': SOURCE,
          'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'Persisted observations and source-test oracles; this verifier does not rerun the application.',
          'inputs': input_hashes, 'expected_placements': expected, 'observed_placements': actual,
          'distinct_permutations': 24, 'accounted_resources': observed['accounted_resources'],
          'duplicate_claim_oracles': sorted(required),
          'postgres_claims': pg['prepare']['claims'],
          'postgres_scope': 'Shared actual full-schema package experiment owned by Lab08, not an independently repeated Lab02 execution.',
          'execution_modes': ['pure planner', 'actual MemoryService methods', 'shared fake-store scheduler tests', 'separate actual PostgreSQL package record'],
          'boundaries': ['No global capacity reservation across planners', 'Desired-stop accounting can precede physical termination', 'Default MemoryService assignment bypasses planner constraints', 'Resource enforcement measured separately in Lab01']}
(BOOK / 'validation/labs/02-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'passed', 'distinct_permutations': 24, 'assignments': 3, 'concurrency_tests': 3}))
