# 028 — Optional Webhook: ADR and Narrow Prototype

Phase: D | Complexity: High | Dependency: 027

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 028
Evaluate whether any remaining requirement truly needs an admission webhook. Prefer structural schema/CEL for local spec checks. Keep a hard workload gate as a separate optional component, not an implied effect of Ready.
Write an ADR covering scope, failure policy, TLS lifecycle, high availability, API call budget, dry-run, break-glass and dependency cycles. A webhook that only trusts stale Ready does not provide strong freshness. A live Secret read still does not make later Pod startup atomic.
Implement only a narrow prototype if these requirements are satisfied and explicitly approved in project configuration. Otherwise deliver the design and a blocked implementation record. Default installation must remain usable without cert-manager or admission infrastructure.

Acceptance: no broad cluster-wide blocking behavior appears by default; limitations and recovery procedure are tested for any implemented prototype.
```
