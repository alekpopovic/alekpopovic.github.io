# 098. Freeze final archives, hashes and edition provenance

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 097 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/; books/inside-orch/manuscript/; books/inside-orch/publication/; books/inside-orch/validation/reviews/final-independent-review.md; books/inside-orch/state/execution-tracker.csv

## Output artifacts

books/inside-orch/dist/inside-orch-release.zip; books/inside-orch/dist/SHA256SUMS.txt; books/inside-orch/publication/RELEASE_NOTES.md; books/inside-orch/publication/HANDOFF.md

## Work to perform

Freeze a complete edition only after the preceding gates pass. Reassemble final PDF/EPUB/online/source/example archives from exact reviewed inputs. Recompute and verify all checksums after this assembly; create an edition manifest listing source SHA, manuscript hash, tool versions, generated outputs, word/page counts measured from final files, rights and validation statuses.

Write release notes that explain scope, intended readers and actual implemented-vs-design boundaries. Include an errata/contribution process and how to build a later edition from a deliberate new source lock. Produce a concise handoff for the author with ready files, the minimal review steps and any unresolved release-blocking issue. Do not describe pending work as complete. Keep the supplied generation prompts outside the public reader archive unless the author wants them as a separate companion. Save outputs to the designated destination when the runtime provides persistence, and verify each successful save rather than relying on an archive path alone.

## Acceptance and evidence

Archives/hashes/manifest match reviewed outputs; measured metadata truthful; release notes and handoff complete; rights/unresolved gates visible; no pending task relabeled complete.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
