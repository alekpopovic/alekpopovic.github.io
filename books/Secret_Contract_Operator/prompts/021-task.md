# 021 — MVP Security Audit

Phase: B | Complexity: High | Dependency: 020

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 021
Audit source, tests, chart and docs for leaks and privilege mistakes. Trace every use of Secret.Data, string conversion, error wrapping, structured logger, event, metric, annotation and status field. Remove raw object formatting and unsafe upstream messages.
Review the validation-oracle model and ensure contract-writer permissions match declared trust assumptions. Check authorization before data reads. Verify the default chart cannot mutate workloads or Secrets. Review pprof/debug exposure, cache contents and public CI artifacts.
Add regression tests for confirmed issues. Produce SECURITY.md and a concise audit report with findings, fixes and residual risks. This is an internal engineering audit, not a claim of independent certification.

Acceptance: no critical known leak or authorization bypass remains; negative tests pass; residual risks and unperformed external reviews are explicit.
```
