# Prompt 063 — Appendix D — Exercises and solutions

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

Read the completed chapter learning objectives, lab specifications, `pkg/types/lifecycle_test.go`, scheduler property tests, reconciler and rollout tests, `internal/controlplane/operation_lock_test.go`, namespace/quota tests, health tests, GitOps tests, cron tests, migration tests, and API error tests. Examine the exact deterministic seams each test uses rather than assuming every feature has an injectable clock or public constructor.

## Produce the exercise set

Create `books/inside-orch/manuscript/appendices/d-exercises-solutions.md`, `books/inside-orch/exercises/catalog.json`, `books/inside-orch/exercises/questions.md`, and `books/inside-orch/manuscript/solutions/appendix-d.md`. Provide twenty-four substantial exercises, eight for developers, eight for DevOps engineers, and eight for architects. Each needs a stable ID, prerequisites, estimated time, source links, precise question, required artifact, objective scoring rubric, hints, and a worked solution. Connect every exercise to at least one chapter and one actual source mechanism.

Use parallel question and solution organization so readers can study without immediately seeing answers. Exercises must reward reasoning about ownership, failure, concurrency, resource units, secret handling, and deployment composition. Include a stale task-claim race, restart-policy trace, terminal cleanup case, rollback availability budget, namespace identifier leak, quota racing requests, bounded GitOps prune, cron overlap/catch-up, secret envelope key loss, process restart, and fake-load-test interpretation. Keep resource arithmetic consistent with millicores and bytes.

At least eight exercises must be executable offline through existing tests or a deliberately isolated teaching harness; eight must require a concrete operational or architecture artifact; the remaining eight can combine source reading and calculation. A correct answer may identify that a requested production guarantee is absent. Never require students to deploy the shipped default server as a durable production cluster, rotate real credentials, contact live metadata endpoints, or mutate the evidence checkout.

For coding exercises, place complete scaffolds and reference solutions only under `books/inside-orch/examples/teaching-extensions/exercises`, with runnable commands, test oracles, and source provenance. If importing `internal` packages needs a separate local teaching copy, make that boundary explicit and retain the original checkout unchanged. Scaffold TODO markers may be pedagogical only, with complete corresponding solutions; the delivered book and verification scripts must contain no unexplained placeholders.

## Acceptance and evidence

Create `books/inside-orch/validation/063-exercise-check.json` proving twenty-four unique IDs, exact audience counts, chapter/source linkage, solution existence, rubric coverage, and eight executable entries. Validate every expected answer against the pinned source or an actual checked computation. For trace exercises, serialize initial state and the expected transition sequence so a machine can distinguish wrong state ownership from wrong arithmetic.

Execute safe offline solution checks when available and record skipped prerequisites honestly. A passing reference solution must satisfy its rubric without hidden assumptions, and each executable test must fail for at least one specified incorrect behavior rather than merely mirror implementation. Have a second pass attempt each question using only its stated prerequisites and compare against the solution. Correct missing context and ambiguous grading. Finish with instructor guidance about adapting exercises to a future durable extension while preserving the distinction between repository facts and student-designed improvements.

## Immutable starting references

- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go)
- [internal/rollout/rollout_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout_test.go)
- [internal/health/health_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health_test.go)

## Native appendix contract

Use the first H1 exactly `# Appendix D - Worked Exercises and Design Solutions` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/d-exercises-solutions.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.
