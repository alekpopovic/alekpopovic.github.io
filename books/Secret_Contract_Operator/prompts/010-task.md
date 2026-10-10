# 010 — Indexes, Watches, and Namespace Isolation

Phase: A | Complexity: High | Dependency: 009

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 010
Index SecretContract by secretRef.name. Watch non-owned Secret resources and enqueue only dependent contracts in the same namespace. Add workload/dependency index helpers without granting ownership of those resources.
Do not apply GenerationChangedPredicate indiscriminately to Secret updates. Filter primary status-only updates while preserving authorization metadata changes that must trigger reconciliation. Handle delete and recreate using identity metadata, not name alone.
Write event-driven envtest cases without manually invoking Reconcile to cause the expected update. Include two namespaces with identically named Secrets, multiple contracts sharing one Secret, a changed contract reference and index/list failure behavior. Avoid cluster-wide fallback scans and avoid logging event objects.

Acceptance: create/update/delete events reach only correct dependents; no status feedback loop or cross-namespace wakeup bug remains.
```
