# From a Capable Package to a Restart-Safe Orchestrator

**Aleksandar Popovic**

An orchestrator is judged when its process disappears. Can another process recover the desired services, recognize existing containers, resume an update, and avoid creating competing work? A package can implement each of those ideas without the executable delivering their combined guarantee. The constructor graph decides which implementation actually runs.

This chapter reads orch at commit `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. All source links are pinned to that snapshot. It contains substantial scheduling, reconciliation, PostgreSQL, agent, and leadership code. Its default server nevertheless constructs an in-memory control plane. Understanding that distinction gives developers a precise integration target, gives operators realistic restart expectations, and gives architects a way to evaluate claims about durability.

The scope is specific: the normal `orch-server` startup path in this snapshot. Migration commands, standalone packages, future changes, and custom compositions can behave differently. We will trace the current path, run a disposable observation lab, and define the evidence required to support a stronger deployment claim.

## Start with the composition root

The composition root is the place where interfaces acquire concrete implementations. In orch it is the `run` function in [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L103-L259). Read that function before drawing the production architecture.

**Unchanged source excerpt — [main.go, lines 146–148](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L148):**

```go
controlPlane := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope), controlplane.WithClusterPolicy(cfg.ClusterPolicy), controlplane.WithRetentionConfig(cfg.Retention))
controlPlane.SetNotificationDispatcher(notifications.NewDispatcher(controlPlane, nil))
serverMetrics := metrics.NewServer()
```

The first line determines where desired services, nodes, tasks, deployments, secrets, and other domain records live. `MemoryService` owns maps guarded by a mutex. Those maps belong to this process. Encrypting a secret before storing it protects its representation, but does not make the map survive process termination.

Later startup code passes the same `controlPlane` into the GitOps controller, cron controller, scheduler, rollout controller, node monitor, and API handler. This is coherent dependency injection. It is also shared volatile state. The database URL does not replace that object. Startup checks the database schema only when `ORCH_SCHEMA_CHECK` is true; migration subcommands are separate paths.

The [operations and release hardening commit](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d) changed this entrypoint, while the [jobs, storage, DNS, and notifications commit](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87) added further surfaces. Those links explain development history. Their subjects do not establish persistence: the current constructor remains the evidence for current behavior.

## Trace the path that creates a task

It is tempting to see `scheduler.New(controlPlane)` in startup and conclude that every service passes through the deterministic planner. Follow the write path before accepting that conclusion.

`CreateService` calls `reconcileServiceTasksLocked`. That method finds ready nodes, resolves volume constraints, and creates tasks already assigned to nodes. Its node selection contains this expression in [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2287-L2314):

**Unchanged source excerpt — [reconcileServiceTasksLocked, line 2292](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2292):**

```go
node := eligibleNodes[len(active)%len(eligibleNodes)]
```

The task literal below it sets `NodeID` and `ActualStatus: types.TaskAssigned`. The standalone scheduler lists pending tasks. A service task created this way has already crossed that boundary. The immediate memory reconciliation path therefore bypasses the standalone planner's resource and placement decisions. Jobs, which are created pending, provide a different path through the scheduler.

This distinction matters in a resource chapter. [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go) has meaningful logic: ready-node filtering, label constraints, CPU and memory requests, port reservations, volume affinity, deterministic scoring, and stable ordering. Those properties describe the planner. They do not automatically describe a service assigned elsewhere.

There is a second boundary at container creation. The Docker adapter accepts resource limits and converts them into Docker `Memory` and `NanoCPUs`. However, the [agent's ensureTask method](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253-L265) does not populate `ContainerSpec.Resources`, and the service assignment DTO does not carry a corresponding resource field. Thus this snapshot does not propagate ordinary service limits through the active agent path. Parsing a resource field, planning against requests, and enforcing a cgroup limit are three distinct obligations.

## A database implementation is one layer

The [PostgreSQL store](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go) is real code, not merely a design document. It connects through pgx, implements transactions, stores core domain objects, and uses optimistic conditions on task mutations.

**Unchanged SQL excerpt — [AssignTask, line 919](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L919):**

```sql
WHERE id = $1 AND updated_at = $5 AND actual_status = 'pending'
```

That condition prevents a stale claimant from assigning a task whose timestamp or state changed. The scheduler also groups assignment and its event through `store.WithTx` when the store supports transactions. These are useful building blocks for reliable persistence.

They solve bounded problems. A task-row condition does not atomically reserve all node capacity or all ports considered in an earlier planning snapshot. A transactional event append does not make the normal API use PostgreSQL. A migration for jobs does not prove the PostgreSQL store implements the same job behavior as `MemoryService`.

A durable composition needs a domain service that implements the API's control-plane contract using durable stores, including the later workload features. It also needs restart recovery across service versions, deployment state, credential records, and agent reports. Simply replacing the constructor with `NewPostgresStore` is not a complete solution: the store and control-plane service expose different responsibilities and interfaces.

## Leadership does not reconstruct state

The [leader-election implementation commit](https://github.com/alekpopovic/orch/commit/eb3a07c20c550a533afaf36f414ede1ba6c00f78) introduced useful primitives. [internal/leadership/leadership.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go#L35-L74) defines a lease with a `Done` channel and a wrapper that cancels controller work when leadership ends. The PostgreSQL elector acquires a session advisory lock on a dedicated pooled connection.

The default server does not wrap its controller loops with `RunWithLeadership`. Launching two default servers therefore creates two independent memory control planes. A load balancer cannot turn them into shared durable state.

Even after wiring the elector, lease cleanup deserves a real database test. In [internal/leadership/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L67-L110), cancellation closes the lease and releases its connection to the pool; `Release` returns early if the lease is already closed. Returning a pooled connection is different from explicitly ending the PostgreSQL session that owns an advisory lock. Test cancellation and failed unlocks before asserting those paths release leadership correctly. This is a source-derived review concern; this chapter does not report an observed lock leak.

State durability, leader coordination, and fencing are separate. A leader lock can limit controller writers while shared state is available. It does not restore missing service records. It does not by itself stop an old container on an isolated worker. Each guarantee needs a defined owner and failure test.

## Follow a server restart as an incident

Imagine one server and two agents serving an application. The operator restarts the server to apply a configuration change. Docker may keep the workload containers alive, but the new server has fresh control-plane maps. The desired service records and node credentials from the old process are gone.

The agents still hold old node IDs and credentials. Their heartbeat requests cannot be authorized against the previous records because those records no longer exist in the new `MemoryService`. The agent heartbeat retry loop retries rather than automatically rebuilding a durable identity. Workload continuity in Docker can therefore coexist with loss of orchestration control.

Do not turn this scenario into a promise that every container will immediately stop or that agents will automatically recover. Exact outcomes depend on which process restarts, how credentials are restored, and when the agent can retrieve assigned tasks. The important invariant is narrower: this startup path has no persisted record from which the new server can reconstruct ownership.

An incident report should distinguish application reachability from control-plane recovery. Record whether the original endpoint serves, whether the service appears in the API, whether agent heartbeats succeed, and whether a rollout can resume. A successful HTTP request to the application answers only the first question.

Recovery also depends on identity. A managed Docker container carries labels identifying its task, service, node, and version. Those labels let the agent adopt a container after a lost status report. They cannot recreate a complete desired-state history by themselves. A label saying “version 3” does not contain the previous rollout strategy, the encrypted secret records, or the operator's desired replica count.

This is why container survival and orchestrator recovery must have separate acceptance criteria. In a durable implementation, task identity persists before the external Docker effect. After a crash, the agent can repeat creation against that same identity, and the adapter can find the previous container. If recovery generates a new task ID, label-based adoption no longer targets the original object; duplicate work becomes possible unless another reconciliation mechanism resolves ownership.

For a developer, the useful question is where identity first becomes durable. For an operator, it is how to tell whether the running container is still owned by the recovered control plane. For an architect, it is what happens when the database record and external runtime effect disagree. Answering those questions requires a recovery protocol, not just a startup order.

## Disposable lab: observe the state boundary

**Teaching addition — the following shell script is written for this chapter, not copied from orch.** Run it from a checkout at the pinned commit, on a development machine with Go 1.25 or newer, Bash with TCP redirections, and curl. It builds into a temporary directory and starts only its own loopback server. It needs no Docker, agent, or database. Use a free local port; the example uses 18080.

The script intentionally starts with a clean environment and disables the schema check. User JWT authentication remains empty for this local observation. The server must stay bound to `127.0.0.1`. The database address is deliberately unreachable and contains only disposable example credentials.

```bash
set -euo pipefail
book_tmp=$(mktemp -d)
book_server_pid=
book_port=18080

cleanup() {
  if [ -n "$book_server_pid" ]; then
    kill -TERM "$book_server_pid" 2>/dev/null || true
    wait "$book_server_pid" 2>/dev/null || true
  fi
  rm -rf "$book_tmp"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

go build -o "$book_tmp/orch-server" ./cmd/orch-server

book_curl() {
  curl --noproxy '*' --connect-timeout 1 --max-time 2 -fsS "$@"
}

start_server() {
  if (exec 3<>"/dev/tcp/127.0.0.1/$book_port") 2>/dev/null; then
    printf 'Local port %s is in use; choose a free port.\n' "$book_port" >&2
    return 1
  fi
  env -i PATH="$PATH" ORCH_SCHEMA_CHECK=false \
    "$book_tmp/orch-server" \
    --addr="127.0.0.1:$book_port" \
    --database-url='postgres://lab:lab@127.0.0.1:1/lab?sslmode=disable' \
    --secret-key='disposable-book-lab-key' \
    >"$book_tmp/server.log" 2>&1 &
  book_server_pid=$!
  for attempt in {1..50}; do
    kill -0 "$book_server_pid" 2>/dev/null || {
      cat "$book_tmp/server.log"
      return 1
    }
    if book_curl "http://127.0.0.1:$book_port/readyz" >/dev/null 2>&1; then
      sleep 0.1
      if kill -0 "$book_server_pid" 2>/dev/null; then
        return 0
      fi
      cat "$book_tmp/server.log"
      return 1
    fi
    sleep 0.1
  done
  cat "$book_tmp/server.log"
  return 1
}

start_server
book_curl -X POST "http://127.0.0.1:$book_port/v1/namespaces" \
  -H 'Content-Type: application/json' \
  --data '{"name":"book-restart-lab"}'
book_curl "http://127.0.0.1:$book_port/v1/namespaces" \
  >"$book_tmp/before.json"

kill -TERM "$book_server_pid"
wait "$book_server_pid" || true
book_server_pid=
start_server
book_curl "http://127.0.0.1:$book_port/v1/namespaces" \
  >"$book_tmp/after.json"

cat "$book_tmp/before.json"
cat "$book_tmp/after.json"
```

**Expected observations, not recorded execution results:** the first response creates `book-restart-lab`; the first list contains it; after a fresh process starts, the second list lacks it and includes the initial default namespace. The server starts without connecting to the intentionally unavailable database because the normal path constructs memory state and the optional schema check is disabled.

If startup fails, inspect its log before interpreting output. If another service owns the port, choose a free one. Do not run the lab against a remote server or reuse a production database URL. No database reset command is required for this demonstration.

The endpoint called `readyz` returns a fixed ready response in this snapshot. Its success establishes that the HTTP handler is serving, not that durable state, database availability, controller leadership, or agent recovery has been verified.

## Turn observations into engineering acceptance criteria

A stronger restart claim needs a process-level test that creates meaningful state, terminates the server, starts a new process, and queries the same durable database. Include an in-progress rollout, service version history, and agent credentials. Keep the old containers alive so the new server must recognize them instead of hiding the problem by recreating everything.

Then test ambiguity. Terminate after a database write but before the API response. Terminate after Docker creates a container but before the status report succeeds. Repeat the operation after restart and count objects. Task identity is useful here: the adapter's [CreateContainer implementation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L191-L221) searches for an existing managed container by task ID before creating one. That supports adoption when the durable control plane still knows the task identity.

The chaos subtest named “server restarts during rollout” in [internal/e2e/chaos_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L41-L62) constructs another rollout controller over the same memory service. It provides evidence for controller reconstruction with preserved state. It is not the process-level test just described.

Finally, make test prerequisites visible. PostgreSQL and Docker suites are opt-in and skip when their environment variables are absent. A green default `go test ./...` result cannot establish those external behaviors. Some database fixtures reset schema, so the appropriate test target is a disposable database dedicated to the lab.

## Exercises and answers

**1. Why does setting `DATABASE_URL` fail to make the default server durable?**

**Answer:** Configuration supplies a value; the composition root still constructs `MemoryService`. Persistence requires an implementation change in the domain/API path, with all relevant operations using durable storage and recovery tests.

**2. Why can planner resource tests pass while an ordinary service exceeds node capacity?**

**Answer:** The tested pure planner and the memory service's direct assigned-task path are different control flows. The latter does not call the former's fit checks. Trace the actual caller before transferring a package invariant to a deployment guarantee.

**3. What would a two-server leadership test need to prove?**

**Answer:** Both processes share durable state; only one controller callback is active per lock; losing the lease cancels work promptly; cancellation releases or ends the lock-owning session; a successor resumes without duplicate decisions. Independent memory maps cannot satisfy the shared-state condition.

**4. Which missing link prevents Docker resource enforcement?**

**Answer:** The active assignment/agent path does not deliver service limits into `ContainerSpec.Resources`. Adapter support is present, but the producer must populate the fields and a Docker inspection test must confirm the resulting HostConfig.

These limits define concrete integration work for this snapshot. The existing packages supply useful algorithms and boundaries. The next architectural task is to connect those boundaries so their individually tested behavior survives real process loss.
