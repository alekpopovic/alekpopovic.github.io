# 030 — Chapter 11: Reconciliation as Repeated Convergence

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/11-reconciliation-as-repeated-convergence.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Explain creation, scale-down, restart policy, soft deletion, and restart idempotency. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Separate reconciliation decisions from placement and runtime side effects.
- Demonstrate repeated RunOnce convergence.
- Handle failed tasks and service soft deletion.

Use these chapter-specific sections as the narrative spine:

1. **Replica Convergence Without Docker Calls**
2. **Repeated Iterations and Restart Idempotency**
3. **Failed Tasks, Restart Policy, and Scale-Down**
4. **How This Controller Is Invoked**

Follow a service from too few replicas to a stable desired count, then repeat the iteration and prove no duplicate work appears. Use the restart-hardening diff to explain transitional tasks and failed-task replacement. Keep scheduling and Docker side effects outside reconciliation ownership. Examine the default service mutation path instead of assuming every package runs as an independent loop. Clarify whether a test restarts a controller while reusing memory or restarts an entire process with persisted state; these demonstrate materially different guarantees.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/reconciler/reconciler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler_test.go)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [docs/RECONCILER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md)

Read the original development intent:

- [prompts/10-reconciler-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/10-reconciler-v1.md)
- [prompts/24-idempotency-audit.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/24-idempotency-audit.md)
- [prompts/32-reconciler-idempotency-under-restart.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/32-reconciler-idempotency-under-restart.md)

Explain relevant implementation history using these real commits:

- [Implement service reconciler](https://github.com/alekpopovic/orch/commit/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3); inspect `books/inside-orch/evidence/commit-diffs/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3.patch`.
- [Harden reconciler restart idempotency](https://github.com/alekpopovic/orch/commit/a11cec091a69720c14b9713d8be68f38fe6df332); inspect `books/inside-orch/evidence/commit-diffs/a11cec091a69720c14b9713d8be68f38fe6df332.patch`.
- [Harden task state idempotency](https://github.com/alekpopovic/orch/commit/316ba80ac1ea7ba465f1b0826b655233a651c043); inspect `books/inside-orch/evidence/commit-diffs/316ba80ac1ea7ba465f1b0826b655233a651c043.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Apply the same desired Atlas replica count repeatedly in deterministic tests and verify no duplicate tasks.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch11/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Show what each repeated iteration reads and writes; account for transitional tasks; document the default server’s actual invocation path rather than assuming a wired standalone loop.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch11/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch11/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch11.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch11.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch11.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 030 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 11 - Reconciliation as Repeated Convergence`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `11-reconciliation-as-repeated-convergence` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
