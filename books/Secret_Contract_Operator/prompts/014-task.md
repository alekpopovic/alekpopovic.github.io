# 014 — Time-based Rotation Policy

Phase: B | Complexity: High | Dependency: 013

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 014
Implement maxAge validation without automatic restarts. Parse the configured annotation as RFC3339 using an injected clock. Report missing/invalid/future timestamps and expiration with stable reason codes.
Document that the annotation is a claim by its authorized writer, not proof of credential rotation. Do not use Secret creationTimestamp, resourceVersion or ESO refreshTime as a substitute. Use positive supported duration syntax and a documented clock-skew tolerance.
Schedule reconciliation at the next relevant deadline, so expiration is detected without any object update. Avoid a zero-delay loop after expiry. Apply requireRotationPolicy exactly as documented; advisory failures may leave Ready true while the dedicated condition is false.

Acceptance: fake-clock tests cover boundary times, skew, invalid dates and restart before expiry; the next requeue deadline is deterministic and bounded.
```
