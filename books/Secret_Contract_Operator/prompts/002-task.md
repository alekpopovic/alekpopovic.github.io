# 002 — Kubebuilder Scaffold and Tool Pinning

Phase: A | Complexity: Medium | Dependency: 001

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 002
Initialize a Go Kubebuilder project only if no scaffold exists. Proposed module is github.com/CodepopTech/secret-contract-operator, domain codepop.tech, group secrets, version v1alpha1, kind SecretContract. When a scaffold already exists, inspect and extend it instead of regenerating over user code.
Select a mutually compatible Kubebuilder, Go, controller-runtime and Kubernetes library set from the scaffold. Record exact versions in the repository. Do not independently upgrade every dependency to latest. Preserve PROJECT, generated Makefile conventions, CRD generation and the manager entrypoint.
Build the unmodified scaffold, run its relevant tests, make generate and make manifests. Explain which tests require envtest binaries and whether those were actually available. Add a reproducible local setup document and ignore local binaries and test credentials.

Acceptance: a clean scaffold builds, generated API/controller files exist, no business logic is introduced, and actual command results are recorded.
```
