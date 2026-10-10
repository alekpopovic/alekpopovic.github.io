# 019 — Kind E2E for the MVP

Phase: B | Complexity: High | Dependency: 018

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 019
Create an isolated kind e2e workflow using a pinned node image and local operator image. Never silently reuse the current user cluster. Require an explicit context and clean up only resources created by the test.
Install CRDs and the actual chart, wait for manager readiness, create synthetic examples, verify contract transitions and confirm validation-only RBAC with the actual ServiceAccount. Restart the manager and verify convergence. Test uninstall without deleting application Secret/workload resources.
Where ESO integration is advertised, add a scenario with an actual supported ESO release and a safe fake/test provider. Do not require real AWS/Vault credentials. Capture redacted status and metadata only; do not archive raw Secret objects.

Acceptance: make e2e has a documented reproducible flow and safe cleanup; results clearly distinguish executed from planned integration scenarios.
```
