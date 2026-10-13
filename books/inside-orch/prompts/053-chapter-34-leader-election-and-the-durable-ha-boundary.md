# 053 — Chapter 34: Leader Election and the Durable HA Boundary

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/34-leader-election-and-the-durable-ha-boundary.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is V — Extend the Platform. Focus: Study lease interfaces, PostgreSQL advisory locks, leadership cancellation, and the default server integration gap. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain per-controller leadership versus API availability.
- Trace lease loss to controller cancellation.
- Evaluate PostgreSQL connection and dual-primary failure assumptions.

Use these chapter-specific sections as the narrative spine:

1. **API Availability and Controller Leadership**
2. **PostgreSQL Advisory Locks and Connections**
3. **Lease Loss Must Cancel Controller Work**
4. **The Durable State and Server Composition Prerequisites**

Read the leadership interface, wrapper, local fake, and PostgreSQL advisory-lock implementation. Explain per-controller active leadership and dedicated connection semantics, then inspect cancellation on lease loss. Model competing leaders and partition assumptions in deterministic tests. Contrast implemented library behavior with the current server, which does not automatically use that elector or PostgreSQL active state. Never demonstrate multiple MemoryService servers as HA. A durable integration ADR should include cluster identity, one database primary, readiness, and idempotent work; that proposal stays outside immutable evidence.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/leadership/leadership.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership.go)
- [internal/leadership/leadership_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/leadership_test.go)
- [internal/leadership/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/leadership/postgres.go)
- [docs/HA_CONTROL_PLANE_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/HA_CONTROL_PLANE_DESIGN.md)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)

Read the original development intent:

- [prompts/56-ha-control-plane-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/56-ha-control-plane-design.md)
- [prompts/57-controller-leader-election-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/57-controller-leader-election-mvp.md)

Explain relevant implementation history using these real commits:

- [Add HA control plane design](https://github.com/alekpopovic/orch/commit/b29a6fe91e90f74721e5175e43bf12aed6410f19); inspect `books/inside-orch/evidence/commit-diffs/b29a6fe91e90f74721e5175e43bf12aed6410f19.patch`.
- [Add controller leader election MVP](https://github.com/alekpopovic/orch/commit/eb3a07c20c550a533afaf36f414ede1ba6c00f78); inspect `books/inside-orch/evidence/commit-diffs/eb3a07c20c550a533afaf36f414ede1ba6c00f78.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run deterministic competing-leader tests and draft a separate durable-server wiring ADR for Atlas.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch34/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not launch multiple default MemoryService servers as HA; advisory lock packages do not imply production wiring; include partition and leadership loss scenarios.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch34/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch34/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch34.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch34.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch34.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 053 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 34 - Leader Election and the Durable HA Boundary`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `34-leader-election-and-the-durable-ha-boundary` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
