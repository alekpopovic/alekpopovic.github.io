# 030 — Final Review and Release Candidate

Phase: D | Complexity: High | Dependency: 029

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 030
Perform a repository-wide release review. Recheck API coherence, generation-aware conditions, namespace authorization, cache exposure, value-free outputs, event cardinality, timer behavior, idempotent mutation and workload strategy support.
Run the available complete test matrix, generation checks, chart policy checks and container build. Record exact commands and distinguish failures, blocked prerequisites and not-run checks. Review every advertised feature against actual code and tests.
Produce a release readiness checklist, residual-risk report, installation/upgrade/uninstall procedure and prioritized follow-up issues. Prepare signed/reproducible artifacts only from an accepted commit. Do not publish externally or claim production certification without explicit user authorization and evidence.

Acceptance: reviewers can trace each public claim to code, tests and documentation; release acceptance remains blocked for unresolved critical issues.
```
