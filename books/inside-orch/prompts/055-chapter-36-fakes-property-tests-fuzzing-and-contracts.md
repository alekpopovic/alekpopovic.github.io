# 055 — Chapter 36: Fakes, Property Tests, Fuzzing, and Contracts

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/36-fakes-property-tests-fuzzing-and-contracts.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is VI — Prove and Operate. Focus: Use existing deterministic fakes, seeded scheduler properties, fuzz targets, and E2E tests as executable specifications. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Select the smallest test boundary that proves an invariant.
- Reproduce a seeded property failure.
- Preserve fuzz findings as minimal regression cases.

Use these chapter-specific sections as the narrative spine:

1. **Fakes as Executable Domain Specifications**
2. **Seeded Scheduler Properties**
3. **Fuzz Inputs and Minimal Reproductions**
4. **Contracts Across Integration Boundaries**

Choose one scheduler invariant, one parser robustness property, and one repeated-convergence behavior to show different test boundaries. Inspect how FakeRuntime records operations and failures. Read fixed seeds and failure messages before writing reproduction instructions. Use actual fuzz target names and mark manual bounded fuzz runs separately from normal CI. Explain why skipped Docker/PostgreSQL tests provide no execution evidence. Worked solutions should justify an invariant or minimize a regression, not merely reproduce a function’s implementation or assert that a constructor exists.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/docker/fake.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go)
- [internal/e2e/orchestrator_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/orchestrator_test.go)
- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/api/fuzz_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/fuzz_test.go)
- [internal/cli/fuzz_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/fuzz_test.go)
- [pkg/types/fuzz_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/fuzz_test.go)
- [docs/TESTING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/TESTING.md)

Read the original development intent:

- [prompts/22-end-to-end-tests.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/22-end-to-end-tests.md)
- [prompts/33-fake-runtime-for-deterministic-tests.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/33-fake-runtime-for-deterministic-tests.md)
- [prompts/86-fuzz-tests-for-parsers-and-validators.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/86-fuzz-tests-for-parsers-and-validators.md)
- [prompts/87-property-tests-for-scheduler.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/87-property-tests-for-scheduler.md)

Explain relevant implementation history using these real commits:

- [Add orchestrator MVP end-to-end tests](https://github.com/alekpopovic/orch/commit/903ece1ea30c5a0f4902b3f2e9cb475fdea41fdc); inspect `books/inside-orch/evidence/commit-diffs/903ece1ea30c5a0f4902b3f2e9cb475fdea41fdc.patch`.
- [Add deterministic fake container runtime](https://github.com/alekpopovic/orch/commit/c69f9ffa830284692aabf9e65ab9eb1f79d3a114); inspect `books/inside-orch/evidence/commit-diffs/c69f9ffa830284692aabf9e65ab9eb1f79d3a114.patch`.
- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Add book-side exercises for duplicate placement, parser panic resistance, and repeated convergence.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch36/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: No mirrored tests that simply restate implementation; fuzz duration and manual CI policy are explicit; skipped integration tests are recorded rather than counted as passed.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch36/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch36/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch36.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch36.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch36.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 055 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 36 - Fakes, Property Tests, Fuzzing, and Contracts`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `36-fakes-property-tests-fuzzing-and-contracts` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
