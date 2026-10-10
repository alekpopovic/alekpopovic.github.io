# 024 — Minimal EnvFrom and EnvVars Injection

Phase: C | Complexity: High | Dependency: 023

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 024
Implement the canonical opt-in injection modes for explicitly selected supported consumers. Add references only; never materialize Secret values into env.value. Do not mutate init containers unless the API explicitly supports and tests that path.
Plan changes before writing. EnvFrom adds a non-duplicated reference; EnvVars maps envName or key name and respects optional rules. Existing conflicting names are reported, not overwritten. Preserve unrelated env order, image, securityContext and all other fields.
Use concurrency-safe minimal patches and re-read/replan on conflict. Avoid force ownership takeover. Document partial success across multiple workload objects because Kubernetes does not provide a multi-object atomic patch. Clarify GitOps field ownership and deletion behavior.

Acceptance: disabled and unapproved cases make no changes; repeated reconcile is a no-op; concurrent user updates are preserved; conflict cases have safe status.
```
