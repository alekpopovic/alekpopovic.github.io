# 034 — Chapter 15: Events, Audits, and Notification Boundaries

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/15-events-audits-and-notification-boundaries.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Treat events as operator history, audit as an attribution record, and notifications as external effects. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops.

Learning outcomes:

- Differentiate domain events, diagnostic logs, and audits.
- Trace redaction and actor attribution.
- Explain notification delivery, retry, and failure isolation from code.

Use these chapter-specific sections as the narrative spine:

1. **Events, Diagnostic Logs, and Audits**
2. **Attribution, Redaction, and History**
3. **Notification Delivery as an External Effect**
4. **When History Is Not Durable**

Use a real deployment event timeline to explain the distinction between domain history, diagnostic logs, and audit attribution. Read redaction before promising that secrets cannot escape through messages or sink payloads. Trace notification dispatcher calls, retry behavior, and handling of sink failures from current code. Use a local fake sink for the lab. The original durable-events prompt title is intent evidence; explain whether the default MemoryService-backed history actually survives process restart and avoid attributing an absent persistent event pipeline to the system.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/events/events.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/events/events.go)
- [internal/events/events_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/events/events_test.go)
- [internal/audit/audit.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/audit/audit.go)
- [internal/notifications/notifications.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go)
- [internal/notifications/notifications_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications_test.go)
- [docs/EVENTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/EVENTS.md)
- [docs/NOTIFICATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NOTIFICATIONS.md)

Read the original development intent:

- [prompts/13-durable-events-system.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/13-durable-events-system.md)
- [prompts/46-audit-logging.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/46-audit-logging.md)
- [prompts/80-notification-sinks.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/80-notification-sinks.md)

Explain relevant implementation history using these real commits:

- [Add durable events system](https://github.com/alekpopovic/orch/commit/7ff58cef0f736ac9076942ce3ef1039d1fe72c72); inspect `books/inside-orch/evidence/commit-diffs/7ff58cef0f736ac9076942ce3ef1039d1fe72c72.patch`.
- [Add audit logging](https://github.com/alekpopovic/orch/commit/7935c334dcd264e70abb9e795889010b9ecdb03b); inspect `books/inside-orch/evidence/commit-diffs/7935c334dcd264e70abb9e795889010b9ecdb03b.patch`.
- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Capture the Atlas deployment event timeline and send notifications to a local fake sink.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch15/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not equate the default memory-backed event history with durable production events; delivery guarantees and redaction claims come from implementation tests.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch15/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch15/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch15.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch15.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch15.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 034 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 15 - Events, Audits, and Notification Boundaries`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `15-events-audits-and-notification-boundaries` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.
