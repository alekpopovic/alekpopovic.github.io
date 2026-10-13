# 003. Reconcile all original prompts with implementation evidence

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 002 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/original-prompts.json; books/inside-orch/evidence/prompt-commit-map.json; books/inside-orch/evidence/orch/prompts/; books/inside-orch/evidence/commit-diffs/

## Output artifacts

books/inside-orch/editorial/PROMPT_HISTORY.md; books/inside-orch/validation/intake/prompt-reconciliation.json

## Work to perform

Read all 91 numbered development prompts, their requirements, the execution tracker and associated diffs. Use the supplied map as a starting hypothesis, retaining associated, batched and design relationships. Record requirements implemented in current code, partially integrated, design only, or unverifiable. Make scope changes explicit rather than deleting original acceptance criteria.

The first 29 prompt files were added after June implementation; their mappings are retrospective implementation associations. Later changes group several prompts into one commit. Show these relationships honestly and never invent missing per-prompt SHAs. Compare concrete requirements such as durable events, resource enforcement, quota transaction safety, digest resolution and HA against source flow and tests. Classify a requirement independently from a tracker's completed range. Produce an annotated map suitable for an appendix, retaining historical path renames separately from current paths. Record contradictions requiring chapter attention. If you revise a mapping, preserve the original, explain the change and verify the new commit diff.

## Acceptance and evidence

Exactly 91 original IDs covered once; all associated SHAs exist; batched/retrospective relationships preserved; claims of implementation include code evidence and limitations.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
