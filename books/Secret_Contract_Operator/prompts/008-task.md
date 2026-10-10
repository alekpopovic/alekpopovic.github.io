# 008 — Deterministic Status Builder

Phase: A | Complexity: High | Dependency: 007

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 008
Create a status builder independent of Kubernetes I/O. Encode the exact Ready formula from the book. Unconfigured optional checks are True/NotConfigured; configured checks can be True, False or Unknown. Enforced missing configuration is invalid spec.
Set observedGeneration on every condition, preserve meaningful lastTransitionTime and sort violations/workload results. Clear obsolete findings after recovery. Bound messages and result lists. Never copy upstream ExternalSecret messages or raw errors.
Do not mutate lastCheckedTime on every no-op reconcile. Define an observation key using contract generation, authorized dependency metadata and scheduled evaluation triggers. A status update is necessary only for a relevant new observation or semantic transition. Treat authorization revocation as a new negative result and remove details no longer authorized for publication.

Acceptance: repeated identical observations yield an equal status; transitions, stale generation, error recovery and authorization revocation have direct unit tests.
```
