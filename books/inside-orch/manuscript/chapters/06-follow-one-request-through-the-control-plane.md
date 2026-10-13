# Chapter 6 - Follow One Request Through the Control Plane

Atlas API's deployment has passed local parsing, but the interesting architectural question starts when the server accepts it. Which object changes first? Which controller observes that change? What survives if the server process exits after returning success? This chapter follows one create request through the executable composition, then measures the last question with a fresh binary process and one precisely owned Docker container.

Keep the previous chapter's resource and port findings nearby. They are examples of why an architecture diagram must follow callers, not just package names. A scheduler, database store, and runtime adapter can all exist while the ordinary service path uses only some of their behavior.

You will be able to trace the active constructor and mutation call sites, distinguish immediate assignment from periodic controllers, and classify a measured process restart without calling it database recovery.

## Server Assembly and Active State Ownership

The decisive constructor is in the server entry point:

```go
	envelope, err := secrets.NewLocalEnvelope(cfg.SecretKey)
	if err != nil {
		return err
	}
	controlPlane := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope), controlplane.WithClusterPolicy(cfg.ClusterPolicy), controlplane.WithRetentionConfig(cfg.Retention))
	controlPlane.SetNotificationDispatcher(notifications.NewDispatcher(controlPlane, nil))
	serverMetrics := metrics.NewServer()
```

Exact source: [cmd/orch-server/main.go:142–148](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L142-L148).

A local secret envelope is created, then passed into a new MemoryService along with cluster policy and retention configuration. The active state owner is this particular in-memory object. The database URL in configuration does not change that constructor. Migration subcommands and optional schema checks can use PostgreSQL without turning service maps into a PostgreSQL-backed control plane.

The entry point then constructs GitOps and cron controllers, a scheduler controller, a rollout controller, and a node monitor around this object. Notification dispatch is configured on it. Optional DNS uses it as its source. Usage snapshots and retention pruning are also driven by loops. These are real integrations because their constructors and Run or RunOnce calls are present in [the active startup path of main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L234).

Timing differs between those loops. Scheduler RunOnce is called on a one-second ticker. Rollout Run runs with a five-second interval. Usage is captured immediately and on a minute ticker; retention uses a daily ticker. Node-monitor timing comes from configuration. A graph with one generic arrow labelled controller loop would conceal these different observation windows and owners.

Some implemented packages are absent from this assembly. The standalone reconciler is not constructed here. Leadership leases do not gate these loops. Autoscaling policy can be represented and its package tested, but the autoscaler is not started by this binary. PostgreSQL store methods remain separately usable implementations. These classifications describe the locked source, not a suggestion that the missing connections can be inferred from configuration names.

The HTTP server receives the same MemoryService pointer, plus authentication options, metrics, and the GitOps syncer. Its graceful shutdown closes the listener and cancels loops through the process context. That is useful process hygiene. It is not a transaction flush of the control plane's maps to a persistent store.

## Mutation Paths and Controller Loops

The create-service handler decodes a request containing `spec`, performs the boundary checks, and invokes CreateService. Inside [MemoryService.CreateService the sequence](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L1253-L1323) is specific: check context cancellation, resolve image representation, validate the specification, run admission, normalize resource defaults, validate again, then acquire the mutation mutex.

The resolver's name should not hide its actual default behavior. It parses image references rather than fetching registry manifests. Setting pinning policy does not manufacture a remotely verified digest. For Atlas, keep requested image, supplied digest, and remotely resolved identity separate until a resolver implementation and an actual registry observation support the stronger claim.

Under the mutex, the method checks namespace existence, duplicate names, referenced secrets, registry credentials, and quota. It constructs an active service at deployment version 1, stores its specification version, reconciles its replica tasks immediately, appends a service-created event, and returns. The critical section coordinates these changes within that process. It is not a database transaction spanning a durable event log and a future Docker operation.

| Boundary | Owner | What completion establishes |
| --- | --- | --- |
| YAML parsing | CLI | A domain specification could be constructed locally |
| CreateService mutation | MemoryService | Accepted intent and related map updates in this process |
| Immediate assignment | MemoryService | Assigned task identity and selected ready node |
| Agent container operation | Agent Runner and Docker adapter | Runtime operation outcome for that task |
| Accepted status report | API and MemoryService | Updated observed task state under report rules |

Notice that creation can assign tasks before the periodic scheduler tick. [Immediate reconciliation chooses](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2249-L2316) a ready eligible node using round robin and creates an actual status of assigned. It does not submit every new replica to scheduler.Plan. This is why the planner's resource and explicit-port checks cannot be promoted to blanket guarantees for ordinary creation.

The scheduler loop still exists. Its presence is not fictitious, but its inputs and applicability must be traced. A controller that operates on pending tasks cannot retroactively prove fit for tasks already assigned by another path. Architecture review should ask which mutation creates each input state, then which controller consumes it.

The worker subsequently lists assigned tasks. [ListAssignedTasks builds](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L758-L814) an envelope from the task and its service, resolving environment values and registry credentials, and adding ports, healthcheck, and security context. That envelope omits resources. The agent then builds ContainerSpec without resources. The previous chapter's actual Docker inspection therefore follows from a specific data-flow break rather than a speculation about Docker's limit support.

A status report returns through the API, checks agent credentials and task ownership, and enters ReportTaskStatus. The memory implementation validates the node relationship and the desired/actual state gate before updating container ID, status, timestamps, and failure information. A duplicate terminal report returns early. This is a caller-specific idempotency behavior; it does not establish universal exactly-once event delivery.

## The MemoryService Restart Experiment

The failure window is between accepted intent and the next fresh server process. Docker is a separate daemon. Ending the control-plane process does not inherently terminate its containers, while recreating MemoryService does recreate empty maps. We want to observe those two facts in one bounded experiment without confusing a controller restart with process replacement.

The book-side harness is `examples/teaching-extensions/ch06/observe_container_restart.py`. It verifies every locked source file in the disposable working copy before launching the binary. Prerequisites are the already built baseline server, Python 3, access to Docker, and a cached `nginx:1.27-alpine` image. It refuses an existing evidence output and uses a newly selected loopback port. No pre-existing server endpoint is contacted.

The harness creates one container from the cached image with network disabled, no published ports, and no host mounts. It retains the exact returned container ID. This container is created manually by the harness, not by an upstream Runner. After registering a synthetic node and creating a service through the first actual server binary, it authenticates a running task report containing that container ID. The server accepts the relationship; the evidence explicitly labels it manually reported rather than automatically created or adopted.

Run the exact illustrated procedure from the website root with permission to access the local Docker daemon:

```bash
python3 books/inside-orch/examples/teaching-extensions/ch06/observe_container_restart.py \
  --working-copy /tmp/inside-orch-labs-cbfc94ade5b5/orch \
  --server /tmp/inside-orch-labs-cbfc94ade5b5/bin/orch-server \
  --output validation/labs/ch06/combined-restart-repeat.json
```

Use a new output name on each run. The recorded execution used `combined-restart.json`, with its command wrapper in `validation/labs/ch06/combined-restart-command.json`. The repeat path above is intentionally not claimed as an executed second run. The script contains all exact Docker and HTTP calls, bounded startup polling, process termination, and cleanup rather than requiring the reader to reconstruct them from a transcript.

The actual run passed. Before shutdown the first binary listed a service, its assigned-and-reported-running task, and the registered node. After a clean stop and a fresh server process on the same origin, all three lists were empty. The manually created container with the captured task container ID was still running. The custom namespace also disappeared, while the default namespace was recreated. Both process IDs and UTC observations are in the record.

That observation demonstrates loss of active process memory while an independently managed runtime object survives. It does not demonstrate database recovery, agent reconnection, automatic container adoption, or safe recreation of an identical service. In particular, a newly created service after restart would have a different identity. We intentionally stop before asking another controller to create competing work.

Cleanup is exact and independently checked: the harness terminates only the server processes it launched, removes only its captured container ID, and verifies that inspecting that ID subsequently fails. It does not remove all containers with an orch label, prune Docker, or delete database schemas. Evidence survives cleanup. If the container ID cannot be captured or startup fails, the failure must remain in the record rather than being converted into an expected success.

## Integration Gaps as Architectural Evidence

The restart result is useful because it answers a narrow question conclusively. A controller test that recreates a rollout controller around the same MemoryService answers another question: can that controller resume from still-existing state? Both can pass while a new server process loses its maps. The original chaos test named server restart actually retains the same memory service; DOC-007 preserves that distinction in the ledger.

Likewise, restoring PostgreSQL tables would help an implementation that reads those tables as its active state. The default binary does not. DOC-008 records the mismatch between a backup runbook's assumed composition and the constructor we inspected. Merely setting a database URL after a crash cannot rehydrate service, task, credential, and event maps that were never stored there.

The separate real-Docker flow record `validation/intake/docker-complete-flow-log-guard.json` demonstrates ordinary handler, Runner, and adapter interactions: deployment, actual nginx HTTP from inside the owned container, logs through the server-agent path, scale1→2→1, events, and deletion. It uses a guarded teaching composition rather than upstream Compose. Combining that record with our restart result is valuable, but their distinct scopes must remain visible.

A practical architecture review can now name concrete change requirements. A durable composition would need complete store parity for mutations and reads, state reconstruction, transaction boundaries for quota and assignment, credential continuity, controller restart behavior, and a policy for surviving runtime objects. Leadership would also need to gate each relevant controller consistently rather than only adding a lease package. These are future integration requirements, not repairs made to the locked source.

The implementation history reinforces that caution. [The REST API commit](https://github.com/alekpopovic/orch/commit/64a0725387b8130be988948b81774aea7051c718) introduced the early executable control plane. [The later operations batch](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d) added many modules and hardening changes. Reading its patch shows broad additions, not a proof that every design document became a connected production subsystem. Original prompts 04,10,25 remain development evidence; current startup and measured failure boundaries govern this edition.

For Atlas, the immediate operational decision is straightforward: treat the default binary as a development control plane with process-local intent. Preserve the actual limitations when teaching its useful packages. A precise integration gap is more informative than either calling the whole project production-ready or dismissing its independently implemented behavior.

## Exercises

1. Identify five active background activities in the server entry point and distinguish them from immediate service assignment.
2. Trace where an Atlas create request acquires the mutation mutex and which checks precede or follow it. What atomicity does that mutex provide?
3. Explain why the combined restart observation does not establish automatic adoption of a surviving Docker container. Name the manual step that limits the claim.
4. A proposed recovery plan changes only DATABASE_URL and restarts the binary. Use the constructor and observed state to explain why this plan is insufficient.

See the [worked answers](../solutions/ch06.md).
