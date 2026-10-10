# Local State, Approval and Quota Invariants

## Prerequisites

No cluster required. Python 3.11+ and Go 1.23+.

## Procedure

Run the Go race tests and Python audit tests. Read each failed-condition test before changing code. Add one altered-policy approval case and one stale transition.

## Acceptance criteria

Record commands, tool versions and results. Demonstrate that the tests fail when a guard is intentionally removed, then restore the guard. Explain why process-local mutexes do not coordinate multiple replicas.

## Evidence record

Record date, source revision, environment, exact commands, expected result, actual result, limitations and teardown status. Never attach secrets or customer payloads. A written procedure is not an executed result.
