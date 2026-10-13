# 029 — Chapter 10: A Deterministic Scheduler

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/10-a-deterministic-scheduler.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Read placement order, eligibility checks, capacity accounting, and concurrent assignment safety. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Explain deterministic ordering and tie-breaking.
- Check labels, status, resources, ports, and storage topology.
- Identify the persistence conflict path during assignment.

Use these chapter-specific sections as the narrative spine:

1. **Candidate Ordering and Deterministic Choice**
2. **Ready Nodes, Labels, Capacity, and Ports**
3. **One Assignment Under Concurrent Work**
4. **Planner Guarantees Versus Live Placement**

Calculate an assignment by hand for three fake nodes, including an ineligible node and a resource or port exhaustion case. Tie the calculation to actual sorting and eligibility code. Explain how assignment persistence handles concurrency and conflicts. Compare scheduler package behavior with MemoryService’s normal service placement before claiming production enforcement of constraints. Inspect seeded property tests as additional invariant evidence. The reader should be able to name both the guarantee proved by the planner and the runtime path still needing verification.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go)
- [internal/scheduler/scheduler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler_test.go)
- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/scheduler/workloads_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/workloads_test.go)
- [docs/SCHEDULER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SCHEDULER.md)
- [docs/RESOURCES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RESOURCES.md)

Read the original development intent:

- [prompts/09-scheduler-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/09-scheduler-v1.md)
- [prompts/17-resource-accounting.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/17-resource-accounting.md)
- [prompts/31-scheduler-concurrency-safety.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/31-scheduler-concurrency-safety.md)

Explain relevant implementation history using these real commits:

- [Implement scheduler v1](https://github.com/alekpopovic/orch/commit/fce0a657651c00ffb697bf4a4aba12d0b171f463); inspect `books/inside-orch/evidence/commit-diffs/fce0a657651c00ffb697bf4a4aba12d0b171f463.patch`.
- [Add scheduler concurrency-safe assignment](https://github.com/alekpopovic/orch/commit/1a1c216e8cfb442465f4d3c2c114d20da0342795); inspect `books/inside-orch/evidence/commit-diffs/1a1c216e8cfb442465f4d3c2c114d20da0342795.patch`.
- [Add host port allocation awareness](https://github.com/alekpopovic/orch/commit/3bfcef82a54dec457cf9d4187705fa70cc7215cf); inspect `books/inside-orch/evidence/commit-diffs/3bfcef82a54dec457cf9d4187705fa70cc7215cf.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Build a tiny fake-node placement experiment with valid, exhausted, and conflicting nodes.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch10/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Calculate one complete placement by hand and confirm with a test; task assignment is unique; resource and port claims are not described as Docker enforcement.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch10/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch10/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch10.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch10.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch10.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 029 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 10 - A Deterministic Scheduler`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `10-a-deterministic-scheduler` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
