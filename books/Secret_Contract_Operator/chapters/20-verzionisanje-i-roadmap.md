# 20. API Evolution and Open-source Maintenance

## 20.1 Alpha Does Not Mean Arbitrary Changes

`v1alpha1` signals that the API is not yet stable, but does not remove a maintainer's responsibility to users. After a public release, even a small default change can block deployment or trigger a rollout. Every change needs a migration note and a test of the old manifest.

Kubernetes supports multiple served CRD versions and a separate storage version, with conversion rules and migration of stored objects. Simply adding a version to YAML does not automatically migrate all existing data. [S27](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/)

## 20.2 Consolidating the Initial Prompts

| Earlier sketch | This book's canonical decision | Reason |
|---|---|---|
| `secrets.platform.io` | Proposed `secrets.codepop.tech` | Own DNS namespace |
| `injection.enabled` + `managed` | `injection.mode` + installation/grant controls | Less ambiguity |
| `containerName` | `workloadRefs[].containers` | Explicit consumers |
| Global `failIfKeyEmpty` | Per-key `nonEmpty` | No conflicting rules |
| `failIfSecretMissing: false` | Missing Secret cannot be Ready | Clear contract |
| `maxAge: 30d` | `maxAge: 720h` | Supported duration semantics |
| Hash of Secret contents | UID/RV metadata token | No secret fingerprint |
| Unrestricted ESO GVK | Constrained ExternalSecret adapter | Smaller privileged scope |

This is consolidation **before implementation or first publication**, not a guaranteed compatible upgrade of an existing operator. If earlier code already exists, inventory it first, then perform a separate migration with tests and specification backups.

## 20.3 Proposed Development Phases

**Phase A: core.** API, authorized read-only scope, validator, status, Secret watch, and leakage tests. The result must work without ESO and without workload write permissions.

**Phase B: usable MVP.** ESO adapter, workload validation, rotation-age signals without restart, metrics, Helm, CI, and the first public release. A runbook and clear supported-version matrix are required.

**Phase C: controlled automation.** Protected approvals, injection, metadata restart, anti-storm policy, and an E2E rollout matrix. This phase must not weaken default RBAC.

**Phase D: wider ecosystem.** Multiple dependencies per workload, policy-report integrations, additional workload controllers, and optional admission rejection. Every integration must justify its extra complexity and security scope.

## 20.4 Community Contributions

The repository should have `CONTRIBUTING.md`, `SECURITY.md`, a code of conduct, issue templates, and a release process. Confirm the license choice before public publication; this book does not impose a legal conclusion about the best license.

A useful bug report contains the operator version, cluster type, a redacted contract, safe condition output, and reproduction steps using a synthetic Secret. The template explicitly prohibits real values and complete kubeconfigs.

## 20.5 PR Review

For an API change, review defaults, compatibility, and schema. For a validator change, review leakage, determinism, and budgets. For mutation, review authorization, field ownership, concurrency, and rollback boundaries. For observability, review cardinality and metadata privacy.

Do not accept a feature with only a positive demo. Every feature needs a negative case and documented behavior when a dependency disappears. “Works in my namespace” is insufficient for a community operator.

## 20.6 When to Reject a Feature

Reject direct provider fetching unless there is a strong reason to change product boundaries. Reject automatic value repair because the operator does not know the intended credential. Reject cross-namespace copying because it changes authorship and exposure models.

Rejecting a feature is not a lack of ambition. A small operator with clear guarantees is often more maintainable than a platform trying to own the entire secret lifecycle.

**Checkpoint.** Every roadmap item must state what new data the operator reads, what new permission it gains, and what additional incident it could cause.
