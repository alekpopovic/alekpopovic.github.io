# Architectural decision register

Source edition `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. These are reconstructed decisions, not attributed statements of author motivation. **All benefits/cost explanations below are editorial inferences from implementation and design evidence.** Observed behavior is source-inspected unless an execution log is separately linked. Alternatives are proposals, not hidden delivered features.

## D01 — Docker-first runtime

**Context:** A small cluster needs a concrete execution API.

**Observed implementation:** Docker Runtime interface and Engine adapter provide pull/create/start/inspect/stop/remove operations; FakeRuntime serves deterministic tests. [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L47-L67).

**Alternatives:** containerd/CRI adapter or external scheduler. **Inferred benefit:** A narrow inspectable runtime seam. **Inferred cost:** Agent socket access is highly privileged; Docker behavior still needs real integration tests.

**Failure scenario:** Create succeeds but the status response is lost; inspect labels before creating another container. **Boundary/unresolved question:** Adapter coverage does not establish isolation or resource fields from every caller.

**Separate teaching-design plan:** Build a separately tested constrained adapter; compare actual DTO fields and real HostConfig.

## D02 — Polling and reporting agents

**Context:** Workers need assignments and control plane needs observations.

**Observed implementation:** Agent loop fetches assignments, executes runtime actions and reports task/heartbeat state. [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L128-L148).

**Alternatives:** push streams or broker-backed delivery. **Inferred benefit:** Small HTTP protocol and retryable observation loop. **Inferred cost:** A lost report acknowledgement can be retried; stale reports require lifecycle checks.

**Failure scenario:** Partitioned worker can keep serving while a new task is assigned elsewhere. **Boundary/unresolved question:** No worker fencing protocol follows merely from polling.

**Separate teaching-design plan:** Use explicit generations and test stale-report rejection independently.

## D03 — Go packages and injected dependencies

**Context:** Algorithms should be testable without an Engine or database.

**Observed implementation:** Schedulers/controllers accept interfaces; package tests use explicit stores, fake runtime and injected clocks. [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L33-L53).

**Alternatives:** single monolithic loop or remote service per subsystem. **Inferred benefit:** Deterministic code navigation and narrow test fixtures. **Inferred cost:** An implemented package may have no caller in main; test success does not activate it.

**Failure scenario:** A package test passes while a live binary uses a different path. **Boundary/unresolved question:** Callers define actual integration.

**Separate teaching-design plan:** Maintain a constructor/caller ledger alongside package coverage.

## D04 — Memory-backed executable composition

**Context:** Executable construction decides where authoritative state lives.

**Observed implementation:** Default server constructs MemoryService with secret-envelope option and passes it to API/controllers. [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146-L166).

**Alternatives:** PostgresStore-backed application composition. **Inferred benefit:** Simple local process setup. **Inferred cost:** State maps disappear on new process startup; nearby PostgreSQL does not alter this.

**Failure scenario:** Fresh server loses services/node identity while old Docker containers may survive. **Boundary/unresolved question:** No default binary durability or HA claim.

**Separate teaching-design plan:** Design a separate shared-store composition and prove restart behavior with new processes.

## D05 — PostgreSQL transactional store

**Context:** Shared state changes need atomic checks and versions.

**Observed implementation:** Store contains transactional operations and AssignTask with state/version predicates. [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L892-L912).

**Alternatives:** in-memory locks or event-sourced durable journal. **Inferred benefit:** Database atomic update/rejection can be tested independently. **Inferred cost:** Store library remains separate from MemoryService-backed binary; schema fixtures cover differing subsets.

**Failure scenario:** Two operators claim or update the same stale object. **Boundary/unresolved question:** Atomic package behavior is not executable durable state ownership.

**Separate teaching-design plan:** Run guarded throwaway integration tests and wire no application changes in this edition.

## D06 — Desired versus actual lifecycle

**Context:** Intent and observed execution arrive asynchronously.

**Observed implementation:** Task model and transition guards distinguish desired state from allowed agent reports. [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L304-L322).

**Alternatives:** single status field or synchronous deployment RPC. **Inferred benefit:** State writers and illegal resurrection are explicit. **Inferred cost:** Several legal shortcut transitions exist; a simplified diagram is only a subset.

**Failure scenario:** A late running report arrives after desired stopped. **Boundary/unresolved question:** Accepted state reports do not prove physical remote action.

**Separate teaching-design plan:** Record generation/time ownership and test late responses at real HTTP boundaries.

## D07 — Deterministic planning versus active placement

**Context:** Repeatable resource/label/port decisions are useful only on the path used.

**Observed implementation:** Scheduler.Plan computes assignments; MemoryService normal replica reconciliation directly creates assigned tasks. [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L270-L290).

**Alternatives:** call pure planner in all paths or keep independent paths. **Inferred benefit:** Pure planner can be property-tested without side effects. **Inferred cost:** Its resource guarantees cannot be transferred to MemoryService service placement.

**Failure scenario:** A node advertised below requests still receives tasks on the active service path. **Boundary/unresolved question:** Planner correctness is a package guarantee.

**Separate teaching-design plan:** Constrained comparative fixture uses identical service/node intent on both paths.

## D08 — Optimistic concurrency

**Context:** Controllers and operators race on stale snapshots.

**Observed implementation:** Store operations carry expected UpdatedAt/version predicates and distinguish assignment conflicts. [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L1376-L1396).

**Alternatives:** coarse global locking or serial command log. **Inferred benefit:** Rejects stale write attempts where guarded. **Inferred cost:** Every relevant write must participate; timestamps and versions are not a fencing token.

**Failure scenario:** Concurrent rollout and scale read the same old service. **Boundary/unresolved question:** Memory locking and PostgreSQL transactions have different scopes.

**Separate teaching-design plan:** Add two-writer stale-update experiment, record returned errors and surviving state.

## D09 — Request-scoped namespaces

**Context:** Same-name workloads and credentials need scoped lookup.

**Observed implementation:** Namespace selection travels in context/header and scoped collection filters. [internal/namespace/context.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go#L32-L52).

**Alternatives:** one cluster per tenant or separate databases. **Inferred benefit:** Simple repeated namespace keying. **Inferred cost:** Isolation must be traced route by route; authentication alone is insufficient.

**Failure scenario:** Operator selects one namespace but follows an unscoped lookup. **Boundary/unresolved question:** This is application scoping, not network or kernel tenant isolation.

**Separate teaching-design plan:** Create same-name services in distinct test contexts and inspect each exposed API path.

## D10 — Local storage and topology

**Context:** Local data belongs to a particular node.

**Observed implementation:** Volume/claim and attachment models exist; workload placement and agent propagation require separate inspection. [pkg/types/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/workloads.go#L119-L139).

**Alternatives:** shared network storage or stateless service. **Inferred benefit:** Explicit topology and straightforward local fixtures. **Inferred cost:** A claim object does not make disks replicated or automatically attachable elsewhere.

**Failure scenario:** Node loss leaves local data unavailable on replacement node. **Boundary/unresolved question:** No default distributed storage guarantee.

**Separate teaching-design plan:** Separate local directory fixture; test unsupported propagation without user host mounts.

## D11 — Node-scoped published host ports

**Context:** Replicas consume limited transport endpoints.

**Observed implementation:** Service ports and scheduler allocation model node-level published ports; Docker adapter creates port bindings. [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L59-L79).

**Alternatives:** service mesh/virtual IP or externally assigned load balancer. **Inferred benefit:** Direct inspectable connectivity. **Inferred cost:** Fixed ports collide on one node; dynamic port identity changes and bindings may expose all interfaces.

**Failure scenario:** Scale two replicas onto the same fixed published port. **Boundary/unresolved question:** Package reservation is not cluster-wide data-plane routing.

**Separate teaching-design plan:** Test collision with a fake first; use isolated daemon for actual wildcard bindings.

## D12 — Optional ingress configuration

**Context:** External routes need discovered backend endpoints.

**Observed implementation:** Traefik config package builds provider configuration and default server exposes the integration endpoint. [internal/traefik/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L46-L66).

**Alternatives:** manual reverse proxy or no ingress. **Inferred benefit:** Keep proxy data plane separate. **Inferred cost:** Upstream demo insecure dashboard is disposable; overlay design is not implemented networking.

**Failure scenario:** API endpoint is healthy while proxy backend list is stale. **Boundary/unresolved question:** No overlay or tenant network isolation follows.

**Separate teaching-design plan:** Validate generated config and compare endpoint selection; bind demo admin listener to loopback.

## D13 — Interfaces versus plugin roadmap

**Context:** Engine, secret and controller seams allow controlled experiments.

**Observed implementation:** Go interfaces permit compiled adapters; plugin design documentation proposes broader extension behavior. [docs/PLUGIN_SYSTEM_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PLUGIN_SYSTEM_DESIGN.md#L1-L11).

**Alternatives:** dynamic runtime loading or external webhooks. **Inferred benefit:** Small teaching extension can be isolated and tested. **Inferred cost:** A design document or interface is not a functioning plugin distribution system.

**Failure scenario:** An operator expects a configured external plugin to load in main. **Boundary/unresolved question:** Plugin system is design-only where no runtime loader exists.

**Separate teaching-design plan:** Implement teaching adapter under examples, never in immutable source.

## D14 — GitOps apply and bookkeeping

**Context:** Several manifests form one desired change but current operations are sequential.

**Observed implementation:** GitOps controller applies parsed manifests through a control-plane interface and records synchronization/ownership state. [internal/gitops/gitops.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L198-L218).

**Alternatives:** preflight complete batch then transactional commit or best-effort explicit per-file results. **Inferred benefit:** A simple inspectable apply loop. **Inferred cost:** The valid first manifest may remain changed when a later one fails; metadata can lag side effects.

**Failure scenario:** Failed second GitOps manifest after first successfully changes atlas-api. **Boundary/unresolved question:** No atomic multi-manifest guarantee.

**Separate teaching-design plan:** Use dedicated local repo with two files; assert first side effect and recorded LastError.

## D15 — Leases, cancellation and fencing

**Context:** Only one active controller should own shared mutations.

**Observed implementation:** PostgresElector holds a session advisory lock and monitors cancellation; default server does not instantiate it. [internal/leadership/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L21-L41).

**Alternatives:** transaction locks, expiring durable leases with fencing epochs. **Inferred benefit:** An independently testable leader-election package. **Inferred cost:** Cancellation and connection release need real-session review; pool reuse may preserve session lock ownership.

**Failure scenario:** Old controller continues actions while another believes it acquired leadership. **Boundary/unresolved question:** Lease package and default binary HA are separate; mutex tests do not prove DB behavior.

**Separate teaching-design plan:** Two-session test checks cancellation, unlock/reacquire, connection identity and callback shutdown.

## D16 — Admission, quota and enforcement

**Context:** Intent should be rejected before exceeding policy or budget.

**Observed implementation:** Admission validates service requests; quota aggregates desired declared resources. AgentTask lacks resource requirements; adapter limit support is not enough. [internal/admission/admission.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission.go#L48-L68).

**Alternatives:** measure actual utilization only or enforce on every mutation with durable reservation. **Inferred benefit:** Early stable errors and bounded declared intent. **Inferred cost:** Declared accounting can diverge from placement and physical Docker enforcement.

**Failure scenario:** Saturated node accepts intent that declared quota permits, but runtime receives zero limits. **Boundary/unresolved question:** No CPU/memory enforcement without complete field propagation.

**Separate teaching-design plan:** Trace API→service→taskDTO→ContainerSpec→HostConfig, then compare active and direct adapter tests.

## Guarantee budget

Atomic persistence requires a shared wired store and transactional changes, not a database URL. Durable ownership requires stored identity/version and restart semantics. Leases require demonstrable cancellation and session cleanup. Fencing requires the data plane to reject stale ownership; task replacement and a leader mutex do not supply it. Packages can demonstrate deterministic planning, transition rejection, adapter label adoption and transactional guarded writes individually; the executable must be evaluated through its own call graph. No comparison here claims equivalence to every Kubernetes guarantee.
