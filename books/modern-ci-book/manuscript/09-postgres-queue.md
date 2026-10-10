# 9. Claim work with short PostgreSQL transactions


## Claiming is a state transition

A durable queue is not just a table with `status = pending`. Claiming must atomically select eligible work, assign its current owner, create an attempt, and reserve the relevant capacity. If these are separate uncoordinated operations, two schedulers can start the same work or exceed a shared limit.

PostgreSQL's `FOR UPDATE SKIP LOCKED` can let queue consumers skip rows another transaction has locked. Its documentation explicitly notes queue-like use cases and warns that this is not a generally consistent view of data. Use it for the claim operation, not as a substitute for every concurrency rule. [S07](e-sources.md#s07)

A simplified transaction looks like this:

```sql
BEGIN;
SELECT id
FROM jobs
WHERE project_id = $1
  AND pool_id = $2
  AND state = 'queued'
  AND ready_at <= statement_timestamp()
ORDER BY priority DESC, ready_at, id
FOR UPDATE SKIP LOCKED
LIMIT 1;
-- Update the selected job and insert its new attempt here.
COMMIT;
```

The parameters denote driver-bound values. This fragment explains selection; the complete illustrative CTE in `examples/sql/claim.sql` performs the update and attempt insertion together. It still assumes that the caller has authorized the project and pool and arranged any required capacity reservation.

## Keep the lock scope small

Never keep the transaction open while a runner downloads an image or performs a build. A claim commits before execution begins. Store an expiry time and fence generation so later messages can prove they refer to the current claim. Heartbeats extend ownership through conditional updates, not by retaining a database connection for the duration of the job.

Locks need a consistent order when multiple resources are involved. For example, reserve an organization concurrency slot, then a pool slot, then a job according to a documented order. A separate `COUNT(*)` followed by an update is vulnerable to concurrent admission decisions. Use locked capacity records or another atomic reservation mechanism, and release reservations through the same terminal-state transaction.

Shared deployment targets need stronger treatment than ordinary build slots. A target reservation can remain held while execution is uncertain. Expiring a runner lease must not silently authorize a second deployment to the same target.

## Define the database contract

Use constraints for invariants the database can express: unique attempt identity, unique generation per job, valid state values, immutable delivery receipt keys, and foreign-key ownership. Store enough attempt history to audit retries without overloading the current job row with every observation.

A practical index begins with fields used to narrow eligible work, such as pool and state, and includes the ordering fields. Measure representative queries with the actual workload. A partial index on queued rows may help, but it is a design to benchmark rather than a guaranteed improvement for every data distribution.

PostgreSQL's default Read Committed isolation gives statements their own snapshots. More stringent transaction isolation can require explicit retry handling. Choose isolation and locking together, and retry the whole intended transaction when its documented conflict condition permits it. [S18](e-sources.md#s18)

Use the database clock for ownership comparisons. Keep transaction duration short enough that the chosen timestamp semantics are intentional. Wall-clock adjustment still matters operationally: leases are a coordination policy, not proof that a disconnected process has stopped.

## Explain queue delay

Persist or derive a reason for why a job is not currently claimable: dependency not satisfied, approval required, no authorized runner, insufficient capacity, paused project, delayed retry, or uncertain target. Do not update thousands of rows every second just to populate a dashboard; combine durable blockers with current pool summaries.

Fairness is a separate concern from atomicity. A priority order may starve low-priority projects. Introduce a deliberate policy such as bounded per-project admission or weighted rotation, and test it with asymmetric workloads. “The query is fast” is not evidence that the queue is fair.

## Exercise

Two schedulers both observe that an organization has four running jobs and a limit of five. They each claim another job. The row locks on the jobs work correctly. Why is the limit still violated?

## Worked answer

The schedulers locked different job rows but made their capacity decisions from separate observations. Serialize admission through an organization capacity record or an equivalent atomic reservation. Claiming a job and reserving its slot must succeed or roll back together. A later metrics correction cannot undo the fact that six jobs were admitted.

## Completion evidence

Run live multi-client tests for claim uniqueness, capacity limits, deadlock retries, transaction aborts, and recovery after losing the connection immediately after commit. The book's SQL is illustrative until those tests are executed against PostgreSQL.
