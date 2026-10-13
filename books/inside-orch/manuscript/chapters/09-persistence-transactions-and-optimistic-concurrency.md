# Chapter 9 - Persistence, Transactions, and Optimistic Concurrency

Atlas API has a service ID, desired replica count and several task observations. Those facts currently live in a process. Adding a database beside that process does not answer the operational question: after the process dies, which component reconstructs the same authoritative state? Before promising recovery, we must separate a durable store implementation from an application that actually uses it.

This chapter assumes the executable trace from chapter 6 and the resource model from chapter 5. You will identify the row and transaction that protect an assignment, distinguish conflict from absence, and evaluate a database test without confusing its fixtures with server wiring. The concrete problem is two schedulers trying to assign one pending Atlas task. A second problem, deliberately kept separate, is restoring the service after a new server process starts.

## The Store Contract and PostgreSQL Schema

The composite Store interface embeds node, service, task, deployment, event, secret, registry, namespace, quota and GitOps contracts. It is a useful inventory, but not the whole current domain: job, cron job, volume and notification interfaces are declared separately and are not embedded in that composite. This matters when imagining a durable replacement for MemoryService. Satisfying the older Store contract does not establish parity with every method the API currently calls. [Claim ch09.contract](../../validation/evidence/ch09.json).

Consider one task row from the initial schema. Its UUID primary key identifies the orchestration task; service_id references a service, and node_id can be null before placement. actual_status records an observation or assignment stage, while desired_status records intent. The row has the desired service version, creation/update timestamps, restart information and a separate row_version. These identifiers serve different purposes. The service version describes application intent; row_version counts database mutation; neither should be casually relabeled a worker fencing epoch.

The original schema indexes tasks by service, node and status. Those indexes correspond to real lookup patterns: reconciliation asks for service tasks, the agent asks for node assignments, and the scheduler asks for pending work. An index makes a predicate efficient; it does not automatically make a multi-row decision serializable. Foreign keys and CHECK constraints provide another layer: they protect stored relationships and selected values even if a caller bypasses the Go API. They do not validate every lifecycle transition.

Later migrations change this initial model. Namespace uniqueness, image metadata and node agent_version are not present in the first migration. Reading 000001 alone therefore describes a historical starting point, not the complete baseline schema. The source lock contains 16 up/down pairs. When a test applies a hand-maintained subset, compare that list to fields selected by current SQL before treating a failure as an algorithmic bug.

Timestamps are normalized to UTC at the Go boundary, and SQL updates explicitly set an update time. TIMESTAMPTZ values describe instants rather than a display timezone. Preserve the value returned by the store as the next optimistic token; do not reconstruct it from a formatted dashboard string with lower precision. The current guarded writes compare expected_updated_at, even where an additional integer version is also incremented. A reader must inspect the predicate actually used, not infer it from a column name.

## Transactional Boundaries and Conflict Errors

PostgresStore wraps a pool-backed postgresStore. Its WithTx method creates a transaction-scoped store whose db points at the transaction and whose begin field is unset. Operations invoked through that scoped object participate in the same transaction instead of opening independent nested transactions. The callback's successful return permits Commit; an error returns without committing, and deferred rollback handles the unfinished transaction.

[internal/store/postgres.go, lines 69–83](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L69-L83) at the locked revision.

```go
func (s *postgresStore) withTx(ctx context.Context, fn func(*postgresStore) error) error {
	if s.begin == nil {
		return fn(s)
	}
	tx, err := s.begin(ctx)
	if err != nil {
		return mapPostgresError(err)
	}
	txStore := &postgresStore{db: tx}
	defer rollback(ctx, tx)
	if err := fn(txStore); err != nil {
		return err
	}
	return mapPostgresError(tx.Commit(ctx))
}
```

This is a meaningful boundary only if every relevant effect uses the transaction-scoped value. Calling the outer pool-backed store from inside the callback escapes that boundary. The generic store.WithTx helper also has a deliberate fallback: if its candidate does not implement Transactor, it simply calls the callback directly. That helps shared controller code work with fakes, but the function name alone cannot prove atomicity for every candidate. [Claim ch09.transaction](../../validation/evidence/ch09.json).

Suppose Atlas service creation and its domain event should be one database fact. If service insertion succeeds but event insertion fails, the transaction can roll both back when strict event emission propagates the error. Without that transaction, the service may exist without its corresponding history record. External Docker creation cannot join this SQL transaction; treating it as another callback statement would leave an unavoidable side-effect gap. The orchestration protocol needs reconciliation rather than pretending all systems share a commit.

The inspected transaction audit makes this distinction concrete. Commit [72fd9baff0bbfde49574257380bcd8f747cc2070](https://github.com/alekpopovic/orch/commit/72fd9baff0bbfde49574257380bcd8f747cc2070) adds transaction-aware controller operations and strict events, including a rollback test. Earlier commit [7eba6544ffe2eba41b81faa811e899faf28b77a2](https://github.com/alekpopovic/orch/commit/7eba6544ffe2eba41b81faa811e899faf28b77a2) introduced the PostgreSQL layer. Their patches establish code evolution, not a production migration or successful execution of every original development prompt. Prompts 03 and 24 were added retrospectively; prompt 30 describes the later transaction audit.

Conflict handling is also part of the contract. A missing row, a stale optimistic token and an invalid state are not interchangeable. The scheduler treats a lost assignment race as a normal contention outcome and can continue; a transport or SQL error needs a different operational response. Retrying every error indefinitely would hide schema failures and could prevent useful work elsewhere.

## Optimistic Writes Under Contention

AssignTask first obtains the current task according to its transaction context, checks whether pending→assigned is legal, serializes allocated ports, and issues a conditional update. The crucial predicate requires the same task ID, expected update time and actual_status pending. The update stores the chosen node and ports together with assigned state. [Claim ch09.assignment](../../validation/evidence/ch09.json).

[internal/store/postgres.go, lines 912–927](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L912-L927) at the locked revision.

```go
	row := s.db.QueryRow(ctx, `
		UPDATE tasks
		SET node_id = $2,
			actual_status = $3,
			ports = $4,
			updated_at = timezone('utc', now()),
			row_version = row_version + 1
		WHERE id = $1 AND updated_at = $5 AND actual_status = 'pending'
		RETURNING id, namespace, service_id, node_id, container_id, desired_status, actual_status,
			image, requested_image, resolved_image_digest, image_registry, image_name, image_tag,
			version, ports, conditions, restart_count, failure_reason, created_at, updated_at, started_at, finished_at`,
		string(id),
		string(nodeID),
		string(types.TaskAssigned),
		portBytes,
		expectedUpdatedAt.UTC(),
```

Imagine schedulers A and B both read task T at time token U. Both compute a valid placement. A's update succeeds and changes T's status and update timestamp. B's later conditional update no longer matches. The acceptable result is one owner and one conflict, not two success responses with different node IDs. Replanning after the conflict is different from blindly repeating B's old write: the new snapshot may show that T is no longer pending.

This protects one task assignment. It does not, by itself, reserve all free CPU and host ports across a set of independently planned tasks. Two schedulers can each read available capacity, plan different pending tasks, and successfully claim both even if their combined plans oversubscribe the snapshot. Chapter 10 separates per-task uniqueness from global reservation. Increasing the number of predicates on one row cannot replace a deliberate cross-row allocation protocol.

Service updates follow a similar pattern: updateService writes the new spec and increments deployment_version only where the service ID, namespace and expected timestamp match. A concurrent operator holding an old token receives ErrConflict rather than silently replacing a newer specification. That is valuable lost-update protection, but the surrounding operation still needs to connect version history and events atomically. A successful SQL row update is not proof a worker is already running the new image.

| Observation | What it establishes | What remains unproved |
| --- | --- | --- |
| Conditional assignment rejects stale writer | One row did not accept both old decisions | Global CPU/port serialization |
| Service/event callback rolls back | Both SQL effects share the tested transaction | Docker-side rollback |
| Full schema migrations apply | Selected schema can be constructed | Default server uses that schema for live state |
| Controller restarts with one store object | Repeated controller logic can reuse retained state | Fresh-process recovery |

## Atlas Lab: Database Evidence Without a Silent Fixture Repair

Use only the disposable source copy and the dedicated labelled PostgreSQL container from the environment contract. The database name must end in _test because the upstream migrate helper refuses other names. The book's additional guard checks the loopback binding, exact database identity and ownership labels before permitting destructive tests. A suffix alone is not sufficient evidence that the database is disposable.

The actual guarded run is preserved in [database evidence](../../validation/intake/postgres-store-owned.json). WithTxRollsBackOnError passed. Integration and ConcurrentAssignTaskOnce failed with SQLSTATE 42703: current node queries require agent_version, while the reset helper applies only migrations 000001–000014 and the column arrives in 000016. This is an executed fixture/schema mismatch. It is not a passing concurrency experiment, nor a reason to erase the failure and rerun altered upstream code under the same label.

```sh
python3 books/inside-orch/scripts/run_database_tests.py \
  --container <recorded-owned-postgres-container> \
  --working-copy /tmp/inside-orch-labs-cbfc94ade5b5/orch \
  --go /path/to/go1.25 --check-only
```

Run that from the website root; only remove --check-only after the scope check succeeds. Keep the designated URL in the environment rather than in copied commands or logs. The separate [full-schema teaching fixture](../../validation/intake/full-schema-recovery-corrected.json) applied all 16 migrations and exercised AssignTask with two concurrent writers: one won and one received a conflict. It also preserved a coherent stored task. Its passing result is named separately from the failing untouched suite, and its fixture remains reviewable.

For a source-only alternative, inspect the conditional predicate and the rollback assertions, recording them as inspected rather than executed database outcomes. Clean up by stopping the exact owned container after all dependent experiments, then removing only its recorded dedicated volume if one was created. Never reset a shared developer database or use a broad volume-prune command.

## Why the Default Server Is Still Not Durable

The executable still constructs NewMemoryService with envelope, policy and retention options. That object owns maps. Database configuration and schema checks do not redirect its methods into PostgresStore. The persisted tables can be correct and the default server can still lose its authoritative service state on process restart. This is the boundary that prevents a storage library from becoming an accidental operational promise. [Claim ch09.composition](../../validation/evidence/ch09.json).

A durable composition exercise therefore starts with a method inventory, not a constructor substitution. Identify service version history, node credentials, jobs, local volume attachments, notification sinks, operations and quota state. For each, choose the authoritative store and transaction boundary. Then decide how controllers rebuild observations, how agents re-enroll without duplicating work, and how pending side effects are recovered. Persisting a service row while dropping its ownership or secret metadata can make restart more dangerous than an honestly disposable memory server.

The release decision should require a fresh-process test using an independently constructed application instance and the same durable database. Preserve container IDs and declared intent before termination, start a genuinely new process, and verify the restored API and reconciliation behavior. Do not reuse one MemoryService object and call the result database recovery. Until that composition exists and passes its own tests, describe PostgresStore as an implemented package and the running default service as memory-backed.

A useful contention record includes both input task snapshots and both outcomes, but excludes the database URL and authentication material. Compare the original UpdatedAt with the returned winning task, then re-read the stored row. The losing result alone is insufficient: an implementation that rejected both writers would also produce a conflict without making progress. The full-schema fixture checks that exactly one writer wins and the stored assignment is coherent. This provides positive and negative evidence together. It still says nothing about whether the chosen node has enough remaining capacity, because that is a different invariant with a larger read set.

## Exercises

1. Trace one task row through AssignTask. Which predicate rejects a second stale writer, and why is row_version alone insufficient evidence of the guard?
2. Explain how a callback can accidentally escape WithTx even while executing inside its lexical body.
3. Classify the observed missing-agent_version failures. What separate fixture would isolate assignment correctness without rewriting the baseline?
4. Design the minimum evidence needed to claim durable Atlas service restart. Include one API state that is absent from the composite Store interface.

[Worked answers](../solutions/ch09.md). Exact source slices and their checksums are retained in [chapter listings](../../examples/source-excerpts/ch09/metadata.json). The chapter's claims distinguish inspected implementation, the executed database fixture failure and the still separate durable-composition design.
