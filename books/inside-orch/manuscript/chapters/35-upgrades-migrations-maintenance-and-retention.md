# Chapter 35 - Upgrades, Migrations, Maintenance, and Retention

Atlas schedules an upgrade for a quiet evening. The change plan names a new server binary, a database migration, and a retention cleanup. Treating these as one action would hide three separate risks: incompatible agents, destructive schema changes, and loss of diagnostic history. A successful installation command would answer none of those questions by itself.

This chapter teaches you to read pinned compatibility ranges, inspect migration locking and rollback guards, and distinguish a maintenance policy from an automatic shutdown of all work. You will also trace retention's preservation rules and the server's opt-in schema check. Atlas's lab combines actual disposable-database observations with deterministic operation tests and a controlled execution of the upgrade-preflight command.

## Version Ranges and Upgrade Preflight

Compatibility is part of the release contract. At this source revision, the server is 0.3.0, the API is v1, supported agents range from 0.2.0 through 0.3.0, and the expected database schema is 16. The accepted schema range is 15–16. These are pinned constants, not promises about an arbitrary future release.

```go
const (
	Server             = "0.3.0"
	MinimumAgent       = "0.2.0"
	MaximumTestedAgent = "0.3.0"
	Schema             = 16
	MinimumSchema      = 15
	MaximumSchema      = 16
)
```

Exact source: [internal/version/version.go:11–18](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/version/version.go#L11-L18).

Agent versions below the minimum are classified too_old; versions above the maximum tested value are classified untested_newer. Empty agent version falls back to the server version in the checker. That fallback preserves older callers but makes missing version metadata weaker evidence than an explicitly observed binary version. Atlas should inventory installed binaries as well as the server's node records before a coordinated upgrade.

The parser expects three numeric version components and strips a leading v. Its limited handling of suffixes should not be mistaken for a complete implementation of every semantic-version precedence rule. The [agent checker compares its parsed tuple against pinned bounds](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/version/version.go#L31-L47). A newer agent is a warning case, not a statement that its behavior has been tested. Compatibility metadata and executed interoperability tests answer different questions.

The CLI's [check-upgrade implementation fetches version information and node records](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/operations.go#L157-L188), classifies each agent, and emits a structured decision. It does not actually apply a migration, replace an agent, or inspect every database column. More subtly, a structured status of blocked is still returned through a successful output-writing path. A shell script that checks only the process exit code can therefore miss an upgrade rejection.

The [controlled preflight fixture](../../examples/teaching-extensions/ch35/preflight_test.go) executes the real Cobra command against explicit node inputs. Agent 0.2.0 produced compatible with no warning; 0.1.0 produced blocked with a warning; 0.4.0 produced compatible with an untested warning. All command invocations returned no command error. This was observed in [controlled-preflight-corrected.json](../../validation/labs/ch35/controlled-preflight-corrected.json), using an injected fixture rather than a live cluster. The initial fixture's nil embedded client failed and remains recorded; the corrected fixture initializes the client but performs no network calls.

Atlas automation must parse the decision and choose its own warning policy. For example, reject blocked, require review for untested versions, and proceed only after schema status and restore evidence pass separately. Do not change the upstream output contract in the teaching harness. Learning to consume the actual interface is more useful than inventing a convenient exit-code guarantee.

## Migration Locks and Guarded Down Paths

Migration discovery reads ordered filenames and groups up/down paths by version. Up acquires a database connection and executes under a PostgreSQL advisory lock. It checks recorded versions, skips those already applied, and applies each pending migration in its own transaction with its version record. This limits partial application within one migration; it does not turn an entire sixteen-migration upgrade into one transaction.

The [transaction sequence records the version only with successful SQL application](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go#L152-L177). If migration ten succeeds and eleven fails, earlier committed migrations remain. Atlas must inspect status after failure and decide how to repair forward or restore. Repeated up is useful because recorded versions are skipped, but idempotency depends on the version table and unchanged migration files. Editing an already committed migration changes the meaning of that history.

The [lock wrapper attempts unlock even when the callback fails](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go#L71-L81). A lock-acquisition failure prevents the callback from running. The runner's lock is separate from controller leadership locks discussed in the previous chapter: it serializes schema-changing migration runners, not every application write. Production planning still needs a policy for old and new binaries accessing the database while a migration runs.

Down rejects the request unless allow-down is true, then locates the newest applied migration and reads its down file. The [explicit guard is an authorization boundary](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go#L182-L205), not proof that the SQL preserves useful data. A file's existence does not make a rollback safe for customer records. Atlas should read both directions, identify dropped columns and tables, and prefer binary rollback against an additive compatible schema where possible.

The captured [full-schema experiment](../../validation/intake/full-schema-recovery-corrected.json) began with no applied versions, observed sixteen pending migrations, applied them to current 000016, and observed no pending work on a second up. It also rejected down without authorization. No destructive down migration was necessary. The record includes separate backup/restore verification against owned databases, and it must not be relabeled as default-server restart recovery.

An earlier upstream store fixture applied only migrations one through fourteen. It then failed with missing agent_version, which migration sixteen introduces. Keep that original failure visible. A successful full-schema extension demonstrates that the later schema works for the tested package operations; it does not retroactively make the original fixture pass or prove that every accepted schema version supplies every currently queried column.

## Maintenance Windows and Bounded Retention

Maintenance policy is selective. A window names allowed operations, a schedule, timezone, duration, and scope. The [control-plane check first searches for relevant enabled windows](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L616-L639). If none apply, the operation is allowed. If a relevant window currently permits the operation, it is allowed. Otherwise the operation conflicts unless a forced context requests an audited bypass. Creating an unrelated window does not freeze the cluster.

The time evaluator converts the current time to the configured location and searches scheduled occurrences within the preceding duration. Tests supply fixed time so that inside/outside decisions are reproducible. Atlas should examine daylight-saving transitions and its chosen timezone when creating operational schedules; a cron string alone does not explain which civil time operators mean. The implementation supports a bounded occurrence search, not a general calendar approval workflow.

Emergency force is also narrower than a universal permission override. It bypasses the maintenance-window check and appends a maintenance.bypass audit record. It does not automatically waive workload admission, quotas, or runtime safety requirements. The [operation test verifies an outside-window rollout rejection and an audited forced request](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations_test.go#L12-L44). The recorded run passed, but no real host was drained or upgraded in that deterministic fixture.

Retention must preserve the state needed to operate and diagnose the system. Defaults keep events for thirty days, audit logs for ninety, completed tasks for seven, failed tasks for thirty, rollouts for thirty, and completed jobs for seven. These values are configuration defaults, not legal retention advice. Atlas should choose them according to its recovery and investigation needs, then verify the actual pruning branches.

The [task pruning logic considers stopped/removed tasks and resolved failures](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L63-L74). An old running task is preserved. An old failed task is preserved when no qualifying replacement or cleanup intent resolves it. The resolution helper accepts a running or healthy task for the same service at an equal or newer version, or stopped/removed desired state. Those are code-level rules; “resolved” is not a human incident status.

Rollout pruning removes old succeeded or rolled-back deployments, and job pruning removes old succeeded jobs. Failed unresolved histories stay available under these branches. GitOpsRecords appears in retention configuration, but this pruning method has no corresponding GitOps-record deletion loop. Configured fields must not be reported as enforcement until the caller and mutation path exist. Similarly, pruning control-plane task records does not remove arbitrary engine containers.

Dry-run computes eligible counts while retaining the collections. The [retention fixture checks an old event, active task, unresolved failure, and resolved failure](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations_test.go#L45-L78). Actual execution passed dry-run preservation and subsequent selected deletion. This is a bounded semantic test, not a performance measurement against years of history. The implementation holds the memory-service mutex while scanning; large retained collections can affect concurrent request latency.

## A Schema Check Must Be Enabled to Run

A database URL in configuration does not itself activate schema validation. The server [checks ORCH_SCHEMA_CHECK only when its value equals true ignoring case](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L107-L120). It opens the migration runner, reads current status, checks the supported range, and then proceeds to construct MemoryService. A successful check says something about the database schema it inspected. It does not switch active state into PostgreSQL.

For a source-checked future procedure, enable the gate explicitly:

```bash
ORCH_SCHEMA_CHECK=true orch-server
```

The command assumes the configured database, migration directory, credentials, and other required server settings are already supplied. It is a procedure, not a claimed execution from this chapter. Values such as 1 do not satisfy this particular comparison. Leaving the variable unset skips the check, which is important when reading a development startup log that looks healthy despite an unavailable database.

Atlas's safe lab has three independent evidence lanes. The [operations run](../../validation/labs/ch35/operations-tests.json) exercised pinned version checks, migration lock/discovery helpers, fixed-time windows, and memory retention preservation. The controlled preflight exercised real CLI decision output with fixture nodes. The already captured disposable-database experiment exercised actual status, up, repeated up, guarded rejection, and restore. None should borrow another lane's coverage.

The cleanup plan should be equally explicit. In the deterministic lane, only test-local data exists. In the database lane, use the captured database names and container identity, verify that they were created for the experiment, and remove only those resources. A command such as dropping every database matching a loose prefix would exceed the experiment's ownership. Keep the restore target separate from the source so a successful verification cannot be confused with reading unchanged original rows. Preserve evidence before cleanup and record cleanup failures as part of the result rather than hiding them behind a passing migration status.

Before a change window, preserve the candidate binary identity, compatibility metadata, actual node versions, current/pending schema, tested backup reference, key availability, maintenance decision, and retention preview. Afterward, capture resulting status and compare intended effects with actual records. If a server restart loses memory state, restoring a database dump cannot reconstruct records that were never written there. That boundary remains true even when migrations, backup scripts, and compatibility checks all succeed.

## Exercises

1. List the locked server, agent, API, and schema bounds. Explain why expected schema sixteen and accepted schema fifteen are different statements.
2. Run the controlled preflight fixture. Design automation that rejects structured blocked status even when the command itself succeeds.
3. Trace a migration failure after earlier migrations committed. Explain what status and backup evidence you need before retrying, without executing down on real data.
4. Classify old running, unresolved failed, and replaced failed tasks for retention. Identify why an unrelated maintenance window and a GitOps retention setting do not establish the intended enforcement.

Worked answers are in [Chapter 35 solutions](../solutions/ch35.md); the [claim ledger](../../validation/evidence/ch35.json) preserves the distinction between inspected procedures and executed observations.
