# 029 — Compatibility and Upgrade Tests

Phase: D | Complexity: High | Dependency: 028

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 029
Build compatibility tests from actual prior release manifests and documented schema versions. Do not simulate a nonexistent historical release as evidence. Track served and storage API versions separately if a new CRD version is introduced.
Test install-old/upgrade-new, defaults, old object readability, safe status transitions and absence of unintended mutation. Document CRD migration and why Helm rollback alone cannot guarantee data-schema rollback.
Review all changed condition reasons, defaults, restart-token rules and authorization semantics as compatibility surfaces. Add migration notes for any earlier sketch field names only when corresponding real users or code exist.

Acceptance: upgrade evidence identifies exact tested versions; migration risks are explicit; no destructive CRD deletion is hidden in routine upgrade.
```
