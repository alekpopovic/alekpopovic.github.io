# Prompt 061 — Appendix B — Lifecycle and invariants reference

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `pkg/types/lifecycle.go`, `pkg/types/lifecycle_test.go`, `pkg/types/types.go`, `pkg/types/workloads.go`, `docs/STATE_MACHINES.md`, `internal/task/task.go`, `internal/controlplane/controlplane.go`, `internal/controlplane/agent_test.go`, `internal/store/postgres.go`, `internal/reconciler/reconciler.go`, `internal/rollout/rollout.go`, and `internal/agent/agent.go`. Inspect all lifecycle consumers and the tests that establish terminal-state semantics.

## Produce the reference

Create `books/inside-orch/manuscript/appendices/b-lifecycle-invariants.md`, `books/inside-orch/reference/lifecycle.json`, and `books/inside-orch/reference/invariants.json`. Extract service, task actual, task desired, node, deployment, job, and cron scheduling semantics separately. Do not confuse ownership and state: the server owns desired state; an assigned agent may report actual state only within valid transitions. For every transition, cite the helper or actual implementation that permits it and record duplicate-report behavior.

Present compact state tables with allowed edges, forbidden representative edges, terminal states, cleanup exceptions, and report authorization. Show why `failed` is terminal for a task while a replacement may be created for its service, why `failed` or `stopped` may move to `removed`, and why rollback creates a new deployment rather than rewriting terminal history. Mark reserved states, including paused deployment behavior, so the reader does not infer a CLI feature from an enum.

Create invariants for desired-replica convergence, atomic task claims, event emission after persisted transitions, node ownership of reports, namespace secrecy, rollout surge/availability accounting, and safe container cleanup. Each invariant must specify scope, assumptions, enforcing function, relevant test, and known counterexample outside that scope. Distinguish store-backed reconciler restart reasoning from process restart of the shipped memory server. Explain that a package test establishes its tested contract, not automatic wiring into the binary.

Include three worked traces: duplicate `healthy` reporting, deleting while rollout is active, and offline stateless versus stateful tasks. Use actual field names and show conditions independently from states. When a trace is reconstructed from source, label it as a source-derived illustration; observed test output gets its own evidence record. Do not add a transition to make a teaching narrative work.

## Acceptance and evidence

Create `books/inside-orch/validation/061-transition-check.json` with the discovered state set, allowed transition matrix, terminal set, and state-owner mapping. Implement a machine check outside the source tree that compares the reference against source transitions or an executed isolated teaching harness. A harness must preserve the locked evidence checkout; use an explicit extension directory and state the import-boundary solution if internal packages are required. Check same-state idempotency, representative invalid transitions, and terminal cleanup exceptions.

Every invariant needs at least one precise symbol citation and a test citation or an explicit test-gap entry. Detect unaccounted enum values and dangling links. Cross-check documentation tables against implementation and preserve discrepancies rather than editing the repository. For each worked trace, include numbered steps, preconditions, state values, outcomes, and the exact scope of confidence. Finish with a paragraph explaining how reviewers can use the matrix to find stale agent reports and unsafe new lifecycle states without treating the appendix as a formal proof of distributed correctness.

## Immutable starting references

- [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go)
- [docs/STATE_MACHINES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATE_MACHINES.md)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go)

## Native appendix contract

Use the first H1 exactly `# Appendix B - Lifecycle States and Invariant Reference` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/b-lifecycle-invariants.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.
