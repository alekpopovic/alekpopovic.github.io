# 096. Run the complete edition gate and resolve blockers

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 095 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/QUALITY_GATES.md; books/inside-orch/state/execution-tracker.csv; books/inside-orch/manuscript/; books/inside-orch/dist/; books/inside-orch/validation/

## Output artifacts

books/inside-orch/validation/RELEASE_GATE.md; books/inside-orch/validation/release-gate.json

## Work to perform

Run structural checks and collect every technical, execution, editorial and publication gate for the exact final edition. Confirm 40 chapters, six appendices, solved exercises, eight executed labs or explicitly declared release-blocking unavailable evidence, pinned source references, provenance and consistent formats. Inspect tracker entries rather than treating done as proof; each requires a concrete evidence path.

Recheck critical claim boundaries: MemoryService process state, separate planner/reconciler behavior, CPU/memory propagation, HA/autoscaler wiring, no network fencing, partial GitOps applies, local volumes, digest parsing, design-only supply chain/plugins/billing. Ensure no chapter describes a prospective extension as current orch behavior. Verify final artifact hashes correspond to reviewed PDF/EPUB/online outputs. Categorize blockers, minor corrections and future errata; fix blockers in canonical sources and rerun only affected checks plus the relevant release gate. Do not hide skipped external suites or unavailable publication checks. Produce a concise accountable release decision with links to actual evidence.

## Acceptance and evidence

Every release criterion has evidence for current hashes; major defects fixed; skipped/unavailable tests explicit; no unsupported guarantee survives; complete edition status justified.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Actual website release gates

From SITE run `npm run build`, `bundle exec jekyll build`, then `.venv/bin/python scripts/check-books.py` (or documented CI Python). Also run `npm run check:site`, `npm run check:content`, and applicable UI/performance checks for shared/browser changes. Confirm all 47 orch sections, full PDFs/EPUBs, three original posts covering different numbered chapters, the inside-orch glossary and stable update entry. Do not weaken checks to pass the new book. Missing toolchains are blockers with actual reasons.
