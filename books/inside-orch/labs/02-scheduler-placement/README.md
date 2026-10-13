# Lab 02 - Deterministic placement and competing claims

Atlas now has six pending candidates and three advertised nodes. Before running
anything, decide which candidates fit, which node wins, and which tasks should
remain pending. The purpose is to distinguish three contracts: a deterministic
plan, one accepted claim for a task, and the runtime limits on a real container.
No one result establishes all three.

## Environment and ownership

Use the source edition
`cbfc94ade5b57e449d6b73bf1485b1c5b1647022`, Go 1.25.0 with its matching GOROOT,
and a disposable Orch copy. The teaching program imports actual internal packages
and therefore runs beneath that module. It starts no listeners, containers or
database connections. Its IDs and timestamp are fixed model inputs; they are not
identities captured from a live cluster.

The complete input is [fixtures/plan.json](fixtures/plan.json). It uses Go's
`scheduler.PlanInput` representation, not a deployment YAML or public HTTP body.
The separate [teaching program](../../examples/teaching-extensions/lab02/main.go)
reads that file and rejects the wrong source revision or candidate count. Copy
the program unchanged into `.book-labs/lab02/main.go` in the disposable source
tree. Record the source and fixture hashes before execution. Do not build inside
`evidence/orch` or modify application files to change the outcome.

## Predict the plan

CPU values below are millicores; memory values are binary mebibytes. The planner
uses allocatable resources and requests. Capacity is deliberately larger than
allocatable, and limits are twice requests, so confusing those fields changes
the calculation.

| Node | Status and label | Capacity | Allocatable | Existing work |
| --- | --- | --- | --- | --- |
| a | offline, zone=green | 8000m / 8192Mi | 4000m / 4096Mi | None |
| b | ready, zone=blue | 2000m / 1024Mi | 1000m / 512Mi | 100m / 64Mi, TCP31080 |
| c | ready, zone=blue | 2000m / 1024Mi | 1000m / 512Mi | None |

The existing task on b has desired running and actual stopping. That combination
is intentionally still active according to the shared helper. It reserves its
request and port in this model even though its process is progressing toward
stop. This is not a claim that every desired-stop state remains accounted until
Docker confirms physical termination; the distinction is tested below.

| Candidate | Request | Required zone | Published TCP port |
| --- | --- | --- | --- |
| atlas-01 | 400m / 128Mi | blue | 31080 |
| atlas-02 | 400m / 128Mi | blue | Dynamic |
| atlas-03 | 400m / 128Mi | blue | Dynamic |
| atlas-04 | 100m / 64Mi | green | Dynamic |
| atlas-05 | 2000m / 1024Mi | blue | Dynamic |
| atlas-06 | 400m / 128Mi | blue | 31080 |

Write the selected node and the reason for every rejection before reading the
observed result. Plan processes candidates in stable task-ID order. Eligibility
precedes scoring: ready status, labels, requests, mounts and ports can reject a
node regardless of its attractive memory score. Among eligible nodes, more free
memory after placement wins, followed by fewer same-service tasks, fewer total
tasks and lexical node ID.

The predicted first choice is c for atlas-01. Node a is offline and b's fixed
port is occupied. After this choice c has 384Mi free, while b still has 448Mi.
Atlas-02 therefore selects b and receives dynamic TCP30000. Now b has 320Mi free,
so atlas-03 selects c and receives TCP30000 on that different host. Reusing a
numeric published port across hosts is valid in the planner's node-scoped model.

Atlas-04 has no ready green node. Atlas-05 exceeds both ready nodes' allocatable
resources. Atlas-06 cannot acquire TCP31080 on either ready node. All three
remain pending. A correct no-fit result is useful feedback, rather than an
exception to suppress or an invitation to ignore constraints.

## Execute and inspect the model

From the disposable source root, set `BOOK_ROOT` to your canonical book directory
and use the pinned Go executable. The variable is a reader-selected path, not a
special application setting.

```sh
go run ./.book-labs/lab02 "$BOOK_ROOT/labs/02-scheduler-placement/fixtures/plan.json"
go test -count=1 -json ./internal/scheduler \
  -run 'TestConcurrentSchedulerAttemptsAssignTaskOnce|TestConcurrentRunOnceAssignsTaskOnceAcrossSchedulers|TestRunOnceAccountsForNonTerminalAssignedTasks'
```

The actual edition runs passed: [model command](../../validation/labs/lab02-model-and-permutations.json)
and [concurrency command](../../validation/labs/lab02-concurrent-claims.json).
The model records three expected assignments, 24 distinct node/task order pairs,
the lexical tie result and unchanged pending input states. Its cumulative
accounting is b=500m/192Mi and c=800m/256Mi, including b's existing task. It also
rejects duplicate node/protocol/port reservations and any offline assignment.

The permutation test uses all six node orders and four distinct task orders,
including reversal. It compares complete assignment outputs, including the
expected update timestamp and allocated ports. A separate equal-score fixture
removes existing work and gives one dynamic candidate two identical ready-node
choices: b wins lexically. These are finite input checks, not a proof over every
possible cluster state.

The upstream concurrent tests use shared fake-store state. One invokes competing
assignment persistence calls; another uses a barrier so two independent
scheduler instances both read the same pending task before proceeding. Their
oracles require exactly one returned claim, an assigned stored task and one
assignment event. The successful run does not create two MemoryService servers
and label them an HA cluster.

## Timestamp guards and the database track

An assignment carries the task snapshot's ExpectedUpdatedAt. The store's update
requires the same timestamp and pending status, so a second stale writer cannot
successfully claim that same row. This is narrower than reserving all CPU and
ports atomically across several different task rows. Two planners choosing
different tasks can each win its own claim while relying on overlapping capacity
snapshots. The local plan's accounted budget does not eliminate that race.

The inspected PostgreSQL path adds `FOR UPDATE SKIP LOCKED` for the
transaction-scoped read and performs the conditional update. The exact
[getTask and AssignTask code](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L879-L935)
defines the behavior; the presence of a row lock should not be generalized to
the entire resource-allocation problem.

The database observation is shared with [Lab 08](../08-recovery-boundaries/README.md),
which owns a labelled disposable PostgreSQL container and fresh recovery
databases. Its [full-schema record](../../validation/intake/full-schema-recovery-corrected.json)
observed one winner and one conflict after all 16 migrations. The untouched
upstream store suite separately had two failures because its reset fixture
applied only migrations 1–14 while current node queries need the column added in
16. Keep that failure visible; a passing teaching fixture does not repair or
rename the upstream suite. Do not execute the reset helper against a shared
database. The fresh whole-book run records database work under Lab 08 rather
than pretending the same execution occurred twice independently.

## Trace the resource boundary

| Boundary | Observation or source | Confidence and limit |
| --- | --- | --- |
| Declared requests and limits | Canonical fixture | Exact input values; not utilization |
| Plan accounting | Three assignments and cumulative budget | Executed finite model, requests/allocatable |
| Registration and heartbeat | Actual MemoryService methods in teaching program | Explicitly supplied advertised values, no physical host measurement |
| Immediate service creation | 600m/256Mi request assigned to a red 100m/64Mi node | Executed bypass comparison; no container started |
| Agent task response | Ordinary task lacks ResourceRequirements | Executed inspection of actual method result |
| ContainerSpec construction | Agent omits Resources | Inspected caller; [creation fields](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253-L265) |
| Actual Docker configuration | Lab 01 resource comparison | Executed owned containers: ordinary zero limits, direct supplied adapter limits |

The bypass comparison deliberately advertises a tiny node and submits a larger
service with a mismatching label. MemoryService immediately assigns its task.
It does not physically stress a host or change the pinned implementation. The
real Docker comparison is in [Lab 01](../01-initialization-restart/README.md);
its request, inspected HostConfig and cleanup are distinct from this fake-state
planning experiment.

Two documentation mismatches affect the worksheet. SCHEDULER.md's limitations
still say there is no port or volume awareness, although current Plan filters
both. RESOURCES.md says requests remain counted until actual terminal status,
but [IsActiveTask](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L270-L275)
excludes desired stopped/removed immediately. The program tests that exception
explicitly. A physically running container can therefore outlive its accounted
reservation. The no-overcommit assertion applies to the supplied accounted
model, not every physical process during stop acknowledgement delays.

## Exercises and worked decisions

1. Why does atlas-01 select c? The fixed port makes b ineligible before scoring;
   a is offline. More free memory cannot rescue an ineligible node.
2. Why does atlas-02 then select b? Its dynamic port fits and b has 448Mi free
   versus c's 384Mi before placement. Limits are not the requested budget.
3. Can atlas-06 share c with atlas-01? No: the same TCP31080 is already reserved
   on c, while b also has that reservation. Another protocol is a different key.
4. What does one competing claim prove? Only one stale pending-task snapshot
   became an accepted assignment in the tested shared store. It proves neither
   durable server composition, global reservation, leader fencing nor cessation
   of a partitioned worker's side effects.

Model cleanup is process exit and removal of only the copied teaching directory
if desired. Keep the fixture and execution records. Lab 08 alone owns database
cleanup; Lab 01 records exact container cleanup. Never replace those owners with
a daemon-wide prune, shared-schema reset or termination of unrelated processes.
