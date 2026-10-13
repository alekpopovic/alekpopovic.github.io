# 019. Review the sample and approve the book’s technical stance

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 018 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/samples/runtime-boundary.md; books/inside-orch/editorial/TECHNICAL_AUDIT.md; books/inside-orch/editorial/TOC.md; books/inside-orch/editorial/CHAPTER_CONTRACTS.md; books/inside-orch/editorial/SOURCE_POLICY.md

## Output artifacts

books/inside-orch/validation/reviews/foundation-gate.md; books/inside-orch/editorial/STYLE_REFERENCE.md

## Work to perform

Read the supplied sample chapter as a style and evidence specimen, not an already executed laboratory. Verify every quoted line against the snapshot and every historical link against the commit corpus. Confirm that the early narrative accurately explains server state ownership, optional schema checks and controller wiring before discussing sophisticated libraries.

Check that the sample teaches a real developer/DevOps/architect lesson with a concrete restart scenario, meaningful exercises and clear expected observations. Copy its strengths into a compact editorial style reference: direct prose, focused listings, an explicit failure window and precise source references. Correct weak wording, dead links or implicit production guarantees in the book draft, while preserving source excerpts unchanged. Review all foundation outputs from prompts 000–018; unresolved critical source/rights/lab-environment gaps must be recorded and block dependent release tasks. Writing can continue on well-grounded source-only chapters while external lab prerequisites are blocked. Set the chapter-writing sequence and validation expectations. Never mark later manuscript or lab tasks done merely because their prompts exist.

## Acceptance and evidence

Sample source/links checked; foundation conflicts resolved or explicitly blocked; consistent narrative style recorded; next writing tasks have exact inputs and acceptance gates.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Write the canonical preface

Write `books/inside-orch/manuscript/00-preface.md` (800-1,200 substantive English words) with first H1 `# Preface`. Explain the audience, source edition, actual executable boundary, three reader paths, safe laboratory expectations and evidence policy. This is the first Book.txt section; site section() treats index 0 as Preface, so do not put Chapter 1 first. It complements the 40 chapters and six appendices; do not count it as a numbered chapter.
