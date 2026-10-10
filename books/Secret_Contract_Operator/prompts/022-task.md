# 022 — Preparing the First MVP Release

Phase: B | Complexity: High | Dependency: 021

```text
You are implementing Secret Contract Operator from the canonical technical book.
Read AGENTS.md, docs/specification.md, docs/security.md and the task dependencies.
Work only within this task. Preserve unrelated changes. Never read production secrets.
Never emit Secret values, fragments, raw parser errors or data hashes into any output.
All references are namespace-local. Mutation is off unless all documented approvals hold.
After work, report changed files, exact executed checks, not-run checks and residual risks.
Update tracking honestly; implementation alone is not verification or acceptance.

TASK 022
Prepare, but do not publish without explicit authorization, the first MVP release. Freeze the v1alpha1 schema, regenerate artifacts, reconcile docs/examples and execute the agreed test matrix.
Prepare release notes, installation manifests, chart package, checksums, image build instructions, SBOM/provenance generation and signing verification guidance. Use real generated digests only; no fabricated release URLs or registry tags.
Document supported versions solely from tested evidence. Separate application version, chart version and CRD API version. List known limitations including no hard deployment gate, trusted contract authors and no default mutation. Record release acceptance status in tracking.

Acceptance: a reviewer can reproduce the local release candidate; unrun checks block verified/accepted status instead of being silently waived.
```
