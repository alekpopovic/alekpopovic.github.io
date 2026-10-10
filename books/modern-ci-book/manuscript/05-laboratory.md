# 5. Run the laboratory before designing the fleet


## A small executable model

The companion code under `examples/lab` is a standard-library-only Go module. It provides deterministic graph validation, an in-memory attempt ledger with fencing, webhook HMAC validation, a bounded log-segment store, and exact approval-subject matching. It does not execute arbitrary commands. That limitation lets us explore ownership and replay without accidentally building an unsafe public executor.

Run these laboratory commands from the book repository:

```bash
cd examples/lab
go test ./...
go test -race ./...
go run ./cmd/demo
```

The demonstration creates a graph, starts an attempt, makes it uncertain after a simulated lease expiry, authorizes a retry only after a stopped observation, and rejects a stale completion from the old attempt. It also shows a log-upload retry being recognized without duplicating bytes. The tests state the precise expected outcomes rather than relying on the prose output alone.

Use a supported Go release for ongoing work. The module's language baseline is not a security-support promise. The verification report records the compiler actually used for this edition. No third-party Go dependencies are downloaded by the examples.

## Time is an input in the model

The ledger accepts an explicit timestamp. Tests can move from `t0` to `t0 + 31 seconds` without waiting in real time. This makes expiry tests fast and deterministic. Production ownership, however, uses database-coordinated time and atomic updates. A unit test of supplied timestamps does not validate host-clock behavior or PostgreSQL transaction isolation.

The in-memory ledger uses a mutex to demonstrate serialized decisions within one process. That mutex is not a distributed lock. Restarting the process loses its state. Chapter 9 explains the database transaction that a durable version requires, and Chapter 23 lists the live concurrency tests that are still necessary.

## Keep syntax and semantics separate

The DAG input to the laboratory is a list of job identifiers and dependency lists. It intentionally does not parse YAML. A complete pipeline frontend needs strict schema validation, duplicate-key handling, bounded input size, and carefully specified scalar behavior before it calls the graph compiler.

The demonstration teaches the graph invariant: a job can depend only on known, distinct jobs; self-dependencies and cycles are rejected; the compiled order is deterministic. It does not establish that an arbitrary YAML parser is safe for untrusted input.

Similarly, the signature helper works on exact byte slices and a signature string. It is not an HTTP server. A production endpoint must limit body size, enforce content type, persist the delivery receipt, and apply repository authorization. Signing tests are necessary but do not perform those other jobs.

## Inspect the code instead of trusting the demo

Read `dag.go`, then the tests for missing dependencies and cycles. Read `ledger.go`, then the tests for expired leases, stale identities, cancellation, and duplicate results. Read `logstore.go`, where the next segment is accepted only if its sequence matches the expected value and its content fits the configured quota. Read `approval.go`, where matching a human-readable release label is deliberately insufficient.

Change one behavior and run the tests again. For example, remove the fence comparison from result acceptance. The stale-result test should fail. Put it back before continuing. A demonstration is educational only when it is sensitive to the defect it claims to prevent.

## Expected boundaries

The laboratory has no persistent queue, cloud credential exchange, container sandbox, browser session, production secret vault, or SSH deployment. It uses synthetic identifiers and loopback-free pure functions. The separate SQL files are reviewable design examples, not an automatically provisioned database.

Keep the book's implementation map as a set of future work items. A passing laboratory suite completes the examples' checks, not all eighty product work items. This distinction prevents an attractive repository from overstating what can actually be operated.

## Exercise

The race detector reports no issue for the in-memory ledger. A teammate concludes that running three schedulers against PostgreSQL is safe. What experiment should come next?

## Worked answer

Run multiple actual database clients claiming the same eligible row under the proposed transaction. Assert that exactly one claim becomes current, other claimers select different rows or receive no work, and stale completions affect zero current rows. Repeat with transaction aborts, statement timeouts, connection loss after commit, and process termination. The race detector helps find memory races in the Go process; it does not exercise database locking or network uncertainty.

## Completion evidence

Save the test command, compiler version, exit status, and output. Record the laboratory's scope explicitly. A failed prerequisite is a blocker to the corresponding experiment, not a reason to report it as passed.
