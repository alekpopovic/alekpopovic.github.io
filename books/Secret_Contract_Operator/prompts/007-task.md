# 007 — Fuzzing and Leakage Tests

Phase: A | Complexity: High | Dependency: 006

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 007
Expand validator tests using synthetic inputs only. Include invalid UTF-8, Unicode byte boundaries, malformed URI escapes, PEM bundles, junk before and after PEM blocks, malformed first PEM blocks followed by valid blocks, regex errors, empty JSON and scalar JSON.
Add deterministic fuzz seeds and a bounded fuzz target checking no panic, deterministic results and safe result shape. Add sentinel tests for raw, base64, hex and deterministic digest representations in serialized outputs. Ensure test failures do not dump the full input.
State explicitly what sentinel testing proves and what it does not prove: it is a regression test for direct channels, not a proof against a validation oracle. Add an authorized-writer policy test separately; do not let a logging test substitute for access control.

Acceptance: unit, race and a recorded bounded fuzz run complete where tools support them; any unrun command is listed as not run.
```
