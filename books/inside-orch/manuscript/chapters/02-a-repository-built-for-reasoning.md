# Chapter 2 - A Repository Built for Reasoning

You will learn to find active interfaces from their callers, distinguish deterministic package fixtures from infrastructure tests, and interpret cancellation as a boundary rather than a rollback guarantee.

## The Actual Tree Versus the Intended Layout

The Atlas developer wants to reproduce an assignment problem before changing production settings. A directory named `scheduler` looks promising, but searching for “runtime” finds a different tree from the architecture sketch. Following the sketch literally would send the developer to a directory that does not exist. The first useful repository skill is therefore not memorizing a preferred layout. It is locating the path a real caller takes and distinguishing that path from the structure somebody intended to build.

This chapter teaches you to navigate the actual packages, find side-effect interfaces, and explain how cancellation and deterministic fixtures constrain a design. You will run a small test with an observable assertion rather than start the whole system to answer every question. The Atlas artifact is a source index that identifies a constructor, dependency, state owner, and effect for each subsystem. Chapter 1's boundary map becomes a map you can use while debugging.

The [application's intended layout](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/AGENTS.md#L13-L35) places future runtime adapters under an `internal/runtime` hierarchy. Current code instead uses `internal/docker`, which contains the Runtime interface, EngineRuntime, FakeRuntime, and instrumentation wrapper together. Health probing lives in `internal/health`; orchestration of repeated probes and threshold counters lives in the agent. Do not rename these paths in an explanation merely to make the tree match an architectural vocabulary. The existing names reveal where responsibilities actually accumulated.

The executables are similarly concrete. `cmd/orch` delegates to Cobra composition. `cmd/orch-server` selects the memory service and starts its controllers/listeners. `cmd/orch-agent` assembles a Docker adapter, runner, and log listener. A fourth executable, `cmd/orch-loadtest`, constructs its own memory service for synthetic workloads. The presence of the load tool is useful, but its observations are not observations of a network-connected production server. Navigation begins with these entrypoints because they decide which packages become active behavior.

A small package can also be less significant than its name suggests. `internal/task/task.go` wraps a Task in DesiredState, and `internal/node/node.go` contains an older local Record/Status wrapper. The active lifecycle contracts live in `pkg/types`, while node monitoring lives in another file in `internal/node`. Import use and constructor calls matter more than the apparent importance of a filename. A reader should resist building a conceptual model around a wrapper that no relevant path consumes.

The practical index is intentionally short. For scheduling, record New, RunOnce, Plan, and persistAssignment. For agent execution, record NewRunner, Run, ensureTask, and the Runtime interface. For persistence, record NewPostgresStore, store.WithTx, and the SQL assignment guard. For each, add a caller reference. This is more useful than reproducing every directory because it gives the next investigation a starting point and a question about state or effects.

## Interfaces at the Side-Effect Boundary

The [Docker Runtime interface](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L47-L56) makes the agent's external effects explicit. It pulls images, creates/starts/stops/removes containers, inspects/list-labeled containers, and streams logs. Its operations accept context and typed inputs rather than arbitrary shell commands. The interface tells us which effects an agent fixture must simulate. It does not say every simulation is equivalent to a real Docker daemon.

```go
type Runtime interface {
	PullImage(ctx context.Context, image string, auth *RegistryAuth) error
	CreateContainer(ctx context.Context, spec ContainerSpec) (ContainerID, error)
	StartContainer(ctx context.Context, id ContainerID) error
	StopContainer(ctx context.Context, id ContainerID, timeout time.Duration) error
	RemoveContainer(ctx context.Context, id ContainerID, force bool) error
	InspectContainer(ctx context.Context, id ContainerID) (ContainerStatus, error)
	ListManagedContainers(ctx context.Context, labels map[string]string) ([]ContainerStatus, error)
	StreamLogs(ctx context.Context, id ContainerID, opts LogOptions) (<-chan LogLine, <-chan error)
}
```

Exact source: [internal/docker/docker.go:47–56](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L47-L56).

Now follow that dependency through composition. `cmd/orch-agent.run` constructs EngineRuntime from the environment, wraps it with agent metrics, and injects it using WithRuntime. NewRunner initially creates bookkeeping and a health checker, while Run fills in missing client/runtime dependencies if they were not supplied. A test can supply FakeRuntime without changing the agent's lifecycle logic. This is a usable seam, not just an interface declared for aesthetic reasons.

The [idempotent fake-runtime fixture](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake_test.go#L11-L38) calls CreateContainer twice with the same task, checks that both calls return one identity, starts it, inspects its labels/state, and verifies the recorded operation sequence. The useful assertion is not “mock called.” It is that repeated local creation for the same task did not produce two container identities in this model. A real-daemon test must check the corresponding adapter behavior separately. The fake has a mutex and a concurrent-create test, but neither proves a distributed exactly-once protocol.

Consumer-owned interfaces also keep dependencies small. Scheduler.Store expresses the reads and assignments the scheduler needs. It does not require the entire API service, a Docker client, or a global repository object. Plan receives a value snapshot and returns proposed assignments; RunOnce performs I/O around it. This separation lets Atlas test insufficient capacity or label mismatch without a daemon. It also makes an important limit visible: a deterministic plan can still be stale when another actor writes before persistence.

A dependency can be replaceable without being connected in the binary you are using. The standalone reconciler has a Store and LeaderLock seam, but ordinary server startup never constructs that reconciler. Leadership has another elector interface and wrapper; its existence does not activate HA. When reading a new interface, find both its implementation and its injection point. If the latter is absent, classify it as an implemented package rather than silently invent a runtime caller.

## Cancellation and Time as Dependencies

Atlas's first shutdown question is simple: what stops when the owner cancels the context? The main programs derive a signal-aware context and pass it downward. Server background loops select on cancellation and stop their tickers. The HTTP listener receives a separate bounded shutdown context. A Docker or HTTP operation can receive the caller's cancellation through its interface. These are different mechanisms serving one ownership rule: work should not outlive its declared owner accidentally.

Cancellation is cooperative, not a rollback transaction. Suppose an image pull succeeds and the context is canceled before the status report. The daemon may retain the image, and a container may already exist after a later interruption. Stopping the goroutine does not erase that side effect. Recovery must rediscover identity and reconcile it. The interface helps propagate cancellation, while labels/idempotency help resolve work that crossed the side-effect boundary before cancellation arrived.

Time deserves the same care. A controller with a clock can test a timeout without sleeping until a real wall clock happens to cross a boundary. The reconciler constructor stores a now function and interval; cron explicitly accepts a Clock. The agent has heartbeat/probe jitter and timer logic. These choices reduce synchronized behavior in a live system but can complicate tests unless randomness and elapsed time are controlled at the seam relevant to the assertion.

An invariant test should assert the decision, not the scheduler luck of the test process. For example, if two nodes tie, Plan sorts and breaks ties deterministically. A fixture can reverse input order and expect the same node identity. If a timeout changes desired state, an injected clock should advance to the boundary explicitly. “Sleep briefly and hope the controller has run” leaves the test sensitive to host load and says little about why the state changed.

There is also a meaningful distinction between stopping one controller and restarting a process. Recreating a controller against the same memory service preserves all domain maps. A fresh server process does not. Keeping state ownership in the index prevents an appealing restart test name from crossing that boundary. Test scope is part of the design explanation, not a footnote attached after a green result.

The [initial scaffold](https://github.com/alekpopovic/orch/commit/72f27ed1d81b75e499ee65e0c9779e44b237f814) created command entrypoints and package boundaries, while [repository conventions](https://github.com/alekpopovic/orch/commit/6f90183927991506de435a55582b5c283212ff09) documented intended responsibilities. Original development prompts 00, 01 and 21 are useful statements of intent, but their retrospective associations do not prove a transcript or a successful run. Later code placed Docker implementations and fakes together rather than adopting every intended path. Preserve the historical filename when discussing the scaffold and the current filename when explaining a caller. That small editorial distinction prevents a reader from trying to execute a command against a directory that existed only in a plan.

## The First Focused Test

The pinned [module file](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/go.mod#L1-L13) requires Go 1.25.0. Use the toolchain matching the baseline, record its executable and GOROOT, and execute application commands only in a disposable source copy. If source is exported without Git history, disable VCS stamping explicitly rather than treating a missing `.git` directory as a failed application feature. Record that build flag so a later reader can reproduce the environment difference.

The [Makefile](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/Makefile#L1-L23) is convenient but has a subtle scope change: make lint runs golangci-lint when installed and otherwise falls back to gofmt and vet. A successful fallback is not an executed golangci-lint run. Likewise, normal go test can skip external database/Docker suites. Commands with identical friendly names can exercise different tools depending on the environment; capture the actual command and prerequisites rather than report only “quality checks passed.”

Atlas first inspects PlanAssignments and the idempotent fake runtime test. These fixtures have finite inputs and concrete expected identities. From the disposable Orch source root, with the pinned toolchain selected, run:

```bash
go version
go build ./...
go test -count=1 -v ./internal/scheduler ./internal/docker \
  -run 'TestPlanAssignments|TestFakeRuntimeRecordsOperationsAndCreatesIdempotently'
```

In this edition the isolated build and focused tests were actually executed successfully. The focused record is `validation/labs/ch02/focused-tests.json`; it stores the exact toolchain path, UTC timestamps, environment keys, exit status, and output. It establishes the assertions of these selected package fixtures. It does not establish real Docker pulls, PostgreSQL transactions, all possible randomized cluster states, or end-to-end resource enforcement.

Read a passing fixture in terms of its counterexample. “Insufficient resources” should yield no assignment for that input. “Deterministic tie breaking” should choose the stable node. Repeated CreateContainer should return the same fake identity. If a selected test name matches nothing, Go can still exit successfully, so inspect verbose output for the expected test names. A useful record includes assertions that ran, not merely a process exit code.

The failure window for this chapter is an injected create success followed by a lost report. The seam allows a test to preserve the fake container while retrying the agent's operation. That is a narrow and useful experiment. It does not reproduce Docker daemon crashes, network partitions, or server state loss. Those require different fixtures or real processes because they alter different owners. Choosing the smallest faithful seam is more rigorous than starting every dependency and hoping the resulting complexity improves evidence.

Cleanup is correspondingly small. Focused tests own their in-memory fixtures and temporary directories. Remove only disposable build outputs you created; never format or compile into the immutable snapshot. Keep the source index and execution record. If local listener or toolchain prerequisites are unavailable, mark that experiment blocked and preserve the source walkthrough. Do not substitute a test title for its missing run.

## Exercises

1. Locate Runtime, EngineRuntime, FakeRuntime, and the executable injection point. Explain why the four references are stronger than a directory name.
2. Explain what PlanAssignments can establish without Docker and which ordinary service path still needs separate examination.
3. A controller is reconstructed against the same MemoryService and the test passes. Which restart claim is supported, and which is unsafe?
4. make lint succeeds on a host without golangci-lint. Draft an honest validation statement and name the remaining check.

[Worked answers](../solutions/ch02.md) justify each scope decision. Atlas now has a source index and a reproducible package check. The next experiment introduces processes and containers only for questions those smaller seams cannot answer.
