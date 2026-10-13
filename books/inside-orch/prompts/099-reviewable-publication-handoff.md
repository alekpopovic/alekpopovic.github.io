# 099. Prepare the exact next publication action without a surprise deployment

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 098 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/publication/HANDOFF.md; books/inside-orch/publication/site-adapter/changes.patch; books/inside-orch/validation/RELEASE_GATE.md; books/inside-orch/dist/

## Output artifacts

books/inside-orch/publication/PUBLISH_CHECKLIST.md; books/inside-orch/publication/site-adapter/pr-description.md; final author-facing handoff

## Work to perform

Present the complete reviewable book and local site integration. Explain what changed, where the book can be previewed, what was actually tested, source/edition identity and any remaining limitation. Draft a focused PR description for the website change using the final implementation and its actual validation; do not include generation conversation history.

If the current user task explicitly authorizes a draft PR, create it on a separate branch after inspecting repository status and staging only relevant files. If it authorizes live publication, execute the established site workflow and verify the published book, chapters and downloads. Otherwise leave a ready local patch/branch and the exact publication commands for review, without pushing the default branch or deploying. The original request for this generation pack does not itself authorize a live website mutation. Complete all independent build/validation work before any approval is the last step. Record the final action taken and update the tracker honestly. A user should be able to judge the concrete result from the handoff alone.

## Acceptance and evidence

Reviewable final artifacts and local integration provided; PR/deployment action matches explicit current authorization; live result verified only if published; tracker reflects reality.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
