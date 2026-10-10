# 009 — Basic Read-only Reconciler

Phase: A | Complexity: High | Dependency: 008

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 009
Implement the first controller using the pure spec/data validators and status builder. Read the contract, authorize the reference before reading Secret data, fetch the same-namespace Secret and record UID/resourceVersion for the actual observation.
Handle deleted contracts, missing Secret, Forbidden, API timeout, invalid spec, invalid data and success as distinct cases. Publish only safe status and bounded events. Use optimistic status patching and recompute on conflict; do not reuse an old desired status against a new generation.
Do not mutate Secrets or workloads. Do not add finalizers or ownerReferences to external objects. Configure event-driven recovery and reasonable transient-error backoff. Ensure an old positive status is not reported as a newly successful check after a failed read.

Acceptance: envtest covers missing/valid/invalid/deleted Secret and observedGeneration; two no-op reconciles cause no further status writes.
```
