# 020 — Documentation, Examples, and CI Gate

Phase: B | Complexity: Medium | Dependency: 019

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 020
Write README, API reference, security model, troubleshooting, metrics and examples matching the implemented schema. Include a missing-key example, a valid preflight example, ESO target validation and workload consumption validation.
Provide a generation-aware gate script that checks contract UID, current generation and Ready.observedGeneration without reading Secret values. Explain the initial-workload deadlock and use two deployment phases. Explicitly state the remaining race and that Ready is not automatic admission enforcement.
Use only synthetic credentials and verified image references or clearly labeled placeholders. Mark future mutation, webhook and rollout features as future. Ensure every quickstart command has its prerequisite and expected safe output.

Acceptance: examples validate against the generated CRD in the test environment; documentation does not advertise unimplemented or untested guarantees.
```
