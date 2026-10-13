# Chapter contracts

Source edition `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`; scope frozen 2026-10-13T00:36:11.158249+00:00. No chapter reordered. All paths below are immutable Orch source-relative paths. Each lab is expected until a separate execution record is cited. Source-only writing may proceed while external lab prerequisites remain explicit release gates.

## Shared editorial boundaries

Explain default in-memory state before advanced packages: Preface and Chapters1,3,6 explicitly carry this invariant; Chapter9 develops durability rather than introducing a surprise. Chapter4 defines lifecycle names; later chapters reference it. Chapter15 defines event/audit semantics; Chapter23 owns identity/RBAC detail, with Chapter14 limited to probe trust and Chapter27 to tenancy scope. Chapter12 defines idempotent Docker identity. Chapter10 defines planner resource accounting; Chapter5 traces declared fields and Chapter26 runtime security.

Every numbered chapter aims for2,100 meaningful narrative words, within1,800–2,500. Six appendices aim for1,300 each and Preface 1,000: planned total 92,800 excluding code, commands and metadata. No repeated boilerplate should satisfy that budget. Worked answers are additional substantive material, separately authored.

## Frozen contracts

### 01. Why Build a Container Orchestrator?

**Problem:** Define the small-cluster problem, desired-state architecture, and the project’s verified implementation boundary.
**Prior knowledge:** Go interfaces, HTTP and Docker fundamentals; Preface safety scope.
**Reader paths:** developer, devops, architect.
**Outcomes:** Trace a service from API request to Docker container.; Separate project intent from default binary behavior.; Explain when a small orchestrator is an appropriate engineering choice.
**Exact source targets:** `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `cmd/orch-server/main.go`
**Atlas task:** Draw the Atlas Lab system map and record the pinned source revision.
**Boundary and review gate:** Every capability claim has a source classification; MemoryService is named explicitly and the architecture map does not imply PostgreSQL server integration.
**Original prompt associations:** 00, 26. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/01-why-build-a-container-orchestrator.md`; answers `manuscript/solutions/ch01.md`; claims `validation/evidence/ch01.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 02. A Repository Built for Reasoning

**Problem:** Read package boundaries, interfaces, injected dependencies, cancellation rules, and the repository’s engineering contract.
**Prior knowledge:** Go interfaces, HTTP and Docker fundamentals; Preface safety scope.
**Reader paths:** developer, architect.
**Outcomes:** Navigate the actual package tree.; Identify side-effect boundaries and dependency injection.; Use deterministic tests and context cancellation as design constraints.
**Exact source targets:** `AGENTS.md`, `go.mod`, `Makefile`, `docs/DEVELOPMENT.md`, `internal/scheduler/scheduler.go`, `internal/docker/docker.go`
**Atlas task:** Create a read-only source index and run the prerequisite and build checks.
**Boundary and review gate:** Show actual package names rather than copying intended AGENTS layout; explain why internal/docker and internal/health differ from planned directory names.
**Original prompt associations:** 00, 01, 21. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/02-a-repository-built-for-reasoning.md`; answers `manuscript/solutions/ch02.md`; claims `validation/evidence/ch02.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 03. Boot the Lab and Deploy the First Service

**Problem:** Run the pinned local development path and inspect CLI-visible service, task, and node state.
**Prior knowledge:** Go interfaces, HTTP and Docker fundamentals; Preface safety scope.
**Reader paths:** developer, devops, architect.
**Outcomes:** Build or install the pinned CLI reproducibly.; Start and tear down the local cluster.; Read service and task state after deployment.
**Exact source targets:** `README.md`, `docs/INSTALLATION.md`, `docs/DEVELOPMENT.md`, `scripts/dev-up.sh`, `scripts/dev-down.sh`, `deployments/examples/http-api.yaml`, `internal/cli/root.go`
**Atlas task:** Deploy the upstream http-api example, inspect events, scale, collect logs, then remove it.
**Boundary and review gate:** All commands are checked against current CLI behavior; document Docker requirements, port prerequisites, and cleanup; do not invent output transcripts.
**Original prompt associations:** 05, 21, 27, 28. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/03-boot-the-lab-and-deploy-the-first-service.md`; answers `manuscript/solutions/ch03.md`; claims `validation/evidence/ch03.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 04. Domain Models and State Machines

**Problem:** Study service, task, node, deployment, and event types as explicit contracts.
**Prior knowledge:** Go interfaces, HTTP and Docker fundamentals; Preface safety scope.
**Reader paths:** developer, architect.
**Outcomes:** Distinguish desired task status from observed status.; Explain valid and invalid lifecycle transitions.; Relate immutable service versions to deployments.
**Exact source targets:** `pkg/types/types.go`, `pkg/types/lifecycle.go`, `pkg/types/lifecycle_test.go`, `internal/task/task.go`, `internal/node/node.go`, `docs/STATE_MACHINES.md`
**Atlas task:** Trace Atlas API lifecycle transitions with a state transition table and one rejected transition test.
**Boundary and review gate:** The diagram includes terminal states and transition ownership; every shown state exists in pinned types and invalid transitions have evidence.
**Original prompt associations:** 02, 29. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/04-domain-models-and-state-machines.md`; answers `manuscript/solutions/ch04.md`; claims `validation/evidence/ch04.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 05. Service Specifications, Resources, and Ports

**Problem:** Read declarative service validation, resource quantities, labels, and host-port allocation constraints.
**Prior knowledge:** 04 (domain/lifecycle definitions)
**Reader paths:** developer, devops, architect.
**Outcomes:** Parse CPU and memory quantities without ambiguity.; Describe requested resources and placement constraints.; Predict a public-port collision and validation error.
**Exact source targets:** `docs/SERVICE_SPEC.md`, `docs/RESOURCES.md`, `pkg/types/types.go`, `pkg/types/parsers.go`, `pkg/types/validation_test.go`, `pkg/types/resources_test.go`, `internal/cli/deploy.go`, `deployments/examples/http-api.yaml`
**Atlas task:** Create good and deliberately invalid Atlas manifests; explain replicas versus finite host-port capacity.
**Boundary and review gate:** Resource arithmetic includes units; published host ports are node-scoped; invalid manifests are tested through the actual parser.
**Original prompt associations:** 17, 34, 43. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/05-service-specifications-resources-and-ports.md`; answers `manuscript/solutions/ch05.md`; claims `validation/evidence/ch05.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 06. Follow One Request Through the Control Plane

**Problem:** Walk the default server assembly, in-memory control plane, controller loops, and runtime integration gaps.
**Prior knowledge:** 04 (domain/lifecycle definitions)
**Reader paths:** developer, devops, architect.
**Outcomes:** Locate the actual control-plane constructor.; Explain how API mutations and controller iterations interact.; Identify state that is lost on a default server restart.
**Exact source targets:** `cmd/orch-server/main.go`, `internal/controlplane/controlplane.go`, `internal/controlplane/operations.go`, `internal/api/api.go`, `docs/ARCHITECTURE.md`
**Atlas task:** Restart the local server in a disposable lab and contrast surviving Docker containers with lost control-plane state.
**Boundary and review gate:** Trace current call sites; do not claim DB URL configuration enables persistent server state; classify restart observations as measured or expected.
**Original prompt associations:** 04, 10, 25. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/06-follow-one-request-through-the-control-plane.md`; answers `manuscript/solutions/ch06.md`; claims `validation/evidence/ch06.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 07. HTTP Contracts and Compatible APIs

**Problem:** Study middleware, validation, stable error responses, versioned routes, and the shared API contract.
**Prior knowledge:** 04 (domain/lifecycle definitions)
**Reader paths:** developer, architect.
**Outcomes:** Follow validation and authorization at the HTTP boundary.; Map domain errors to stable client-facing errors.; Check OpenAPI documentation against route behavior.
**Exact source targets:** `internal/api/api.go`, `internal/api/versioning.go`, `internal/apperrors/errors.go`, `internal/api/api_test.go`, `api/openapi.yaml`, `api/openapi_test.go`, `pkg/client/client.go`, `docs/API.md`, `docs/API_VERSIONING.md`
**Atlas task:** Call the API with valid and invalid requests and add a book-side contract smoke test using the public client.
**Boundary and review gate:** OpenAPI versus route gaps go into the contradiction ledger; public and internal agent contracts remain distinct; additive compatibility is demonstrated.
**Original prompt associations:** 04, 45, 61, 62. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/07-http-contracts-and-compatible-apis.md`; answers `manuscript/solutions/ch07.md`; claims `validation/evidence/ch07.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 08. A CLI That Operators Can Automate

**Problem:** Explore Cobra command composition, configuration precedence, JSON output, and deployment parsing.
**Prior knowledge:** 04 (domain/lifecycle definitions)
**Reader paths:** developer, devops.
**Outcomes:** Explain flag, environment, configuration, and default precedence.; Use stable JSON output for a small automation script.; Distinguish local validation from server-side acceptance.
**Exact source targets:** `internal/cli/root.go`, `internal/cli/root_test.go`, `internal/cli/client.go`, `internal/cli/deploy.go`, `internal/cli/output.go`, `internal/config/config.go`, `docs/CLI.md`, `docs/CONFIGURATION.md`
**Atlas task:** Write an Atlas status script that uses current JSON fields and reports actionable failures.
**Boundary and review gate:** Run the exact illustrated commands; do not introduce unsupported switches; examples redact tokens and do not assume an implicit server URL.
**Original prompt associations:** 05, 43, 44. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/08-a-cli-that-operators-can-automate.md`; answers `manuscript/solutions/ch08.md`; claims `validation/evidence/ch08.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 09. Persistence, Transactions, and Optimistic Concurrency

**Problem:** Read PostgreSQL store interfaces and transactions while distinguishing them from the default in-memory server.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Identify transaction boundaries and optimistic conflict checks.; Explain store integration test isolation.; Distinguish persisted schemas from integrated production durability.
**Exact source targets:** `internal/store/store.go`, `internal/store/postgres.go`, `internal/store/postgres_test.go`, `internal/store/errors.go`, `migrations/000001_initial_schema.up.sql`, `migrations/000001_initial_schema.down.sql`, `docs/MIGRATIONS.md`
**Atlas task:** Run store integration tests against a disposable PostgreSQL database and examine a conflicting write.
**Boundary and review gate:** Database tests may reapply down/up migrations and require disposable data; show actual transaction code; server wiring stays an explicitly separate architectural exercise.
**Original prompt associations:** 03, 24, 30. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/09-persistence-transactions-and-optimistic-concurrency.md`; answers `manuscript/solutions/ch09.md`; claims `validation/evidence/ch09.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 10. A Deterministic Scheduler

**Problem:** Read placement order, eligibility checks, capacity accounting, and concurrent assignment safety.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, architect.
**Outcomes:** Explain deterministic ordering and tie-breaking.; Check labels, status, resources, ports, and storage topology.; Identify the persistence conflict path during assignment.
**Exact source targets:** `internal/scheduler/scheduler.go`, `internal/scheduler/scheduler_test.go`, `internal/scheduler/property_test.go`, `internal/scheduler/workloads_test.go`, `docs/SCHEDULER.md`, `docs/RESOURCES.md`
**Atlas task:** Build a tiny fake-node placement experiment with valid, exhausted, and conflicting nodes.
**Boundary and review gate:** Calculate one complete placement by hand and confirm with a test; task assignment is unique; resource and port claims are not described as Docker enforcement.
**Original prompt associations:** 09, 17, 31. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/10-a-deterministic-scheduler.md`; answers `manuscript/solutions/ch10.md`; claims `validation/evidence/ch10.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 11. Reconciliation as Repeated Convergence

**Problem:** Explain creation, scale-down, restart policy, soft deletion, and restart idempotency.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, architect.
**Outcomes:** Separate reconciliation decisions from placement and runtime side effects.; Demonstrate repeated RunOnce convergence.; Handle failed tasks and service soft deletion.
**Exact source targets:** `internal/reconciler/reconciler.go`, `internal/reconciler/reconciler_test.go`, `internal/controlplane/controlplane.go`, `docs/RECONCILER.md`
**Atlas task:** Apply the same desired Atlas replica count repeatedly in deterministic tests and verify no duplicate tasks.
**Boundary and review gate:** Show what each repeated iteration reads and writes; account for transitional tasks; document the default server’s actual invocation path rather than assuming a wired standalone loop.
**Original prompt associations:** 10, 24, 32. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/11-reconciliation-as-repeated-convergence.md`; answers `manuscript/solutions/ch11.md`; claims `validation/evidence/ch11.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 12. Idempotent Docker Operations and Drift

**Problem:** Study the typed Docker adapter, managed labels, fake runtime, cleanup boundaries, and external container drift.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Identify idempotency keys and managed-container labels.; Explain how repeated create/start/remove calls converge.; Separate unmanaged containers from safe cleanup candidates.
**Exact source targets:** `internal/docker/docker.go`, `internal/docker/docker_test.go`, `internal/docker/fake.go`, `internal/docker/fake_test.go`, `internal/agent/agent.go`, `docs/AGENT.md`
**Atlas task:** Repeat runtime operations through FakeRuntime and inject a missing or manually stopped managed container.
**Boundary and review gate:** Use actual Runtime methods and labels; drift repair respects task identity; no example removes unrelated host containers.
**Original prompt associations:** 06, 33, 41. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/12-idempotent-docker-operations-and-drift.md`; answers `manuscript/solutions/ch12.md`; claims `validation/evidence/ch12.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 13. Agents, Heartbeats, and Task Reports

**Problem:** Trace registration, heartbeat, polling, local reconciliation, and status reporting.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Follow agent bootstrap and credential use.; Explain agent versus server decision ownership.; Interpret repeated task reports and heartbeat failure.
**Exact source targets:** `cmd/orch-agent/main.go`, `internal/agent/agent.go`, `internal/agent/agent_test.go`, `internal/auth/agent.go`, `internal/controlplane/agent_test.go`, `docs/AGENT.md`
**Atlas task:** Observe one Atlas worker agent and simulate dropped reports using deterministic fakes.
**Boundary and review gate:** Task status updates are grounded in request types; explain retry and cancellation behavior without implying exactly-once delivery or mTLS.
**Original prompt associations:** 07, 08, 19. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/13-agents-heartbeats-and-task-reports.md`; answers `manuscript/solutions/ch13.md`; claims `validation/evidence/ch13.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 14. Health Checks That Respect Trust Boundaries

**Problem:** Read HTTP/TCP health checks, timeout behavior, status transitions, and SSRF controls.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Distinguish process running from healthy service state.; Explain timeout, retry, and health reporting semantics.; Demonstrate allowed and rejected probe targets.
**Exact source targets:** `internal/health/health.go`, `internal/health/health_test.go`, `docs/HEALTHCHECKS.md`, `docs/SECURITY.md`, `prompts/53-healthcheck-ssrf-protection.md`
**Atlas task:** Inject healthy, timeout, and forbidden-target probes for Atlas API without contacting metadata services.
**Boundary and review gate:** SSRF examples use fake network/probe boundaries; capture actual allow/deny conditions and acknowledge remaining host-network risks.
**Original prompt associations:** 11, 53. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/14-health-checks-that-respect-trust-boundaries.md`; answers `manuscript/solutions/ch14.md`; claims `validation/evidence/ch14.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 15. Events, Audits, and Notification Boundaries

**Problem:** Treat events as operator history, audit as an attribution record, and notifications as external effects.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops.
**Outcomes:** Differentiate domain events, diagnostic logs, and audits.; Trace redaction and actor attribution.; Explain notification delivery, retry, and failure isolation from code.
**Exact source targets:** `internal/events/events.go`, `internal/events/events_test.go`, `internal/audit/audit.go`, `internal/notifications/notifications.go`, `internal/notifications/notifications_test.go`, `docs/EVENTS.md`, `docs/NOTIFICATIONS.md`
**Atlas task:** Capture the Atlas deployment event timeline and send notifications to a local fake sink.
**Boundary and review gate:** Do not equate the default memory-backed event history with durable production events; delivery guarantees and redaction claims come from implementation tests.
**Original prompt associations:** 13, 46, 80. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/15-events-audits-and-notification-boundaries.md`; answers `manuscript/solutions/ch15.md`; claims `validation/evidence/ch15.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 16. Log Streaming Without Losing Control

**Problem:** Trace server-to-agent log paths, Docker stream framing, cancellation, and bounded operator consumption.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops.
**Outcomes:** Locate actual log stream boundaries and response formats.; Explain tail, follow, cancellation, and transport errors.; Separate orchestration events from application stdout/stderr.
**Exact source targets:** `internal/agent/logs.go`, `internal/api/logs.go`, `internal/docker/docker.go`, `docs/LOGS.md`, `internal/cli/operations.go`
**Atlas task:** Stream Atlas application logs, disconnect the client, and check cancellation through a local test.
**Boundary and review gate:** Use actual agent/API/runtime log files; explain cancellation and stream errors; never fabricate a centralized persistent log collector.
**Original prompt associations:** 12. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/16-log-streaming-without-losing-control.md`; answers `manuscript/solutions/ch16.md`; claims `validation/evidence/ch16.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 17. Rolling Updates and Rollback Invariants

**Problem:** Explore service versions, deployment locks, max surge, max unavailable, and rollback state machines.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Compute rollout availability and surge limits.; Explain failed target versions and previous successful versions.; Reject conflicting user mutations during a deployment.
**Exact source targets:** `internal/rollout/rollout.go`, `internal/rollout/rollout_test.go`, `internal/controlplane/rollback_test.go`, `internal/controlplane/operation_lock_test.go`, `docs/ROLLOUTS.md`
**Atlas task:** Roll Atlas API forward, inject an unhealthy target, and trace a rollback in fake and optional Docker lab modes.
**Boundary and review gate:** Include invariant arithmetic and one failure timeline; no zero-downtime guarantee exceeds tested health and routing behavior.
**Original prompt associations:** 14, 15, 42. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/17-rolling-updates-and-rollback-invariants.md`; answers `manuscript/solutions/ch17.md`; claims `validation/evidence/ch17.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 18. Safe Deletion and Resource Cleanup

**Problem:** Follow deleting versus deleted services, task stop/remove behavior, finalization, and failures.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Explain why removal is a workflow rather than one HTTP delete.; Trace cleanup ownership and retry behavior.; Identify resource leaks and safe finalization conditions.
**Exact source targets:** `internal/reconciler/reconciler.go`, `internal/controlplane/controlplane.go`, `internal/agent/agent.go`, `internal/docker/docker.go`, `docs/RECONCILER.md`, `docs/RELIABILITY.md`
**Atlas task:** Delete Atlas API while injecting one remove failure; inspect repeated cleanup attempts.
**Boundary and review gate:** Distinguish desired deletion from confirmed runtime removal; demonstrate repeated calls and avoid destructive force-cleanup recipes.
**Original prompt associations:** 16, 25. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/18-safe-deletion-and-resource-cleanup.md`; answers `manuscript/solutions/ch18.md`; claims `validation/evidence/ch18.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 19. Offline Nodes, Draining, and Rescheduling

**Problem:** Read heartbeat expiry, node statuses, drain/uncordon operations, and workload rescheduling safety.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Interpret stale heartbeat transitions.; Explain why drain differs from immediate node deletion.; Reason about replacement tasks and partition uncertainty.
**Exact source targets:** `internal/node/monitor.go`, `internal/node/monitor_test.go`, `internal/controlplane/drain_test.go`, `internal/controlplane/offline_test.go`, `internal/controlplane/operations.go`, `docs/OPERATIONS.md`
**Atlas task:** Pause a disposable Atlas agent and perform a deterministic drain/reschedule trace.
**Boundary and review gate:** Correct stale docs that call node monitoring unimplemented; include a partition case and clearly identify what orch cannot fence on an isolated worker.
**Original prompt associations:** 39, 40. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/19-offline-nodes-draining-and-rescheduling.md`; answers `manuscript/solutions/ch19.md`; claims `validation/evidence/ch19.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 20. Endpoint Discovery and Internal DNS

**Problem:** Study endpoint filtering, namespace names, host addresses and published ports, DNS TTL, and unhealthy endpoints.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Explain endpoint identity and health filtering.; Distinguish DNS names from stable virtual IPs.; Reason about stale caches and rescheduled endpoints.
**Exact source targets:** `internal/discovery/discovery.go`, `internal/discovery/discovery_test.go`, `internal/dns/server.go`, `internal/dns/server_test.go`, `docs/SERVICE_DISCOVERY.md`, `deployments/examples/internal-dns-compose.yaml`
**Atlas task:** Query Atlas endpoints and internal DNS under healthy and unhealthy fake task states.
**Boundary and review gate:** Explain DNS returns node addresses and clients still need ports; no Kubernetes compatibility, overlay, VIP, or automatic cross-node networking claim.
**Original prompt associations:** 35, 78. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/20-endpoint-discovery-and-internal-dns.md`; answers `manuscript/solutions/ch20.md`; claims `validation/evidence/ch20.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 21. Ingress, Host Networking, and the Overlay Roadmap

**Problem:** Read Traefik configuration and current host-port traffic flow before evaluating future overlay/CNI design.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** devops, architect.
**Outcomes:** Trace ingress to node-level published ports.; Identify collisions, topology exposure, and routing limitations.; Evaluate an overlay/CNI design without claiming it is built.
**Exact source targets:** `internal/traefik/config.go`, `internal/traefik/config_test.go`, `docs/TRAEFIK.md`, `docs/NETWORKING.md`, `docs/NETWORKING_DESIGN.md`, `deployments/examples/routed-api.yaml`, `deployments/examples/traefik-demo.yaml`
**Atlas task:** Route Atlas API with the upstream Traefik example and draw the current packet path.
**Boundary and review gate:** Separate executable ingress examples from design-only overlay/CNI; show actual router/service fields and a failure path.
**Original prompt associations:** 36, 77. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/21-ingress-host-networking-and-the-overlay-roadmap.md`; answers `manuscript/solutions/ch21.md`; claims `validation/evidence/ch21.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 22. Autoscaling Decisions and Missing Integration

**Problem:** Read CPU recommendations, bounds, cooldown, rollout exclusion, and production provider gaps.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Calculate a replica recommendation from observed CPU.; Explain bounded scaling and cooldown.; Identify the missing production metrics provider and default-server wiring.
**Exact source targets:** `internal/autoscaler/autoscaler.go`, `internal/autoscaler/autoscaler_test.go`, `docs/AUTOSCALING.md`, `docs/AUTOSCALING_DESIGN.md`, `cmd/orch-server/main.go`
**Atlas task:** Drive Atlas replica recommendations with FakeMetricsProvider and inspect cooldown behavior.
**Boundary and review gate:** Do not assert automatic production autoscaling is active; distinguish declared stabilizationWindow from enforced behavior and state whether cooldown is durable.
**Original prompt associations:** 54, 55. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/22-autoscaling-decisions-and-missing-integration.md`; answers `manuscript/solutions/ch22.md`; claims `validation/evidence/ch22.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 23. Authentication, Authorization, and Node Trust

**Problem:** Study operator JWT roles, agent enrollment tokens, route authorization, and node trust limits.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Distinguish user authentication from agent bootstrap.; Trace role checks for sensitive operations.; Explain Docker socket privilege and missing mTLS identity.
**Exact source targets:** `internal/auth/auth.go`, `internal/auth/agent.go`, `internal/auth/agent_test.go`, `internal/api/api.go`, `docs/SECURITY.md`, `docs/SECURITY_REVIEW.md`
**Atlas task:** Run Atlas API authorization tests with viewer, operator, admin, and invalid agent credentials.
**Boundary and review gate:** Use placeholder credentials only; document auth enablement and actual defaults; no claim token authentication is equivalent to mutual TLS.
**Original prompt associations:** 18, 19, 51. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/23-authentication-authorization-and-node-trust.md`; answers `manuscript/solutions/ch23.md`; claims `validation/evidence/ch23.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 24. Encrypted Secrets and Configuration Redaction

**Problem:** Read secret envelope construction, namespace reference resolution, configuration precedence, and redacted output.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports); 23 (authorization)
**Reader paths:** developer, devops, architect.
**Outcomes:** Trace secret encrypt/decrypt and reference resolution.; Explain local key custody and rotation gaps.; Check diagnostic paths for redaction.
**Exact source targets:** `internal/secrets/envelope.go`, `internal/secrets/envelope_test.go`, `internal/config/config.go`, `internal/config/config_test.go`, `docs/SECRETS.md`, `docs/CONFIGURATION.md`, `deployments/examples/secrets-api.yaml`
**Atlas task:** Deploy an Atlas placeholder-secret example and assert sample sensitive values are absent from printed configuration.
**Boundary and review gate:** Do not promise external KMS or rotation not implemented; examples never put real secrets in command arguments or committed files.
**Original prompt associations:** 37, 44. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/24-encrypted-secrets-and-configuration-redaction.md`; answers `manuscript/solutions/ch24.md`; claims `validation/evidence/ch24.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 25. Registry Credentials and Immutable Image Identity

**Problem:** Connect registry authentication, image references, tag policy, and digest pinning to rollout traceability.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Parse tags and digests through actual image-reference code.; Trace namespace-scoped registry credentials.; Explain mutable-tag risk and the implemented pinning policy.
**Exact source targets:** `internal/image/reference.go`, `internal/image/reference_test.go`, `internal/controlplane/image_test.go`, `internal/docker/docker.go`, `docs/REGISTRIES.md`, `deployments/examples/private-image.yaml`, `migrations/000013_image_metadata.up.sql`
**Atlas task:** Validate Atlas image references and use an explicitly labeled placeholder digest for non-executing examples.
**Boundary and review gate:** Use real verified digest only for executable labs; classify fake digests as explanatory; image signing is reserved for the design chapter.
**Original prompt associations:** 38, 67. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/25-registry-credentials-and-immutable-image-identity.md`; answers `manuscript/solutions/ch25.md`; claims `validation/evidence/ch25.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 26. Security Contexts, Admission, and Policy

**Problem:** Read enforceable container security fields and policy/admission entry points.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports); 23 (authorization)
**Reader paths:** developer, devops, architect.
**Outcomes:** Distinguish supported security context fields from host isolation.; Explain admission sequencing and rejection evidence.; Verify CLI, API, and GitOps share policy acceptance boundaries.
**Exact source targets:** `internal/policy/policy.go`, `internal/policy/policy_test.go`, `internal/admission/admission.go`, `internal/admission/admission_test.go`, `internal/controlplane/admission_test.go`, `docs/POLICY_ENGINE_DESIGN.md`, `docs/SECURITY.md`
**Atlas task:** Reject an unsafe Atlas manifest and inspect stable policy error details.
**Boundary and review gate:** Do not imply a sandbox beyond Docker enforcement; supported admission hooks are code-evidenced and external policy-engine concepts remain proposals.
**Original prompt associations:** 52, 63, 64. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/26-security-contexts-admission-and-policy.md`; answers `manuscript/solutions/ch26.md`; claims `validation/evidence/ch26.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 27. Namespaces and the Limits of Multi-Tenancy

**Problem:** Study namespace context, 404 isolation behavior, namespace-local uniqueness, role maps, and shared host risks.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports); 23 (authorization)
**Reader paths:** developer, devops, architect.
**Outcomes:** Resolve namespaces consistently across API and CLI.; Show cross-namespace secret and object isolation.; Explain why logical namespaces are not a hostile-tenant security boundary.
**Exact source targets:** `internal/namespace/context.go`, `internal/controlplane/namespace_test.go`, `internal/api/namespace_test.go`, `internal/auth/auth.go`, `docs/MULTI_TENANCY.md`, `migrations/000011_namespaces.up.sql`, `migrations/000011_namespaces.down.sql`
**Atlas task:** Deploy two Atlas API services with the same name in different namespaces and verify invisible cross-namespace IDs.
**Boundary and review gate:** Every isolation guarantee is scoped; discuss shared nodes, Docker and networking; down-migration data loss is explicit in the appendix runbook.
**Original prompt associations:** 65. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/27-namespaces-and-the-limits-of-multi-tenancy.md`; answers `manuscript/solutions/ch27.md`; claims `validation/evidence/ch27.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 28. Quotas and Usage Accounting

**Problem:** Read atomic quota checks, requested resource accounting, usage snapshots, and operational exports.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports); 23 (authorization)
**Reader paths:** developer, devops, architect.
**Outcomes:** Calculate namespace requested CPU/memory and port usage.; Explain concurrent quota enforcement and zero-as-unlimited.; Distinguish operational usage reports from invoices or payment billing.
**Exact source targets:** `internal/quota/quota.go`, `internal/controlplane/quota_test.go`, `internal/controlplane/operations.go`, `internal/store/postgres.go`, `internal/api/quota_gitops_test.go`, `docs/MULTI_TENANCY.md`, `migrations/000012_resource_quotas.up.sql`
**Atlas task:** Exhaust an Atlas namespace quota and export a bounded usage report with known dimensions.
**Boundary and review gate:** State whether each guarantee comes from MemoryService or PostgreSQL store; CSV units are documented; no complete billing product claim.
**Original prompt associations:** 66, 85. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/28-quotas-and-usage-accounting.md`; answers `manuscript/solutions/ch28.md`; claims `validation/evidence/ch28.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 29. Supply Chain Designs Without False Guarantees

**Problem:** Analyze image signing, SBOM and vulnerability scanning proposals against implemented image-policy boundaries.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Separate digest identity from signature authenticity.; Design a verification and provenance decision path.; Define fail-open/fail-closed and scanner freshness tradeoffs.
**Exact source targets:** `docs/IMAGE_SIGNING_DESIGN.md`, `docs/SUPPLY_CHAIN_SECURITY_DESIGN.md`, `internal/image/reference.go`, `internal/policy/policy.go`, `prompts/68-image-signing-design.md`, `prompts/69-sbom-and-vulnerability-scanning-design.md`
**Atlas task:** Write an Atlas threat model and a book-side verification contract; mark every proposed adapter as illustrative.
**Boundary and review gate:** Signing and scanning are design material unless implementation evidence proves otherwise; do not install moving external tools without official versioned references.
**Original prompt associations:** 68, 69. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/29-supply-chain-designs-without-false-guarantees.md`; answers `manuscript/solutions/ch29.md`; claims `validation/evidence/ch29.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 30. GitOps, Drift, and Controlled Reconciliation

**Problem:** Trace isolated git checkout, manifest parse/admission, recorded revision, warn/auto-revert drift, and prune ownership.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Explain source revision provenance and deterministic manifest order.; Contrast warn and auto_revert drift behavior.; Bound pruning to the source’s managed services.
**Exact source targets:** `internal/gitops/gitops.go`, `internal/gitops/gitops_test.go`, `internal/controlplane/operations.go`, `docs/GITOPS.md`, `migrations/000014_gitops_sources.up.sql`
**Atlas task:** Use a local Atlas manifest repository, introduce manual drift, and demonstrate warn versus auto_revert.
**Boundary and review gate:** Use a real local committed revision; no userinfo credentials in URLs; illustrate failure isolation and ensure prune never touches unrelated services.
**Original prompt associations:** 70, 71. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/30-gitops-drift-and-controlled-reconciliation.md`; answers `manuscript/solutions/ch30.md`; claims `validation/evidence/ch30.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 31. Finite Jobs and Time-Based Work

**Problem:** Read Job attempts, retry limits, CronJob parsing, timezone semantics, concurrency policies, and missed runs.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Trace Job exit status to success, failure, or retry.; Explain Allow, Forbid, and Replace concurrency.; Reason about timezone and bounded missed occurrences.
**Exact source targets:** `internal/controlplane/workloads.go`, `internal/controlplane/workloads_test.go`, `internal/cronjobs/cronjobs.go`, `internal/cronjobs/cronjobs_test.go`, `internal/cli/workloads.go`, `pkg/types/workloads.go`, `docs/JOBS.md`, `docs/JOBS_DESIGN.md`
**Atlas task:** Run a finite Atlas report job and drive CronJob fake time through overlap and missed-occurrence cases.
**Boundary and review gate:** Use exact supported five-field cron syntax and workload YAML; UTC and timezone cases are explicit; do not claim exactly-once scheduling.
**Original prompt associations:** 72, 73, 74. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/31-finite-jobs-and-time-based-work.md`; answers `manuscript/solutions/ch31.md`; claims `validation/evidence/ch31.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 32. Local Volumes, Claims, and Workload Topology

**Problem:** Study local volume claims, scheduler topology, active writer locks, attachment lifecycle, and unsupported distributed storage.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Explain why a local claim binds future placement to a node.; Trace writer-lock and read-only attachment behavior.; Separate storage metadata safety from data replication and backup.
**Exact source targets:** `internal/controlplane/workloads.go`, `internal/controlplane/workloads_test.go`, `internal/scheduler/workloads_test.go`, `internal/docker/docker.go`, `pkg/types/workloads.go`, `docs/STORAGE.md`, `docs/STATEFUL_WORKLOADS_DESIGN.md`
**Atlas task:** Attach a disposable Atlas local volume and reject a second writer or wrong-node placement in tests.
**Boundary and review gate:** Do not portray RWO as distributed fencing; no replicated stateful-service promise; cleanup requires explicit data retention choices.
**Original prompt associations:** 75, 76. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/32-local-volumes-claims-and-workload-topology.md`; answers `manuscript/solutions/ch32.md`; claims `validation/evidence/ch32.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 33. Extension Interfaces and a Plugin Roadmap

**Problem:** Read existing side-effect interfaces and design external RPC plugin lifecycle without inventing a plugin implementation.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, architect.
**Outcomes:** Identify present runtime, secrets, metrics, and notification seams.; Design versioned handshake and capability negotiation.; Analyze least privilege, cancellation, crash isolation, and idempotency.
**Exact source targets:** `docs/PLUGIN_SYSTEM_DESIGN.md`, `internal/docker/docker.go`, `internal/secrets/envelope.go`, `internal/notifications/notifications.go`, `internal/autoscaler/autoscaler.go`
**Atlas task:** Create an Atlas adapter contract exercise and label the external RPC protocol as a design proposal.
**Boundary and review gate:** Separate existing interfaces from design-only supervisors and RPC; no arbitrary code-loading sample; contract pseudocode is clearly labeled and not presented as upstream source.
**Original prompt associations:** 79. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/33-extension-interfaces-and-a-plugin-roadmap.md`; answers `manuscript/solutions/ch33.md`; claims `validation/evidence/ch33.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 34. Leader Election and the Durable HA Boundary

**Problem:** Study lease interfaces, PostgreSQL advisory locks, leadership cancellation, and the default server integration gap.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Explain per-controller leadership versus API availability.; Trace lease loss to controller cancellation.; Evaluate PostgreSQL connection and dual-primary failure assumptions.
**Exact source targets:** `internal/leadership/leadership.go`, `internal/leadership/leadership_test.go`, `internal/leadership/postgres.go`, `docs/HA_CONTROL_PLANE_DESIGN.md`, `cmd/orch-server/main.go`
**Atlas task:** Run deterministic competing-leader tests and draft a separate durable-server wiring ADR for Atlas.
**Boundary and review gate:** Do not launch multiple default MemoryService servers as HA; advisory lock packages do not imply production wiring; include partition and leadership loss scenarios.
**Original prompt associations:** 56, 57. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/34-leader-election-and-the-durable-ha-boundary.md`; answers `manuscript/solutions/ch34.md`; claims `validation/evidence/ch34.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 35. Upgrades, Migrations, Maintenance, and Retention

**Problem:** Read version compatibility, safe migration locks, down guards, maintenance windows, and bounded retention.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Read current server, agent, API, and schema compatibility ranges.; Explain migration checks and guarded rollback.; Apply maintenance and retention policies with preservation boundaries.
**Exact source targets:** `internal/version/version.go`, `internal/version/version_test.go`, `internal/migrations/manager.go`, `internal/migrations/manager_test.go`, `internal/maintenance/maintenance.go`, `internal/controlplane/operations.go`, `docs/UPGRADES.md`, `docs/MIGRATIONS.md`
**Atlas task:** Perform a disposable Atlas migration-status and upgrade-preflight exercise, then dry-run retention.
**Boundary and review gate:** All schema ranges are pinned to source version; show ORCH_SCHEMA_CHECK enablement from main.go instead of implying unconditional checks; never test down migrations on real data.
**Original prompt associations:** 81, 82, 83, 84. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/35-upgrades-migrations-maintenance-and-retention.md`; answers `manuscript/solutions/ch35.md`; claims `validation/evidence/ch35.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 36. Fakes, Property Tests, Fuzzing, and Contracts

**Problem:** Use existing deterministic fakes, seeded scheduler properties, fuzz targets, and E2E tests as executable specifications.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition)
**Reader paths:** developer, devops, architect.
**Outcomes:** Select the smallest test boundary that proves an invariant.; Reproduce a seeded property failure.; Preserve fuzz findings as minimal regression cases.
**Exact source targets:** `internal/docker/fake.go`, `internal/e2e/orchestrator_test.go`, `internal/scheduler/property_test.go`, `internal/api/fuzz_test.go`, `internal/cli/fuzz_test.go`, `pkg/types/fuzz_test.go`, `docs/TESTING.md`
**Atlas task:** Add book-side exercises for duplicate placement, parser panic resistance, and repeated convergence.
**Boundary and review gate:** No mirrored tests that simply restate implementation; fuzz duration and manual CI policy are explicit; skipped integration tests are recorded rather than counted as passed.
**Original prompt associations:** 22, 33, 86, 87. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/36-fakes-property-tests-fuzzing-and-contracts.md`; answers `manuscript/solutions/ch36.md`; claims `validation/evidence/ch36.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 37. Failure Injection and Recovery Evidence

**Problem:** Turn failure-mode hardening and chaos scenarios into bounded recovery investigations.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Define an invariant before injecting a fault.; Distinguish timeout, runtime failure, node loss, and partition.; Measure convergence and identify unsupported recovery guarantees.
**Exact source targets:** `internal/e2e/chaos_test.go`, `internal/docker/fake.go`, `docs/CHAOS_TESTING.md`, `docs/RELIABILITY.md`, `prompts/25-failure-modes-hardening.md`, `prompts/26-senior-distributed-systems-review.md`
**Atlas task:** Run Atlas failure drills with fake runtime faults and optional local process interruption.
**Boundary and review gate:** Every drill specifies fault, expected behavior, observations, recovery, and cleanup; do not mistake fake-system success for distributed production resilience.
**Original prompt associations:** 25, 26, 59. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/37-failure-injection-and-recovery-evidence.md`; answers `manuscript/solutions/ch37.md`; claims `validation/evidence/ch37.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 38. Metrics, Dashboards, and Actionable Signals

**Problem:** Trace Prometheus instruments, cardinality, alert rules, dashboard panels, and links to operator actions.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Map an emitted metric to a subsystem and failure mode.; Explain counters, gauges, labels, and cardinality cost.; Connect an alert to a concrete investigation.
**Exact source targets:** `internal/metrics/prometheus.go`, `internal/metrics/prometheus_test.go`, `internal/docker/metrics.go`, `deploy/monitoring/prometheus-rules.yaml`, `deploy/monitoring/prometheus.yml`, `deploy/monitoring/grafana/orchestrator-dashboard.json`, `docs/OBSERVABILITY.md`
**Atlas task:** Inspect Atlas metrics and validate one real alert expression and dashboard query against emitted metric names.
**Boundary and review gate:** Metric names and PromQL are copied from pinned source; dashboard mismatches are reported; no invented SLO, recording rule, or benchmark chart.
**Original prompt associations:** 20, 46, 47, 48. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/38-metrics-dashboards-and-actionable-signals.md`; answers `manuscript/solutions/ch38.md`; claims `validation/evidence/ch38.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 39. Performance and Scale Tests That Say What They Measure

**Problem:** Read fake-agent load tests, scheduler/API benchmarks, pprof controls, and large-service stress scenarios.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Separate fake control-plane throughput from real Docker capacity.; Record hardware, commit, seed, flags, and measurement uncertainty.; Profile only on protected debug surfaces.
**Exact source targets:** `cmd/orch-loadtest/main.go`, `cmd/orch-loadtest/scale_test.go`, `internal/scheduler/benchmark_test.go`, `internal/controlplane/benchmark_test.go`, `internal/api/benchmark_test.go`, `internal/api/debug.go`, `docs/LOAD_TESTING.md`, `docs/PERFORMANCE.md`, `docs/SCALE_TESTING.md`
**Atlas task:** Run a bounded Atlas benchmark and create a measured-results template without fabricated data.
**Boundary and review gate:** A 1,000-service fake-agent scenario is not a production capacity claim; pprof exposure controls are source-checked; all numbers are measured or explicitly hypothetical.
**Original prompt associations:** 58, 88, 89. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/39-performance-and-scale-tests-that-say-what-they-measure.md`; answers `manuscript/solutions/ch39.md`; claims `validation/evidence/ch39.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

### 40. Release a System You Can Honestly Operate

**Problem:** Bring together reproducible release checks, deployment manifests, recovery drills, readiness limits, and an evidence-based production backlog.
**Prior knowledge:** 04 (domain/lifecycle definitions); 06 (actual memory composition); 12–13 (runtime identity and reports)
**Reader paths:** developer, devops, architect.
**Outcomes:** Verify build/test/lint/release contracts and distinguish skipped checks.; Explain what PostgreSQL backup does and does not restore for default MemoryService.; Produce a source-grounded readiness review and next-step ADRs.
**Exact source targets:** `.github/workflows/ci.yml`, `Makefile`, `CHANGELOG.md`, `RELEASE_NOTES.md`, `docs/PRODUCTION_DEPLOYMENT.md`, `docs/BACKUP_RESTORE.md`, `deployments/production/docker-compose.yml`, `deployments/production/systemd/orch-server.service`, `deployments/production/systemd/orch-agent.service`, `scripts/backup-db.sh`, `scripts/restore-db.sh`
**Atlas task:** Assemble Atlas evidence: tested lab, unresolved gaps, backup drill, compatibility preflight, and publication-ready case study.
**Boundary and review gate:** Final checklist cannot override MemoryService, missing HA/autoscaler wiring, mTLS, and networking gaps; title/subtitle and product copy never claim production readiness.
**Original prompt associations:** 23, 27, 28, 49, 50, 60, 90. Associations are topical implementation history, not literal prompt-execution transcripts.
**Chapter output:** `manuscript/chapters/40-release-a-system-you-can-honestly-operate.md`; answers `manuscript/solutions/ch40.md`; claims `validation/evidence/ch40.json`.
**Evidence requirement:** focused unchanged source excerpts with pinned line anchors; actual test symbol inspected; source/result distinction; motivating failure timeline; 3–5 progressive exercises with separately worked answers. A package fixture cannot establish distributed runtime behavior. Narrative budget 2,100 words.

## Appendices and deferred scope

### Appendix A — CLI, API, and Configuration Reference
**Problem:** Produce a source-derived command, route, field and configuration reference.
**Exact sources:** `docs/CLI.md`, `docs/API.md`, `docs/CONFIGURATION.md`, `api/openapi.yaml`
**Practical task:** Reset a disposable Atlas lab without deleting unrelated Docker data.
**Limit:** Every cleanup command is scoped; source version, architecture, Docker availability, and skipped checks are recorded.
**Output:** `manuscript/appendices/a-cli-api-config.md`; budget 1,300 meaningful words.

### Appendix B — Lifecycle States and Invariant Reference
**Problem:** Define lifecycle states, transitions, ownership and concurrency invariants.
**Exact sources:** `pkg/types/lifecycle.go`, `docs/STATE_MACHINES.md`, `internal/task/task.go`, `internal/controlplane/controlplane.go`
**Practical task:** Validate all executable Atlas manifests.
**Limit:** Defaults and supported spellings come from current source; reference examples include both success and rejection.
**Output:** `manuscript/appendices/b-lifecycle-invariants.md`; budget 1,300 meaningful words.

### Appendix C — Commit Atlas and Original Prompt Crosswalk
**Problem:** Explain the 91 original prompts and real implementation associations across 105 commits.
**Exact sources:** `prompts/EXECUTION_TRACKER.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`
**Practical task:** Open immutable commit and blob links from the evidence ledger.
**Limit:** Full commit SHA and file anchors only; prompt completion is intent evidence rather than proof; unmapped items remain visible.
**Output:** `manuscript/appendices/c-annotated-history.md`; budget 1,300 meaningful words.

### Appendix D — Worked Exercises and Design Solutions
**Problem:** Collect tested and source-justified answers keyed to chapters and labs.
**Exact sources:** `internal/scheduler/scheduler_test.go`, `internal/reconciler/reconciler_test.go`, `internal/e2e/chaos_test.go`
**Practical task:** Write Atlas ADRs for durable store wiring, leadership, and networking.
**Limit:** Do not attribute general distributed-systems guarantees to orch without code and test proof.
**Output:** `manuscript/appendices/d-exercises-solutions.md`; budget 1,300 meaningful words.

### Appendix E — Operator Runbooks and Measurement Contracts
**Problem:** Provide observable triage, backup boundary, migration, maintenance and measurement procedures.
**Exact sources:** `docs/OPERATIONS.md`, `docs/BACKUP_RESTORE.md`, `docs/MIGRATIONS.md`, `docs/OBSERVABILITY.md`
**Practical task:** Complete one Atlas incident worksheet and restore drill.
**Limit:** No production runbook suggests restart-safe default control-plane state; irreversible down/restore operations require explicit disposable lab boundaries.
**Output:** `manuscript/appendices/e-ops-measurement.md`; budget 1,300 meaningful words.

### Appendix F — Glossary, Bibliography, and Boundary Index
**Problem:** Define technical terms and primary references; link the capability/extension backlog.
**Exact sources:** `docs/ARCHITECTURE.md`, `docs/HA_CONTROL_PLANE_DESIGN.md`, `docs/PLUGIN_SYSTEM_DESIGN.md`, `docs/NETWORKING_DESIGN.md`
**Practical task:** Prioritize Atlas extension ADRs by risk and prerequisites.
**Limit:** Use pinned code as authority when docs conflict; all extensions are proposals and no hidden patch to orch is implied.
**Output:** `manuscript/appendices/f-glossary-bibliography.md`; budget 1,300 meaningful words.

Durable domain service, active HA/autoscaler composition, network overlays, runtime plugins, signing/scanning enforcement, replicated storage and complete host tenancy are intentionally not implemented as hidden application changes. Where source is design-only, teach the decision and missing mechanism. Proposals become separately tested teaching extensions. No future API or changed baseline is silently substituted.

## Cross-reference contract

Use stable chapter filenames from Book.txt; no invented unnumbered section joins the native47 sectionspine. The public adapter must safely resolve nested chapter/appendix paths without escapes or duplicate stems. Draft cross-references target the frozen IDs, and release link checks require all targets exist. The future unified edition must match Book.txt exactly.
