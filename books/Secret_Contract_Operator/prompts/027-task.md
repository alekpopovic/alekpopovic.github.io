# 027 — E2E Matrix for Mutation Features

Phase: C | Complexity: High | Dependency: 026

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 027
Extend kind tests using the actual mutation profile and protected approvals. Verify supported Deployment rollout, unchanged behavior when disabled, revocation, env conflicts, same-name Secret recreation and invalid-rotation suppression.
Add supported StatefulSet/DaemonSet cases only when their implementation is complete. Include OnDelete and partition/paused negative cases. Observe Pod identities and workload rollout status without exec env or printing credentials.
Test simultaneous GitOps-like changes and the operator patch. Ensure restart storms stop when mutation is disabled. Confirm uninstall preserves application resources and documents retained references. Capture only sanitized metadata artifacts.

Acceptance: advertised mutation support is backed by actual e2e evidence; read-only installation remains least privilege; unexecuted scenarios are not labeled passing.
```
