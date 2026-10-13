# Capability ledger

Pinned snapshot `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. Stable CAP IDs are editorial controls, not production certifications. The JSON twin records source lines and an experiment for each boundary. Every source citation below is pinned to the full immutable SHA. Source inspection is complete for these paths; experiments are **unrun in this ledger** and must be joined to actual validation records before claiming observed results.

## CAP-001 — Active persistence

**runtime-integrated**. Default server constructs NewMemoryService, whose constructor allocates process-local maps.

Boundary: DatabaseURL plus migrations/schema check does not persist these maps.

Evidence: [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146); [internal/controlplane/controlplane.go:279](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L279); [cmd/orch-server/main.go:107](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L107).

Resolving experiment: Create namespace on own loopback server, terminate process, restart and compare list; record database configuration independently.

Chapter attention: 1, 2, 6, 9, 10, 35. source-derived boundary; no runtime outcome asserted

## CAP-002 — PostgreSQL store

**implemented package**. pgx-backed core stores and transactions exist; guarded task assignment checks expected timestamp and pending state.

Boundary: No normal server constructor injects this store; Store excludes additional workload interfaces and task SQL omits JobID/Command/VolumeMounts.

Evidence: [internal/store/postgres.go:38](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L38); [internal/store/postgres.go:892](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L892); [internal/store/postgres.go:1461](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L1461); [internal/store/store.go:111](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/store.go#L111).

Resolving experiment: Run store integration tests on isolated resettable PostgreSQL, then design separate durable-service parity/process-restart test.

Chapter attention: 9, 10, 11, 31, 35. source-derived boundary; no runtime outcome asserted

## CAP-003 — Immediate service placement

**runtime-integrated**. MemoryService immediately chooses ready, volume-eligible nodes by len(active)%len(eligibleNodes) and stores TaskAssigned.

Boundary: This path bypasses Plan CPU/memory and placement-label filtering; port helper differs from planner. Do not attribute planner guarantees to ordinary service create.

Evidence: [internal/controlplane/controlplane.go:2249](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2249); [internal/controlplane/controlplane.go:2292](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2292); [internal/controlplane/controlplane.go:2299](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2299).

Resolving experiment: Create service requesting impossible resources/labels against ready fixture node; compare direct Plan output.

Chapter attention: 5, 6, 12, 13, 19. source-derived boundary; no runtime outcome asserted

## CAP-004 — Scheduler planning and claims

**partial integration**. One-second server scheduler calls RunOnce; pure Plan filters ready nodes, labels, request capacity, volume eligibility and ports, then deterministic scores.

Boundary: Most ordinary service tasks are already assigned; independent planning snapshots are not a globally serialized capacity/port reservation.

Evidence: [cmd/orch-server/main.go:177](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L177); [internal/scheduler/scheduler.go:270](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L270); [internal/scheduler/scheduler.go:170](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L170); [internal/scheduler/scheduler.go:424](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L424).

Resolving experiment: Run pure fixtures/properties and two-claimer PostgreSQL test separately; distinguish algorithm, one-task claim and global reservations.

Chapter attention: 12, 13, 14, 31. source-derived boundary; no runtime outcome asserted

## CAP-005 — Standalone reconciler

**implemented package**. Creates pending tasks, handles version/count/delete/restart policy, can wrap write/event mutations in store.WithTx.

Boundary: Server uses immediate MemoryService reconciliation and never constructs this Reconciler; default LeaderLock is NoopLeaderLock.

Evidence: [internal/reconciler/reconciler.go:58](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L58); [internal/reconciler/reconciler.go:293](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L293); [internal/reconciler/reconciler.go:266](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L266); [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146).

Resolving experiment: Run fake-store repeated passes; separately inspect server process call graph.

Chapter attention: 14, 15, 16. source-derived boundary; no runtime outcome asserted

## CAP-006 — Resource enforcement

**partial integration**. Adapter can set Docker HostConfig.Memory and NanoCPUs from ContainerSpec.Resources.

Boundary: AgentTask lacks resource member and ensureTask omits Resources from its ContainerSpec literal. Admission/normalization/planning are not active cgroup enforcement.

Evidence: [internal/controlplane/controlplane.go:130](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L130); [internal/agent/agent.go:253](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253); [internal/docker/docker.go:436](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L436).

Resolving experiment: Inspect actual Docker HostConfig for ordinary deployment versus direct adapter fixture; no inferred limits.

Chapter attention: 5, 7, 12, 24, 40. source-derived boundary; no runtime outcome asserted

## CAP-007 — Lifecycle and operation guards

**runtime-integrated**. Shared desired/actual transition checks, terminal-state restrictions and service operation conflicts protect supported mutations.

Boundary: Guards do not make independent server memories share state or establish remote side-effect fencing.

Evidence: [pkg/types/lifecycle.go:136](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L136); [pkg/types/lifecycle.go:304](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go#L304); [internal/controlplane/controlplane.go:2697](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2697).

Resolving experiment: Run table-driven lifecycle and concurrent service-operation tests; process topology remains separate.

Chapter attention: 4, 15, 16, 17, 18. source-derived boundary; no runtime outcome asserted

## CAP-008 — Rollouts and rollback

**runtime-integrated**. Startup constructs rollout controller; asynchronous deployment progression waits for target availability and chooses prior successful service spec for rollback.

Boundary: Memory-preserving controller restart test is not process restart or database recovery; image history is logical desired spec.

Evidence: [cmd/orch-server/main.go:219](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L219); [internal/controlplane/controlplane.go:1659](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L1659); [internal/e2e/chaos_test.go:41](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L41).

Resolving experiment: Record same-instance controller restart and separate real process restart as different experiments.

Chapter attention: 16, 17, 18. source-derived boundary; no runtime outcome asserted

## CAP-009 — Heartbeat/offline/drain

**runtime-integrated**. Startup constructs node monitor; MemoryService records node_lost and conservatively replaces stateless workloads; drain waits for replacement availability.

Boundary: Offline means missing heartbeat, not proof old containers stopped. Stateful-volume tasks stay for manual recovery; no physical fencing.

Evidence: [cmd/orch-server/main.go:225](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L225); [internal/controlplane/controlplane.go:669](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L669); [internal/controlplane/controlplane.go:2073](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2073); [internal/controlplane/controlplane.go:2343](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2343).

Resolving experiment: Isolate own two-node fake/real workload; stop heartbeat while old endpoint keeps responding and record stale-report handling.

Chapter attention: 7, 19, 20, 40. source-derived boundary; no runtime outcome asserted

## CAP-010 — Agent runtime adoption

**runtime-integrated**. Agent finds managed containers by task/node/version metadata and reuses/adopts them; unassigned managed containers are cleaned.

Boundary: Adoption metadata is narrower than full spec equivalence; retries lack permanent/transient taxonomy; connectivity retry can hold polling.

Evidence: [internal/agent/agent.go:357](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L357); [internal/agent/agent.go:604](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L604); [internal/docker/docker.go:191](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L191).

Resolving experiment: Inject report loss after create with FakeRuntime, then dedicated Docker test; record managed labels and duplicate count.

Chapter attention: 7, 20, 32. source-derived boundary; no runtime outcome asserted

## CAP-011 — HA leadership

**implemented package**. Local/PostgreSQL electors and RunWithLeadership wrapper implement lease/cancellation seams.

Boundary: No server loop uses wrapper. Two default servers are independent memories. Session lock return-to-pool cleanup requires real PostgreSQL verification.

Evidence: [internal/leadership/leadership.go:35](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go#L35); [internal/leadership/postgres.go:81](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L81); [internal/leadership/postgres.go:105](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L105).

Resolving experiment: Acquire with session A, cancel parent, attempt with session B and inspect pg_locks; test normal release and failed unlock separately.

Chapter attention: 21, 22, 36. Potential pooled-session advisory-lock cleanup defect is a hypothesis from cancellation→close→pool release; not an observed outage.

## CAP-012 — Autoscaling

**implemented package**. Controller uses MetricsProvider, recommendation/min/max/cooldown and existing ScaleService path; fake provider exists.

Boundary: Not constructed in server; no production Prometheus provider or enabled runtime autoscaling inferred.

Evidence: [internal/autoscaler/autoscaler.go:78](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L78); [internal/autoscaler/autoscaler.go:142](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L142); [internal/autoscaler/autoscaler.go:230](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L230).

Resolving experiment: Run injected-metric clock tests; verify server composition independently.

Chapter attention: 23, 36, 40. source-derived boundary; no runtime outcome asserted

## CAP-013 — User auth and namespaces

**runtime-integrated**. API supports HS256 JWT roles and namespace roles, namespace-scoped service operations and static-user override.

Boundary: Empty JWT secret disables user authentication; exp is checked only if positive. Logical namespaces do not provide network/kernel tenant isolation.

Evidence: [internal/api/api.go:1259](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1259); [internal/auth/auth.go:82](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/auth.go#L82); [internal/auth/auth.go:126](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/auth.go#L126); [internal/namespace/context.go:32](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go#L32).

Resolving experiment: Test missing/expired/optional-exp tokens and cross-namespace API permissions; protect all listeners externally.

Chapter attention: 24, 25, 26. source-derived boundary; no runtime outcome asserted

## CAP-014 — Agent credentials

**runtime-integrated**. Registration/heartbeat issue short-lived credentials, hash stored token material and support revocation.

Boundary: Bootstrap auth optional with empty token; server-to-agent logs use bootstrap token; native HTTP is not mTLS.

Evidence: [internal/auth/agent.go:36](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go#L36); [internal/api/api.go:570](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L570); [internal/api/api.go:1249](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1249); [cmd/orch-agent/main.go:90](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-agent/main.go#L90).

Resolving experiment: Run issuance/expiry/revocation and log access tests; do not claim mTLS integration.

Chapter attention: 7, 24. source-derived boundary; no runtime outcome asserted

## CAP-015 — Secrets and registry auth

**runtime-integrated**. Local AES-GCM envelope encrypts stored values; metadata endpoints exclude plaintext; assigned agents receive needed env/pull credentials.

Boundary: Local key derivation is not KMS rotation. Docker/node admins can read injected env. Default state still vanishes on server restart.

Evidence: [internal/secrets/envelope.go:47](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L47); [internal/secrets/envelope.go:99](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L99); [internal/controlplane/controlplane.go:821](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L821); [internal/controlplane/controlplane.go:854](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L854).

Resolving experiment: Run wrong-key/tamper and metadata-vs-agent tests; capture only redacted synthetic credentials.

Chapter attention: 24, 27, 28. source-derived boundary; no runtime outcome asserted

## CAP-016 — Admission and container security

**runtime-integrated**. Service admission uses cluster policy; propagated security context reaches Docker adapter for user/rootfs/capabilities/host options.

Boundary: Policy acceptance says nothing about resource-limit propagation. Privileged allowances and host mounts require own threat model; no universal non-root image guarantee.

Evidence: [internal/admission/admission.go:71](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission.go#L71); [internal/policy/policy.go:34](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/policy/policy.go#L34); [internal/agent/agent.go:314](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L314); [internal/docker/docker.go:438](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L438).

Resolving experiment: Test denied/allowed policy fields and inspect HostConfig separately.

Chapter attention: 5, 24, 25. source-derived boundary; no runtime outcome asserted

## CAP-017 — Namespace quotas

**runtime-integrated**. Memory mutations account requests/replicas/services/ports/secrets/registry entries under one mutex; PostgreSQL path serializes namespace quota checks.

Boundary: Accounting is requested allocation rather than measured usage; memory-process atomicity differs from shared-DB transactional path and unused durable server composition.

Evidence: [internal/controlplane/controlplane.go:2153](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2153); [internal/store/postgres.go:149](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L149); [internal/store/postgres.go:154](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go#L154).

Resolving experiment: Race concurrent memory scales; separately execute DB quota/store transactions with resettable database.

Chapter attention: 10, 11, 26, 37. source-derived boundary; no runtime outcome asserted

## CAP-018 — Image identity

**partial integration**. Parser records supplied registry/name/tag/digest; explicit digest reference can be pinned and admission rejects mutable references when policy requires.

Boundary: ParserResolver performs parsing, not network tag-to-digest resolution. Mutable tag receives no independently fetched digest.

Evidence: [internal/image/reference.go:20](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go#L20); [internal/image/reference.go:78](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go#L78); [internal/controlplane/controlplane.go:303](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L303).

Resolving experiment: Compare supplied digest to mutable reference in parser and end-to-end payload; registry-resolution extension requires new tested Resolver.

Chapter attention: 5, 28, 29. source-derived boundary; no runtime outcome asserted

## CAP-019 — GitOps sync

**runtime-integrated**. Startup controller clones via exec.CommandContext, parses sorted manifests, applies sequentially, records revision/ownership and optionally prunes.

Boundary: Not atomic across manifests; no signed commit enforcement or private credential provider. Lexical path checks are not a proven symlink sandbox.

Evidence: [cmd/orch-server/main.go:165](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L165); [internal/gitops/gitops.go:65](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L65); [internal/gitops/gitops.go:198](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L198); [internal/gitops/gitops.go:300](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L300).

Resolving experiment: Temporary local repo with first valid and second bad manifest, prune and adversarial symlink path fixture.

Chapter attention: 29, 30, 40. Symlink escape is an unresolved filesystem threat-model hypothesis until adversarial fixture executed.

## CAP-020 — GitOps drift

**runtime-integrated**. MemoryService.GitOpsStatus compares live desired specs and can auto-revert while status is read.

Boundary: Status GET can mutate state; periodic Git sync reapply is a different path. No all-service transaction.

Evidence: [internal/controlplane/workloads.go:64](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L64); [internal/gitops/gitops.go:174](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L174).

Resolving experiment: Manual scale then status under warn/auto-revert and compare mutations/events.

Chapter attention: 30. source-derived boundary; no runtime outcome asserted

## CAP-021 — Jobs

**runtime-integrated**. MemoryService creates pending job tasks; scheduler synthesizes service view; agent sends command/exit report; retries use new task IDs.

Boundary: retryOrFailJobLocked retries immediately, not timed exponential backoff. Additional service env/auth/security envelope is absent on job ListAssignedTasks branch.

Evidence: [internal/controlplane/workloads.go:116](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L116); [internal/controlplane/workloads.go:217](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L217); [internal/scheduler/scheduler.go:340](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L340); [internal/controlplane/controlplane.go:780](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L780).

Resolving experiment: Run success/failure/retry/delete fixtures; record attempts and timestamps; inspect job payload separately.

Chapter attention: 31. source-derived boundary; no runtime outcome asserted

## CAP-022 — Cron jobs

**runtime-integrated**. Startup cron controller uses clock abstraction, five-field parser, timezone, concurrency policy and missed-run limits.

Boundary: Day-of-month AND day-of-week, bounded 366-day next search; loop returns on pass error and startup only logs stop. Verify namespace traversal before universal claims.

Evidence: [cmd/orch-server/main.go:171](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L171); [internal/cronjobs/cronjobs.go:194](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go#L194); [internal/cronjobs/cronjobs.go:205](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go#L205); [internal/cronjobs/cronjobs.go:40](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go#L40).

Resolving experiment: Inject clock for AND/next-year boundary, Forbid/Replace/Allow and per-namespace traversal.

Chapter attention: 31, 32. source-derived boundary; no runtime outcome asserted

## CAP-023 — Local volumes

**runtime-integrated**. Volume/claim/attachment records constrain node and single-writer eligibility; agent sends Docker named volume mounts.

Boundary: Local Docker volume is not replicated storage; safe automated stateful identity/order/recovery remains design only. Memory attachment ownership is not physical fencing.

Evidence: [internal/controlplane/workloads.go:488](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L488); [internal/controlplane/workloads.go:512](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L512); [internal/agent/agent.go:287](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L287); [internal/docker/docker.go:453](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L453).

Resolving experiment: Dedicated named volume write/read, incompatible node/second-writer fixture, cleanup only owned volumes.

Chapter attention: 19, 32, 33. source-derived boundary; no runtime outcome asserted

## CAP-024 — Discovery, DNS and Traefik

**runtime-integrated**. API derives healthy endpoints and Traefik config; optional ORCH_DNS_ADDR starts UDP DNS in server with configured TTL.

Boundary: Host-port discovery is not overlay/CNI/network policy, and external reverse proxy remains separate process.

Evidence: [internal/api/api.go:1165](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1165); [cmd/orch-server/main.go:149](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L149); [internal/dns/server.go:47](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server.go#L47); [internal/traefik/config.go:46](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L46).

Resolving experiment: Run endpoint filters/config fixtures plus own loopback UDP DNS; container routing requires own isolated network lab.

Chapter attention: 33, 34. source-derived boundary; no runtime outcome asserted

## CAP-025 — Notifications

**runtime-integrated**. MemoryService dispatcher uses webhook HTTP sender, retries/backoff, optional HMAC and redaction.

Boundary: No durable queue or encrypted sink persistence established; arbitrary outbound target URLs need separate network threat model.

Evidence: [cmd/orch-server/main.go:147](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L147); [internal/notifications/notifications.go:77](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go#L77); [internal/controlplane/workloads.go:524](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go#L524).

Resolving experiment: httptest signed delivery/retry/redaction plus explicitly scoped prohibited-network cases.

Chapter attention: 34, 38. Outbound-network abuse risk is source-derived hypothesis, not proof all URLs are exploitable.

## CAP-026 — Upgrade and migrations

**runtime-integrated**. Registration/heartbeat check agent ranges; opt-in startup schema guard and explicit migration subcommands use manager locking/version transactions.

Boundary: Schema check is opt-in; compatibility constants and version warning do not prove rolling upgrades or shared durable runtime.

Evidence: [internal/version/version.go:12](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/version/version.go#L12); [internal/controlplane/controlplane.go:544](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L544); [cmd/orch-server/main.go:107](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L107); [internal/migrations/manager.go:138](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go#L138).

Resolving experiment: Run compatibility fixtures and all 16 migrations up/status/down on isolated DB; test mixed-version binaries separately.

Chapter attention: 35. source-derived boundary; no runtime outcome asserted

## CAP-027 — Retention

**runtime-integrated**. Daily startup loop calls memory pruning; API supports dry run; active/unresolved task history is protected by explicit predicates.

Boundary: Prunes memory maps/slices, not an integrated durable retention service; requested targets must be checked one by one.

Evidence: [cmd/orch-server/main.go:206](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L206); [internal/controlplane/operations.go:26](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L26); [internal/controlplane/operations.go:102](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L102).

Resolving experiment: Fixed-clock dry-run and preservation tests; compare every target, not just aggregate count.

Chapter attention: 35, 38. source-derived boundary; no runtime outcome asserted

## CAP-028 — Usage/export and billing

**runtime-integrated**. Minute startup snapshots record requested resource/replica/service/task-runtime/port/storage-claim aggregates and report/CSV surfaces.

Boundary: Requested allocation snapshots are not measured cgroup consumption or financial-grade accounting. Payments/invoicing are future work.

Evidence: [cmd/orch-server/main.go:195](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L195); [internal/controlplane/operations.go:116](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L116); [internal/controlplane/operations.go:158](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go#L158).

Resolving experiment: Fixed-clock known allocation and CSV fixture; never infer currency or actual CPU usage.

Chapter attention: 37. source-derived boundary; no runtime outcome asserted

## CAP-029 — Events, audits, metrics, profiling

**runtime-integrated**. Default events/audits remain memory-backed; request/scheduler/rollout/node/agent metrics use injected instruments; optional debug listener serves pprof.

Boundary: Standalone reconciler metrics are not live if no reconciler loop. Audit append best effort; metrics exempt user JWT; debug listener unauthenticated and configurable.

Evidence: [internal/api/api.go:1255](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1255); [internal/api/api.go:1199](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1199); [cmd/orch-server/main.go:126](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L126); [internal/api/debug.go:8](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/debug.go#L8).

Resolving experiment: Inspect actual /metrics series/auth and default-disabled debug endpoint; prove event atomicity separately with DB transaction.

Chapter attention: 10, 11, 24, 38, 39. source-derived boundary; no runtime outcome asserted

## CAP-030 — Signing, scanning, CNI, plugins, stateful orchestration

**design only**. Dedicated design documents describe future signing/trust, SBOM/scans, overlay networking, plugin ABI and stateful identity/order/recovery.

Boundary: No default implementation/enforcement or production outcome follows from design presence.

Evidence: [docs/IMAGE_SIGNING_DESIGN.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/IMAGE_SIGNING_DESIGN.md#L1); [docs/SUPPLY_CHAIN_SECURITY_DESIGN.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SUPPLY_CHAIN_SECURITY_DESIGN.md#L1); [docs/NETWORKING_DESIGN.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NETWORKING_DESIGN.md#L1); [docs/PLUGIN_SYSTEM_DESIGN.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PLUGIN_SYSTEM_DESIGN.md#L1); [docs/STATEFUL_WORKLOADS_DESIGN.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATEFUL_WORKLOADS_DESIGN.md#L1).

Resolving experiment: No experiment can validate unimplemented enforcement; use tested teaching extension and new edition lock if implemented.

Chapter attention: 29, 32, 33, 36, 40. source-derived boundary; no runtime outcome asserted

## Rules for later claims

A chapter cannot promote an implemented package to runtime-integrated because a unit test passes. Runtime integration requires a constructor/call path in the selected binary, state ownership and an observable effect. A teaching extension must live outside evidence/orch with its own tests. Future work remains future until a deliberate source lock update. Unconfirmed risks stay labeled as hypotheses even when the code makes them plausible. Normal passing suites with external skips do not satisfy Docker/PostgreSQL experiments. The source path for lease cancellation warrants a pooled-session experiment; it is not a demonstrated outage. The controller-restart chaos subtest preserves MemoryService and cannot support a process-durability claim.

## Fresh execution finding: original database fixture

Root execution record validation/intake/postgres-store-owned.json reports two guarded PostgreSQL store tests failing with SQLSTATE42703 (missing agent_version). The original fixture applies migrations1–14 while current node queries expect agent_version introduced by migration16 (000016_operations_safety.up.sql:6). This is a demonstrated fixture/schema mismatch, not an invented runtime failure or a source change. Full-schema extension execution is tracked separately; it cannot retroactively turn the original suite green.
