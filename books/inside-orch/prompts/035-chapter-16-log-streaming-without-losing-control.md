# 035 — Chapter 16: Log Streaming Without Losing Control

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/16-log-streaming-without-losing-control.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Trace server-to-agent log paths, Docker stream framing, cancellation, and bounded operator consumption. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops.

Learning outcomes:

- Locate actual log stream boundaries and response formats.
- Explain tail, follow, cancellation, and transport errors.
- Separate orchestration events from application stdout/stderr.

Use these chapter-specific sections as the narrative spine:

1. **The Client-to-Server-to-Agent Stream**
2. **Docker Frames and Application Output**
3. **Tail, Follow, Disconnect, and Cancellation**
4. **Boundaries of Log Retention**

Trace logs through the actual agent, API, CLI, and Docker files rather than the repository’s originally planned package layout. Explain stdout/stderr framing and the behavior of tail and follow using current request fields. Demonstrate a client disconnect and inspect cancellation or transport-error handling. Separate this stream from a persistent centralized logging service. The exercise should force readers to reason about slow consumers and a disappearing task while following logs, grounding proposed improvements in an explicitly separate teaching extension.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/agent/logs.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/logs.go)
- [internal/api/logs.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/logs.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [docs/LOGS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/LOGS.md)
- [internal/cli/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/operations.go)

Read the original development intent:

- [prompts/12-logs-support.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/12-logs-support.md)

Explain relevant implementation history using these real commits:

- [Add basic log streaming](https://github.com/alekpopovic/orch/commit/39e2359653e0e8790feda86eb5fbee3eb5ae509f); inspect `books/inside-orch/evidence/commit-diffs/39e2359653e0e8790feda86eb5fbee3eb5ae509f.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Stream Atlas application logs, disconnect the client, and check cancellation through a local test.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch16/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use actual agent/API/runtime log files; explain cancellation and stream errors; never fabricate a centralized persistent log collector.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch16/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch16/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch16.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch16.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch16.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 035 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 16 - Log Streaming Without Losing Control`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `16-log-streaming-without-losing-control` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
