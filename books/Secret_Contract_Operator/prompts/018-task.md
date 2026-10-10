# 018 — GitHub Actions CI

Phase: B | Complexity: Medium | Dependency: 017

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 018
Add CI for pull requests and main changes with least privilege. Run format, vet, unit, race, envtest, generation checks, chart validation and container build. Use exact supported tool versions and pin third-party Actions to verified immutable commits where appropriate.
Do not give fork pull requests write tokens or cloud credentials. Avoid unsafe pull_request_target execution of untrusted head code. Treat branch names, titles and other PR metadata as untrusted input, not shell code.
Fail when generated files differ after make generate/manifests. Keep e2e separated or clearly configured. Record actual execution and make test output safe for public CI artifacts. Do not publish an image from ordinary PR checks.

Acceptance: a clean checkout runs the workflow locally where possible; valid YAML and job permissions are reviewed; no fake Action hashes or secret credentials are committed.
```
