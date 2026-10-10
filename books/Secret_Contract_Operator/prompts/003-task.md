# 003 — Threat Model and Architecture Decisions

Phase: A | Complexity: High | Dependency: 002

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 003
Write architecture decision records before expanding the controller. Cover namespace-local references, trusted contract authors, Secret read scope, cache exposure, static safe diagnostics, no content hashes, no default mutation, no ownership of referenced resources and no finalizer in the read-only MVP.
Design authorization boundaries explicitly. A user-controlled allow flag or annotation inside SecretContract is not an authorization mechanism. For the first deployment profile, contract writers must be trusted administrators with rights to the target Secret. Document a future protected grant model without claiming that it is already implemented.
Describe a confused-deputy risk for injection into a workload controlled by another actor. Define the two independent approvals needed before mutation. Document the remaining time-of-check/time-of-use race and that Ready alone never blocks Kubernetes deployment.

Acceptance: ADRs identify actors, new privileges and failure cases; security claims have matching planned tests; no unsupported multi-tenant safety promise remains.
```
