# 001. Inventory the implementation and its executable entrypoints

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 000 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/cmd/; books/inside-orch/evidence/orch/internal/; books/inside-orch/evidence/orch/pkg/; books/inside-orch/evidence/orch/migrations/; books/inside-orch/evidence/orch/go.mod

## Output artifacts

books/inside-orch/validation/intake/source-inventory.json; books/inside-orch/editorial/SOURCE_MAP.md

## Work to perform

Build a symbol-oriented map rather than a directory listing. Trace orch-server, orch-agent and the CLI from main through configuration, constructors, controllers and side-effect boundaries. List public interfaces, storage implementations, runtime adapters, lifecycle types, HTTP surfaces, external integrations and tests. Include 16 migration pairs with touched tables and schema compatibility constants. Explain why the intended layout in the application AGENTS.md differs from some actual paths.

For each subsystem list the entrypoint, main constructor, inputs, outputs, state owner and the source lines that establish them. Start an executable composition matrix; a package's presence must not be mistaken for a running controller. Inspect how MemoryService creates and assigns service tasks before the separate scheduler runs. Record fields carried to AgentTask and Docker ContainerSpec. Find all test prerequisites and build tags. Identify seams that can be taught with pure unit tests versus those requiring processes, a database, network access or Docker. Keep the inventory compact enough that chapter authors can navigate it without rereading the whole repository.

## Acceptance and evidence

Every source path exists at the lock; binary composition is traced; resource and placement propagation are included; test scope and external prerequisites are explicit.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.
