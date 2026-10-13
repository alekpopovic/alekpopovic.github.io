# 037 — Chapter 18: Safe Deletion and Resource Cleanup

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/18-safe-deletion-and-resource-cleanup.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Follow deleting versus deleted services, task stop/remove behavior, finalization, and failures. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain why removal is a workflow rather than one HTTP delete.
- Trace cleanup ownership and retry behavior.
- Identify resource leaks and safe finalization conditions.

Use these chapter-specific sections as the narrative spine:

1. **Soft Deletion Is a State Machine**
2. **Stop and Remove Ownership**
3. **Retries After Partial Cleanup**
4. **When Finalization Is Safe**

Open with an operator deleting a service while one worker fails during container removal. Follow the service deleting state, desired task changes, agent stop/remove attempts, and final deleted condition. Compare safe-deletion introduction with later failure hardening. Repeated delete and remove calls should demonstrate convergence without duplicate or unrelated resource removal. Explain any leak or ambiguous window directly. The lab uses disposable resources and fake failures; it must not provide an indiscriminate Docker prune recipe as a shortcut for missing cleanup logic.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [docs/RECONCILER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md)
- [docs/RELIABILITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RELIABILITY.md)

Read the original development intent:

- [prompts/16-safe-service-deletion-and-cleanup.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/16-safe-service-deletion-and-cleanup.md)
- [prompts/25-failure-modes-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/25-failure-modes-hardening.md)

Explain relevant implementation history using these real commits:

- [Implement safe service deletion](https://github.com/alekpopovic/orch/commit/2084f5f77bd35ba2a4114d29c7e5588c0fd1f3e7); inspect `books/inside-orch/evidence/commit-diffs/2084f5f77bd35ba2a4114d29c7e5588c0fd1f3e7.patch`.
- [Improve failure recovery behavior](https://github.com/alekpopovic/orch/commit/66cfb7049fc1fbceeec9e36a7067febe8cbab698); inspect `books/inside-orch/evidence/commit-diffs/66cfb7049fc1fbceeec9e36a7067febe8cbab698.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Delete Atlas API while injecting one remove failure; inspect repeated cleanup attempts.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch18/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Distinguish desired deletion from confirmed runtime removal; demonstrate repeated calls and avoid destructive force-cleanup recipes.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch18/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch18/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch18.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch18.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch18.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 037 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 18 - Safe Deletion and Resource Cleanup`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `18-safe-deletion-and-resource-cleanup` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
