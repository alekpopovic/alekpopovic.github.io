# Documentation conflicts and how to teach them

Documentation records intent and evolving explanations. Current executable behavior comes from startup and call paths; tests clarify contracts but cannot replace composition. This review leaves every evidence file untouched and retains historical context. Accurate passages in RELIABILITY, EVENTS, SCALE_TESTING and release limitations are useful anchors; do not manufacture contradictions in those passages.

## DOC-001 — stale roadmap

Documentation: [docs/ARCHITECTURE.md:20](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ARCHITECTURE.md#L20). Authority/comparison: [cmd/orch-server/main.go:225](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L225).

Consequence: Reader might omit offline-monitor timing and replacement risks.

Book wording: The roadmap predates the constructed monitor; current startup runs it with configured timeout and interval.

Resolution: resolved by source inspection. Chapter attention: 2, 19.

## DOC-002 — package graph presented as executable graph

Documentation: [docs/ARCHITECTURE.md:106](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ARCHITECTURE.md#L106). Authority/comparison: [internal/controlplane/controlplane.go:2292](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2292).

Consequence: Reader assumes normal service placement obeys Plan fit checks.

Book wording: The generic pending→scheduler lifecycle describes standalone modules. Normal MemoryService service creation instead makes assigned tasks immediately.

Resolution: resolved by source inspection. Chapter attention: 2, 6, 12, 14.

## DOC-003 — conditional storage assumption

Documentation: [docs/RECONCILER.md:27](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md#L27). Authority/comparison: [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146).

Consequence: Controller restart can be confused with process restart durability.

Book wording: Recomputation uses supplied store state. A fresh default server reconstructs empty maps, and standalone reconciler is not started there.

Resolution: resolved by source inspection. Chapter attention: 9, 14, 15.

## DOC-004 — historical review stale after code additions

Documentation: [docs/SECURITY_REVIEW.md:112](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY_REVIEW.md#L112). Authority/comparison: [pkg/types/types.go:219](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L219).

Consequence: Reader misses privileged/host security settings and policy gates.

Book wording: The July review preceded securityContext support. Current policy gates and adapter mappings are the authority for present exposed fields.

Resolution: resolved by source inspection. Chapter attention: 5, 24, 25.

## DOC-005 — package guarantee lacks composition qualifier

Documentation: [docs/RESOURCES.md:35](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RESOURCES.md#L35). Authority/comparison: [internal/controlplane/controlplane.go:2292](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2292).

Consequence: Planner guarantee misapplied to ordinary deployments.

Book wording: Request accounting constrains Plan; the active immediate service path needs its own fit checks before that guarantee can be promoted.

Resolution: resolved by source inspection. Chapter attention: 5, 12, 13.

## DOC-006 — terminology ambiguity

Documentation: [docs/REGISTRIES.md:48](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/REGISTRIES.md#L48). Authority/comparison: [internal/image/reference.go:21](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go#L21).

Consequence: Parsed supplied digest can be mistaken for fetched registry identity.

Book wording: The built-in resolver parses supplied references. Remote registry resolution requires a different configured implementation; mutable tags stay mutable.

Resolution: resolved by source inspection. Chapter attention: 28, 29.

## DOC-007 — test name overstates failure boundary

Documentation: [docs/CHAOS_TESTING.md:10](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CHAOS_TESTING.md#L10). Authority/comparison: [internal/e2e/chaos_test.go:41](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go#L41).

Consequence: Reader falsely infers fresh-process/durable recovery.

Book wording: This subtest reconstructs rollout controller while retaining the same MemoryService; it demonstrates controller resume, not server process durability.

Resolution: resolved by source inspection. Chapter attention: 16, 17, 39.

## DOC-008 — conditional runbook exceeds default wiring

Documentation: [docs/BACKUP_RESTORE.md:67](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md#L67). Authority/comparison: [cmd/orch-server/main.go:146](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L146).

Consequence: Restored tables cannot restore active default server maps.

Book wording: Database restoration applies to persisted store fixtures or a future durable composition. Default server state is not restored by setting DatabaseURL.

Resolution: resolved by source inspection. Chapter attention: 9, 10, 35.

## DOC-009 — session death versus pool return

Documentation: [docs/HA_CONTROL_PLANE_DESIGN.md:102](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/HA_CONTROL_PLANE_DESIGN.md#L102). Authority/comparison: [internal/leadership/postgres.go:105](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go#L105).

Consequence: Cancellation returns connection to pool and may retain session advisory lock.

Book wording: Session termination releases session locks; returning a live pooled session is different. Measure cancellation/reacquisition on real PostgreSQL before claiming cleanup.

Resolution: unresolved hypothesis; planned isolated two-session cancellation/failed-unlock experiment; not a demonstrated outage. Chapter attention: 21, 22.

## DOC-010 — publication assertion outside source evidence

Documentation: [docs/INSTALLATION.md:3](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/INSTALLATION.md#L3). Authority/comparison: [RELEASE_NOTES.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/RELEASE_NOTES.md#L1).

Consequence: Source-only edition could promise nonexistent/unverified assets.

Book wording: The inspected installation guide documents platform archives. This source lock establishes tags and files, not GitHub release publication or download availability.

Resolution: unresolved external release metadata; source archive cannot independently certify release assets. Chapter attention: 3, 35.

## DOC-011 — aspirational project positioning

Documentation: [AGENTS.md:3](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/AGENTS.md#L3). Authority/comparison: [docs/RELIABILITY.md:7](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RELIABILITY.md#L7).

Consequence: Reader could treat intent as reliability certification.

Book wording: orch is a Docker-first engineering project with substantial implemented packages; current default composition remains an in-memory development boundary.

Resolution: resolved by source inspection. Chapter attention: 1, 2, 40.

## DOC-012 — package presence versus enabled loop

Documentation: [docs/AUTOSCALING.md:3](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AUTOSCALING.md#L3). Authority/comparison: [cmd/orch-server/main.go:103](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go#L103).

Consequence: Spec autoscaling flag may seem sufficient to activate a controller.

Book wording: The repository includes an autoscaler package; startup does not construct it or a metrics provider. This chapter teaches the package and explicitly labels integration work.

Resolution: resolved by source inspection. Chapter attention: 23, 36.

Verification:12 conflicts, exact existing pinned paths/lines,10 source-resolved and2 explicitly unresolved. No historical document was silently upgraded into current behavior. No application test executed by this comparison. Next: compatibility assumptions006.

## Fresh execution finding: original database fixture

Root execution record validation/intake/postgres-store-owned.json reports two guarded PostgreSQL store tests failing with SQLSTATE42703 (missing agent_version). The original fixture applies migrations1–14 while current node queries expect agent_version introduced by migration16 (000016_operations_safety.up.sql:6). This is a demonstrated fixture/schema mismatch, not an invented runtime failure or a source change. Full-schema extension execution is tracked separately; it cannot retroactively turn the original suite green.

## DOC-014 — explicit host-port collision boundary

Scheduler.allocatePorts rejects reserved explicit ports; MemoryService immediate assignment reserves explicit ports without rejecting collisions. Do not infer service-path protection from planner tests. Source: [memory helper](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2552-L2573); [planner](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L511-L539). This is a confirmed source/caller difference, not a live Docker port-collision result. Chapters5,6,12,13 retain it.

## DOC-015 — public OpenAPI method omissions

Three registered public GET operations are absent from OpenAPI: discovery/services, discovery/services/{name}, integrations/traefik/config. Internal agent exclusion is intentional and is not a gap. [Router](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L199-L201). Actual static comparison: validation/labs/ch07/openapi-routes.json. This does not claim full OpenAPI semantic validation.

## DOC-016 — numeric zero resource roundtrip

Omitted fields/empty resource objects can default; explicit numeric CPU or memory zero is rejected. Public client CreateService normalizes before serialization, so client and raw HTTP examples differ. [Decoder](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L115-L147); [client normalization](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/client/client.go#L211-L220). Actual comparison: validation/labs/ch07/public-contract-final.json. This is a confirmed conversion boundary, not an upstream fix.

## DOC-017 — source-declared port fuzz target

docs/TESTING.md15 names FuzzParsePortSpec, while pkg/types/fuzz_test.go11 declares FuzzPortSpec. Actual bounded correct-target run: validation/labs/ch36/bounded-port-fuzz.json.

## DOC-018 — desired intent frees counted capacity before physical stop

docs/RESOURCES.md33–35 says capacity remains until actual terminal. lifecycle.go269–275 excludes desired stopped/removed immediately, and rollout.go165–180 can complete while physical stop is pending. Root Lab02 asserts both stopping cases; lab04 captured succeeded with pending_stops=1. This is source/controller accounting, not physical fencing.
