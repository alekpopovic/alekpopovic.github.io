# Complete book-production sequence 000-099

Execute every task from alekpopovic/alekpopovic.github.io repository root. Installed book folder: books/inside-orch. These are full prompts, not a completed manuscript.

---

# 000. Establish a separate, reproducible book workspace

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** None; this is the intake task.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

AGENTS.md; BOOK_SPEC.md; books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/orch/AGENTS.md

## Output artifacts

books/inside-orch/state/workspace.json; books/inside-orch/validation/intake/baseline.md; books/inside-orch/manuscript/README.md

## Work to perform

Inspect the working directory and any existing Git state before creating files. Identify the book workspace, the immutable evidence snapshot, and a separate location for runnable labs. Record the full application SHA, tree SHA, corpus counts, tags, author, title, language, and local tool versions. Run books/inside-orch/scripts/verify_pack.py and retain its actual output. If a Git checkout of the source is needed for historical navigation, clone into a separate read-only source location and checkout the locked SHA; do not substitute the moving main branch. Never initialize or push a repository inside books/inside-orch/evidence/orch.

Create the manuscript directory layout and a scope note explaining that this workflow generates a new engineering book. Preserve any existing draft rather than overwriting it. Record which tools are present for Go, Docker, PostgreSQL, PDF rendering, EPUB checks and the site build; absence blocks the dependent lab or publication task, not the research tasks. Leave unavailable commands unrun and record why. Set up a durable validation directory with UTC execution records. Explain that the supplied snapshot contains tracked files and exported diffs, not a .git database.

## Acceptance and evidence

Every locked source hash matches; all 91 development prompts and 105 commit records are available; workspace paths are isolated; no user files overwritten; exact baseline and actual tool capabilities are recorded.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Site-root bootstrap

Verify the current Git remote identifies alekpopovic/alekpopovic.github.io, inspect branch/status and read any deeper instructions before changes. Do not reset the site to the inspection SHA or overwrite unrelated work. Compare the current site contract with the locked evidence and reconcile material changes. Add `books/inside-orch` to `_config.yml` exclude before running Jekyll, preventing raw research/prompts/source snapshots from becoming public static files. Preserve all existing excludes and the production origin. Keep the new book unregistered until its complete manuscript and native exports are ready; ordinary site builds must remain valid meanwhile. Create canonical `books/inside-orch/book.json` with English metadata and planned edition status; this file does not make the book publicly available.


---

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


---

# 002. Reconstruct the engineering history with verifiable milestones

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 001 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/commits.json; books/inside-orch/evidence/commits.csv; books/inside-orch/evidence/commit-diffs/; books/inside-orch/evidence/COMMIT_INDEX.md

## Output artifacts

books/inside-orch/editorial/HISTORY.md; books/inside-orch/validation/intake/milestones.json

## Work to perform

Read the complete 105-commit corpus and selected diffs, retaining both author and committer dates. Group meaningful engineering changes into scaffold/API/runtime, scheduling/reconciliation, lifecycle/reliability, v0.2-era hardening, v0.3 contracts/workloads/operations, documentation and maintenance. Inspect changed files before describing a milestone's result. Differentiate merge commits, dependency updates, tracker-only commits and implementation commits.

Verify tag identities from source-lock and the prompt mapping: 0.1.0 and 0.3.0 are present; a release-preparation commit does not establish a 0.2.0 tag or a published artifact. Explain that 0.3.0 tags a formatting fix preceding the final documentation HEAD. Preserve this difference when selecting editions and linking sources. A chapter discussing historical code links to the historical SHA; a walkthrough of present code links to the locked HEAD. Build a reader-friendly timeline that explains why each change matters and what remained incomplete. Do not turn release notes or titles into executed-test evidence. Retain compact exact commit subjects for navigation with full-SHA URLs.

## Acceptance and evidence

Timeline dates and tag SHAs match corpus; historical/current links are separated; every milestone has diff evidence; no claim of release publication is made without direct evidence.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

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


---

# 004. Build the capability ledger that governs every chapter

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 003 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/TECHNICAL_AUDIT.md; books/inside-orch/evidence/orch/cmd/orch-server/main.go; books/inside-orch/evidence/orch/internal/controlplane/; books/inside-orch/evidence/orch/internal/agent/; books/inside-orch/evidence/orch/internal/docker/

## Output artifacts

books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/validation/intake/capabilities.json

## Work to perform

Reinspect the supplied technical audit against the pinned source. For each capability classify runtime-integrated, implemented package, partial integration, design only, teaching extension or future work. Include persistence, scheduler/reconciler paths, Docker resource enforcement, lifecycle guards, heartbeat/offline recovery, HA, autoscaling, auth, secrets, tenants, quotas, image identity, GitOps, jobs, cron, volumes, DNS, notifications, upgrades and billing.

For every row trace a constructor or call path and cite the defining lines. The default server uses MemoryService. Its immediate round-robin assigned tasks differ from scheduler.Plan. AgentTask and ensureTask do not carry resource limits to the adapter's supported enforcement fields. Autoscaling and leadership packages are absent from server composition. Tests using the same MemoryService after a controller restart are not process durability tests. Distinguish a potential pooled-session advisory-lock cleanup defect from a demonstrated test result. Identify direct code evidence, uncertainty and the experiment that could resolve it. Give this ledger a stable row ID so later manuscript claims can reference it. Treat the ledger as an editorial control, not a badge of production fitness.

## Acceptance and evidence

All major executable/library/design differences documented with source lines; critical gaps cannot disappear in later chapters; unconfirmed security/reliability risks are labeled as hypotheses.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 005. Resolve stale documentation through code-first comparison

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 004 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/ARCHITECTURE.md; books/inside-orch/evidence/orch/docs/RELIABILITY.md; books/inside-orch/evidence/orch/README.md; books/inside-orch/evidence/orch/RELEASE_NOTES.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/DOCUMENTATION_CONFLICTS.md; books/inside-orch/validation/intake/documentation-conflicts.json

## Work to perform

Compare architecture, operational guides and release notes to startup wiring, handlers, controllers, runtime calls and tests. Log each disagreement with quoted short source fragments or precise references, the more authoritative path, the engineering consequence and a proposed book explanation. Examples to verify include a node-monitor roadmap entry when the monitor is already constructed, durable-storage wording with an in-memory server, and integration claims inferred from design documents.

Use implementation as the authority for current executable behavior, while retaining design documents as evidence of intent. Tests clarify expected contracts but do not override actual startup composition. Avoid silently reconciling contradictory documents into an invented ideal system. Write editorial wording that introduces the discrepancy without attacking the project. A reader should learn to inspect a real evolving repository. Keep historical documentation differences separate from present defects. When a conflict cannot be resolved by source inspection, mark it unresolved and propose a narrowly scoped test or author question. Do not modify application documentation in the evidence snapshot.

## Acceptance and evidence

Every conflict has exact source paths and a resolution/uncertainty; chapters receive the relevant conflict IDs; stale roadmaps are not copied as current behavior.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 006. Freeze the dependency and compatibility assumptions

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 005 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/go.mod; books/inside-orch/evidence/orch/go.sum; books/inside-orch/evidence/orch/internal/version/; books/inside-orch/evidence/orch/docs/UPGRADES.md; books/inside-orch/evidence/orch/docs/MIGRATIONS.md; books/inside-orch/evidence/orch/.github/workflows/ci.yml

## Output artifacts

books/inside-orch/editorial/COMPATIBILITY.md; books/inside-orch/validation/intake/toolchain.json

## Work to perform

Record Go version, direct dependency versions, API/server/agent/schema compatibility constants and CI tools from the inspected source. This is a versioned baseline, not a claim about the newest upstream releases. If the book discusses external semantics, retrieve and cite primary documentation at a version that applies. Do not recommend upgrading dependencies as part of manuscript generation.

Explain the distinction between compile/toolchain compatibility, wire compatibility, schema compatibility and rolling-upgrade compatibility. Trace how version metadata is checked in registration, heartbeat and migration commands. Document external suites' environment variables, build tags and skip conditions, including the danger that a normal passing suite skipped Docker or PostgreSQL. Explain why CI coverage artifacts prove only the checks actually executed. Record supported platforms from the source installation guide without inventing release assets. Include precise database test isolation requirements; schema-reset tests need a disposable database. Establish a policy for version annotations in command listings and lock regeneration for a future edition.

## Acceptance and evidence

Versions match locked files; compatibility dimensions are distinct; skips/prerequisites are explicit; external technical references are primary and version-appropriate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 007. Design an isolated laboratory with honest prerequisites

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 006 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/compose.yaml; books/inside-orch/evidence/orch/docs/DEVELOPMENT.md; books/inside-orch/evidence/orch/docs/TESTING.md; books/inside-orch/evidence/orch/deployments/examples/; books/inside-orch/editorial/TECHNICAL_AUDIT.md

## Output artifacts

books/inside-orch/labs/ENVIRONMENT.md; books/inside-orch/validation/intake/lab-environment.json

## Work to perform

Define two tracks: source-only deterministic tests and disposable process/Docker/PostgreSQL experiments. Name all host privileges, exposed ports, databases, temporary repositories, images and cleanup scopes. Docker socket access is privileged; local development tokens and insecure dashboards must remain disposable lab defaults. Bind operator-facing services to loopback where the chosen commands support it and inspect actual configuration handling before changing values.

Create a prerequisite checker that reports capabilities without installing software or altering user infrastructure. Document exactly which experiments can run without Docker or a database. Database integration tests that reset schema must verify an explicitly designated throwaway URL; do not execute them against an existing real database. Define unique labels or namespaces for lab-created containers and only remove those resources. Explain that PostgreSQL running beside orch-server does not persist MemoryService state. Prefer pinned source builds rather than piping an uninspected latest installer into a shell. Store real execution evidence separately from expected-output examples. Include rollback/cleanup instructions for interrupted labs.

## Acceptance and evidence

Lab privilege and destruction scopes are visible; prerequisite checks are read-only; database isolation enforced; cleanup targets only lab-owned resources; expected output never represented as observed.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 008. Turn the outline into three coherent learning paths

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 007 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; BOOK_SPEC.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/READER_PATHS.md; books/inside-orch/editorial/LEARNING_OBJECTIVES.md

## Work to perform

Construct developer, DevOps and architect reading sequences using the fixed 40-chapter outline. Identify a shared foundation, dependencies between chapters, optional advanced branches and checkpoints with observable outcomes. A reader must understand the runtime boundary before encountering sophisticated scheduler, autoscaler or leadership packages.

For each chapter name the prior knowledge, the new mental model, a code-navigation skill and a practical result. Translate vague outcomes such as understand reliability into tasks such as trace a stale report through lifecycle guards or show what is lost after restarting a process. Use a dependency table rather than a decorative linear diagram. Plan cross-references so readers moving through a path can find definitions without duplicate multi-page explanations. Require all paths to encounter resource propagation, persistence and fencing limits. Introduce a single running service that later labs mutate in controlled ways. Include time estimates as editorial estimates rather than measured completion guarantees. Keep navigation and accessibility goals distinct from the project's maturity.

## Acceptance and evidence

All 40 chapters assigned; prerequisites form an acyclic graph; each path includes critical boundaries; outcomes are demonstrable; no path depends on unwritten implementation.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 009. Extract the decisions and tradeoffs behind the code

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 008 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/*DESIGN.md; books/inside-orch/evidence/orch/docs/ARCHITECTURE.md; books/inside-orch/evidence/orch/internal/; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/editorial/DECISION_REGISTER.md; books/inside-orch/validation/intake/decisions.json

## Work to perform

Create an architectural decision register from source and design evidence. Include Docker-first runtime boundaries, polling agents, Go packages, PostgreSQL stores, memory-backed executable composition, desired/actual state, deterministic planning, optimistic concurrency, namespaces, local storage, host ports, optional ingress, and extension interfaces. For every decision record context, observed implementation, alternatives, benefits, costs and unresolved questions.

Do not attribute an author's motivation when only the code is visible. Label your reconstruction as an inference and state the evidence. Explain the costs of simpler orchestration in small clusters without claiming that orch replaces every Kubernetes guarantee. Use concrete scenarios: a lost status response, saturated node, partitioned worker, concurrent operators, failed second GitOps manifest, and process restart. Identify which guarantees require atomic persistence, durable ownership, leases or fencing and which can be demonstrated with current packages. Keep prospective fixes in a separate teaching-design section with a validation plan. These decisions should guide chapter explanations rather than become generic cloud architecture essays.

## Acceptance and evidence

Decisions have code/design anchors; inferred rationale is labeled; tradeoffs use concrete failures; future guarantees are separate from baseline capabilities.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 010. Establish immutable citations and a compact bibliography

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 009 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/commits.json; books/inside-orch/evidence/prompt-commit-map.json; books/inside-orch/editorial/SOURCE_POLICY.md

## Output artifacts

books/inside-orch/editorial/REFERENCES.md; books/inside-orch/validation/intake/reference-register.json

## Work to perform

Define source references for exact code excerpts, historical implementation commits, original prompts, design documents, tests and external documentation. Use full-SHA GitHub blob/commit URLs; include line anchors for excerpts and preserve the SHA that actually contains historical code. Avoid moving main/latest references for facts that must be reproducible. Record retrieval dates for external versioned primary sources.

Build a bibliography only for material the book actually uses. Primary sources may include Go language/runtime documentation, Docker Engine API, PostgreSQL transaction/locking documentation, HTTP specifications, Prometheus guidance and relevant security standards. Retrieve them before making precise external claims. Do not fabricate DOI, ISBN, endpoint, issue or release links. Deduplicate references and give readable labels. A commit title is not a citation for an implementation detail unless the diff/source supports it. Specify how to cite an excerpt, a teaching adaptation and an inference differently. Add an offline navigation route through the bundled snapshot, prompt map and patch corpus when web links are unavailable.

## Acceptance and evidence

All repository SHAs resolve to known corpus objects; excerpt anchors match actual lines; external references are retrieved/primary; no fabricated attribution or moving source links.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 011. Select and lock the book’s source listings

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 010 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/examples/source-excerpts/registry.json; books/inside-orch/scripts/extract_snippets.py; books/inside-orch/evidence/orch/; books/inside-orch/editorial/book-outline.json

## Output artifacts

books/inside-orch/examples/source-excerpts/registry.json; books/inside-orch/validation/intake/excerpt-review.md

## Work to perform

Review the supplied excerpt seeds and extend them chapter by chapter. Choose coherent units: a constructor path, a lifecycle guard, atomic assignment, Docker adoption, rollout calculation, namespace context, policy decision or error boundary. Record exact file, line interval, source SHA, checksum, symbol and teaching purpose. Use books/inside-orch/scripts/extract_snippets.py to regenerate listings from immutable bytes rather than copying code manually.

Keep listings short enough to read, with necessary surrounding context explained in prose. If unrelated lines are omitted, mark the omission as editorial and do not present the result as an exact contiguous excerpt. Do not change identifiers or silently fix a source listing. A simplified or adapted example belongs in teaching-extensions with its own tests and attribution. Avoid embedding actual secrets, tokens or personal metadata. Add companion source links with line ranges and an explanation of how the excerpt participates in the executable. Check that source examples featuring a standalone library do not imply server integration. Give every listing a stable ID for later PDF/HTML/EPUB cross-references.

## Acceptance and evidence

Listings are byte-derived and pinned; checksums match; purpose and runtime scope are documented; adapted code is separately labeled and testable.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 012. Design one progressive case study across the whole book

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 011 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; books/inside-orch/evidence/orch/deployments/examples/; books/inside-orch/evidence/orch/docs/SERVICE_SPEC.md; books/inside-orch/editorial/CAPABILITIES.md

## Output artifacts

books/inside-orch/labs/CASE_STUDY.md; books/inside-orch/labs/case-study-manifest.json

## Work to perform

Choose a small stateless HTTP service and a finite worker/job as the running case study, using existing example specifications where possible. Introduce only the fields supported by the pinned parsers and validation. Carry the same service identity through deploy, scale, rollout, rollback, health failure, drift, node loss, namespace isolation, quota changes, GitOps and observation. Storage experiments use separate explicitly local fixtures.

For every stage record desired changes, expected state transitions, operator command source, telemetry, failure injection and cleanup. Identify which experiments run against the default server, standalone packages or teaching extensions. Add a deliberately resource-constrained scenario that exposes the difference between package planner behavior and MemoryService placement; do not hide it by selecting oversized lab machines. Include a restart scenario that demonstrates state loss before discussing durable store design. Specify how later chapters refer back to earlier observed IDs and logs without relying on an unreproducible environment. Keep results marked expected until executed. Build a small state graph that corresponds to actual lifecycle constants.

## Acceptance and evidence

One coherent case study covers eight lab stages; specs parse at baseline; failures target real paths; runtime/package/extension contexts and cleanup are explicit.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 013. Define the evidence that proves each operational lesson

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 012 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/internal/metrics/; books/inside-orch/evidence/orch/internal/events/; books/inside-orch/evidence/orch/internal/audit/; books/inside-orch/evidence/orch/deploy/monitoring/; books/inside-orch/evidence/orch/docs/OBSERVABILITY.md

## Output artifacts

books/inside-orch/editorial/OBSERVATION_CONTRACT.md; books/inside-orch/labs/observations.json

## Work to perform

List real metrics, events, audit records, API responses and runtime inspections usable in the case study. Trace where each metric/event is emitted and what its absence means. Differentiate control-plane intent, agent report and independently observed container behavior. A healthy process is not proof of convergence; a succeeded controller pass is not proof of durable state.

For each lab set evidence criteria using specific fields and timing boundaries: assignment outcome, stale status rejection, replica health, rollout availability, heartbeat age, failed GitOps sync, quota response, job attempts and actual Docker HostConfig. Inspect dashboards and alerts rather than assuming every panel has a live metric. Identify source-package signals absent from default runtime paths. Define low-cardinality metric labels and token-safe logs with exact redaction limitations. Explain collection interval and stale data when discussing alerts. Create a trace worksheet that correlates service/task/node/deployment IDs across API, event and agent evidence. Keep illustrative output separate from captured output and declare measurement duration/sample size for performance claims.

## Acceptance and evidence

Every observation maps to a real emitted field; intent vs runtime distinguished; no invented metric names; redaction and measurement limits visible.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 014. Build a precise failure and recovery matrix

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 013 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/RELIABILITY.md; books/inside-orch/evidence/orch/docs/CHAOS_TESTING.md; books/inside-orch/evidence/orch/internal/e2e/chaos_test.go; books/inside-orch/editorial/TECHNICAL_AUDIT.md

## Output artifacts

books/inside-orch/editorial/FAILURE_MODEL.md; books/inside-orch/labs/failure-matrix.json

## Work to perform

Enumerate failures by boundary: request validation, state mutation/event append, task claim, image pull, container creation, lost report, probe failure, agent restart, server process restart, daemon outage, heartbeat timeout, partition, duplicate controller, failed GitOps manifest, scheduled-job misfire and migration interruption. Describe the last durable or volatile point and the recovery owner for each.

Separate controller restart, agent restart and whole-server process restart. The existing chaos test reusing MemoryService cannot prove process durability. Node timeout and replacement do not fence an isolated worker; an old container can remain live until connectivity returns. Explain the practical consequence for stateful/single-writer workloads. For each failure define a safe deterministic test, an integration experiment, acceptable outcomes and unresolved gaps. Reconcile claims with actual desired/actual state guards. Do not promise exactly-once execution, zero downtime, atomic GitOps batches, replicated volumes or complete tenant isolation without supporting mechanisms. Use failure windows to motivate future improvements, explicitly outside baseline source.

## Acceptance and evidence

Failure matrix names state ownership and residual live side effects; restart/fencing/atomicity limits explicit; each guarantee has evidence or is labeled unproven.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 015. Map trust boundaries before writing security chapters

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 014 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/internal/auth/; books/inside-orch/evidence/orch/internal/health/; books/inside-orch/evidence/orch/internal/secrets/; books/inside-orch/evidence/orch/internal/gitops/; books/inside-orch/evidence/orch/internal/notifications/; books/inside-orch/evidence/orch/docs/SECURITY_REVIEW.md

## Output artifacts

books/inside-orch/editorial/THREAT_MODEL.md; books/inside-orch/validation/intake/security-boundaries.json

## Work to perform

Identify operator, agent, server, Docker daemon, image registry, Git source, notification receiver, DNS client and database trust boundaries. Trace optional user JWT auth, registration tokens, node credentials, namespace context, secret envelopes, registry auth and debug routes. Describe default development configurations and the conditions under which authenticated behavior is active.

Inspect SSRF validation and actual dialing, DNS resolution, proxy behavior, redirects, notification URLs and GitOps filesystem boundaries. Distinguish source-derived concerns from demonstrated vulnerabilities; propose safe tests using local fakes or loopback fixtures rather than external targets. Treat Docker socket access as host privilege. Explain that namespaces and RBAC are API boundaries, not full kernel/network isolation. Check secret values through logs/errors/events and encryption-key management; encrypted storage does not eliminate plaintext at the execution boundary. Define testable security assertions for admission, redaction, path traversal and unauthorized status reports. Avoid blanket production-hardening claims, hypothetical warnings and unexplained checklists.

## Acceptance and evidence

Trust paths source-traced; default/optional auth visible; SSRF/file-boundary hypotheses labeled and testable; tenant isolation claims scoped; no credential data captured.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 016. Prepare author metadata and an explicit rights record

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 015 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

BOOK_SPEC.md; books/inside-orch/evidence/source-lock.json; books/inside-orch/evidence/orch/go.mod; books/inside-orch/publication/book-metadata.json

## Output artifacts

books/inside-orch/publication/RIGHTS.md; books/inside-orch/publication/NOTICE.md; books/inside-orch/publication/book-metadata.json

## Work to perform

Set author Aleksandar Popovic, website https://www.alekpopovic.com and the canonical title/subtitle from BOOK_SPEC. Record copyright and edition metadata consistently in Markdown, PDF, EPUB and site catalog outputs. This pack has not selected a public manuscript license or assigned a new license to the source repository.

Inspect actual repository license files and dependency notices. GitHub metadata reported no source license at baseline, so public availability alone does not justify an open-source designation. Separate original manuscript prose, exact source excerpts, adaptations, vector brand assets and third-party material. Retain provenance and required notices. If the intended public release license is still unspecified, keep the release licensing decision explicit and unresolved rather than guessing or copying another book's license. Do not fabricate ISBN, publisher approval or professional certifications. Record any external image/font rights used by generated publication assets. Keep the narrative free from workflow instructions while preserving a transparent technical provenance appendix.

## Acceptance and evidence

Author/title metadata consistent; no invented public license/ISBN; all reused materials have provenance; unresolved rights decisions remain clearly recorded for release.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Canonical metadata and license page

Write and synchronize `books/inside-orch/book.json` as the site's canonical metadata source, not only the companion publication JSON. The new catalog entry requires truthful metadata.publication_notes or a source LICENSE.md for its license page. Do not copy Modern CI's CC BY/MIT claims, hardcoded title, edition date or cover into orch. Preserve the explicitly selected rights and author attribution.


---

# 017. Define a readable multi-format book design

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 016 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/evidence/orch/docs/BRAND.md; books/inside-orch/evidence/orch/docs/assets/; books/inside-orch/editorial/book-outline.json; books/inside-orch/publication/book-metadata.json

## Output artifacts

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/style-tokens.json

## Work to perform

Derive the visual identity from orch's existing orbit-and-node vector assets and documented cyan/blue/violet/slate palette. Create a restrained technical-book system for cover, chapter openers, source listings, evidence callouts, tables and diagrams. Preserve long-form readability: generous margins, legible body type, contrasting code panels, accessible links and printable grayscale distinctions.

Define separate print PDF, reflowable EPUB and responsive online-reader rules. Code must not be shrunk to unreadability or clipped; long lines require editorial selection, wrapping that preserves meaning, or a downloadable listing. Tables need repeated headers and may require a different layout on small screens. Give diagrams semantic labels and text alternatives. Keep vectors exact and avoid generated raster diagrams for precise topology. Plan front matter, contents, numbering, bookmarks and cross-reference labels. Review current site catalog/reader conventions before proposing a site-specific adapter; the visible site is not evidence that WordPress is used. Produce a small style specimen and describe how visual QA will be executed.

## Acceptance and evidence

Design tokens trace existing brand; body/code contrast readable; print/reflow/online rules distinct; diagrams accessible; no unverified site technology assumed.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 018. Freeze chapter scope, dependencies and evidence coverage

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 017 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/editorial/book-outline.json; books/inside-orch/editorial/READER_PATHS.md; books/inside-orch/editorial/PROMPT_HISTORY.md; books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/editorial/QUALITY_GATES.md

## Output artifacts

books/inside-orch/editorial/TOC.md; books/inside-orch/editorial/CHAPTER_CONTRACTS.md; books/inside-orch/validation/intake/toc-coverage.json

## Work to perform

Review all 40 chapters and six appendices against the original prompt corpus, implementation map and reader paths. Each chapter needs a distinct motivating problem, exact source targets, a concrete lab or analysis task and an explicit boundary. Ensure all 91 original prompts are covered without demanding one chapter per prompt. Design-only topics should explain decisions and gaps, not pretend to operate absent features.

Reorder only if necessary for prerequisites and retain stable chapter IDs or a documented migration map. The in-memory/runtime-composition boundary must appear early. Check that developers get source walkthroughs, operators get observable recovery procedures and architects get tradeoffs/invariants. Avoid duplicate explanations of authentication, events or lifecycle constants; point to their defining chapter and revisit only when behavior changes. Set word budgets to meet BOOK_SPEC without filler. Establish narrative continuity for the running case study and cross-reference placeholders that resolve to actual future chapter IDs. Record any deferred topics and why. Freeze the contract before writing the chapter prompts.

## Acceptance and evidence

Exactly 40 distinct chapters plus A–F; original prompt coverage complete; prerequisite order coherent; every chapter has specific books/inside-orch/evidence/lab/limits; no ornamental filler.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Canonical reading order

Write `books/inside-orch/manuscript/Book.txt` with exactly 47 relative entries: `00-preface.md`, the 40 `chapters/<slug>.md` entries from the outline in order, then six `appendices/<slug>.md` entries. Paths are relative to the manuscript directory and must resolve inside it with unique stems. The existing Modern CI selection helper rejects nested paths, so orch needs its own safe selection adapter rather than blindly reusing that function. Do not register unfinished paths in the live catalog.


---

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


---

# 020 — Chapter 01: Why Build a Container Orchestrator?

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/01-why-build-a-container-orchestrator.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Define the small-cluster problem, desired-state architecture, and the project’s verified implementation boundary. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Trace a service from API request to Docker container.
- Separate project intent from default binary behavior.
- Explain when a small orchestrator is an appropriate engineering choice.

Use these chapter-specific sections as the narrative spine:

1. **A Small Cluster Is Still a Distributed System**
2. **Who Owns Desired and Observed State?**
3. **What the Default Binary Actually Runs**
4. **The First Capability Boundary**

Open with an operator who needs repeatable deployment on a handful of Docker hosts. Trace the service, task, node, agent, and runtime responsibilities before discussing alternative platforms. Use the real server constructor to establish the book’s baseline. Make the distinction between a useful MVP and a production promise precise enough that all later chapters can refer to it. The reader should leave with a question to ask of every subsystem: where is this behavior connected to the running system?

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [README.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/README.md)
- [AGENTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/AGENTS.md)
- [docs/ARCHITECTURE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ARCHITECTURE.md)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)

Read the original development intent:

- [prompts/00-agents-md-and-architecture-docs.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/00-agents-md-and-architecture-docs.md)
- [prompts/26-senior-distributed-systems-review.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/26-senior-distributed-systems-review.md)

Explain relevant implementation history using these real commits:

- [Add repository agent and architecture docs](https://github.com/alekpopovic/orch/commit/6f90183927991506de435a55582b5c283212ff09); inspect `books/inside-orch/evidence/commit-diffs/6f90183927991506de435a55582b5c283212ff09.patch`.
- [Add control plane REST API](https://github.com/alekpopovic/orch/commit/64a0725387b8130be988948b81774aea7051c718); inspect `books/inside-orch/evidence/commit-diffs/64a0725387b8130be988948b81774aea7051c718.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Draw the Atlas Lab system map and record the pinned source revision.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch01/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Every capability claim has a source classification; MemoryService is named explicitly and the architecture map does not imply PostgreSQL server integration.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch01/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch01/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch01.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch01.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch01.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 020 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 1 - Why Build a Container Orchestrator?`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `01-why-build-a-container-orchestrator` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 021 — Chapter 02: A Repository Built for Reasoning

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/02-a-repository-built-for-reasoning.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Read package boundaries, interfaces, injected dependencies, cancellation rules, and the repository’s engineering contract. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Navigate the actual package tree.
- Identify side-effect boundaries and dependency injection.
- Use deterministic tests and context cancellation as design constraints.

Use these chapter-specific sections as the narrative spine:

1. **The Actual Tree Versus the Intended Layout**
2. **Interfaces at the Side-Effect Boundary**
3. **Cancellation and Time as Dependencies**
4. **The First Focused Test**

Use the repository conventions to explain concrete Go package choices. Contrast the intended directory layout in AGENTS.md with real package paths rather than treating documentation as an automatically accurate map. Follow one consumer-owned interface into its fake and implementation. Explain how context and injected dependencies make a controller testable. Keep the narrative on decisions supported by actual files; avoid introducing a generic clean-architecture taxonomy that obscures this project’s small, cohesive packages.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [AGENTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/AGENTS.md)
- [go.mod](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/go.mod)
- [Makefile](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/Makefile)
- [docs/DEVELOPMENT.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/DEVELOPMENT.md)
- [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)

Read the original development intent:

- [prompts/00-agents-md-and-architecture-docs.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/00-agents-md-and-architecture-docs.md)
- [prompts/01-repository-bootstrap.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/01-repository-bootstrap.md)
- [prompts/21-local-development-environment.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/21-local-development-environment.md)

Explain relevant implementation history using these real commits:

- [Initialize Go orchestrator scaffold](https://github.com/alekpopovic/orch/commit/72f27ed1d81b75e499ee65e0c9779e44b237f814); inspect `books/inside-orch/evidence/commit-diffs/72f27ed1d81b75e499ee65e0c9779e44b237f814.patch`.
- [Add repository agent and architecture docs](https://github.com/alekpopovic/orch/commit/6f90183927991506de435a55582b5c283212ff09); inspect `books/inside-orch/evidence/commit-diffs/6f90183927991506de435a55582b5c283212ff09.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Create a read-only source index and run the prerequisite and build checks.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch02/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Show actual package names rather than copying intended AGENTS layout; explain why internal/docker and internal/health differ from planned directory names.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch02/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch02/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch02.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch02.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch02.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 021 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 2 - A Repository Built for Reasoning`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `02-a-repository-built-for-reasoning` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 022 — Chapter 03: Boot the Lab and Deploy the First Service

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/03-boot-the-lab-and-deploy-the-first-service.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Run the pinned local development path and inspect CLI-visible service, task, and node state. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Build or install the pinned CLI reproducibly.
- Start and tear down the local cluster.
- Read service and task state after deployment.

Use these chapter-specific sections as the narrative spine:

1. **Pinned Prerequisites and Installation**
2. **One Local Server and One Worker**
3. **The First Deployment Timeline**
4. **Cleanup and the Limits of the Demo**

Build the first experiment from the upstream development scripts and http-api manifest. Read each script before quoting its startup and migration behavior. Trace the commands from validation through service/task inspection, scaling, events, logs, and deletion. If authentication or ports differ from the README example, explain the discrepancy with source evidence. The observations should show desired replicas and actual task progression separately, while cleanup should stop only the disposable lab resources created by this chapter.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [README.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/README.md)
- [docs/INSTALLATION.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/INSTALLATION.md)
- [docs/DEVELOPMENT.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/DEVELOPMENT.md)
- [scripts/dev-up.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-up.sh)
- [scripts/dev-down.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-down.sh)
- [deployments/examples/http-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/http-api.yaml)
- [internal/cli/root.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go)

Read the original development intent:

- [prompts/05-cobra-cli.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/05-cobra-cli.md)
- [prompts/21-local-development-environment.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/21-local-development-environment.md)
- [prompts/27-production-documentation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/27-production-documentation.md)
- [prompts/28-mvp-release-preparation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/28-mvp-release-preparation.md)

Explain relevant implementation history using these real commits:

- [Add local development environment](https://github.com/alekpopovic/orch/commit/f7e77377fbc8565d737ad2cdcf2f2e318b03e4fa); inspect `books/inside-orch/evidence/commit-diffs/f7e77377fbc8565d737ad2cdcf2f2e318b03e4fa.patch`.
- [Add Cobra orch CLI](https://github.com/alekpopovic/orch/commit/042a4a44ecfaa884d6173f9d93afafa81a24ea27); inspect `books/inside-orch/evidence/commit-diffs/042a4a44ecfaa884d6173f9d93afafa81a24ea27.patch`.
- [Update v0.3.0 release documentation (#8)](https://github.com/alekpopovic/orch/commit/cbfc94ade5b57e449d6b73bf1485b1c5b1647022); inspect `books/inside-orch/evidence/commit-diffs/cbfc94ade5b57e449d6b73bf1485b1c5b1647022.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Deploy the upstream http-api example, inspect events, scale, collect logs, then remove it.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch03/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: All commands are checked against current CLI behavior; document Docker requirements, port prerequisites, and cleanup; do not invent output transcripts.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch03/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch03/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch03.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch03.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch03.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 022 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 3 - Boot the Lab and Deploy the First Service`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `03-boot-the-lab-and-deploy-the-first-service` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 023 — Chapter 04: Domain Models and State Machines

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/04-domain-models-and-state-machines.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Study service, task, node, deployment, and event types as explicit contracts. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Distinguish desired task status from observed status.
- Explain valid and invalid lifecycle transitions.
- Relate immutable service versions to deployments.

Use these chapter-specific sections as the narrative spine:

1. **Service Intent and Per-Replica Tasks**
2. **Desired Status Versus Actual Status**
3. **Deployment Versions and Transition Owners**
4. **Rejecting an Impossible Transition**

Make the state model teachable through one replica’s complete lifecycle. Use a table to distinguish desired and actual status, and a compact state diagram to show the owners of transitions. Inspect validation and lifecycle tests before drawing arrows. Include an invalid transition and explain the domain error it returns. Explicitly avoid inferring stronger persistence or distributed delivery guarantees from the presence of state types; the chapter is about contracts, their enforcement, and their known scope.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [pkg/types/types.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go)
- [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go)
- [pkg/types/lifecycle_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle_test.go)
- [internal/task/task.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/task/task.go)
- [internal/node/node.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/node.go)
- [docs/STATE_MACHINES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATE_MACHINES.md)

Read the original development intent:

- [prompts/02-core-domain-models.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/02-core-domain-models.md)
- [prompts/29-freeze-api-and-state-machine-contract.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/29-freeze-api-and-state-machine-contract.md)

Explain relevant implementation history using these real commits:

- [Add core domain model types](https://github.com/alekpopovic/orch/commit/c756f9d7f3a46e8bfe4d7bca291d67f6a783553d); inspect `books/inside-orch/evidence/commit-diffs/c756f9d7f3a46e8bfe4d7bca291d67f6a783553d.patch`.
- [Freeze lifecycle state machine contracts](https://github.com/alekpopovic/orch/commit/6526b47f66da88117bab80468ce6b6c711d1e118); inspect `books/inside-orch/evidence/commit-diffs/6526b47f66da88117bab80468ce6b6c711d1e118.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Trace Atlas API lifecycle transitions with a state transition table and one rejected transition test.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch04/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: The diagram includes terminal states and transition ownership; every shown state exists in pinned types and invalid transitions have evidence.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch04/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch04/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch04.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch04.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch04.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 023 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 4 - Domain Models and State Machines`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `04-domain-models-and-state-machines` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 024 — Chapter 05: Service Specifications, Resources, and Ports

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/05-service-specifications-resources-and-ports.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Read declarative service validation, resource quantities, labels, and host-port allocation constraints. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Parse CPU and memory quantities without ambiguity.
- Describe requested resources and placement constraints.
- Predict a public-port collision and validation error.

Use these chapter-specific sections as the narrative spine:

1. **From YAML to a Validated Service**
2. **CPU and Memory in Exact Units**
3. **Labels, Replicas, and Finite Host Ports**
4. **When Admission Is Not Runtime Enforcement**

Work a concrete resource calculation using replicas, millicores, and bytes, then show how parser validation rejects malformed quantities. Use a public-port collision to demonstrate why declarative replicas do not alone create network capacity. Follow relevant fields beyond the specification before claiming Docker CPU or memory enforcement. The live service path and scheduler package can differ, so explicitly state which path each example exercises. Include valid and invalid manifests with a reasoned expected response for each.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [docs/SERVICE_SPEC.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SERVICE_SPEC.md)
- [docs/RESOURCES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RESOURCES.md)
- [pkg/types/types.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go)
- [pkg/types/parsers.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/parsers.go)
- [pkg/types/validation_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/validation_test.go)
- [pkg/types/resources_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/resources_test.go)
- [internal/cli/deploy.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go)
- [deployments/examples/http-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/http-api.yaml)

Read the original development intent:

- [prompts/17-resource-accounting.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/17-resource-accounting.md)
- [prompts/34-port-allocation-and-collision-handling.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/34-port-allocation-and-collision-handling.md)
- [prompts/43-deployment-yaml-schema-and-validation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/43-deployment-yaml-schema-and-validation.md)

Explain relevant implementation history using these real commits:

- [Implement resource accounting](https://github.com/alekpopovic/orch/commit/44b60a210c5a17e444b02d622b6af0c1c11375e2); inspect `books/inside-orch/evidence/commit-diffs/44b60a210c5a17e444b02d622b6af0c1c11375e2.patch`.
- [Add host port allocation awareness](https://github.com/alekpopovic/orch/commit/3bfcef82a54dec457cf9d4187705fa70cc7215cf); inspect `books/inside-orch/evidence/commit-diffs/3bfcef82a54dec457cf9d4187705fa70cc7215cf.patch`.
- [Add service spec validation](https://github.com/alekpopovic/orch/commit/6f7954b8d31b52a7909ebe20d1e22b384af19530); inspect `books/inside-orch/evidence/commit-diffs/6f7954b8d31b52a7909ebe20d1e22b384af19530.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Create good and deliberately invalid Atlas manifests; explain replicas versus finite host-port capacity.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch05/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Resource arithmetic includes units; published host ports are node-scoped; invalid manifests are tested through the actual parser.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch05/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch05/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch05.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch05.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch05.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 024 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 5 - Service Specifications, Resources, and Ports`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `05-service-specifications-resources-and-ports` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 025 — Chapter 06: Follow One Request Through the Control Plane

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/06-follow-one-request-through-the-control-plane.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is I — Establish the System. Focus: Walk the default server assembly, in-memory control plane, controller loops, and runtime integration gaps. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Locate the actual control-plane constructor.
- Explain how API mutations and controller iterations interact.
- Identify state that is lost on a default server restart.

Use these chapter-specific sections as the narrative spine:

1. **Server Assembly and Active State Ownership**
2. **Mutation Paths and Controller Loops**
3. **The MemoryService Restart Experiment**
4. **Integration Gaps as Architectural Evidence**

Read run in the server entry point line by line at the important construction and loop boundaries. Distinguish immediately performed MemoryService operations from background scheduler, rollout, node-monitor, GitOps, and other loops. State the exact integration status of store, leadership, and autoscaling packages. A restart experiment should compare surviving Docker containers with lost in-memory service knowledge; it must not masquerade as a database recovery test. Resolve stale roadmap statements by citing executable wiring and preserve the discrepancy in the ledger.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go)
- [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go)
- [docs/ARCHITECTURE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ARCHITECTURE.md)

Read the original development intent:

- [prompts/04-api-server-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/04-api-server-v1.md)
- [prompts/10-reconciler-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/10-reconciler-v1.md)
- [prompts/25-failure-modes-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/25-failure-modes-hardening.md)

Explain relevant implementation history using these real commits:

- [Add control plane REST API](https://github.com/alekpopovic/orch/commit/64a0725387b8130be988948b81774aea7051c718); inspect `books/inside-orch/evidence/commit-diffs/64a0725387b8130be988948b81774aea7051c718.patch`.
- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Restart the local server in a disposable lab and contrast surviving Docker containers with lost control-plane state.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch06/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Trace current call sites; do not claim DB URL configuration enables persistent server state; classify restart observations as measured or expected.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch06/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch06/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch06.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch06.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch06.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 025 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 6 - Follow One Request Through the Control Plane`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `06-follow-one-request-through-the-control-plane` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 026 — Chapter 07: HTTP Contracts and Compatible APIs

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/07-http-contracts-and-compatible-apis.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Study middleware, validation, stable error responses, versioned routes, and the shared API contract. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Follow validation and authorization at the HTTP boundary.
- Map domain errors to stable client-facing errors.
- Check OpenAPI documentation against route behavior.

Use these chapter-specific sections as the narrative spine:

1. **Request Boundaries and Middleware Order**
2. **Domain Errors as Public JSON Contracts**
3. **The v1 Compatibility Surface**
4. **OpenAPI and the Client Agree—or Differ**

Follow one service creation request through decode, validation, authorization, domain mutation, and response translation. Inspect a rejected request rather than only the happy path. Explain versioned routes and stable structured errors with the actual response shapes. Compare OpenAPI and hand-written client definitions against handlers and tests, recording mismatches. Avoid saying a client is generated unless the repository proves that workflow. Use a compact compatibility example to show why additive schema changes are easier to support than renamed response fields.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go)
- [internal/api/versioning.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/versioning.go)
- [internal/apperrors/errors.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/apperrors/errors.go)
- [internal/api/api_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api_test.go)
- [api/openapi.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/api/openapi.yaml)
- [api/openapi_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/api/openapi_test.go)
- [pkg/client/client.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/client/client.go)
- [docs/API.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/API.md)
- [docs/API_VERSIONING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/API_VERSIONING.md)

Read the original development intent:

- [prompts/04-api-server-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/04-api-server-v1.md)
- [prompts/45-structured-error-model.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/45-structured-error-model.md)
- [prompts/61-openapi-specification-and-generated-clients.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/61-openapi-specification-and-generated-clients.md)
- [prompts/62-api-versioning-strategy.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/62-api-versioning-strategy.md)

Explain relevant implementation history using these real commits:

- [Add structured error model](https://github.com/alekpopovic/orch/commit/b5d4573f8fa5d56a5dcfde609e3794e93644a39d); inspect `books/inside-orch/evidence/commit-diffs/b5d4573f8fa5d56a5dcfde609e3794e93644a39d.patch`.
- [Add OpenAPI spec and client](https://github.com/alekpopovic/orch/commit/f94414db486b96e7088fccc8c4c502a1fa616d38); inspect `books/inside-orch/evidence/commit-diffs/f94414db486b96e7088fccc8c4c502a1fa616d38.patch`.
- [Implement API policies and namespaces](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014); inspect `books/inside-orch/evidence/commit-diffs/9e78fed31df03d7a985a9f4ceae4770739b05014.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Call the API with valid and invalid requests and add a book-side contract smoke test using the public client.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch07/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: OpenAPI versus route gaps go into the contradiction ledger; public and internal agent contracts remain distinct; additive compatibility is demonstrated.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch07/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch07/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch07.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch07.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch07.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 026 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 7 - HTTP Contracts and Compatible APIs`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `07-http-contracts-and-compatible-apis` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 027 — Chapter 08: A CLI That Operators Can Automate

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/08-a-cli-that-operators-can-automate.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Explore Cobra command composition, configuration precedence, JSON output, and deployment parsing. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops.

Learning outcomes:

- Explain flag, environment, configuration, and default precedence.
- Use stable JSON output for a small automation script.
- Distinguish local validation from server-side acceptance.

Use these chapter-specific sections as the narrative spine:

1. **Cobra Composition and Local Validation**
2. **Configuration Precedence You Can Predict**
3. **JSON Output for Operator Automation**
4. **Failures That Belong in Exit Status**

Use one concrete operator task to connect command composition, configuration, and the HTTP client. Work through a conflicting flag, environment variable, and YAML setting so readers can predict precedence. Read output fields before writing a shell automation example; JSON field guesses are not acceptable. Explain where local parsing ends and server admission begins. Quote only supported command switches. The status script should report an actionable failure without leaking credentials or assuming the CLI has a default server URL.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/cli/root.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go)
- [internal/cli/root_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root_test.go)
- [internal/cli/client.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/client.go)
- [internal/cli/deploy.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go)
- [internal/cli/output.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/output.go)
- [internal/config/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go)
- [docs/CLI.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CLI.md)
- [docs/CONFIGURATION.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CONFIGURATION.md)

Read the original development intent:

- [prompts/05-cobra-cli.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/05-cobra-cli.md)
- [prompts/43-deployment-yaml-schema-and-validation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/43-deployment-yaml-schema-and-validation.md)
- [prompts/44-config-management-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/44-config-management-hardening.md)

Explain relevant implementation history using these real commits:

- [Add Cobra orch CLI](https://github.com/alekpopovic/orch/commit/042a4a44ecfaa884d6173f9d93afafa81a24ea27); inspect `books/inside-orch/evidence/commit-diffs/042a4a44ecfaa884d6173f9d93afafa81a24ea27.patch`.
- [Harden config management](https://github.com/alekpopovic/orch/commit/a4844c571a0ddf33879556413a62d49a408609e3); inspect `books/inside-orch/evidence/commit-diffs/a4844c571a0ddf33879556413a62d49a408609e3.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Write an Atlas status script that uses current JSON fields and reports actionable failures.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch08/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Run the exact illustrated commands; do not introduce unsupported switches; examples redact tokens and do not assume an implicit server URL.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch08/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch08/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch08.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch08.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch08.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 027 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 8 - A CLI That Operators Can Automate`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `08-a-cli-that-operators-can-automate` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 028 — Chapter 09: Persistence, Transactions, and Optimistic Concurrency

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/09-persistence-transactions-and-optimistic-concurrency.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Read PostgreSQL store interfaces and transactions while distinguishing them from the default in-memory server. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Identify transaction boundaries and optimistic conflict checks.
- Explain store integration test isolation.
- Distinguish persisted schemas from integrated production durability.

Use these chapter-specific sections as the narrative spine:

1. **The Store Contract and PostgreSQL Schema**
2. **Transactional Boundaries and Conflict Errors**
3. **Optimistic Writes Under Contention**
4. **Why the Default Server Is Still Not Durable**

Use one schema row and store method to explain keys, indexes, UTC timestamps, and optimistic concurrency. Inspect the transaction changes introduced during the store audit and compare current behavior with historical code. Demonstrate a conflict in a disposable database when prerequisites allow. Explain that migration and PostgreSQL store tests do not wire persistence into orch-server. Include a short design exercise for durable server composition, clearly marked as a teaching extension whose correctness depends on more than changing one constructor.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/store/store.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/store.go)
- [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go)
- [internal/store/postgres_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres_test.go)
- [internal/store/errors.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/errors.go)
- [migrations/000001_initial_schema.up.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000001_initial_schema.up.sql)
- [migrations/000001_initial_schema.down.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000001_initial_schema.down.sql)
- [docs/MIGRATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MIGRATIONS.md)

Read the original development intent:

- [prompts/03-postgresql-schema-and-store-layer.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/03-postgresql-schema-and-store-layer.md)
- [prompts/24-idempotency-audit.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/24-idempotency-audit.md)
- [prompts/30-transaction-boundaries-audit.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/30-transaction-boundaries-audit.md)

Explain relevant implementation history using these real commits:

- [Add PostgreSQL persistence layer](https://github.com/alekpopovic/orch/commit/7eba6544ffe2eba41b81faa811e899faf28b77a2); inspect `books/inside-orch/evidence/commit-diffs/7eba6544ffe2eba41b81faa811e899faf28b77a2.patch`.
- [Add transaction boundaries for store operations](https://github.com/alekpopovic/orch/commit/72fd9baff0bbfde49574257380bcd8f747cc2070); inspect `books/inside-orch/evidence/commit-diffs/72fd9baff0bbfde49574257380bcd8f747cc2070.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run store integration tests against a disposable PostgreSQL database and examine a conflicting write.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch09/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Database tests may reapply down/up migrations and require disposable data; show actual transaction code; server wiring stays an explicitly separate architectural exercise.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch09/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch09/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch09.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch09.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch09.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 028 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 9 - Persistence, Transactions, and Optimistic Concurrency`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `09-persistence-transactions-and-optimistic-concurrency` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 029 — Chapter 10: A Deterministic Scheduler

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/10-a-deterministic-scheduler.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Read placement order, eligibility checks, capacity accounting, and concurrent assignment safety. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Explain deterministic ordering and tie-breaking.
- Check labels, status, resources, ports, and storage topology.
- Identify the persistence conflict path during assignment.

Use these chapter-specific sections as the narrative spine:

1. **Candidate Ordering and Deterministic Choice**
2. **Ready Nodes, Labels, Capacity, and Ports**
3. **One Assignment Under Concurrent Work**
4. **Planner Guarantees Versus Live Placement**

Calculate an assignment by hand for three fake nodes, including an ineligible node and a resource or port exhaustion case. Tie the calculation to actual sorting and eligibility code. Explain how assignment persistence handles concurrency and conflicts. Compare scheduler package behavior with MemoryService’s normal service placement before claiming production enforcement of constraints. Inspect seeded property tests as additional invariant evidence. The reader should be able to name both the guarantee proved by the planner and the runtime path still needing verification.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go)
- [internal/scheduler/scheduler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler_test.go)
- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/scheduler/workloads_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/workloads_test.go)
- [docs/SCHEDULER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SCHEDULER.md)
- [docs/RESOURCES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RESOURCES.md)

Read the original development intent:

- [prompts/09-scheduler-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/09-scheduler-v1.md)
- [prompts/17-resource-accounting.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/17-resource-accounting.md)
- [prompts/31-scheduler-concurrency-safety.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/31-scheduler-concurrency-safety.md)

Explain relevant implementation history using these real commits:

- [Implement scheduler v1](https://github.com/alekpopovic/orch/commit/fce0a657651c00ffb697bf4a4aba12d0b171f463); inspect `books/inside-orch/evidence/commit-diffs/fce0a657651c00ffb697bf4a4aba12d0b171f463.patch`.
- [Add scheduler concurrency-safe assignment](https://github.com/alekpopovic/orch/commit/1a1c216e8cfb442465f4d3c2c114d20da0342795); inspect `books/inside-orch/evidence/commit-diffs/1a1c216e8cfb442465f4d3c2c114d20da0342795.patch`.
- [Add host port allocation awareness](https://github.com/alekpopovic/orch/commit/3bfcef82a54dec457cf9d4187705fa70cc7215cf); inspect `books/inside-orch/evidence/commit-diffs/3bfcef82a54dec457cf9d4187705fa70cc7215cf.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Build a tiny fake-node placement experiment with valid, exhausted, and conflicting nodes.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch10/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Calculate one complete placement by hand and confirm with a test; task assignment is unique; resource and port claims are not described as Docker enforcement.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch10/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch10/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch10.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch10.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch10.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 029 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 10 - A Deterministic Scheduler`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `10-a-deterministic-scheduler` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 030 — Chapter 11: Reconciliation as Repeated Convergence

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/11-reconciliation-as-repeated-convergence.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Explain creation, scale-down, restart policy, soft deletion, and restart idempotency. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Separate reconciliation decisions from placement and runtime side effects.
- Demonstrate repeated RunOnce convergence.
- Handle failed tasks and service soft deletion.

Use these chapter-specific sections as the narrative spine:

1. **Replica Convergence Without Docker Calls**
2. **Repeated Iterations and Restart Idempotency**
3. **Failed Tasks, Restart Policy, and Scale-Down**
4. **How This Controller Is Invoked**

Follow a service from too few replicas to a stable desired count, then repeat the iteration and prove no duplicate work appears. Use the restart-hardening diff to explain transitional tasks and failed-task replacement. Keep scheduling and Docker side effects outside reconciliation ownership. Examine the default service mutation path instead of assuming every package runs as an independent loop. Clarify whether a test restarts a controller while reusing memory or restarts an entire process with persisted state; these demonstrate materially different guarantees.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/reconciler/reconciler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler_test.go)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [docs/RECONCILER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md)

Read the original development intent:

- [prompts/10-reconciler-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/10-reconciler-v1.md)
- [prompts/24-idempotency-audit.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/24-idempotency-audit.md)
- [prompts/32-reconciler-idempotency-under-restart.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/32-reconciler-idempotency-under-restart.md)

Explain relevant implementation history using these real commits:

- [Implement service reconciler](https://github.com/alekpopovic/orch/commit/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3); inspect `books/inside-orch/evidence/commit-diffs/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3.patch`.
- [Harden reconciler restart idempotency](https://github.com/alekpopovic/orch/commit/a11cec091a69720c14b9713d8be68f38fe6df332); inspect `books/inside-orch/evidence/commit-diffs/a11cec091a69720c14b9713d8be68f38fe6df332.patch`.
- [Harden task state idempotency](https://github.com/alekpopovic/orch/commit/316ba80ac1ea7ba465f1b0826b655233a651c043); inspect `books/inside-orch/evidence/commit-diffs/316ba80ac1ea7ba465f1b0826b655233a651c043.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Apply the same desired Atlas replica count repeatedly in deterministic tests and verify no duplicate tasks.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch11/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Show what each repeated iteration reads and writes; account for transitional tasks; document the default server’s actual invocation path rather than assuming a wired standalone loop.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch11/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch11/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch11.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch11.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch11.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 030 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 11 - Reconciliation as Repeated Convergence`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `11-reconciliation-as-repeated-convergence` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 031 — Chapter 12: Idempotent Docker Operations and Drift

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/12-idempotent-docker-operations-and-drift.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Study the typed Docker adapter, managed labels, fake runtime, cleanup boundaries, and external container drift. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Identify idempotency keys and managed-container labels.
- Explain how repeated create/start/remove calls converge.
- Separate unmanaged containers from safe cleanup candidates.

Use these chapter-specific sections as the narrative spine:

1. **A Typed Runtime Boundary**
2. **Managed Labels as Resource Identity**
3. **Repeated Create, Start, Stop, and Remove**
4. **Drift From Manual Docker Changes**

Read the actual Runtime interface and managed-label lookup logic before presenting idempotency. Show a duplicate operation through FakeRuntime, then compare the adapter’s Docker behavior. Inject a manually stopped or missing container and trace the agent’s repair decision. Explain what happens to unmanaged host containers and why broad cleanup is unsafe. Treat Docker socket access as a privilege boundary, not an implementation convenience. Every listing should either be exact upstream code or a separately compiled and clearly named teaching test.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [internal/docker/docker_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker_test.go)
- [internal/docker/fake.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go)
- [internal/docker/fake_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake_test.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [docs/AGENT.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AGENT.md)

Read the original development intent:

- [prompts/06-docker-engine-runtime-wrapper.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/06-docker-engine-runtime-wrapper.md)
- [prompts/33-fake-runtime-for-deterministic-tests.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/33-fake-runtime-for-deterministic-tests.md)
- [prompts/41-manual-docker-drift-reconciliation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/41-manual-docker-drift-reconciliation.md)

Explain relevant implementation history using these real commits:

- [Add Docker Engine runtime](https://github.com/alekpopovic/orch/commit/2969dfcebd0b15dea99cdf97b5ccdd1ddfd36b41); inspect `books/inside-orch/evidence/commit-diffs/2969dfcebd0b15dea99cdf97b5ccdd1ddfd36b41.patch`.
- [Add deterministic fake container runtime](https://github.com/alekpopovic/orch/commit/c69f9ffa830284692aabf9e65ab9eb1f79d3a114); inspect `books/inside-orch/evidence/commit-diffs/c69f9ffa830284692aabf9e65ab9eb1f79d3a114.patch`.
- [Add Docker drift reconciliation](https://github.com/alekpopovic/orch/commit/cf9769553d6599d798fafaffe1495d3d739fe993); inspect `books/inside-orch/evidence/commit-diffs/cf9769553d6599d798fafaffe1495d3d739fe993.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Repeat runtime operations through FakeRuntime and inject a missing or manually stopped managed container.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch12/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use actual Runtime methods and labels; drift repair respects task identity; no example removes unrelated host containers.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch12/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch12/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch12.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch12.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch12.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 031 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 12 - Idempotent Docker Operations and Drift`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `12-idempotent-docker-operations-and-drift` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 032 — Chapter 13: Agents, Heartbeats, and Task Reports

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/13-agents-heartbeats-and-task-reports.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Trace registration, heartbeat, polling, local reconciliation, and status reporting. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Follow agent bootstrap and credential use.
- Explain agent versus server decision ownership.
- Interpret repeated task reports and heartbeat failure.

Use these chapter-specific sections as the narrative spine:

1. **Enrollment and Agent Credentials**
2. **Heartbeat, Polling, and Assigned Tasks**
3. **Local Container Convergence and Reports**
4. **Dropped Reports and Cancellation**

Use one node registration and task assignment to explain the server/agent protocol. Trace what the agent controls locally and what remains a server decision. Follow bootstrap token exchange, credential reuse, and status updates from code rather than inventing a transport guarantee. Model a lost report and repeated polling in deterministic tests. Explain that agent authentication is not mTLS, that task reporting is not exactly-once delivery, and that a worker with Docker access belongs to the trusted computing base.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [cmd/orch-agent/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-agent/main.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [internal/agent/agent_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent_test.go)
- [internal/auth/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go)
- [internal/controlplane/agent_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/agent_test.go)
- [docs/AGENT.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AGENT.md)

Read the original development intent:

- [prompts/07-worker-agent-registration-and-heartbeat.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/07-worker-agent-registration-and-heartbeat.md)
- [prompts/08-task-assignment-between-server-and-agent.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/08-task-assignment-between-server-and-agent.md)
- [prompts/19-agent-security-bootstrap.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/19-agent-security-bootstrap.md)

Explain relevant implementation history using these real commits:

- [Add agent registration and heartbeat flow](https://github.com/alekpopovic/orch/commit/5cf9213849164ce1bebc4e042cc37bf5553c2427); inspect `books/inside-orch/evidence/commit-diffs/5cf9213849164ce1bebc4e042cc37bf5553c2427.patch`.
- [Add agent task assignment reconciliation](https://github.com/alekpopovic/orch/commit/239eb6abab67773e20a18944ac38e2589802946a); inspect `books/inside-orch/evidence/commit-diffs/239eb6abab67773e20a18944ac38e2589802946a.patch`.
- [Improve agent authentication](https://github.com/alekpopovic/orch/commit/4f25e78c229ba040c07a84801490485b5a0cbb2e); inspect `books/inside-orch/evidence/commit-diffs/4f25e78c229ba040c07a84801490485b5a0cbb2e.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Observe one Atlas worker agent and simulate dropped reports using deterministic fakes.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch13/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Task status updates are grounded in request types; explain retry and cancellation behavior without implying exactly-once delivery or mTLS.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch13/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch13/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch13.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch13.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch13.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 032 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 13 - Agents, Heartbeats, and Task Reports`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `13-agents-heartbeats-and-task-reports` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 033 — Chapter 14: Health Checks That Respect Trust Boundaries

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/14-health-checks-that-respect-trust-boundaries.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is II — Implement the Core. Focus: Read HTTP/TCP health checks, timeout behavior, status transitions, and SSRF controls. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Distinguish process running from healthy service state.
- Explain timeout, retry, and health reporting semantics.
- Demonstrate allowed and rejected probe targets.

Use these chapter-specific sections as the narrative spine:

1. **Running Is Not Healthy**
2. **HTTP and TCP Probe Decisions**
3. **Timeouts and Repeated Health Reports**
4. **SSRF Protection With Explicit Limits**

Start with a container that is running while its endpoint is unavailable. Follow HTTP and TCP probe configuration, timeout handling, and status reporting through implementation and tests. Read the SSRF hardening diff and enumerate the actual checks on targets and redirects. Demonstrate rejection through fakes or safe local fixtures without contacting metadata endpoints. Do not turn application health checks into a complete networking isolation claim. Include a failure timeline showing when an unhealthy observation can affect rollout or discovery behavior.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/health/health.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go)
- [internal/health/health_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health_test.go)
- [docs/HEALTHCHECKS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/HEALTHCHECKS.md)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)
- [prompts/53-healthcheck-ssrf-protection.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/53-healthcheck-ssrf-protection.md)

Read the original development intent:

- [prompts/11-health-checker.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/11-health-checker.md)
- [prompts/53-healthcheck-ssrf-protection.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/53-healthcheck-ssrf-protection.md)

Explain relevant implementation history using these real commits:

- [Add task health checks](https://github.com/alekpopovic/orch/commit/ee067bd0f02566eb600031a0cb81f25919d52445); inspect `books/inside-orch/evidence/commit-diffs/ee067bd0f02566eb600031a0cb81f25919d52445.patch`.
- [Harden healthcheck SSRF protection](https://github.com/alekpopovic/orch/commit/f92f0a4fcfd760cbc9f850ab4c2e3e6d5dc8a081); inspect `books/inside-orch/evidence/commit-diffs/f92f0a4fcfd760cbc9f850ab4c2e3e6d5dc8a081.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Inject healthy, timeout, and forbidden-target probes for Atlas API without contacting metadata services.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch14/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: SSRF examples use fake network/probe boundaries; capture actual allow/deny conditions and acknowledge remaining host-network risks.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch14/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch14/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch14.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch14.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch14.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 033 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 14 - Health Checks That Respect Trust Boundaries`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `14-health-checks-that-respect-trust-boundaries` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

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


---

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


---

# 036 — Chapter 17: Rolling Updates and Rollback Invariants

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/17-rolling-updates-and-rollback-invariants.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Explore service versions, deployment locks, max surge, max unavailable, and rollback state machines. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Compute rollout availability and surge limits.
- Explain failed target versions and previous successful versions.
- Reject conflicting user mutations during a deployment.

Use these chapter-specific sections as the narrative spine:

1. **Service Versions and Deployment Ownership**
2. **Max Surge and Max Unavailable Arithmetic**
3. **Failed Targets and Previous Successful Versions**
4. **Locks Against Conflicting User Actions**

Work a rolling-update calculation with concrete replica, surge, and availability values. Trace the deployment controller’s decisions over successive iterations, including one unhealthy target. Read the rollback and operation-lock tests before claiming a safe return to an earlier version. Explain which user actions are blocked while rollout proceeds. Address the failure window between observed health and routing reality; the chapter must not promise uninterrupted traffic solely because the controller respects its count invariant. Record an observed or expected failure timeline for the Atlas workload.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go)
- [internal/rollout/rollout_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout_test.go)
- [internal/controlplane/rollback_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/rollback_test.go)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go)
- [docs/ROLLOUTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ROLLOUTS.md)

Read the original development intent:

- [prompts/14-rolling-update-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/14-rolling-update-v1.md)
- [prompts/15-rollback-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/15-rollback-v1.md)
- [prompts/42-deployment-lock-and-concurrent-user-operations.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/42-deployment-lock-and-concurrent-user-operations.md)

Explain relevant implementation history using these real commits:

- [Implement rolling service rollouts](https://github.com/alekpopovic/orch/commit/de5900bced92ad9d5786cd258ff7941d67369d33); inspect `books/inside-orch/evidence/commit-diffs/de5900bced92ad9d5786cd258ff7941d67369d33.patch`.
- [Implement service rollback support](https://github.com/alekpopovic/orch/commit/430a061fe7f01df966e33d0b86654c627b7d5e39); inspect `books/inside-orch/evidence/commit-diffs/430a061fe7f01df966e33d0b86654c627b7d5e39.patch`.
- [Add service operation locks](https://github.com/alekpopovic/orch/commit/5bfb4ac394a609469263de9e14d25d5c2660ee8f); inspect `books/inside-orch/evidence/commit-diffs/5bfb4ac394a609469263de9e14d25d5c2660ee8f.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Roll Atlas API forward, inject an unhealthy target, and trace a rollback in fake and optional Docker lab modes.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch17/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Include invariant arithmetic and one failure timeline; no zero-downtime guarantee exceeds tested health and routing behavior.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch17/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch17/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch17.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch17.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch17.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 036 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 17 - Rolling Updates and Rollback Invariants`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `17-rolling-updates-and-rollback-invariants` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 037 — Chapter 18: Safe Deletion and Resource Cleanup

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/18-safe-deletion-and-resource-cleanup.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Follow deleting versus deleted services, task stop/remove behavior, finalization, and failures. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain why removal is a workflow rather than one HTTP delete.
- Trace cleanup ownership and retry behavior.
- Identify resource leaks and safe finalization conditions.

Use these chapter-specific sections as the narrative spine:

1. **Soft Deletion Is a State Machine**
2. **Stop and Remove Ownership**
3. **Retries After Partial Cleanup**
4. **When Finalization Is Safe**

Open with an operator deleting a service while one worker fails during container removal. Follow the service deleting state, desired task changes, agent stop/remove attempts, and final deleted condition. Compare safe-deletion introduction with later failure hardening. Repeated delete and remove calls should demonstrate convergence without duplicate or unrelated resource removal. Explain any leak or ambiguous window directly. The lab uses disposable resources and fake failures; it must not provide an indiscriminate Docker prune recipe as a shortcut for missing cleanup logic.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [docs/RECONCILER.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RECONCILER.md)
- [docs/RELIABILITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RELIABILITY.md)

Read the original development intent:

- [prompts/16-safe-service-deletion-and-cleanup.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/16-safe-service-deletion-and-cleanup.md)
- [prompts/25-failure-modes-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/25-failure-modes-hardening.md)

Explain relevant implementation history using these real commits:

- [Implement safe service deletion](https://github.com/alekpopovic/orch/commit/2084f5f77bd35ba2a4114d29c7e5588c0fd1f3e7); inspect `books/inside-orch/evidence/commit-diffs/2084f5f77bd35ba2a4114d29c7e5588c0fd1f3e7.patch`.
- [Improve failure recovery behavior](https://github.com/alekpopovic/orch/commit/66cfb7049fc1fbceeec9e36a7067febe8cbab698); inspect `books/inside-orch/evidence/commit-diffs/66cfb7049fc1fbceeec9e36a7067febe8cbab698.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Delete Atlas API while injecting one remove failure; inspect repeated cleanup attempts.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch18/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Distinguish desired deletion from confirmed runtime removal; demonstrate repeated calls and avoid destructive force-cleanup recipes.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch18/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch18/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch18.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch18.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch18.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 037 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 18 - Safe Deletion and Resource Cleanup`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `18-safe-deletion-and-resource-cleanup` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 038 — Chapter 19: Offline Nodes, Draining, and Rescheduling

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/19-offline-nodes-draining-and-rescheduling.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Read heartbeat expiry, node statuses, drain/uncordon operations, and workload rescheduling safety. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Interpret stale heartbeat transitions.
- Explain why drain differs from immediate node deletion.
- Reason about replacement tasks and partition uncertainty.

Use these chapter-specific sections as the narrative spine:

1. **Heartbeat Expiry and Offline Status**
2. **Drain Versus Node Disappearance**
3. **Replacement Tasks and Rescheduling**
4. **Partitions Without a Fencing Promise**

Differentiate planned node maintenance from an unresponsive worker. Read the heartbeat monitor and its actual server wiring, correcting roadmap documentation that calls monitoring future work. Trace drain, reschedule, and uncordon behavior with tests. Include a partition where the server considers a node offline but the old container may continue running. Do not claim fencing unless runtime control and code prove it. Show the operator’s observations, abort criteria, and cleanup for a single disposable agent pause rather than a production host shutdown.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/node/monitor.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/monitor.go)
- [internal/node/monitor_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/node/monitor_test.go)
- [internal/controlplane/drain_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/drain_test.go)
- [internal/controlplane/offline_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/offline_test.go)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go)
- [docs/OPERATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OPERATIONS.md)

Read the original development intent:

- [prompts/39-node-drain-and-reschedule.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/39-node-drain-and-reschedule.md)
- [prompts/40-node-offline-detection-and-recovery.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/40-node-offline-detection-and-recovery.md)

Explain relevant implementation history using these real commits:

- [Add node drain rescheduling](https://github.com/alekpopovic/orch/commit/42d4caa4451f4dea24113d48eb1e9e47f2cef558); inspect `books/inside-orch/evidence/commit-diffs/42d4caa4451f4dea24113d48eb1e9e47f2cef558.patch`.
- [Add node offline monitor](https://github.com/alekpopovic/orch/commit/a5d4bfb37f70a3119bc6e2d49f8fefc5a1c748a5); inspect `books/inside-orch/evidence/commit-diffs/a5d4bfb37f70a3119bc6e2d49f8fefc5a1c748a5.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Pause a disposable Atlas agent and perform a deterministic drain/reschedule trace.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch19/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Correct stale docs that call node monitoring unimplemented; include a partition case and clearly identify what orch cannot fence on an isolated worker.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch19/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch19/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch19.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch19.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch19.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 038 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 19 - Offline Nodes, Draining, and Rescheduling`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `19-offline-nodes-draining-and-rescheduling` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 039 — Chapter 20: Endpoint Discovery and Internal DNS

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/20-endpoint-discovery-and-internal-dns.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Study endpoint filtering, namespace names, host addresses and published ports, DNS TTL, and unhealthy endpoints. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain endpoint identity and health filtering.
- Distinguish DNS names from stable virtual IPs.
- Reason about stale caches and rescheduled endpoints.

Use these chapter-specific sections as the narrative spine:

1. **Endpoint Sets and Health Filtering**
2. **Namespace Names and DNS Records**
3. **Node Addresses Still Need Ports**
4. **Rescheduling, TTL, and Stale Clients**

Connect discovery responses to task IDs, node advertise addresses, public ports, versions, and health. Use exact filtering conditions and include_unhealthy behavior. Explain that DNS names resolve to node addresses and do not create stable service virtual IPs. Work through one rescheduled endpoint with a cached record and explicit TTL. Do not imply overlay networking or Kubernetes API compatibility. The lab should compare healthy and unhealthy task sets with deterministic fixtures and optionally query the upstream local DNS compose example.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/discovery/discovery.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery.go)
- [internal/discovery/discovery_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery_test.go)
- [internal/dns/server.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server.go)
- [internal/dns/server_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server_test.go)
- [docs/SERVICE_DISCOVERY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SERVICE_DISCOVERY.md)
- [deployments/examples/internal-dns-compose.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/internal-dns-compose.yaml)

Read the original development intent:

- [prompts/35-basic-service-discovery.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/35-basic-service-discovery.md)
- [prompts/78-internal-dns-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/78-internal-dns-mvp.md)

Explain relevant implementation history using these real commits:

- [Add basic service discovery](https://github.com/alekpopovic/orch/commit/03f8c30f6df8d6eb9abadb729b9a92cf7f460c4a); inspect `books/inside-orch/evidence/commit-diffs/03f8c30f6df8d6eb9abadb729b9a92cf7f460c4a.patch`.
- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Query Atlas endpoints and internal DNS under healthy and unhealthy fake task states.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch20/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Explain DNS returns node addresses and clients still need ports; no Kubernetes compatibility, overlay, VIP, or automatic cross-node networking claim.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch20/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch20/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch20.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch20.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch20.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 039 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 20 - Endpoint Discovery and Internal DNS`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `20-endpoint-discovery-and-internal-dns` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 040 — Chapter 21: Ingress, Host Networking, and the Overlay Roadmap

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/21-ingress-host-networking-and-the-overlay-roadmap.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Read Traefik configuration and current host-port traffic flow before evaluating future overlay/CNI design. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: devops, architect.

Learning outcomes:

- Trace ingress to node-level published ports.
- Identify collisions, topology exposure, and routing limitations.
- Evaluate an overlay/CNI design without claiming it is built.

Use these chapter-specific sections as the narrative spine:

1. **The Current Host-Port Packet Path**
2. **Traefik Routers and Services**
3. **Failures at Node and Gateway Boundaries**
4. **An Overlay or CNI Design Is a Separate Step**

Draw current ingress from the client through Traefik to a node’s published port and the workload container. Verify generated router and service settings against code and examples. Explain scarce host ports, topology exposure, and what changes on reschedule. Only then discuss the overlay/CNI design document, marking every new addressing, identity, policy, and plugin concept as proposed. Include a gateway or missing-endpoint failure case. The lab must use current manifests and routing configuration; it cannot silently implement an overlay to make the narrative appear complete.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/traefik/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go)
- [internal/traefik/config_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config_test.go)
- [docs/TRAEFIK.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/TRAEFIK.md)
- [docs/NETWORKING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NETWORKING.md)
- [docs/NETWORKING_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NETWORKING_DESIGN.md)
- [deployments/examples/routed-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/routed-api.yaml)
- [deployments/examples/traefik-demo.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/traefik-demo.yaml)

Read the original development intent:

- [prompts/36-traefik-integration.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/36-traefik-integration.md)
- [prompts/77-cni-advanced-networking-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/77-cni-advanced-networking-design.md)

Explain relevant implementation history using these real commits:

- [Add optional Traefik integration](https://github.com/alekpopovic/orch/commit/ea0760e8201c842371caf6671a90bcfeb90197bb); inspect `books/inside-orch/evidence/commit-diffs/ea0760e8201c842371caf6671a90bcfeb90197bb.patch`.
- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Route Atlas API with the upstream Traefik example and draw the current packet path.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch21/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Separate executable ingress examples from design-only overlay/CNI; show actual router/service fields and a failure path.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch21/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch21/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch21.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch21.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch21.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 040 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 21 - Ingress, Host Networking, and the Overlay Roadmap`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `21-ingress-host-networking-and-the-overlay-roadmap` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 041 — Chapter 22: Autoscaling Decisions and Missing Integration

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/22-autoscaling-decisions-and-missing-integration.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is III — Change and Recover. Focus: Read CPU recommendations, bounds, cooldown, rollout exclusion, and production provider gaps. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Calculate a replica recommendation from observed CPU.
- Explain bounded scaling and cooldown.
- Identify the missing production metrics provider and default-server wiring.

Use these chapter-specific sections as the narrative spine:

1. **The CPU Recommendation Equation**
2. **Bounds, Cooldown, and Rollout Exclusion**
3. **Fake Metrics and Package Tests**
4. **The Provider and Server Wiring Gaps**

Work the ceil-based CPU recommendation with one scale-up and one bounded scale-down example. Inspect which fields are enforced, including cooldown and the declared stabilization window. Trace where recommendation state lives and whether it survives restart. Use the actual fake metrics provider in the lab. Read the server entry point to verify integration rather than assuming the autoscaler runs because its package exists. A production Prometheus provider or server composition change is an independent teaching extension; neither can be presented as baseline orch capability.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/autoscaler/autoscaler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go)
- [internal/autoscaler/autoscaler_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler_test.go)
- [docs/AUTOSCALING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AUTOSCALING.md)
- [docs/AUTOSCALING_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/AUTOSCALING_DESIGN.md)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)

Read the original development intent:

- [prompts/54-autoscaling-design-doc.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/54-autoscaling-design-doc.md)
- [prompts/55-autoscaling-mvp-implementation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/55-autoscaling-mvp-implementation.md)

Explain relevant implementation history using these real commits:

- [Add autoscaling design](https://github.com/alekpopovic/orch/commit/cf4766ccc7ae05dffda1337d9fe89a7bf33bc9e2); inspect `books/inside-orch/evidence/commit-diffs/cf4766ccc7ae05dffda1337d9fe89a7bf33bc9e2.patch`.
- [Add autoscaling MVP](https://github.com/alekpopovic/orch/commit/b575252d6c5ff0918439e2f209af9d9695eebbb6); inspect `books/inside-orch/evidence/commit-diffs/b575252d6c5ff0918439e2f209af9d9695eebbb6.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Drive Atlas replica recommendations with FakeMetricsProvider and inspect cooldown behavior.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch22/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not assert automatic production autoscaling is active; distinguish declared stabilizationWindow from enforced behavior and state whether cooldown is durable.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch22/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch22/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch22.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch22.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch22.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 041 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 22 - Autoscaling Decisions and Missing Integration`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `22-autoscaling-decisions-and-missing-integration` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 042 — Chapter 23: Authentication, Authorization, and Node Trust

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/23-authentication-authorization-and-node-trust.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Study operator JWT roles, agent enrollment tokens, route authorization, and node trust limits. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Distinguish user authentication from agent bootstrap.
- Trace role checks for sensitive operations.
- Explain Docker socket privilege and missing mTLS identity.

Use these chapter-specific sections as the narrative spine:

1. **User JWTs and Role Checks**
2. **Agent Bootstrap Is a Different Trust Path**
3. **Which Routes Require Which Identity**
4. **Docker Access and Missing Mutual TLS**

Follow a privileged user operation and an agent operation through different authentication paths. Inspect how JWT and static-user settings affect enabled authentication, then exercise viewer, operator, and admin roles. Explain the actual agent enrollment credential model and its revocation/rotation limits. Keep the discussion concrete: Docker socket authority can be equivalent to host compromise. Avoid implying OAuth, external identity providers, or mTLS exist. Use sample tokens generated for disposable tests and redact them from listings, reports, command output, and evidence logs.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/auth/auth.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/auth.go)
- [internal/auth/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go)
- [internal/auth/agent_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent_test.go)
- [internal/api/api.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)
- [docs/SECURITY_REVIEW.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY_REVIEW.md)

Read the original development intent:

- [prompts/18-user-api-auth-v1.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/18-user-api-auth-v1.md)
- [prompts/19-agent-security-bootstrap.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/19-agent-security-bootstrap.md)
- [prompts/51-security-review.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/51-security-review.md)

Explain relevant implementation history using these real commits:

- [Implement user API auth and RBAC](https://github.com/alekpopovic/orch/commit/403a9fc9d9005aca95ade9f5edfbbc77acd1a911); inspect `books/inside-orch/evidence/commit-diffs/403a9fc9d9005aca95ade9f5edfbbc77acd1a911.patch`.
- [Improve agent authentication](https://github.com/alekpopovic/orch/commit/4f25e78c229ba040c07a84801490485b5a0cbb2e); inspect `books/inside-orch/evidence/commit-diffs/4f25e78c229ba040c07a84801490485b5a0cbb2e.patch`.
- [Add security review and healthcheck hardening](https://github.com/alekpopovic/orch/commit/a5cb0c5fb4cab92130b1cdfd15df88256267bcb7); inspect `books/inside-orch/evidence/commit-diffs/a5cb0c5fb4cab92130b1cdfd15df88256267bcb7.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run Atlas API authorization tests with viewer, operator, admin, and invalid agent credentials.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch23/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use placeholder credentials only; document auth enablement and actual defaults; no claim token authentication is equivalent to mutual TLS.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch23/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch23/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch23.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch23.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch23.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 042 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 23 - Authentication, Authorization, and Node Trust`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `23-authentication-authorization-and-node-trust` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 043 — Chapter 24: Encrypted Secrets and Configuration Redaction

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/24-encrypted-secrets-and-configuration-redaction.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Read secret envelope construction, namespace reference resolution, configuration precedence, and redacted output. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Trace secret encrypt/decrypt and reference resolution.
- Explain local key custody and rotation gaps.
- Check diagnostic paths for redaction.

Use these chapter-specific sections as the narrative spine:

1. **Secret References and Namespace Resolution**
2. **The Local Encryption Envelope**
3. **Configuration Precedence and Redaction**
4. **Key Custody and Rotation Boundaries**

Trace an encrypted placeholder secret from storage to a workload reference and the agent path. Read the envelope implementation rather than guessing its algorithm or external key-provider support. Explain local key custody and any unimplemented rotation behavior. Compare configuration load precedence with redacted config output. Test that a known sample secret is absent from diagnostics. Clarify that environment injection and encrypted control-plane storage protect different boundaries, and that in-memory control-plane state remains distinct from a persistently integrated secret store.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go)
- [internal/secrets/envelope_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope_test.go)
- [internal/config/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go)
- [internal/config/config_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config_test.go)
- [docs/SECRETS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECRETS.md)
- [docs/CONFIGURATION.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CONFIGURATION.md)
- [deployments/examples/secrets-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/secrets-api.yaml)

Read the original development intent:

- [prompts/37-secrets-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/37-secrets-mvp.md)
- [prompts/44-config-management-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/44-config-management-hardening.md)

Explain relevant implementation history using these real commits:

- [Add secrets MVP](https://github.com/alekpopovic/orch/commit/ad738d1867eefb3c92cc4280659ae76943341426); inspect `books/inside-orch/evidence/commit-diffs/ad738d1867eefb3c92cc4280659ae76943341426.patch`.
- [Harden config management](https://github.com/alekpopovic/orch/commit/a4844c571a0ddf33879556413a62d49a408609e3); inspect `books/inside-orch/evidence/commit-diffs/a4844c571a0ddf33879556413a62d49a408609e3.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Deploy an Atlas placeholder-secret example and assert sample sensitive values are absent from printed configuration.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch24/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not promise external KMS or rotation not implemented; examples never put real secrets in command arguments or committed files.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch24/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch24/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch24.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch24.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch24.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 043 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 24 - Encrypted Secrets and Configuration Redaction`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `24-encrypted-secrets-and-configuration-redaction` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 044 — Chapter 25: Registry Credentials and Immutable Image Identity

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/25-registry-credentials-and-immutable-image-identity.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Connect registry authentication, image references, tag policy, and digest pinning to rollout traceability. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Parse tags and digests through actual image-reference code.
- Trace namespace-scoped registry credentials.
- Explain mutable-tag risk and the implemented pinning policy.

Use these chapter-specific sections as the narrative spine:

1. **Registry Authentication Without Plaintext History**
2. **Image References, Tags, and Digests**
3. **Immutable Policy Checks and Rollout Identity**
4. **Supplied Digests Versus Registry Resolution**

Use a private-image example to trace encrypted credential selection and namespace scope. Read image-reference parsing and policy tests before describing tag immutability or digest pinning. Determine whether orch resolves mutable tags against a registry or only accepts a supplied digest; do not invent network resolution. Distinguish digest identity from signed authenticity. Executable manifests need a verified, available image and real digest; an explanatory fake digest must be visibly marked as non-executing and cannot pass the lab’s observation gate.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/image/reference.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go)
- [internal/image/reference_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference_test.go)
- [internal/controlplane/image_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/image_test.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [docs/REGISTRIES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/REGISTRIES.md)
- [deployments/examples/private-image.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/private-image.yaml)
- [migrations/000013_image_metadata.up.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000013_image_metadata.up.sql)

Read the original development intent:

- [prompts/38-image-registry-authentication.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/38-image-registry-authentication.md)
- [prompts/67-image-tag-immutability-and-digest-pinning.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/67-image-tag-immutability-and-digest-pinning.md)

Explain relevant implementation history using these real commits:

- [Add registry credentials support](https://github.com/alekpopovic/orch/commit/fe41c80f83b62a3c8ea8430046acf088ec4014a1); inspect `books/inside-orch/evidence/commit-diffs/fe41c80f83b62a3c8ea8430046acf088ec4014a1.patch`.
- [Add quotas image pinning and GitOps](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1); inspect `books/inside-orch/evidence/commit-diffs/f2836eabfff8e442d38984433f3e1f5c642667d1.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Validate Atlas image references and use an explicitly labeled placeholder digest for non-executing examples.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch25/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use real verified digest only for executable labs; classify fake digests as explanatory; image signing is reserved for the design chapter.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch25/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch25/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch25.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch25.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch25.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 044 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 25 - Registry Credentials and Immutable Image Identity`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `25-registry-credentials-and-immutable-image-identity` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 045 — Chapter 26: Security Contexts, Admission, and Policy

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/26-security-contexts-admission-and-policy.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Read enforceable container security fields and policy/admission entry points. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Distinguish supported security context fields from host isolation.
- Explain admission sequencing and rejection evidence.
- Verify CLI, API, and GitOps share policy acceptance boundaries.

Use these chapter-specific sections as the narrative spine:

1. **Container Security Fields That Reach Docker**
2. **Admission Order and Policy Decisions**
3. **The Same Checks Across Entry Points**
4. **What Admission Does Not Isolate**

Trace each discussed security-context field beyond service validation into agent DTOs and Docker create options before claiming enforcement. Explain the policy/admission decision flow with a rejected manifest and stable error shape. Compare API, CLI-assisted deployment, and GitOps application entry points. The policy design document may describe broader extensibility than the implemented engine, so classify them separately. Explicitly connect policy decisions to host trust limits: rejecting privileged options is useful, but shared Docker workers are not thereby a complete sandbox for hostile tenants.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/policy/policy.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/policy/policy.go)
- [internal/policy/policy_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/policy/policy_test.go)
- [internal/admission/admission.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission.go)
- [internal/admission/admission_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission_test.go)
- [internal/controlplane/admission_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/admission_test.go)
- [docs/POLICY_ENGINE_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/POLICY_ENGINE_DESIGN.md)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)

Read the original development intent:

- [prompts/52-container-security-policy.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/52-container-security-policy.md)
- [prompts/63-policy-engine-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/63-policy-engine-design.md)
- [prompts/64-admission-controller-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/64-admission-controller-mvp.md)

Explain relevant implementation history using these real commits:

- [Add container security policy](https://github.com/alekpopovic/orch/commit/a140c4190af17969d207b5738cc7527e4ad96075); inspect `books/inside-orch/evidence/commit-diffs/a140c4190af17969d207b5738cc7527e4ad96075.patch`.
- [Implement API policies and namespaces](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014); inspect `books/inside-orch/evidence/commit-diffs/9e78fed31df03d7a985a9f4ceae4770739b05014.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Reject an unsafe Atlas manifest and inspect stable policy error details.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch26/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not imply a sandbox beyond Docker enforcement; supported admission hooks are code-evidenced and external policy-engine concepts remain proposals.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch26/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch26/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch26.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch26.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch26.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 045 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 26 - Security Contexts, Admission, and Policy`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `26-security-contexts-admission-and-policy` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 046 — Chapter 27: Namespaces and the Limits of Multi-Tenancy

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/27-namespaces-and-the-limits-of-multi-tenancy.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Study namespace context, 404 isolation behavior, namespace-local uniqueness, role maps, and shared host risks. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Resolve namespaces consistently across API and CLI.
- Show cross-namespace secret and object isolation.
- Explain why logical namespaces are not a hostile-tenant security boundary.

Use these chapter-specific sections as the narrative spine:

1. **Namespace Context and Local Names**
2. **Cross-Namespace IDs and Secret References**
3. **Namespace Roles and Cluster Administration**
4. **Logical Isolation on Shared Workers**

Deploy two same-named services in separate namespaces and trace header/flag resolution to domain access checks. Use tests to demonstrate cross-namespace IDs returning 404 and secrets resolving only in their workload namespace. Explain cluster-wide versus namespace role claims. Read both namespace migration directions before describing rollback. Shared nodes, networking, scheduler capacity, and Docker authority limit hostile multi-tenancy; make that operational implication explicit. The lab proves logical isolation only and must never be presented as a tenant security certification.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/namespace/context.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go)
- [internal/controlplane/namespace_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/namespace_test.go)
- [internal/api/namespace_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/namespace_test.go)
- [internal/auth/auth.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/auth.go)
- [docs/MULTI_TENANCY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MULTI_TENANCY.md)
- [migrations/000011_namespaces.up.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000011_namespaces.up.sql)
- [migrations/000011_namespaces.down.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000011_namespaces.down.sql)

Read the original development intent:

- [prompts/65-namespaces-projects.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/65-namespaces-projects.md)

Explain relevant implementation history using these real commits:

- [Implement API policies and namespaces](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014); inspect `books/inside-orch/evidence/commit-diffs/9e78fed31df03d7a985a9f4ceae4770739b05014.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Deploy two Atlas API services with the same name in different namespaces and verify invisible cross-namespace IDs.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch27/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Every isolation guarantee is scoped; discuss shared nodes, Docker and networking; down-migration data loss is explicit in the appendix runbook.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch27/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch27/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch27.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch27.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch27.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 046 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 27 - Namespaces and the Limits of Multi-Tenancy`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `27-namespaces-and-the-limits-of-multi-tenancy` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 047 — Chapter 28: Quotas and Usage Accounting

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/28-quotas-and-usage-accounting.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Read atomic quota checks, requested resource accounting, usage snapshots, and operational exports. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Calculate namespace requested CPU/memory and port usage.
- Explain concurrent quota enforcement and zero-as-unlimited.
- Distinguish operational usage reports from invoices or payment billing.

Use these chapter-specific sections as the narrative spine:

1. **Requested Resource Arithmetic**
2. **Atomic Quotas Under Concurrent Changes**
3. **Usage Snapshots and CSV Units**
4. **An Export Boundary, Not a Billing System**

Calculate namespace usage with requested per-replica CPU/memory, service counts, published-port declarations, and any implemented storage dimensions. Inspect zero-limit meaning and concurrent quota checks separately in MemoryService and PostgreSQL paths. Show a rejected scale with exact error details. Follow snapshots into API and CSV exports, documenting units and time range semantics. Explain that requested usage and accumulated task runtime are different measures. Payment collection, pricing, tax, and invoicing are outside this implementation; do not inflate an operational export into a SaaS billing product.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/quota/quota.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/quota/quota.go)
- [internal/controlplane/quota_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/quota_test.go)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go)
- [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go)
- [internal/api/quota_gitops_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/quota_gitops_test.go)
- [docs/MULTI_TENANCY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MULTI_TENANCY.md)
- [migrations/000012_resource_quotas.up.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000012_resource_quotas.up.sql)

Read the original development intent:

- [prompts/66-resource-quotas.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/66-resource-quotas.md)
- [prompts/85-tenant-aware-billing-export-report.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/85-tenant-aware-billing-export-report.md)

Explain relevant implementation history using these real commits:

- [Add quotas image pinning and GitOps](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1); inspect `books/inside-orch/evidence/commit-diffs/f2836eabfff8e442d38984433f3e1f5c642667d1.patch`.
- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Exhaust an Atlas namespace quota and export a bounded usage report with known dimensions.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch28/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: State whether each guarantee comes from MemoryService or PostgreSQL store; CSV units are documented; no complete billing product claim.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch28/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch28/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch28.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch28.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch28.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 047 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 28 - Quotas and Usage Accounting`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `28-quotas-and-usage-accounting` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 048 — Chapter 29: Supply Chain Designs Without False Guarantees

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/29-supply-chain-designs-without-false-guarantees.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Analyze image signing, SBOM and vulnerability scanning proposals against implemented image-policy boundaries. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Separate digest identity from signature authenticity.
- Design a verification and provenance decision path.
- Define fail-open/fail-closed and scanner freshness tradeoffs.

Use these chapter-specific sections as the narrative spine:

1. **Digest Identity and Signature Authenticity**
2. **Trust Policy and Verification Placement**
3. **SBOM, Vulnerability Freshness, and Fail Modes**
4. **What the Repository Proposes Rather Than Runs**

Use the signing and supply-chain design documents as an architecture case study. Explain why a digest identifies content while a signature addresses trust, and why a scanner report can become stale. Propose verification placement, evidence retention, and fail-open/fail-closed behavior with an explicit threat model. Check implementation before labeling any verifier or scanner as active. A teaching contract can be executable against fake verdicts, but external integrations and current tool commands need official versioned documentation and independent validation. Keep recommendations visibly separate from historical orch behavior.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [docs/IMAGE_SIGNING_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/IMAGE_SIGNING_DESIGN.md)
- [docs/SUPPLY_CHAIN_SECURITY_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SUPPLY_CHAIN_SECURITY_DESIGN.md)
- [internal/image/reference.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go)
- [internal/policy/policy.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/policy/policy.go)
- [prompts/68-image-signing-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/68-image-signing-design.md)
- [prompts/69-sbom-and-vulnerability-scanning-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/69-sbom-and-vulnerability-scanning-design.md)

Read the original development intent:

- [prompts/68-image-signing-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/68-image-signing-design.md)
- [prompts/69-sbom-and-vulnerability-scanning-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/69-sbom-and-vulnerability-scanning-design.md)

Explain relevant implementation history using these real commits:

- [Add quotas image pinning and GitOps](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1); inspect `books/inside-orch/evidence/commit-diffs/f2836eabfff8e442d38984433f3e1f5c642667d1.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Write an Atlas threat model and a book-side verification contract; mark every proposed adapter as illustrative.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch29/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Signing and scanning are design material unless implementation evidence proves otherwise; do not install moving external tools without official versioned references.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch29/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch29/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch29.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch29.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch29.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 048 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 29 - Supply Chain Designs Without False Guarantees`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `29-supply-chain-designs-without-false-guarantees` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 049 — Chapter 30: GitOps, Drift, and Controlled Reconciliation

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/30-gitops-drift-and-controlled-reconciliation.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is IV — Enforce Boundaries. Focus: Trace isolated git checkout, manifest parse/admission, recorded revision, warn/auto-revert drift, and prune ownership. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain source revision provenance and deterministic manifest order.
- Contrast warn and auto_revert drift behavior.
- Bound pruning to the source’s managed services.

Use these chapter-specific sections as the narrative spine:

1. **A Source Revision You Can Trace**
2. **Fetch, Parse, Admission, and Apply**
3. **Warn Versus Auto-Revert Drift**
4. **Prune Only What This Source Owns**

Create a disposable local manifest repository with real commits and trace the GitOps source revision stored after synchronization. Inspect deterministic path traversal and shared parser/admission entry points. Make a manual scale change and compare warn with auto_revert drift handling. Read ownership checks before demonstrating prune. Explain failed fetch or invalid manifest behavior without promising atomic repository-wide deployment if code does not provide it. Avoid credentials in repository URLs, remove temporary checkouts as the implementation does, and preserve the committed revision as lab evidence.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/gitops/gitops.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go)
- [internal/gitops/gitops_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops_test.go)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go)
- [docs/GITOPS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/GITOPS.md)
- [migrations/000014_gitops_sources.up.sql](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/migrations/000014_gitops_sources.up.sql)

Read the original development intent:

- [prompts/70-gitops-deployment-flow.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/70-gitops-deployment-flow.md)
- [prompts/71-drift-detection-between-gitops-desired-state-and-cluster-state.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/71-drift-detection-between-gitops-desired-state-and-cluster-state.md)

Explain relevant implementation history using these real commits:

- [Add quotas image pinning and GitOps](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1); inspect `books/inside-orch/evidence/commit-diffs/f2836eabfff8e442d38984433f3e1f5c642667d1.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Use a local Atlas manifest repository, introduce manual drift, and demonstrate warn versus auto_revert.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch30/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use a real local committed revision; no userinfo credentials in URLs; illustrate failure isolation and ensure prune never touches unrelated services.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch30/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch30/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch30.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch30.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch30.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 049 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 30 - GitOps, Drift, and Controlled Reconciliation`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `30-gitops-drift-and-controlled-reconciliation` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 050 — Chapter 31: Finite Jobs and Time-Based Work

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/31-finite-jobs-and-time-based-work.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is V — Extend the Platform. Focus: Read Job attempts, retry limits, CronJob parsing, timezone semantics, concurrency policies, and missed runs. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Trace Job exit status to success, failure, or retry.
- Explain Allow, Forbid, and Replace concurrency.
- Reason about timezone and bounded missed occurrences.

Use these chapter-specific sections as the narrative spine:

1. **Finite Attempts and Exit Codes**
2. **Retry Limits and Terminal Outcomes**
3. **Cron Expressions and Explicit Timezones**
4. **Allow, Forbid, Replace, and Missed Runs**

Follow one finite Job through a successful attempt and one nonzero-exit retry. Read CronJob parser and controller tests before quoting syntax, timezone defaults, and concurrency behavior. Include overlap and missed occurrences with a fake clock, so the lab remains deterministic and bounded. Inspect supported workload fields rather than inventing Kubernetes manifests. Explain time-based scheduling’s failure window and avoid exactly-once claims. Show cleanup for generated Jobs and task artifacts; any production scheduling guarantee beyond tested behavior belongs in a separate design exercise.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/controlplane/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go)
- [internal/controlplane/workloads_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads_test.go)
- [internal/cronjobs/cronjobs.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go)
- [internal/cronjobs/cronjobs_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs_test.go)
- [internal/cli/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/workloads.go)
- [pkg/types/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/workloads.go)
- [docs/JOBS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/JOBS.md)
- [docs/JOBS_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/JOBS_DESIGN.md)

Read the original development intent:

- [prompts/72-cron-jobs-and-one-shot-jobs-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/72-cron-jobs-and-one-shot-jobs-design.md)
- [prompts/73-one-shot-jobs-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/73-one-shot-jobs-mvp.md)
- [prompts/74-cron-jobs-mvp.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/74-cron-jobs-mvp.md)

Explain relevant implementation history using these real commits:

- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run a finite Atlas report job and drive CronJob fake time through overlap and missed-occurrence cases.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch31/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Use exact supported five-field cron syntax and workload YAML; UTC and timezone cases are explicit; do not claim exactly-once scheduling.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch31/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch31/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch31.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch31.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch31.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 050 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 31 - Finite Jobs and Time-Based Work`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `31-finite-jobs-and-time-based-work` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 051 — Chapter 32: Local Volumes, Claims, and Workload Topology

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/32-local-volumes-claims-and-workload-topology.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is V — Extend the Platform. Focus: Study local volume claims, scheduler topology, active writer locks, attachment lifecycle, and unsupported distributed storage. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Explain why a local claim binds future placement to a node.
- Trace writer-lock and read-only attachment behavior.
- Separate storage metadata safety from data replication and backup.

Use these chapter-specific sections as the narrative spine:

1. **Local Volumes and Claim Binding**
2. **Attachments and Active Writer Rules**
3. **Topology Constraints During Placement**
4. **The Storage Guarantees That Are Absent**

Trace a Docker local volume claim through workload resolution, task attachment, and scheduler topology tests. Distinguish implemented writer locks from distributed fencing and storage replication. Determine which topology guarantees reach normal live placement rather than assuming scheduler tests prove the default service path. Read read-only and concurrent-writer options with exact field spellings. Use disposable data in the lab and define whether cleanup retains or deletes it. Distributed storage, replication, snapshots, and automatic data migration remain unimplemented unless explicit source evidence establishes otherwise.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/controlplane/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go)
- [internal/controlplane/workloads_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads_test.go)
- [internal/scheduler/workloads_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/workloads_test.go)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [pkg/types/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/workloads.go)
- [docs/STORAGE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STORAGE.md)
- [docs/STATEFUL_WORKLOADS_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATEFUL_WORKLOADS_DESIGN.md)

Read the original development intent:

- [prompts/75-stateful-workloads-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/75-stateful-workloads-design.md)
- [prompts/76-persistent-volume-abstraction.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/76-persistent-volume-abstraction.md)

Explain relevant implementation history using these real commits:

- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Attach a disposable Atlas local volume and reject a second writer or wrong-node placement in tests.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch32/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Do not portray RWO as distributed fencing; no replicated stateful-service promise; cleanup requires explicit data retention choices.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch32/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch32/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch32.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch32.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch32.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 051 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 32 - Local Volumes, Claims, and Workload Topology`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `32-local-volumes-claims-and-workload-topology` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 052 — Chapter 33: Extension Interfaces and a Plugin Roadmap

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/33-extension-interfaces-and-a-plugin-roadmap.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is V — Extend the Platform. Focus: Read existing side-effect interfaces and design external RPC plugin lifecycle without inventing a plugin implementation. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, architect.

Learning outcomes:

- Identify present runtime, secrets, metrics, and notification seams.
- Design versioned handshake and capability negotiation.
- Analyze least privilege, cancellation, crash isolation, and idempotency.

Use these chapter-specific sections as the narrative spine:

1. **Interfaces Already Present in the Code**
2. **A Versioned External Plugin Handshake**
3. **Supervisor Lifecycle and Failure Containment**
4. **Contract Testing a Proposed Adapter**

Build the chapter around narrow runtime, secret-envelope, notification, and metrics boundaries already present. Contrast these with the external RPC plugin system proposed in documentation. Define capabilities, version mismatch, timeout, crash, cancellation, redaction, and idempotency requirements as a teaching contract. Use a fake adapter exercise rather than representing an invented plugin supervisor as upstream code. Explain that runtime/storage plugins remain privileged parts of the trusted computing base. The reader should understand how to extend a boundary without confusing dependency injection with an implemented third-party plugin platform.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [docs/PLUGIN_SYSTEM_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PLUGIN_SYSTEM_DESIGN.md)
- [internal/docker/docker.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go)
- [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go)
- [internal/notifications/notifications.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go)
- [internal/autoscaler/autoscaler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go)

Read the original development intent:

- [prompts/79-plugin-system-design.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/79-plugin-system-design.md)

Explain relevant implementation history using these real commits:

- [Add jobs storage DNS and notifications](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87); inspect `books/inside-orch/evidence/commit-diffs/4d641bbe8913da568d6d9f4697a0144314e10b87.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Create an Atlas adapter contract exercise and label the external RPC protocol as a design proposal.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch33/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Separate existing interfaces from design-only supervisors and RPC; no arbitrary code-loading sample; contract pseudocode is clearly labeled and not presented as upstream source.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch33/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch33/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch33.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch33.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch33.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 052 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 33 - Extension Interfaces and a Plugin Roadmap`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `33-extension-interfaces-and-a-plugin-roadmap` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

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


---

# 054 — Chapter 35: Upgrades, Migrations, Maintenance, and Retention

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/35-upgrades-migrations-maintenance-and-retention.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is V — Extend the Platform. Focus: Read version compatibility, safe migration locks, down guards, maintenance windows, and bounded retention. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Read current server, agent, API, and schema compatibility ranges.
- Explain migration checks and guarded rollback.
- Apply maintenance and retention policies with preservation boundaries.

Use these chapter-specific sections as the narrative spine:

1. **Version Ranges and Upgrade Preflight**
2. **Migration Locks and Guarded Down Paths**
3. **Maintenance Windows and Bounded Retention**
4. **A Schema Check Must Be Enabled to Run**

Read compatibility constants and expose their source-pinned ranges, rather than treating the latest release as a moving target. Follow migration status/up/down locking and the allow-down guard. Inspect the server’s schema-check environment gate and show its actual default behavior. Explain maintenance checks and dry-run pruning preservation boundaries. The lab uses a disposable database and preserved evidence. A rollback plan must distinguish additive schema compatibility from dangerous data-removing down migrations and cannot imply database restore recovers active MemoryService state.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/version/version.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/version/version.go)
- [internal/version/version_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/version/version_test.go)
- [internal/migrations/manager.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go)
- [internal/migrations/manager_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager_test.go)
- [internal/maintenance/maintenance.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/maintenance/maintenance.go)
- [internal/controlplane/operations.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operations.go)
- [docs/UPGRADES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/UPGRADES.md)
- [docs/MIGRATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MIGRATIONS.md)

Read the original development intent:

- [prompts/81-maintenance-windows.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/81-maintenance-windows.md)
- [prompts/82-cluster-upgrade-framework.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/82-cluster-upgrade-framework.md)
- [prompts/83-database-migration-safety.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/83-database-migration-safety.md)
- [prompts/84-data-retention-and-pruning.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/84-data-retention-and-pruning.md)

Explain relevant implementation history using these real commits:

- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Perform a disposable Atlas migration-status and upgrade-preflight exercise, then dry-run retention.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch35/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: All schema ranges are pinned to source version; show ORCH_SCHEMA_CHECK enablement from main.go instead of implying unconditional checks; never test down migrations on real data.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch35/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch35/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch35.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch35.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch35.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 054 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 35 - Upgrades, Migrations, Maintenance, and Retention`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `35-upgrades-migrations-maintenance-and-retention` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

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


---

# 056 — Chapter 37: Failure Injection and Recovery Evidence

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/37-failure-injection-and-recovery-evidence.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is VI — Prove and Operate. Focus: Turn failure-mode hardening and chaos scenarios into bounded recovery investigations. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Define an invariant before injecting a fault.
- Distinguish timeout, runtime failure, node loss, and partition.
- Measure convergence and identify unsupported recovery guarantees.

Use these chapter-specific sections as the narrative spine:

1. **Name the Invariant Before the Fault**
2. **Runtime Failure, Node Loss, and Partition**
3. **Recovery Timelines and Residual Work**
4. **What a Fake Chaos Test Can Prove**

Choose a bounded fault from existing chaos tests and state the safety and convergence invariant before triggering it. Use injected pull/create/start/health errors or disposable local process interruption. Record a timeline, expected or observed recovery, and residual resources. Compare fake-system results with assumptions required for a real cluster, especially partitions and state persistence. Explain top recovery-hardening commits through their relevant changes. The chapter earns trust by naming unsupported guarantees and release-blocking gaps rather than calling every recovery test production resilience.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/e2e/chaos_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/e2e/chaos_test.go)
- [internal/docker/fake.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go)
- [docs/CHAOS_TESTING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CHAOS_TESTING.md)
- [docs/RELIABILITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/RELIABILITY.md)
- [prompts/25-failure-modes-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/25-failure-modes-hardening.md)
- [prompts/26-senior-distributed-systems-review.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/26-senior-distributed-systems-review.md)

Read the original development intent:

- [prompts/25-failure-modes-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/25-failure-modes-hardening.md)
- [prompts/26-senior-distributed-systems-review.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/26-senior-distributed-systems-review.md)
- [prompts/59-chaos-testing-scenarios.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/59-chaos-testing-scenarios.md)

Explain relevant implementation history using these real commits:

- [Improve failure recovery behavior](https://github.com/alekpopovic/orch/commit/66cfb7049fc1fbceeec9e36a7067febe8cbab698); inspect `books/inside-orch/evidence/commit-diffs/66cfb7049fc1fbceeec9e36a7067febe8cbab698.patch`.
- [Add chaos testing scenarios](https://github.com/alekpopovic/orch/commit/fe385251b7a2051b10af3dd6caaad8bb4821fa21); inspect `books/inside-orch/evidence/commit-diffs/fe385251b7a2051b10af3dd6caaad8bb4821fa21.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run Atlas failure drills with fake runtime faults and optional local process interruption.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch37/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Every drill specifies fault, expected behavior, observations, recovery, and cleanup; do not mistake fake-system success for distributed production resilience.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch37/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch37/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch37.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch37.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch37.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 056 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 37 - Failure Injection and Recovery Evidence`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `37-failure-injection-and-recovery-evidence` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 057 — Chapter 38: Metrics, Dashboards, and Actionable Signals

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/38-metrics-dashboards-and-actionable-signals.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is VI — Prove and Operate. Focus: Trace Prometheus instruments, cardinality, alert rules, dashboard panels, and links to operator actions. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Map an emitted metric to a subsystem and failure mode.
- Explain counters, gauges, labels, and cardinality cost.
- Connect an alert to a concrete investigation.

Use these chapter-specific sections as the narrative spine:

1. **A Metric’s Emission Site and Meaning**
2. **Labels, Cardinality, Counters, and Gauges**
3. **Alert Expressions and Dashboard Queries**
4. **From Signal to Operator Action**

Select a real emitted metric and walk from instrumentation to Prometheus scrape, alert expression, Grafana panel, and operator investigation. Verify every referenced metric name, label, and query against code and supplied configuration. Explain cardinality using current service/task/node labels where relevant. Record missing or mismatched dashboard signals rather than silently inventing them. A worked exercise should diagnose a concrete failed Docker operation or pending task. SLOs and thresholds introduced for teaching must be labeled as chosen assumptions rather than established production measurements.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [internal/metrics/prometheus.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go)
- [internal/metrics/prometheus_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus_test.go)
- [internal/docker/metrics.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/metrics.go)
- [deploy/monitoring/prometheus-rules.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/prometheus-rules.yaml)
- [deploy/monitoring/prometheus.yml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/prometheus.yml)
- [deploy/monitoring/grafana/orchestrator-dashboard.json](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deploy/monitoring/grafana/orchestrator-dashboard.json)
- [docs/OBSERVABILITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OBSERVABILITY.md)

Read the original development intent:

- [prompts/20-prometheus-metrics.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/20-prometheus-metrics.md)
- [prompts/46-audit-logging.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/46-audit-logging.md)
- [prompts/47-prometheus-alert-rules.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/47-prometheus-alert-rules.md)
- [prompts/48-grafana-dashboard-json.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/48-grafana-dashboard-json.md)

Explain relevant implementation history using these real commits:

- [Add Prometheus metrics](https://github.com/alekpopovic/orch/commit/b3e29e593f46b4e90899a56bd9391c03d7c42f1a); inspect `books/inside-orch/evidence/commit-diffs/b3e29e593f46b4e90899a56bd9391c03d7c42f1a.patch`.
- [Add Prometheus alert rules](https://github.com/alekpopovic/orch/commit/357903ef7cb95a7d6d8fad5f426a48ed48bc0b76); inspect `books/inside-orch/evidence/commit-diffs/357903ef7cb95a7d6d8fad5f426a48ed48bc0b76.patch`.
- [Add Grafana dashboard](https://github.com/alekpopovic/orch/commit/aa44e586fd79147173588f0bf86763814bd23ec4); inspect `books/inside-orch/evidence/commit-diffs/aa44e586fd79147173588f0bf86763814bd23ec4.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Inspect Atlas metrics and validate one real alert expression and dashboard query against emitted metric names.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch38/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Metric names and PromQL are copied from pinned source; dashboard mismatches are reported; no invented SLO, recording rule, or benchmark chart.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch38/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch38/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch38.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch38.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch38.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 057 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 38 - Metrics, Dashboards, and Actionable Signals`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `38-metrics-dashboards-and-actionable-signals` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 058 — Chapter 39: Performance and Scale Tests That Say What They Measure

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/39-performance-and-scale-tests-that-say-what-they-measure.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is VI — Prove and Operate. Focus: Read fake-agent load tests, scheduler/API benchmarks, pprof controls, and large-service stress scenarios. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Separate fake control-plane throughput from real Docker capacity.
- Record hardware, commit, seed, flags, and measurement uncertainty.
- Profile only on protected debug surfaces.

Use these chapter-specific sections as the narrative spine:

1. **Fake-Agent Load and Real Runtime Capacity**
2. **Benchmark Inputs and Repeatable Conditions**
3. **Profiles Behind the Debug Boundary**
4. **Interpreting the Thousand-Service Scenario**

Inspect the load-test runner and scale-test flags before execution. Define exactly which controller/API work fake agents exercise and which Docker, network, storage, and resource effects are excluded. Record commit, toolchain, hardware, seed, flags, timestamps, sample count, and uncertainty for any measured result. Read protected debug-listener behavior before presenting pprof. Explain one benchmark finding only if obtained; otherwise provide an empty measurement template. A thousand-service simulation is a scope-specific test scenario and cannot become a supported production cluster-size claim.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go)
- [cmd/orch-loadtest/scale_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/scale_test.go)
- [internal/scheduler/benchmark_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/benchmark_test.go)
- [internal/controlplane/benchmark_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/benchmark_test.go)
- [internal/api/benchmark_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/benchmark_test.go)
- [internal/api/debug.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/debug.go)
- [docs/LOAD_TESTING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/LOAD_TESTING.md)
- [docs/PERFORMANCE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PERFORMANCE.md)
- [docs/SCALE_TESTING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SCALE_TESTING.md)

Read the original development intent:

- [prompts/58-multi-agent-load-test.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/58-multi-agent-load-test.md)
- [prompts/88-performance-profiling.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/88-performance-profiling.md)
- [prompts/89-scale-test-1000-services-with-fake-agents.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/89-scale-test-1000-services-with-fake-agents.md)

Explain relevant implementation history using these real commits:

- [Add multi-agent load test](https://github.com/alekpopovic/orch/commit/7fcdaf5877145b77bb484b2bc7cabae8eb75acab); inspect `books/inside-orch/evidence/commit-diffs/7fcdaf5877145b77bb484b2bc7cabae8eb75acab.patch`.
- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Run a bounded Atlas benchmark and create a measured-results template without fabricated data.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch39/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: A 1,000-service fake-agent scenario is not a production capacity claim; pprof exposure controls are source-checked; all numbers are measured or explicitly hypothetical.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch39/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch39/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch39.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch39.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch39.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 058 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 39 - Performance and Scale Tests That Say What They Measure`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `39-performance-and-scale-tests-that-say-what-they-measure` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# 059 — Chapter 40: Release a System You Can Honestly Operate

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Read `AGENTS.md` and `BOOK_SPEC.md` before work. Read `books/inside-orch/evidence/source-lock.json`, the source excerpts listed below, and the relevant exported commit diffs. Preserve the locked baseline; never edit `books/inside-orch/evidence/orch/` or the evidence corpus. Write this chapter in English for **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic, for https://www.alekpopovic.com.

## Chapter assignment

Produce `books/inside-orch/manuscript/chapters/40-release-a-system-you-can-honestly-operate.md` with 1,800–2,500 meaningful narrative words, excluding code, command output, and metadata. This is VI — Prove and Operate. Focus: Bring together reproducible release checks, deployment manifests, recovery drills, readiness limits, and an evidence-based production backlog. Connect to previous Atlas Lab state without repeating earlier explanations. Reader paths: developer, devops, architect.

Learning outcomes:

- Verify build/test/lint/release contracts and distinguish skipped checks.
- Explain what PostgreSQL backup does and does not restore for default MemoryService.
- Produce a source-grounded readiness review and next-step ADRs.

Use these chapter-specific sections as the narrative spine:

1. **Release Checks With Honest Coverage**
2. **Deployment Manifests and Runtime Prerequisites**
3. **A Backup Drill With the Correct State Boundary**
4. **The Final Readiness Decision and Backlog**

Close the book with a reviewable operational dossier rather than celebratory product claims. Connect release tests, lint fallback, API checks, pinned manifests, compatibility, and backup/restore evidence. Read scripts before showing a restore and use only a disposable PostgreSQL database. Explain that restored tables do not restore active default MemoryService state. Assemble a concrete backlog for durable store wiring, HA, metrics providers, resource enforcement, stronger node identity, and networking. The final case study should tell the reader exactly what the lab demonstrated and what remains necessary before a production deployment.

## Primary source and history

Read implementations and tests together; the following links are immutable starting points, not permission to infer absent behavior:

- [.github/workflows/ci.yml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/.github/workflows/ci.yml)
- [Makefile](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/Makefile)
- [CHANGELOG.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/CHANGELOG.md)
- [RELEASE_NOTES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/RELEASE_NOTES.md)
- [docs/PRODUCTION_DEPLOYMENT.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PRODUCTION_DEPLOYMENT.md)
- [docs/BACKUP_RESTORE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md)
- [deployments/production/docker-compose.yml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/production/docker-compose.yml)
- [deployments/production/systemd/orch-server.service](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/production/systemd/orch-server.service)
- [deployments/production/systemd/orch-agent.service](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/production/systemd/orch-agent.service)
- [scripts/backup-db.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/backup-db.sh)
- [scripts/restore-db.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/restore-db.sh)

Read the original development intent:

- [prompts/23-github-actions-ci.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/23-github-actions-ci.md)
- [prompts/27-production-documentation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/27-production-documentation.md)
- [prompts/28-mvp-release-preparation.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/28-mvp-release-preparation.md)
- [prompts/49-backup-and-restore-runbook.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/49-backup-and-restore-runbook.md)
- [prompts/50-production-deployment-manifest.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/50-production-deployment-manifest.md)
- [prompts/60-release-hardening-v0-2-0.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/60-release-hardening-v0-2-0.md)
- [prompts/90-v0-3-0-release-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/90-v0-3-0-release-hardening.md)

Explain relevant implementation history using these real commits:

- [Add production deployment manifests](https://github.com/alekpopovic/orch/commit/18fcf32524007ba7d8a71acd70e5acc48f758e49); inspect `books/inside-orch/evidence/commit-diffs/18fcf32524007ba7d8a71acd70e5acc48f758e49.patch`.
- [Add backup and restore runbook](https://github.com/alekpopovic/orch/commit/64abe001e83932cba294831424557dfd16f77c8c); inspect `books/inside-orch/evidence/commit-diffs/64abe001e83932cba294831424557dfd16f77c8c.patch`.
- [Harden v0.3 operations and release](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d); inspect `books/inside-orch/evidence/commit-diffs/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d.patch`.

Inspect the changed hunks against current code. Early prompts can be retrospective; later work can be batched. Do not invent one implementation commit per prompt, treat a tracking update as implementation, or call an inspected test an executed test.

## Atlas Lab and observation contract

Concrete scenario: Assemble Atlas evidence: tested lab, unresolved gaps, backup drill, compatibility preflight, and publication-ready case study.

Build the experiment from current interfaces, fixtures, CLI definitions, and documentation. State prerequisites, initial conditions, exact commands, expected transitions, observable success and rejection criteria, and scoped cleanup. Include a failure window and explain what it reveals. Label results expected until execution records prove otherwise. If Docker, PostgreSQL, or network prerequisites are unavailable, preserve a useful deterministic alternative and mark the live observation blocked. Store real command, UTC timestamp, exit code, environment, and scope under `books/inside-orch/validation/labs/ch40/`; never manufacture terminal output, diagrams, timings, or benchmark values.

Mandatory chapter-specific quality contract: Final checklist cannot override MemoryService, missing HA/autoscaler wiring, mTLS, and networking gaps; title/subtitle and product copy never claim production readiness.

## Evidence, listings, and worked exercises

Use short exact listings with baseline SHA, source path, and verified line anchors. Store copied excerpts under `books/inside-orch/examples/source-excerpts/ch40/` with extraction metadata. Follow every discussed behavior through its caller and integration point before assigning a capability label: runtime-integrated, implemented package, partial integration, design only, teaching extension, or future work. A proposed fix belongs only in `books/inside-orch/examples/teaching-extensions/ch40/`, independently tested and visibly separate from upstream code. Never repair the baseline to make the narrative true.

Produce `books/inside-orch/validation/evidence/ch40.json` with claim records containing `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Set validation to expected_only, inspected, executed, or blocked as supported. Include uncertainties, documentation conflicts, and tests’ actual coverage. Link evidence to prose claims and immutable source/history URLs.

Add three to five exercises increasing from source comprehension to a failure or design decision. Write fully justified answers in `books/inside-orch/manuscript/solutions/ch40.md`; validate runnable answers and explain why reasoning-only answers follow from evidence. Include one exercise exposing an unsafe assumption specific to this chapter. Prefer one compact checked diagram or precise comparison table where it improves understanding.

## Finish and self-review

Write `books/inside-orch/validation/reviews/ch40.md` covering source accuracy, lab reproducibility, secret redaction, compatibility, diagram correctness, exercise solutions, and the unique quality contract. Check links and target word count; resolve major contradictions before marking completion. Update `books/inside-orch/state/execution-tracker.csv` for prompt 059 with status, outputs, validation paths, blockers, and local book commit if one exists. Use blocked or review_needed for unresolved requirements. Stop at a concrete chapter and honest evidence; do not push or publish anything.

## Native site manuscript contract

Write plain canonical Markdown with the first H1 exactly `# Chapter 40 - Release a System You Can Honestly Operate`. The site's chapter classifier does not recognize a colon or an em dash after the number. Keep metadata in `books/inside-orch/book.json` and chapter evidence records; do not add YAML front matter that the book Markdown renderer would display as prose. The chapter filename stem is its public slug. Preserve `40-release-a-system-you-can-honestly-operate` and keep its entry in `books/inside-orch/manuscript/Book.txt`. This book has a separate preface before its 40 numbered chapters and six appendices, making 47 reader sections. Never publish a partial manuscript as a complete book.


---

# Prompt 060 — Appendix A — CLI, API, and configuration reference

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `docs/CLI.md`, `docs/API.md`, `docs/CONFIGURATION.md`, `docs/SERVICE_SPEC.md`, `api/openapi.yaml`, `schemas/service.schema.json`, `internal/cli/root.go`, `internal/cli/operations.go`, `internal/cli/workloads.go`, `internal/cli/deploy.go`, `internal/config/config.go`, `internal/api/api.go`, `internal/api/operations.go`, `internal/api/workloads.go`, and all three binary entrypoints. Discover deeper instruction files before inspecting their subtree.

## Produce the reference

Create `books/inside-orch/manuscript/appendices/a-cli-api-config.md` and `books/inside-orch/reference/cli-api-config.json`. Enumerate the actual Cobra command tree, supported flags, output formats, argument arity, environment variables, config keys, defaults, and validation rules. Cover migration commands separately because `orch-server migrate` is dispatched outside the CLI. Explain precedence with a fully specified local example using `ORCH_SERVER_URL=http://127.0.0.1:18080`, a dedicated temporary config, and an overriding `--server` value. Do not assume the server URL defaults to localhost.

For each implemented API operation, record method, normalized path, authentication boundary, namespace behavior, DTO symbols, status/error envelopes, and OpenAPI coverage. Public OpenAPI deliberately excludes agent-only routes: mark this boundary rather than reporting exclusion as missing implementation. Compare the static specification against registered handlers and report real discrepancies. Include the namespace header, request ID behavior, soft deletion, operational conflicts, health endpoints, and agent credential exchange without sample secret values.

Build a configuration table distinguishing loaded, validated, consumed, redacted, and ignored fields. Trace `DATABASE_URL` through migration/schema-check paths and prove it does not wire the default live control plane. Trace the Docker socket setting to runtime construction rather than trusting its advertised description. Explain integer CPU millicores and memory bytes in API DTOs versus human-readable quantities in deployment YAML, including duration encoding differences.

Generate local command help through source-built binaries only if the toolchain exists; offline help and validation must not contact a server. Retain generated help as evidence, never as prose dumped into the appendix. Use complete manifests accepted by the locked parser; keep examples in `books/inside-orch/examples/reference` and validate without deployment. Show safe redacted config printing based on actual executable options.

## Acceptance and evidence

Create `books/inside-orch/validation/060-reference-check.json` containing every command path and flag, every route/method pair, and every config field with its consumer. Add a checker that rejects duplicates, unresolved symbols, invented commands, missing provenance, and any unsupported claim of persistence. Require exact agreement between the extracted command inventory and your reference inventory; document excluded automatic help/completion nodes. Compare handler routes and OpenAPI methods programmatically, separating public and agent surfaces. Each example must have parser evidence or an explicit unexecuted status. Finish with a concise discrepancy ledger: source behavior, documentation statement, reader consequence, and immutable source links. No result may silently collapse unknown behavior into support.

## Immutable starting references

- [internal/cli/root.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go)
- [internal/config/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)
- [api/openapi.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/api/openapi.yaml)

## Native appendix contract

Use the first H1 exactly `# Appendix A - CLI, API, and Configuration Reference` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/a-cli-api-config.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.


---

# Prompt 061 — Appendix B — Lifecycle and invariants reference

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `pkg/types/lifecycle.go`, `pkg/types/lifecycle_test.go`, `pkg/types/types.go`, `pkg/types/workloads.go`, `docs/STATE_MACHINES.md`, `internal/task/task.go`, `internal/controlplane/controlplane.go`, `internal/controlplane/agent_test.go`, `internal/store/postgres.go`, `internal/reconciler/reconciler.go`, `internal/rollout/rollout.go`, and `internal/agent/agent.go`. Inspect all lifecycle consumers and the tests that establish terminal-state semantics.

## Produce the reference

Create `books/inside-orch/manuscript/appendices/b-lifecycle-invariants.md`, `books/inside-orch/reference/lifecycle.json`, and `books/inside-orch/reference/invariants.json`. Extract service, task actual, task desired, node, deployment, job, and cron scheduling semantics separately. Do not confuse ownership and state: the server owns desired state; an assigned agent may report actual state only within valid transitions. For every transition, cite the helper or actual implementation that permits it and record duplicate-report behavior.

Present compact state tables with allowed edges, forbidden representative edges, terminal states, cleanup exceptions, and report authorization. Show why `failed` is terminal for a task while a replacement may be created for its service, why `failed` or `stopped` may move to `removed`, and why rollback creates a new deployment rather than rewriting terminal history. Mark reserved states, including paused deployment behavior, so the reader does not infer a CLI feature from an enum.

Create invariants for desired-replica convergence, atomic task claims, event emission after persisted transitions, node ownership of reports, namespace secrecy, rollout surge/availability accounting, and safe container cleanup. Each invariant must specify scope, assumptions, enforcing function, relevant test, and known counterexample outside that scope. Distinguish store-backed reconciler restart reasoning from process restart of the shipped memory server. Explain that a package test establishes its tested contract, not automatic wiring into the binary.

Include three worked traces: duplicate `healthy` reporting, deleting while rollout is active, and offline stateless versus stateful tasks. Use actual field names and show conditions independently from states. When a trace is reconstructed from source, label it as a source-derived illustration; observed test output gets its own evidence record. Do not add a transition to make a teaching narrative work.

## Acceptance and evidence

Create `books/inside-orch/validation/061-transition-check.json` with the discovered state set, allowed transition matrix, terminal set, and state-owner mapping. Implement a machine check outside the source tree that compares the reference against source transitions or an executed isolated teaching harness. A harness must preserve the locked evidence checkout; use an explicit extension directory and state the import-boundary solution if internal packages are required. Check same-state idempotency, representative invalid transitions, and terminal cleanup exceptions.

Every invariant needs at least one precise symbol citation and a test citation or an explicit test-gap entry. Detect unaccounted enum values and dangling links. Cross-check documentation tables against implementation and preserve discrepancies rather than editing the repository. For each worked trace, include numbered steps, preconditions, state values, outcomes, and the exact scope of confidence. Finish with a paragraph explaining how reviewers can use the matrix to find stale agent reports and unsafe new lifecycle states without treating the appendix as a formal proof of distributed correctness.

## Immutable starting references

- [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go)
- [docs/STATE_MACHINES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATE_MACHINES.md)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go)

## Native appendix contract

Use the first H1 exactly `# Appendix B - Lifecycle States and Invariant Reference` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/b-lifecycle-invariants.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.


---

# Prompt 062 — Appendix C — Annotated commit and prompt history

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read all locked original files under `prompts/`, `CHANGELOG.md`, release notes, and the existing evidence inventories. Use exported history/diffs or a separate verified clone to traverse the complete reachable history at the source lock, including commit parents, timestamps, messages, changed paths, and selected diffs. Use Git objects or the connector's commit API, not release summaries as a substitute. The audited starting inventory contains 105 commits and 91 original prompts; independently reconcile these counts and record exactly how reachability and prompt files are counted.

## Produce the history

Create `books/inside-orch/manuscript/appendices/c-annotated-history.md`, `books/inside-orch/reference/history.json`, and `books/inside-orch/reference/prompt-commit-map.csv`. Every original prompt must appear exactly once in the prompt inventory with its original number, full filename, immutable blob link, first containing commit, and thematic chapter destinations. Every reachable commit must appear exactly once with its full SHA, parents, authored and committed timestamps, subject, changed paths, and an immutable commit link.

Map prompts to commits with an evidence grade: direct textual match, strong path/diff correspondence, partial relationship, or unresolved. Explain the criteria and keep one-to-many and many-to-one relationships. A commit message resembling a prompt title is a candidate, not proof of causality. Authoring instructions document requested work; diffs and tests establish delivered work. Preserve corrections, documentation-only commits, branding, releases, and changes unrelated to an original prompt as legitimate history entries.

Select twelve historically useful checkpoints spanning bootstrap, domain contracts, PostgreSQL stores, agents, scheduler, reconciliation, rollout, security, namespaces/quotas, GitOps/jobs, operational hardening, and release/site packaging. For each, explain the concrete problem, changed mechanism, relevant files and tests, later refinements, and surviving limitation. Extract short real snippets from the corresponding commit rather than showing today's code as if it existed earlier. Annotate removals and renamed files with the historical path.

Describe tension between ambitious original instructions and the executable release. In particular, durable state, HA, autoscaling, and production deployment language require a call-path check against the locked server. Identify which changes introduced APIs or isolated packages and which changes wired actual behavior. Discuss evolution with engineering judgment, preserving uncertainty where the evidence cannot show author intent.

## Acceptance and evidence

Create `books/inside-orch/validation/062-history-check.json` with count definitions, observed counts, duplicate detection, missing numbers, parent completeness, reachable SHA membership, and permalink validation. Machine-check that prompt numbers are exactly 00 through 90, with 91 distinct records; compare the 105-commit expectation with the observed reachable inventory, and explain any repository history scope difference instead of forcing a count. Validate every mapped commit SHA exists and every cited historical path is present at that SHA.

No commit title, timestamp, diff excerpt, or author may be fabricated. Store extracted snippet hashes and source object identifiers in `books/inside-orch/validation/history-snippets.json`. Ensure chapter links resolve and mappings do not imply unproven one-prompt-one-commit execution. Publish a short list of unresolved mappings with the specific missing evidence. Finish with a practical reading guide for developers studying diffs, DevOps engineers auditing operational boundaries, and architects comparing planned contracts against executable composition.

## Immutable starting references

- [prompts/00-agents-md-and-architecture-docs.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/00-agents-md-and-architecture-docs.md)
- [prompts/90-v0-3-0-release-hardening.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/prompts/90-v0-3-0-release-hardening.md)
- [CHANGELOG.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/CHANGELOG.md)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)

## Native appendix contract

Use the first H1 exactly `# Appendix C - Commit Atlas and Original Prompt Crosswalk` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/c-annotated-history.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.


---

# Prompt 063 — Appendix D — Exercises and solutions

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read the completed chapter learning objectives, lab specifications, `pkg/types/lifecycle_test.go`, scheduler property tests, reconciler and rollout tests, `internal/controlplane/operation_lock_test.go`, namespace/quota tests, health tests, GitOps tests, cron tests, migration tests, and API error tests. Examine the exact deterministic seams each test uses rather than assuming every feature has an injectable clock or public constructor.

## Produce the exercise set

Create `books/inside-orch/manuscript/appendices/d-exercises-solutions.md`, `books/inside-orch/exercises/catalog.json`, `books/inside-orch/exercises/questions.md`, and `books/inside-orch/manuscript/solutions/appendix-d.md`. Provide twenty-four substantial exercises, eight for developers, eight for DevOps engineers, and eight for architects. Each needs a stable ID, prerequisites, estimated time, source links, precise question, required artifact, objective scoring rubric, hints, and a worked solution. Connect every exercise to at least one chapter and one actual source mechanism.

Use parallel question and solution organization so readers can study without immediately seeing answers. Exercises must reward reasoning about ownership, failure, concurrency, resource units, secret handling, and deployment composition. Include a stale task-claim race, restart-policy trace, terminal cleanup case, rollback availability budget, namespace identifier leak, quota racing requests, bounded GitOps prune, cron overlap/catch-up, secret envelope key loss, process restart, and fake-load-test interpretation. Keep resource arithmetic consistent with millicores and bytes.

At least eight exercises must be executable offline through existing tests or a deliberately isolated teaching harness; eight must require a concrete operational or architecture artifact; the remaining eight can combine source reading and calculation. A correct answer may identify that a requested production guarantee is absent. Never require students to deploy the shipped default server as a durable production cluster, rotate real credentials, contact live metadata endpoints, or mutate the evidence checkout.

For coding exercises, place complete scaffolds and reference solutions only under `books/inside-orch/examples/teaching-extensions/exercises`, with runnable commands, test oracles, and source provenance. If importing `internal` packages needs a separate local teaching copy, make that boundary explicit and retain the original checkout unchanged. Scaffold TODO markers may be pedagogical only, with complete corresponding solutions; the delivered book and verification scripts must contain no unexplained placeholders.

## Acceptance and evidence

Create `books/inside-orch/validation/063-exercise-check.json` proving twenty-four unique IDs, exact audience counts, chapter/source linkage, solution existence, rubric coverage, and eight executable entries. Validate every expected answer against the pinned source or an actual checked computation. For trace exercises, serialize initial state and the expected transition sequence so a machine can distinguish wrong state ownership from wrong arithmetic.

Execute safe offline solution checks when available and record skipped prerequisites honestly. A passing reference solution must satisfy its rubric without hidden assumptions, and each executable test must fail for at least one specified incorrect behavior rather than merely mirror implementation. Have a second pass attempt each question using only its stated prerequisites and compare against the solution. Correct missing context and ambiguous grading. Finish with instructor guidance about adapting exercises to a future durable extension while preserving the distinction between repository facts and student-designed improvements.

## Immutable starting references

- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go)
- [internal/rollout/rollout_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout_test.go)
- [internal/health/health_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health_test.go)

## Native appendix contract

Use the first H1 exactly `# Appendix D - Worked Exercises and Design Solutions` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/d-exercises-solutions.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.


---

# Prompt 064 — Appendix E — Operational playbooks and measurement contracts

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `docs/OPERATIONS.md`, `docs/OBSERVABILITY.md`, `docs/RELIABILITY.md`, `docs/LOAD_TESTING.md`, `docs/SCALE_TESTING.md`, `docs/PERFORMANCE.md`, `docs/BACKUP_RESTORE.md`, `docs/UPGRADES.md`, `internal/metrics/prometheus.go`, node monitoring, control-plane operations, migration entrypoints, `cmd/orch-loadtest/main.go`, backup/restore scripts, and the Grafana dashboard. Verify exact metrics, labels, command syntax, and applicability to the memory server.

## Produce operational references

Create `books/inside-orch/manuscript/appendices/e-ops-measurement.md`, `books/inside-orch/runbooks/index.json`, `books/inside-orch/runbooks/playbooks.md`, and `books/inside-orch/reference/measurement-contracts.json`. Write ten playbooks: pending tasks, unhealthy workload, agent enrollment failure, node loss, drain without capacity, rollout failure, GitOps sync/drift failure, quota denial, memory-server restart, and future PostgreSQL restore rehearsal. Each must specify trigger, observation commands, triage order, decision points, bounded action, verification, rollback or stop condition, and the exact supported mode.

Distinguish `/readyz` process readiness from backing-store health; document why a green readiness endpoint does not prove durable orchestration. Explain which background controllers the server actually starts and which leadership/autoscaling metrics may reflect isolated package contracts. Classify alert ideas as proposals until configured and tested. Use source-defined event names, metric types, labels, and error codes; never invent monitoring outputs.

Define measurement contracts for placement success, task convergence, replacement latency, rollout health budget, agent heartbeat age, drift recovery, quota usage, cron occurrence uniqueness, and backup recovery completeness. For every metric, state numerator/denominator or start/stop event, unit, timestamp source, sampling, missing-data behavior, workload size, warm-up, and limitations. Requested resources are reservations, not observed Docker usage; task runtime accounting is not billing. Avoid combining counters with gauges in a way that invents rates.

Provide an experiment sheet for the fake-agent load tool: exact flags, seed, service/node/replica counts, machine and Go versions, duration, raw output, and run status. State prominently that it exercises in-memory control-plane behavior, not Docker startup throughput or PostgreSQL throughput. Provide a separate future durable-cluster measurement plan without fabricated performance numbers or promised service-level objectives.

## Acceptance and evidence

Create `books/inside-orch/validation/064-ops-contract-check.json`. Programmatically resolve all command references against Appendix A, verify every cited metric and label against registered collectors, and ensure all ten playbooks include verification and stop conditions. Parse the measurement JSON and reject missing units, undefined denominators, ambiguous clock origins, and claims without an evidence class.

All irreversible or environment-wide actions must be outside the default exercise path and explicitly scoped to a disposable lab. Backup instructions must state the envelope-key requirement and that the default server does not persist live state in the database. Record actual measurement results separately from empty experiment templates; a template must be labeled unexecuted and contain fully defined inputs rather than invented values. Finish by mapping each playbook to the architecture boundary it tests, so an operator can tell whether the incident concerns intent, placement, runtime execution, identity, or the database extension.

## Immutable starting references

- [internal/metrics/prometheus.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/metrics/prometheus.go)
- [docs/OPERATIONS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/OPERATIONS.md)
- [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go)
- [docs/BACKUP_RESTORE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md)

## Native appendix contract

Use the first H1 exactly `# Appendix E - Operator Runbooks and Measurement Contracts` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/e-ops-measurement.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.


---

# Prompt 065 — Appendix F — Glossary and annotated bibliography

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read all manuscript chapters, appendix references, `go.mod`, actual runtime/client dependencies, original architectural design documents, `docs/ARCHITECTURE.md`, `docs/STATE_MACHINES.md`, `docs/SECURITY.md`, and the public API specification. Inspect the bibliography and claim register already generated elsewhere in the pack. Verify external technical references through official documentation or original papers when available; do not rely on search snippets as citations.

## Produce terminology and sources

Create `books/inside-orch/manuscript/appendices/f-glossary-bibliography.md`, `books/inside-orch/reference/glossary.json`, and `books/inside-orch/reference/bibliography.json`. Include at least sixty useful terms with concise definitions, an orch-specific interpretation, related terms, chapter links, and source provenance. Cover desired versus actual state, reconciliation, convergence, idempotency, optimistic concurrency, task claim, advisory lock, split brain, terminal state, namespace, admission, quota, credential enrollment, secret envelope, SSRF, local volumes, rollout surge, health readiness, GitOps drift, cron concurrency, and recovery objectives.

Definitions must distinguish concepts that readers commonly merge: process readiness and workload health, requested capacity and observed use, local durability and replicated availability, leader election package and activated HA, artifact backup and recovery of live intent. Define the memory server boundary directly. Mark terms that describe future extensions as such; the presence of a term in the glossary does not establish implementation.

Build an annotated bibliography organized around source code/history, Go/Docker contracts, distributed systems, HTTP/security, PostgreSQL/concurrency, observability, and operating practice. Use exact titles, authors or owning organizations, books/inside-orch/publication/version identifiers where applicable, stable URLs, access dates, and a brief explanation of the source's relevance. Repository entries require immutable full-SHA links; moving official documentation needs version or access context. Cite primary sources for technical claims and preserve uncertainty when a URL cannot be accessed.

Include a reading path for each audience with six selected entries and the questions those references answer. Developers should find ownership and test seams, DevOps engineers should find measurement/recovery boundaries, and architects should find consistency and failure assumptions. Explain differences between useful inspiration and evidence for orch behavior. A paper about consensus cannot prove orch implements consensus, and official Docker documentation cannot prove the agent passes every resource field.

## Acceptance and evidence

Create `books/inside-orch/validation/065-reference-check.json` with glossary count, stable IDs, duplicate detection, chapter link status, bibliography metadata completeness, and checked URL outcomes. Machine-check that every manuscript citation resolves to a bibliography entry and that every repository citation resolves to a file or commit in the source inventory. Validate glossary cross-references and reject circular definitions that never identify the mechanism.

Record external access failures as unresolved references with a specific reason; do not replace them with invented publication metadata. Avoid long copied text and license-ambiguous extracts. Inspect all definitions for accidental promises of production readiness, tenancy isolation, automatic rollback, or durable recovery beyond the source boundary. Finish with a short methodological note explaining evidence classes and version pinning, suitable for readers who revisit the book after orch changes. The result must function as a precise navigation aid rather than a list of generic links.

## Immutable starting references

- [docs/ARCHITECTURE.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ARCHITECTURE.md)
- [docs/STATE_MACHINES.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/STATE_MACHINES.md)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)
- [go.mod](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/go.mod)

## Native appendix contract

Use the first H1 exactly `# Appendix F - Glossary, Bibliography, and Boundary Index` with a plain ASCII hyphen. Keep the canonical output at `books/inside-orch/manuscript/appendices/f-glossary-bibliography.md` and preserve its Book.txt entry. Add no YAML front matter to canonical book Markdown. Cross-links must be relative to their originating manuscript file and stay within BOOK, so the native adapter can rewrite them to real `/books/inside-orch/` URLs.

## Site glossary source

Prepare at least three substantive terms for `_data/glossary.yml` under book key `inside-orch`, each with term, definition and a real numbered chapter slug. Keep a larger book glossary in BOOK. Apply the site glossary in the same integration change as catalog registration, since check-site requires its key set to exactly match catalog IDs. Preserve every existing book's glossary.


---

# Prompt 066 — Lab 01 — Initialize the teaching cluster and observe process restart

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `docs/INSTALLATION.md`, `docs/CONFIGURATION.md`, `docs/OPERATIONS.md`, Compose/deployment files, `scripts/dev-up.sh`, `scripts/dev-down.sh`, `cmd/orch-server/main.go`, `internal/controlplane/controlplane.go`, configuration tests, and the CLI client. Inspect the fixture path and startup environment before proposing a command. No Docker run is required or permitted during prompt-pack authoring; execution is an explicitly separate reader activity in a disposable environment.

## Build the lab

Create `books/inside-orch/labs/01-initialization-restart/README.md`, `books/inside-orch/labs/01-initialization-restart/lab.json`, complete manifests/configs under that directory, and evidence-output instructions. Support an offline source-inspection/test track and an optional reader-run Docker track. State prerequisites, precise local addresses, tool versions, working directories, setup ownership, timeouts, and cleanup. Use the locked source without editing it; where files are needed outside the checkout, configure absolute paths instead of rewriting its Compose project.

Start with version and source verification, command help, redacted configuration, local manifest validation, and a capability inventory. Use a complete workload named `book-http` rather than an external sample organization. Capture service/task/node IDs from real JSON responses into a structured lab state file; subsequent commands must read them rather than embed invented UUIDs. Do not contact a live production service or expose an unauthenticated listener beyond loopback.

Teach the central boundary through a controlled server process restart. Before restart, capture services, tasks, versions, namespace objects, and database migration status independently. Stop/restart only the disposable server instance, then repeat read-only API observations. Explain the predicted loss of memory-owned intent as an expected result, not a failed PostgreSQL backup. Existing Docker containers and agent re-registration can complicate observed behavior; record exactly what happens instead of inventing a clean convergence story.

Show that `DATABASE_URL` presence and successful migration commands do not change `NewMemoryService` composition. Inspect `/readyz` before and after restart and explain its limited meaning. Give a short source-reading exercise locating the persistence seam and propose a durable composition design as an extension, with no code change in the evidence repository.

## Acceptance and evidence

Define machine-readable assertions for source SHA, CLI/version output, manifest validity, baseline object counts, captured object IDs, restart boundary, and post-restart observations. Create `books/inside-orch/validation/labs/01-check.json` and a verifier that distinguishes inspection, offline execution, Docker execution, and blocked prerequisites as modes; use standard claim validation values. No expected service count after restart may be presented as an observed count without the raw response and timestamp.

Use bounded polling with deadlines; failed setup must stop before destructive cleanup. Cleanup must act only on this lab's Compose project or captured resource IDs, never global Docker pruning. Check that generated instructions use supported commands and that every file referenced exists. The offline track must reach a useful conclusion without Go module downloads or Docker access by identifying the actual constructor and configuration consumers. Finish with three reader questions about intent durability, agent/runtime survival, and readiness semantics, plus complete evidence-based answers.

## Immutable starting references

- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)
- [scripts/dev-up.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-up.sh)
- [internal/controlplane/controlplane.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go)
- [docs/CONFIGURATION.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CONFIGURATION.md)


---

# Prompt 067 — Lab 02 — Deterministic placement and concurrent task claims

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/scheduler/scheduler.go`, scheduler unit/property/benchmark tests, `internal/store/postgres.go`, task assignment interfaces, `internal/controlplane/controlplane.go`, `internal/controlplane/agent_test.go`, `docs/SCHEDULER.md`, `docs/RESOURCES.md`, and agent capacity reporting. Reconcile stale scheduler documentation against current source for ports, heartbeat handling, and volume constraints. Trace registration, heartbeat, and Docker container spec fields before claiming end-to-end resource enforcement.

## Build the lab

Create `books/inside-orch/labs/02-scheduler-placement/README.md`, `lab.json`, complete fixture inputs, and a separate teaching extension only if existing tests cannot expose required observations. Build a deterministic scenario with three nodes, explicit capacities and allocatable resources, label constraints, public-port conflicts, and six task candidates. Choose fixed IDs and timestamps for fake-state inputs; actual runtime identifiers must be captured from responses.

Ask readers to calculate fit and score before revealing the selected node. Use requests, not limits, for scheduling arithmetic, and state CPU/memory units. Account for non-terminal assigned work, including stopping tasks. Demonstrate lexicographic tie-breaking and stable pending-task order by permuting input order repeatedly. Add one no-fit case whose pending state is a correct outcome rather than a scheduler failure.

Introduce two scheduler passes reading the same pending task and explain the expected timestamp guard. In the in-memory track, run existing concurrency/regression tests and cite their precise oracle. In the PostgreSQL track, specify a disposable database, migration prerequisites, and actual existing test gates; use row-lock/`SKIP LOCKED` behavior only if evidenced by the implementation. Do not call concurrent isolated MemoryService processes an HA cluster.

Expose the agent resource-plumbing boundary: inspect the DTO produced by registration/heartbeat and the container specification used by `CreateContainer`. Compare model resource values, advertised allocatable values, and actual Docker limits. A missing consumer becomes an explicit lab finding; do not patch the source to make the happy path pass. An optional separate extension may add instrumentation or fill the gap, but must compare its behavior against the original.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/02-check.json` with input hashes, expected placements, observed placements, capacity/port calculations, duplicate claims, and execution modes. Machine-check deterministic outputs for at least twenty distinct input permutations; exactly one successful task claim under the chosen concurrency test; no capacity overcommit within the scheduler's accounted model; no assignment to non-ready nodes; and truthful pending behavior for no-fit candidates.

Use `go test` package commands only after discovering exact test names and prerequisites, preserving logs as executed evidence. PostgreSQL absence yields `not_run`, never a synthetic claim result. Require a call-path evidence table from workload request to scheduling accounting and to runtime limit construction, with separate confidence levels. Record documentation mismatches and explain their reader consequence. Cleanup drops only the explicitly created disposable database/schema and removes extension output owned by this lab. Finish with a worked explanation of why atomic claims reduce duplicate placement races but do not solve durable control-plane wiring, leadership, or split-brain recovery.

## Immutable starting references

- [internal/scheduler/scheduler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go)
- [internal/scheduler/property_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/property_test.go)
- [internal/store/postgres.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/store/postgres.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)


---

# Prompt 068 — Lab 03 — Reconciliation and Docker drift ownership

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/reconciler/reconciler.go`, reconciler tests, `internal/controlplane/controlplane.go`, `internal/agent/agent.go`, agent drift tests, `internal/docker/docker.go`, `internal/docker/fake.go`, fake-runtime tests, Docker integration tests, and `docs/RECONCILER.md`. Trace how the shipped memory control plane creates/stops tasks and how the store-backed reconciler package differs. Inspect exact ownership labels and cleanup predicates before designing drift cases.

## Build the lab

Create `books/inside-orch/labs/03-reconciler-drift/README.md`, `lab.json`, fixture descriptions, and an optional isolated teaching harness. Begin with replicas below target, failed tasks with `always` versus `never` policies, scale-down ordering, and soft deletion. Ask the reader to predict task counts and stop directives over two identical passes. Explain that the reconciler changes intent while the agent changes Docker state; neither owns the other's responsibility.

Use fake runtime cases for a missing managed container, a stopped managed container, a mismatched label/image/version, an unexpected owned container, and an unrelated unmanaged container. Derive expected behavior from `currentTaskContainer`, cleanup helpers, and lifecycle validation. In particular, test whether a missing container for a previously running task can be re-created through legal status reports; do not assume resetting to `pulling` is legal. A discovered error is valuable evidence and must be preserved as a boundary finding.

Follow ownership precisely. A matching container may be adopted using its labels; cleanup must never remove another node's workload or an unmanaged container solely because of a name similarity. Show the role of `orch` labels, task identity, node identity, and version. Use short genuine code excerpts with immutable source attribution rather than an invented ideal reconcile loop.

Provide an optional Docker integration track only for the reader's disposable host. Require explicit opt-in, daemon/socket permission checks, captured container IDs, and cleanup by lab-owned IDs or labels. Existing runtime integration tests use `ORCH_DOCKER_INTEGRATION=1`; retain that exact gate. No live Docker execution occurs while generating the pack. Do not imply fake-runtime success validates daemon behavior or restart-safe distributed convergence.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/03-check.json` with each case's initial service/task/container state, expected directive, observed directive, event count, and ownership conclusion. Require repeated unchanged reconciliation to avoid extra pending tasks and duplicate transition events within the tested package contract. Verify scale-down order from actual implementation and demonstrate the preservation of failed non-restartable tasks.

Machine-check that the unrelated container survives every cleanup case and that deleted service terminal state waits for removed-task reports. Record any missing-container transition rejection with exact error and state rather than changing an assertion to disguise a bug. Include raw test output, source SHA, fixture hashes, and explicit runtime mode. If a harness needs internal package access, place a teaching copy under `books/inside-orch/examples/teaching-extensions` and document its diff. Finish with a comparison table: desired-state replica reconciliation, local Docker drift reconciliation, process restart, and database restoration, each with owner, evidence, and remaining limitation.

## Immutable starting references

- [internal/reconciler/reconciler.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go)
- [internal/agent/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go)
- [internal/docker/docker_integration_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker_integration_test.go)
- [pkg/types/lifecycle.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/lifecycle.go)


---

# Prompt 069 — Lab 04 — Rollout, rollback, and availability accounting

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/rollout/rollout.go`, rollout tests, `internal/controlplane/operation_lock_test.go`, `internal/controlplane/rollback_test.go`, service version logic, `pkg/types/lifecycle.go`, `docs/ROLLOUTS.md`, maintenance enforcement, and CLI/API rollout flags and DTOs. Confirm the exact health gate and terminal conditions in code. Inspect the distinction between running and healthy, reserved pause behavior, and the absence of a progress deadline or automatic rollback.

## Build the lab

Create `books/inside-orch/labs/04-rollout-rollback/README.md`, `lab.json`, complete scenario inputs, and an optional deterministic teaching extension. Use three replicas with `maxUnavailable=0` and `maxSurge=1` for a clear baseline. Trace every controller pass with old-version active tasks, target-version active tasks, target healthy tasks, pending stop directives, and deployment status. Ask the reader to predict whether the next action creates, waits, stops, fails, or completes.

Inject slow target health, a target failure, exhausted placement capacity, and stale status reports through existing test seams. Show the safe waiting case when one extra replica cannot be placed and distinguish rollout availability accounting from measured external request success. The controller's model is not proof that an application endpoint experiences no downtime. A service without the required healthy transitions may expose a different boundary; keep that observation explicit.

Demonstrate operation concurrency: a repeated identical active rollout is idempotent, a different rollout conflicts, scale is blocked during active rollout, and delete cancels active work. Cite actual tests or execute an isolated harness with fixed IDs and clocks. Do not invent pause/resume, forced active rollback, progress deadline, or automatic failed-rollout recovery commands.

For rollback, retain the failed deployment history and create a separate rollback deployment targeting the previous successful version. Show the initial baseline special case from source and the rejection when no eligible previous version exists. Inspect maintenance-window enforcement and audited emergency bypass independently; never add `--force` to every example as a default convenience.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/04-check.json` and a timeline CSV with per-step replica budget calculations, health counts, deployment IDs/versions, terminal immutability, and operation outcomes. Machine-check surge never exceeds the configured modeled bound in the deterministic scenario, old-version stops respect the implementation's availability gate, repeated passes do not duplicate target work, and rollback preserves previous terminal records.

Require at least six timeline checkpoints plus three negative operation cases. Compare invariants against actual tests and explain any difference between documented semantics and shipped composition. Test outputs must include real exit codes; source-derived timelines must carry an `expected` label and remain separate from observed values. The Docker track is optional reader activity with explicit prerequisites and workload cleanup; it must not claim measured availability without a real probe trace, timestamp resolution, and sampling contract. Finish with complete answers explaining why a failed rollout can require an operator decision and why a durable controller restart differs from restarting the memory-based server.

## Immutable starting references

- [internal/rollout/rollout.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/rollout/rollout.go)
- [internal/controlplane/operation_lock_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/operation_lock_test.go)
- [internal/controlplane/rollback_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/rollback_test.go)
- [docs/ROLLOUTS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/ROLLOUTS.md)


---

# Prompt 070 — Lab 05 — Secrets, authorization, and healthcheck trust boundaries

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/secrets/envelope.go`, envelope tests, `internal/auth/auth.go`, agent credential tests, `internal/api/api.go`, API authorization tests, redaction helpers, `internal/health/health.go`, health tests, `pkg/types` healthcheck validators, assigned-agent payload construction, and `docs/SECURITY.md`, `docs/SECRETS.md`, and `docs/REGISTRIES.md`. Inspect both input validation and the network client's redirect behavior; neither alone proves SSRF resistance.

## Build the lab

Create `books/inside-orch/labs/05-security-boundaries/README.md`, `lab.json`, complete local fixtures, and any teaching harness under `books/inside-orch/examples/teaching-extensions/security`. Use synthetic one-use secret canaries generated at run time, never real credentials. Keep token/envelope keys in private temporary files or process environment and record only hashes or redacted markers. Define cleanup before the reader runs the exercise.

Demonstrate secret encryption/decryption through the local envelope, metadata-only API reads, namespace-scoped reference resolution, assigned-agent plaintext delivery, redacted errors/audits, and the consequence of losing envelope-key material. Explain that encrypted data in MemoryService remains volatile despite cryptographic protection. List which processes necessarily receive plaintext and what trust assumptions follow.

Test user roles and agent identity separately. Build positive and negative cases for viewer reads, denied mutation, namespace operator scope, cluster administration, bootstrap registration, issued agent credentials, wrong-node reports, and expired/rotated credential handling. Use actual signing/issuer interfaces and source-defined response codes; no hand-written JWT should imply unsupported production identity integration.

For healthcheck security, use local `httptest` servers or loopback-only disposable endpoints. Demonstrate legal relative paths, invalid absolute/protocol-relative inputs where the parser rejects them, same-origin redirects, blocked cross-origin redirects, timeout handling, and bounded response consumption. Do not contact cloud metadata, public attacker infrastructure, private production services, or external DNS targets. Discuss gaps such as address selection and DNS behavior only to the extent the source exposes them; do not claim a complete SSRF defense from a single redirect guard.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/05-check.json` with a case matrix, actor/namespace, expected HTTP result, actual result, secret visibility boundary, and network destinations. Add a canary scanner over captured logs/errors/audits and metadata responses; separate explicitly permitted assigned-agent plaintext from forbidden output so legitimate delivery does not mask leaks. Record scanned file hashes and forbid raw canaries in published evidence.

Machine-check at least twelve authorization/secret/probe cases, including wrong-node denial and blocked cross-origin redirects. Every network connection must remain local and every cleanup target must be lab-owned. Missing crypto/toolchain prerequisites produce explicit skipped status. Verify expected error codes against actual handler mapping rather than assuming all denials are 403. The final explanation must identify the disabled-auth local default, trusted Docker socket privilege, static bootstrap limitations, missing mTLS, and durable-state boundary without declaring the release production-safe. Finish with a complete trust-boundary table that names producer, consumer, permitted sensitive data, enforcement point, and residual assumption.

## Immutable starting references

- [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go)
- [internal/auth/agent.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go)
- [internal/health/health.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go)
- [docs/SECURITY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECURITY.md)


---

# Prompt 071 — Lab 06 — Namespace scoping and atomic quota admission

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/namespace/context.go`, `internal/api/namespace_test.go`, API quota tests, `internal/controlplane/namespace_test.go`, control-plane quota tests, `internal/quota/quota.go`, store namespace/quota locking logic, migrations 000011 and 000012, `docs/MULTI_TENANCY.md`, and CLI quota/namespace commands. Follow namespace selection from CLI/config/header through lookup, reference resolution, and mutation, including routes with query parameters.

## Build the lab

Create `books/inside-orch/labs/06-namespaces-quotas/README.md`, `lab.json`, explicit fixtures, and optional isolated checks. Use two namespaces, `book-payments` and `book-observability`, each containing a service named `api`. Use distinct labels and non-sensitive environment values so accidental cross-scope reads are identifiable. Capture real IDs for executable API steps and use fixed identifiers only in deterministic fake inputs.

Demonstrate default namespace compatibility, selected namespace precedence, namespace-scoped roles, cluster administration, same-name service/secret independence, and cross-namespace object-ID hiding. A request for an inaccessible object must be compared with source-defined not-found behavior. Include the undeletable `default` namespace and deletion blocked by remaining workload/history; explain why deleting visible services may not empty namespace history.

Set concrete quota limits for services, replicas, CPU millicores, memory bytes, public ports, secrets, and registry credentials. Work through the exact accounting arithmetic from per-replica requests and current service state. Show zero limits as unlimited, deletion release semantics, and an update whose denied admission must leave the previous spec unchanged. Public-port quota counts declarations according to implementation, not an invented network allocation metric.

Introduce two concurrent scale requests competing for the last available replicas. Use existing in-memory tests or an isolated teaching harness, then separately define PostgreSQL advisory-lock integration prerequisites. Assert atomic admission only within the tested storage mode. Do not infer hostile tenant isolation, separate networks, separate Docker daemons, or independent control-plane failure domains from logical namespaces.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/06-check.json` with tenant/actor, source route, initial quota, requested delta, expected response, observed response, and final usage. Machine-check at least ten scope/admission cases, including duplicate service names in separate namespaces, cross-ID hiding, secret reference isolation, zero-limit behavior, concurrent capacity competition, and rejected mutation atomicity.

Require the arithmetic fixture to reproduce CPU/memory/replica totals and verify quota denials include actual structured details without secret values. Check the namespace header/query interaction against implementation and record discrepancies. Capture proof that only the admitted concurrent mutation affects final usage; skipped PostgreSQL tests must not inherit in-memory success status. Cleanup removes only lab objects when permitted; retained history gets an explicit explanation rather than direct unsafe database deletion. Finish with a worked architecture review distinguishing logical scoping, RBAC, resource admission, runtime isolation, and durable tenant recovery, identifying what this version implements and which boundaries still require extension.

## Immutable starting references

- [internal/api/namespace_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/namespace_test.go)
- [internal/controlplane/quota_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/quota_test.go)
- [internal/namespace/context.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/namespace/context.go)
- [docs/MULTI_TENANCY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/MULTI_TENANCY.md)


---

# Prompt 072 — Lab 07 — GitOps drift, finite jobs, and cron scheduling

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `internal/gitops/gitops.go`, GitOps tests, `internal/controlplane/workloads.go`, workload tests, `internal/cronjobs/cronjobs.go`, cron tests, `internal/cli/workloads.go`, `pkg/types/workloads.go`, job status handling in the agent, `docs/GITOPS.md`, `docs/JOBS.md`, and `docs/JOBS_DESIGN.md`. Identify which job fields are implemented versus proposed design fields and verify exact CLI YAML parsing before authoring manifests.

## Build the lab

Create `books/inside-orch/labs/07-gitops-jobs-cron/README.md`, `lab.json`, complete service/job/cron manifests, and an isolated local Git fixture. The fixture is a disposable repository owned by the lab, not the source evidence checkout. Prefer an injected fetch adapter for offline tests; if local URLs are not supported by validation, do not invent a supported URL or contact a fake external repository. Document that boundary and use an explicit teaching adapter.

Define a GitOps source with deterministic lexical manifest order, namespace selection, branch/revision provenance, `warn` drift, `auto_revert`, and prune. Show manual scale drift, desired-spec restoration, managed-manifest deletion, preservation of unrelated manual services, and a failed sync that must not trigger unsafe prune. Record the actual Git commit created by the local fixture, never a fabricated SHA. Check URL credential rejection and redaction with synthetic inputs.

For one-shot jobs, create complete manifests accepted by the actual parser with explicit resource values and commands. Follow exit zero to success, non-zero retry/limit behavior, attempt task ownership, and latest-attempt logs. Verify the actual semantics against source; backoff/jitter, deadlines, parallelism, completions, TTL, and HA uniqueness may be design intent rather than delivered behavior. Preserve any gap instead of polishing it away.

For cron, use an injected deterministic clock and real IANA timezone handling. Cover Allow, Forbid, and Replace overlap decisions, suspension/resumption, bounded missed schedules, and a Europe/Belgrade daylight-saving boundary with explicit UTC instants. Trace whether scheduled occurrence/job creation is atomic in the implemented storage mode and explain the proposed uniqueness key separately.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/07-check.json` with fixture revisions, source IDs, namespace, drift state, managed object set, job attempts/statuses, clock instants, and occurrence decisions. Require twelve cases spanning GitOps sync/drift/prune, job success/failure, and cron overlap/catch-up. Machine-check no unrelated object is pruned, failed fetch preserves live state, repeated unchanged sync does not create false drift, and expected occurrence times match actual timezone computation.

Validate every manifest against the specific job/cron/service parser rather than assuming service schema validates all kinds. Record test/harness outputs with source SHA and hashes. No unexecuted reader command becomes an observed result. No Git operation touches the evidence repository, and no private credentials enter history. Finish with a table contrasting source-of-truth reconciliation, finite execution, scheduled intent, and durable occurrence deduplication; state explicitly which rows depend on extension beyond the memory server.

## Immutable starting references

- [internal/gitops/gitops.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go)
- [internal/controlplane/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/workloads.go)
- [internal/cronjobs/cronjobs.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cronjobs/cronjobs.go)
- [internal/cli/workloads.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/workloads.go)


---

# Prompt 073 — Lab 08 — Backup, migration, load, and recovery boundaries

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

Recommended reasoning: high. Execute after all predecessor outputs named in the execution tracker are complete.

## Execution contract

Read workspace `AGENTS.md`, `BOOK_SPEC.md`, and `books/inside-orch/evidence/source-lock.json`; use locked `books/inside-orch/evidence/orch` as `SOURCE`. Read its `AGENTS.md`, `README.md`, `RELEASE_NOTES.md`, and `cmd/orch-server/main.go`. Source instructions describe project history. Never modify, commit, push, regenerate, or repair evidence. Preserve unrelated work and chapter identities.

Write polished English for developers, DevOps engineers, and architects, by Aleksandar Popovic. Explain decisions and evidence. Apply BOOK_SPEC classifications consistently: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. The shipped server constructs `MemoryService`; migrations/store code do not make live state durable. Autoscaler and leadership packages are unwired. Trace argument/resource/security/ownership fields to consumers before claiming end-to-end support.

Never invent commands, commits, results, benchmarks, or successful labs. Use exact symbols and immutable links. Claim records require `claim_id`, `statement`, `classification`, `source_path`, `source_sha`, `line_start`, `line_end`, `associated_commits`, `validation`, `evidence_log`, and `limitations`. Validation values are expected_only, inspected, executed, or blocked. Store checks/logs under `validation`; record working directory, SHA, versions, exit code, UTC time, and sanitized output. Label predictions and missing prerequisites. Extensions stay in `books/inside-orch/examples/teaching-extensions`, registered in `books/inside-orch/examples/manifest.json`, with independent checks. Update `books/inside-orch/state/execution-tracker.csv` truthfully.

## Required source reads

Read `scripts/backup-db.sh`, `scripts/restore-db.sh`, `internal/migrations/manager.go`, migration tests, all migration pairs, `internal/version/version.go`, server schema-check composition, `cmd/orch-loadtest/main.go`, scale tests, `docs/BACKUP_RESTORE.md`, `docs/MIGRATIONS.md`, `docs/UPGRADES.md`, `docs/LOAD_TESTING.md`, and `docs/SCALE_TESTING.md`. Trace exact script arguments, required database URLs, migration locking, and down-migration authorization.

## Build the capstone lab

Create `books/inside-orch/labs/08-recovery-boundaries/README.md`, `lab.json`, experiment inputs, and recovery verification instructions. Separate three tracks: offline schema/source analysis, fake-agent load measurement, and optional reader-run PostgreSQL backup/restore into a disposable replacement database. No Docker or PostgreSQL operation runs during authoring. Every database URL must be supplied by the reader's lab environment; never embed credentials or default to a production connection.

Use a precise inventory of desired state, actual observations, events/audit, encrypted secret rows, envelope-key material, Docker images/volumes, runtime configuration, and monitoring data. State which belong in a database dump and which require separate protection. Most importantly, demonstrate that a dump of the existing database cannot recover live intent owned by the shipped MemoryService. A successful restore proves restoration of database artifacts within its scope.

For migrations, inspect up/down directions, run status/up/up idempotency in the optional database track, verify locking/compatibility tests, and show explicit rejection of down without `--allow-down`. Do not execute destructive down or clean restore against an existing environment. Prefer restore into a fresh named replacement and check schema, row counts, references, and secret decryptability with the same envelope key.

For fake load, use the actual `orch-loadtest` flags with a fixed seed and bounded duration. Capture machine/Go versions, workload size, raw counters, errors, convergence timing, and execution status. Repeat only if the experiment asks a meaningful variance question. No fake-agent number may be described as Docker performance, PostgreSQL throughput, production capacity, or a service-level objective.

Define recovery objectives as a proposed measurement contract: exact start/stop events, intended-state completeness, missing secrets, orphan containers, agent re-enrollment, application validation, and residual data loss. A future durable extension can supply its own evidence separately, but cannot retroactively change claims about the locked release.

## Acceptance and evidence

Create `books/inside-orch/validation/labs/08-check.json` with track status, prerequisite checks, dump hash, source/target database identities redacted safely, schema versions, row-count comparisons, decryption outcome, load inputs/output, and recovery claim scope. Machine-check migration pairs and declared compatibility ranges, repeat-up idempotency when executed, and restoration only into the lab's replacement target.

A recovery pass requires all defined restored-artifact checks; full live orchestration recovery remains `unsupported_default_runtime` unless a separately labeled extension is executed and tested. Guard scripts must reject empty target identity and accidental source/target equality. Confirm cleanup deletes only lab-owned files/databases and preserves raw measurement evidence. Finish with complete answers explaining why backups, restart safety, controller leadership, and measured workload capacity are distinct guarantees. The capstone must leave the reader able to audit a future production proposal without confusing repository scaffolding with proven behavior.

## Immutable starting references

- [scripts/backup-db.sh](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/backup-db.sh)
- [internal/migrations/manager.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/migrations/manager.go)
- [cmd/orch-loadtest/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-loadtest/main.go)
- [cmd/orch-server/main.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/cmd/orch-server/main.go)


---

# 074 — Synchronize and verify exact source excerpts

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** excerpt-sync

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Review every source listing, inline symbol reference, pseudocode block and repository-derived configuration example. Build an excerpt inventory that distinguishes exact source, adapted explanation, historical source and teaching extension. An exact excerpt must identify the full SHA, repository-relative path, source line interval and excerpt hash. Generate its text from that locked file; never manually reconstruct it from memory or a README. Include imports and surrounding context only when needed to understand the listing, but explain any omitted code without pretending the shortened listing is independently executable.

For each source excerpt, compare the displayed text with the cited version byte for byte after the documented presentation transform. A transform may add line numbers or dedent a block, but it must not change identifiers, error branches or control flow. Hash raw and transformed text separately. An adapted example needs a visible label, an explicit account of changes and its own validation target. Historical and current examples must not share a misleading common link. The root compose file was once docker-compose.yml and is compose.yaml at the snapshot: preserve historical filenames in historical links and verify current paths independently.

Prioritize passages describing MemoryService construction in cmd/orch-server/main.go, scheduling and reconcile paths, WithTx, Docker ContainerSpec, digest parsing, agent status DTOs, secrets encryption and leadership. Verify the exact symbol exists and that a quoted test exercises the explained function. A current caller can bypass a perfectly correct package, so the excerpt annotation must identify the execution path rather than relying on the package name. Do not quote a PostgreSQL implementation as evidence that the server persists live state.

Produce books/inside-orch/validation/excerpts/index.json with chapter, block id, kind, full SHA, file path, line interval, raw hash, displayed hash and checked transform. Add a reproducible extraction/check command with clear diagnostics for stale text, incorrect anchors and renamed files. Source links must use immutable blob SHAs with measured line numbers. Verify all code and configuration excerpts; sampling is insufficient for this mechanical task. Acceptance requires an inventory entry for every repository-derived block, zero unlabelled adaptations, zero unsupported historical substitutions, and successful regeneration without modifying the source corpus.

Deliver books/inside-orch/validation/reviews/excerpt-sync.md and books/inside-orch/validation/reviews/excerpt-sync.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 075 — Compile and test runnable teaching examples

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** code-compilation

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Inventory every example that the book presents as runnable, including Go files, command fragments, Compose YAML, HTTP requests, deployment manifests and sample API clients. Classify whether it is a complete program, a fragment, an exact repository excerpt or a teaching extension. Fragments must say what package, imports and setup they need. Do not make a fragment appear runnable merely by surrounding it with a fence. Use books/inside-orch/examples/teaching-extensions/ for new code and disposable copies for builds of baseline or historical source.

Construct a validation matrix keyed by chapter and example id. Record the intended Go version from the relevant locked go.mod, dependencies, runtime services and optional environment flags. Compile complete Go examples and execute their focused tests; use source-confirmed Makefile or module commands instead of assuming a toolchain version. Parse relevant YAML and JSON and, when available, run the appropriate Compose configuration validation. Validate OpenAPI only to the scope supported by the chosen validator. A syntax parser is not semantic schema validation or complete request/response conformance.

Use meaningful checks for teaching code. For a scheduler demonstration, assert ready-node selection, capacity limits, port conflicts and deterministic tie-breaking. For cancellation, assert the goroutine exits after cancellation. For idempotent runtime behavior, repeat an operation and verify no duplicate managed container. Avoid tests that just repeat the example's assignment. Keep commands from touching the live Docker socket or a user database until the lab has an explicitly isolated environment. Missing Docker, PostgreSQL or dependencies must produce blocked status with exact prerequisites; an ordinary Go test pass cannot certify optional integration behavior.

Inspect the default server and distinguish compilation from wiring. The presence of compiled autoscaler and leadership packages does not mean the binary starts them. A parser-only image resolver does not prove network digest resolution. Teaching additions that wire persistence or leadership must remain labelled extensions, never changes to the pinned baseline. Record exact additions, independent tests and the boundary they address.

Write books/inside-orch/validation/examples/manifest.json and individual build/test logs. Acceptance requires every runnable example to have an executable validation target and observed outcome, every fragment to have clear context, and no silent source patch to obtain a pass. Release readiness requires no unvalidated mandatory runnable examples; this review may accurately remain blocked until the required execution environment exists.

Deliver books/inside-orch/validation/reviews/code-compilation.md and books/inside-orch/validation/reviews/code-compilation.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 076 — Execute all eight connected laboratory exercises

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** lab-execution

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Read the eight lab definitions and their dependency order. Build a disposable lab environment, with unique resource names, a dedicated database when required and an explicit Docker context. Record OS, Go version, Docker and Compose versions, source SHA, configuration hashes and environment prerequisites while redacting secrets. Verify that every command in the lab exists in the locked CLI or scripts. Separate the intended observation from actual output in the manuscript before starting.

Execute the labs in their stated order and capture each command's result. Connect the evolving service state between labs explicitly rather than assuming a previous environment survived. Each lab needs setup, action, bounded observation, assertion, cleanup and rerun criteria. Use bounded polling for asynchronous state instead of arbitrary long sleeps. Record identifiers and expected task/container counts so another reader can distinguish incomplete convergence from a broken system. Preserve failed observations as evidence and correct the book rather than deleting inconvenient logs.

Prioritize failure experiments with clear scope. A controller restart that retains the same MemoryService object does not represent an orch-server process restart. A fresh server process loses baseline live memory state even when PostgreSQL tables exist; demonstrate this only inside the isolated lab and explain the boundary. Reusing FakeRuntime is not a real Docker daemon recovery experiment. Namespace RBAC checks do not prove hostile tenant isolation. A fake 1,000-service load scenario does not certify real containers, image pulls or PostgreSQL throughput.

If a lab explores persistence wiring, leader election, autoscaling, distributed storage or registry digest fetching absent from the default runtime, route it to a separately versioned teaching extension. Execute that extension independently and compare its observations with the baseline. Do not merge extension results into baseline capability claims. For secret labs, protect plaintext from shell traces and captured output. Destructive restore, container deletion and network faults must target only the lab's dedicated resources, with a verified cleanup inventory.

Write books/inside-orch/validation/labs/lab-01 through lab-08 result records and logs, plus books/inside-orch/validation/labs/summary.json. Include convergence timing as an observation with environment context, not a universal benchmark. Acceptance requires observed results for all mandatory labs, reproducible cleanup, corrected instructions after any failed command, and exact documentation of the experiment scope. Any missing mandatory prerequisite is a release-blocking gap; expected results alone cannot make a lab executed.

Deliver books/inside-orch/validation/reviews/lab-execution.md and books/inside-orch/validation/reviews/lab-execution.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 077 — Review composition, invariants and architectural guarantees

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** architect-review

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Trace actual process construction before reading architectural diagrams. Start at cmd/orch-server/main.go and cmd/orch-agent/main.go, follow injected dependencies and identify state owners, API handlers, active controller loops and runtime adapters. Compare the default MemoryService paths with the standalone scheduler, reconciler and PostgreSQL store packages. Draw separate diagrams for current executable topology, implemented but unwired packages, and proposed extensions. An arrow to PostgreSQL must mean a real call path, not a design intention.

Review each guarantee against a stated invariant, failure domain and persistence boundary. Examine task identity, retries, status transitions, replica convergence, concurrent operations, rollout health gates, capacity accounting, port allocation, namespace isolation and local volume attachment. Describe the time window in which a guarantee can fail, including server process loss, delayed heartbeats, partition healing and duplicate controller activity. Local mutex protection is not cross-process transaction safety; a claimed task is not fencing for a still-running container on an isolated node.

Treat the important gaps as teaching material. The default server retains live state in memory; backups and migration pairs do not solve runtime durability. Leadership and autoscaling packages exist but are not started or used by the default server. Autoscaling stabilization and a real metrics provider have additional scope limits. ParserResolver accepts supplied digests but does not fetch registry digests. Local volumes do not provide distributed storage, stable stateful identities or safe failover. Namespace-aware IDs and RBAC do not imply network or hostile tenant isolation.

Assess design tradeoffs without replacing the book with a hypothetical platform. Compare alternative mechanisms only when they answer a concrete current constraint: store wiring, transaction boundaries, ownership, advisory locks, durable queues, reconciliation generations or resource enforcement. For an improvement, specify the smallest compositional change, migration cost and new failure modes. Make evidence-backed recommendations separate from source facts.

Produce books/inside-orch/validation/architecture/topology.md, a guarantee matrix and prioritized review findings. Each matrix row needs claim, component, active caller, state owner, atomicity/persistence boundary, failure scenario, source anchors and observed validation. Check all diagrams against this matrix. Acceptance requires accurate current topology, explicitly bounded guarantees and no remaining major claim of durability, HA, isolation or enforcement unsupported by the executable. Library correctness and system guarantees must have separate evidence even when their code shares an interface.

Deliver books/inside-orch/validation/reviews/architect-review.md and books/inside-orch/validation/reviews/architect-review.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 078 — Review source-guided explanations for working developers

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** developer-review

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Read the developer path in chapter order as an engineer new to the repository. Verify that each explanation starts with a concrete problem and follows enough real code to make the solution understandable. Check the progression from types and validation to API/client contracts, runtime labels, task status reports, scheduler decisions, reconciliation, rollout and tests. The reader must be able to locate every described symbol at the cited full SHA without guessing package names or following a mutable branch.

Focus on semantics rather than code paraphrase. Explain why a context is propagated, where cancellation is observed, which layer handles an error, how idempotency keys or container labels establish identity, what a transaction protects and where deterministic ordering matters. Verify typed states against legal transition helpers. Check that request DTOs, JSON tags, YAML fields, enums and errors use exact repository forms rather than prompt examples that later changed. Teach retryable errors and failure windows with a real call path and a focused test.

Trace alternate implementations honestly. The baseline API uses MemoryService and may reconcile or place tasks differently from the standalone scheduler/reconciler package. A chapter teaching scheduler scoring must name the caller and conditions under which that algorithm is used. A PostgreSQL method or WithTx example is a implemented-package lesson until runtime wiring exists. The resource quantity parser, admission accounting and Docker enforcement have separate responsibilities; carry fields through API-to-agent-to-runtime DTOs before stating CPU or memory limits are enforced.

Inspect exercises and code walkthroughs for missing prerequisites, excessive source dumps and unexplained setup. Exact code listings must link to measured source intervals. Adapted examples must identify their changes and run independently. Avoid claiming unrun tests pass because the repository includes a test file. Explain what fake runtime, fixed seeds and table-driven cases prove and what they exclude. Every complex chapter should have a failure scenario that motivates the implementation and a minimal test or experiment to investigate it.

Produce an ordered reading report with comprehension obstacles, incorrect explanations, missing symbol context and suggested repairs. Acceptance requires all important behavior descriptions to match source and active call paths, every runnable developer example to reference its validation target, and no unexplained leap between a requested prompt and observed implementation. Leave valuable unsolved extensions explicitly labelled, with clear invariants and tests that a reader would need to add.

Deliver books/inside-orch/validation/reviews/developer-review.md and books/inside-orch/validation/reviews/developer-review.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 079 — Review operations, recovery and troubleshooting guidance

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** devops-review

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Follow the DevOps reading path from install through configuration, deployment, health, logs/events, secrets, node drain, observability, upgrades, migrations and recovery. Validate commands against the locked binary and scripts. Record user-facing permissions, listening ports, filesystem mounts, Docker daemon access, network assumptions and component versions. Installation examples must pin a release when reproducibility matters and distinguish the chosen HEAD source edition from tagged release artifacts.

Give each runbook a trigger, prerequisites, evidence to gather, action, bounded expected observation, verification and cleanup or rollback. Trace configuration precedence and secret redaction against real load/print functions. Verify Compose and systemd examples as examples rather than claiming they make the default server durable or highly available. The root compose file is compose.yaml at the snapshot; historical docker-compose.yml references need historical context. Explain privileged Docker socket access through the actual agent deployment.

Review recovery with particular care. A PostgreSQL dump restores database rows, not the live MemoryService state of the baseline server, Docker volumes, master encryption keys, image registries or log/metrics storage. Schema checking and migrations do not wire persistence. A restart scenario preserving the same service object exercises a loop restart rather than a full process failure. Node-offline replacement and partition healing can have different effects from ordinary draining; do not promise fencing or exactly-once execution without proof. Stateful failover remains a design boundary.

Evaluate alerts, dashboards and capacity tests against emitted metrics and active controller paths. An alert referring to a metric unused by the default process must explain its conditions. Labels and dimensions must match source, including cardinality risks. Autoscaler and leadership modules are not active default loops. The fake scale tool's timings describe scheduler/reconciler behavior in its chosen in-process environment; they are not real-cluster service density or database throughput figures.

Review upgrade prerequisites, supported schema and agent versions, opt-in schema checking, down-migration authorization and whether reversal can delete data. Use source and migration SQL instead of assuming every down file is safe. Test destructive procedures only against dedicated fixtures.

Produce a runbook matrix with command fidelity, risk boundary, validation log and recovery scope. Acceptance requires operational instructions to use real supported commands, explicit isolated experiments and accurate books/inside-orch/state/backup boundaries. Mandatory runbooks lacking execution evidence or containing unsupported recovery guarantees must block publication as a complete operational edition.

Deliver books/inside-orch/validation/reviews/devops-review.md and books/inside-orch/validation/reviews/devops-review.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 080 — Review security claims, threat paths and redaction

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** security-review

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Review the security narrative against a threat model with distinct operator, viewer, namespace administrator, authenticated workload author, compromised agent and unauthenticated network actor. Trace user JWT/RBAC and agent authentication separately. Verify token issuance, expiration, rotation and revocation against code and tests; do not describe planned mTLS as active. Record trust in the Docker daemon, host socket and node identity. Avoid presenting a lab bootstrap token or example password as a production secret configuration.

Inspect all exposed listeners and outbound request paths. Verify API authentication and authorization for namespace-scoped reads/writes, logs, secrets metadata, registry credentials, audit search and debug/profiling access. Internal DNS and optional provider endpoints need their actual binding and exposure conditions. For healthchecks, trace constructed targets, path validation, port selection, redirects, timeouts and response-body limits. Healthcheck SSRF protections do not automatically cover notification webhooks or GitOps repository fetching; review each egress mechanism independently.

Trace secret data from input to storage, agent DTO, environment injection, logs, errors and captured lab output. Encryption in the PostgreSQL package is not evidence of durable encrypted live state in the default memory runtime. The local envelope key remains a separate operational secret. Notification signing secrets, retries and write-only API representations must be explained according to their real state path. Describe at-least-once notification delivery and receiver deduplication rather than implying exactly-once events.

Review container security context, host namespaces, privileged mode, capabilities, mounts and resource enforcement through the actual Docker adapter. Admission policy and runtime enforcement are separate controls. Logical namespaces do not provide hostile tenant network or host isolation. Supplied image digests are not remote verification; signing and vulnerability scanning are design documents without runtime enforcement. Make every restriction's default, override and enforcement point explicit.

Inspect all manuscript files, examples and validation logs for leaked tokens, private keys, plaintext secret values, user credentials and private author metadata. Redact without erasing the diagnostic structure needed to understand a test. Use isolated test fixtures and controlled targets for security experiments. Do not attempt exploitation of a live site or shared cluster.

Deliver a threat/control matrix, prioritized findings and source-linked redaction results. Acceptance requires no leaked sensitive material, no major unsupported security claim and clear coverage boundaries for active controls, unwired modules, design-only controls and tested extensions. A security review accurately blocked on execution is preferable to an unearned certification.

Deliver books/inside-orch/validation/reviews/security-review.md and books/inside-orch/validation/reviews/security-review.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 081 — Audit every technical claim and its guarantee boundary

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** claim-guarantee-audit

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Inventory factual claims across all chapters, appendices, captions, diagrams, callouts, exercises, catalog copy and summaries. Include small statements such as a default port, encoded timestamp, CLI flag or JSON field, plus broad claims such as durability, HA, isolation, performance and production readiness. Every claim must have a stable id and a classification from BOOK_SPEC.md. Inferences must say how evidence supports them and what assumptions remain.

Validate the claim schema and then assess semantics. A record with source_sha and a link is not sufficient if the cited line does not establish the statement. Exact code can demonstrate a branch, inspected tests can show an intended scenario, and executed logs can demonstrate one environment's result. Keep expected_only, inspected, executed and blocked distinct. Associated commit SHAs establish relevant history, not a literal execution transcript. Source prompts 00–28 were added after June implementation; late prompts share batched commits. A completed execution tracker cannot close a capability or guarantee gap.

Apply a mandatory checklist to major claims. Live server state is owned by MemoryService, with PostgreSQL implementation not wired into the baseline. Default server loops do not use the leadership package or start autoscaling. Scheduler planning and MemoryService placement may use different paths. Docker limits require an end-to-end field trace. ParserResolver does not fetch remote digests. Local volume attachments do not provide distributed stateful failover. Namespaces do not establish network/host isolation. Fake scale measurements do not measure real containers or PostgreSQL throughput. Supply-chain scanning, image signing, CNI and external plugin execution remain proposals.

For reliability guarantees, require a defined failure model and boundary: process, controller, host, network, database, daemon or external service. A loop restart with the same memory object cannot prove process durability. Atomic assignment cannot guarantee a removed or isolated worker stopped a prior container. Retry-safe metadata does not automatically imply exactly-once side effects. Upgrade compatibility metadata is not proof of safe mixed-version operation across every API.

Write books/inside-orch/validation/claims/index.json and a contradiction register linking statement, evidence, counterexample, correction and affected artifacts. Repair unsupported prose by narrowing the claim or labelling a proposal, not by quietly extending the application. Acceptance requires every substantive engineering claim to have support of the appropriate scope, all major guarantees to be bounded and no contradictory representation between a chapter, diagram, catalog blurb and release summary. Release-critical unverified claims must remain visible blockers.

Deliver books/inside-orch/validation/reviews/claim-guarantee-audit.md and books/inside-orch/validation/reviews/claim-guarantee-audit.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 082 — Verify CLI commands, API routes and configuration examples

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** command-api-fidelity

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Extract every shell command, CLI transcript, environment variable, YAML field, HTTP route, header and JSON payload from manuscript, appendices, labs and website examples. Build a machine-readable inventory with chapter, block id, source definition and validation target. Check each against the locked CLI command tree, request/response DTOs, route registration, config loader and scripts. Development prompts show intended interfaces; use actual code for the edition's interface promises.

Verify command syntax, positional arguments, required flags, aliases, output modes, namespace selection and error behavior. Current root Compose uses compose.yaml. Determine whether scripts invoke modern docker compose or a different executable before publishing commands. Confirm migrate status/up/down syntax, explicit down authorization, schema-check environment behavior, version output, cronjob suspend/resume and workload commands from source. Do not infer an option from a design document or generate a command that merely looks conventional.

Trace API contract fidelity beyond parsing api/openapi.yaml. Compare methods, paths, authentication, namespace headers, status codes, field names, enums, request validation, errors, pagination/filtering and streaming behavior. Public endpoints and internal agent endpoints must remain clearly separated. Unknown field tolerance, deprecation headers and response timestamps require actual evidence. A passing YAML/OpenAPI parser does not establish complete route, schema or example conformance.

Validate namespace and secret examples with harmless fixtures. A global role differs from namespace_roles; object-id hiding and per-namespace names need correct examples. Never include live credentials or plaintext production values in output snapshots. A supplied digest can be accepted or required, but no network tag-to-digest behavior should be implied by ParserResolver. Deployment examples claiming resource enforcement need a separate API-to-agent-to-Docker field trace rather than valid-looking resource syntax.

Run read-only or fixture-backed commands wherever possible. For mutation commands, use the isolated lab environment and include cleanup. Preserve actual error/status output instead of replacing it with an attractive invented transcript. Clearly label expected responses until observed. List unavailable prerequisites with exact blockers and rerun criteria.

Produce books/inside-orch/validation/interfaces/inventory.json, API comparison findings and command logs. Acceptance requires zero fictional commands, routes or fields, correct namespace/auth examples, and every executable transcript to match an observed command or carry an expected-only label. Resolve mismatches in the book while keeping the immutable baseline intact. Complete contract testing is a distinct result and must never be inferred from structural spec validation alone.

Deliver books/inside-orch/validation/reviews/command-api-fidelity.md and books/inside-orch/validation/reviews/command-api-fidelity.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 083 — Copyedit technical prose without changing its meaning

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** copyedit

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Read the entire manuscript for clarity, continuity, terminology, accuracy-preserving concision and reader orientation. Preserve the author as Aleksandar Popovic and the destination https://www.alekpopovic.com. The public narrative is an engineering book about a real system; generation prompts and writing workflow belong in the pack. Remove repetitive generic praise, unsupported adjectives, artificial suspense and filler. Keep distinctions that materially affect understanding even if they make a sentence longer.

Maintain a terminology sheet for service, task, container, node, deployment, rollout, desired state, actual state, reconciliation, scheduling, admission, namespace, claim, attachment and runtime. Do not interchange these terms casually. Spell commands, package paths and symbol names exactly as in the pinned source. Keep capability labels consistent: runtime-integrated, implemented package, partial integration, design only, teaching extension and future work. An editorial rewrite must never collapse these into done, supported or production-grade without evidence.

Review the three reader paths. Define a prerequisite before using it, link to the right chapter and preserve local readability for online visitors. Give each chapter a concrete motivating problem and a coherent argument that connects code to behavior. Make cross-references precise, remove abandoned numbering and check that historical narratives distinguish current HEAD from the associated historical commit. Source prompts added retrospectively should not be described as observed June prompt executions.

Guard the most consequential wording. Do not polish away the default MemoryService durability limit, unwired leadership/autoscaling, parser-only digest resolution, local storage scope, namespace isolation boundary or fake load-test interpretation. Replace claims such as guarantees safety with the actual invariant and conditions. Preserve expected-only versus executed lab observations and limited validator scope. A human-readable shortened explanation must still distinguish package tests from integrated process behavior.

Inspect headings, code introductions, captions, callouts, exercise wording, answer placement and references for consistent voice. Avoid long unstructured listings and define omissions when a code block is shortened. Leave code bytes and source anchors untouched unless an excerpt issue is filed for its dedicated review. Standardize units, UTC notation, version spelling, capitalization and punctuation without inventing facts.

Deliver books/inside-orch/editorial/TERMINOLOGY.md if absent, a copyediting change log and a concise unresolved-query list. Acceptance requires clear connected prose, consistent terms and no semantic weakening of capability or validation boundaries. Technical questions that cannot be resolved from source must remain review findings; prose smoothness is not sufficient grounds to mark them fixed.

Deliver books/inside-orch/validation/reviews/copyedit.md and books/inside-orch/validation/reviews/copyedit.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 084 — Review exercises and independently justify worked answers

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** exercises-solutions

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Inventory three to five exercises per chapter and all worked answers in books/inside-orch/manuscript/solutions/. Match exercise ids, chapter links, prerequisites, expected difficulty, learning outcomes and solution references. Include progressively harder reasoning, source investigation, safe experiments and optional extension design rather than repeating comprehension questions. Every exercise must be solvable from the chapter, the pinned source or explicitly stated prerequisites; do not require an undocumented production environment.

Solve representative reasoning exercises independently before reading the supplied answer, then inspect every answer for correctness. For code exercises, run focused tests where feasible and record results. A correct solution needs either execution evidence or a clear argument with assumptions and counterexamples. An answer that simply restates the implementation is inadequate for an invariant question. Confirm that source-search questions name existing paths and exact symbols at the locked SHA.

Use the repository's real boundaries to teach judgment. Ask readers to compare MemoryService and PostgreSQL ownership, a controller restart and a fresh process, an atomic claim and a fencing guarantee, scheduling accounting and Docker enforcement, a supplied digest and remote registry resolution, namespace RBAC and network isolation, local storage and stateful failover, or fake-agent convergence and production throughput. Solutions must explain the differences without promising missing integration. A completed tracker or well-named test does not prove the broader guarantee.

Separate baseline investigation from teaching extensions. A persistence-wiring exercise should identify the required transaction, interface, restart and migration tests, not silently prescribe an unverified drop-in change. A leader-election exercise should consider lock/session lifecycle, loss detection and side-effect ownership. Autoscaling work should identify metrics provider, cooldown durability and stabilization limits. Any design-only signing, CNI, plugins or scanning exercise must be labelled a proposal and describe what validation would be required.

Review safety and cleanup for operational exercises. Use dedicated lab objects and simulated failures wherever appropriate; prohibit accidental interaction with the user's live database or shared Docker workloads. Replace vague expected outcomes with bounded observable criteria and specify when several approaches are acceptable. Include hints separately so the answer does not spoil the investigation immediately.

Produce books/inside-orch/validation/exercises/index.json and solution-verification logs. Acceptance requires one correct answer for each exercise, no orphan ids, honest validation status and useful progression in difficulty. Mandatory executable exercises with missing prerequisites remain blocked; reasoning-only exercises may be accepted through explicit review. Count exercises only after verifying their substance, not merely the presence of numbered headings.

Deliver books/inside-orch/validation/reviews/exercises-solutions.md and books/inside-orch/validation/reviews/exercises-solutions.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 085 — Lock and validate all source, history and cross-reference links

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Reasoning:** high
**Scope:** evidence-link-lock

```text
Work as an independent technical reviewer of Inside orch: Building and Operating a Docker Orchestrator in Go, by Aleksandar Popovic. Read AGENTS.md, BOOK_SPEC.md, books/inside-orch/evidence/source-lock.json, the chapter map, the capability ledger and books/inside-orch/editorial/QUALITY_GATES.md before reviewing. Freeze the full source SHA; review historical material at its separate cited SHA. The application corpus under books/inside-orch/evidence/orch/ is immutable. Run commands against disposable copies when execution is necessary. Inspect manuscript and prior validation artifacts before deciding what needs attention. If the required manuscript, examples, prerequisites or source evidence are missing, record a concrete blocker rather than manufacturing a pass. Do not silently implement missing application features to make the book's claims true.

Inventory every link in manuscript, appendices, solutions, diagrams/captions, HTML metadata, catalog copy and downloadable artifact references. Separate pinned repository source, associated commits, prompt evidence, external primary documentation, internal chapter anchors and publication downloads. Freeze full 40-character SHAs for source and commit links. Reject mutable main/master blob links used as source evidence, abbreviated commit identifiers used as locks, invented line anchors and unverified public download paths.

Read books/inside-orch/evidence/source-lock.json and the complete prompt-to-commit map. Verify all 91 prompt ids appear exactly once in the source provenance mapping, while allowing one implementation commit to support multiple prompts. Nine source prompts are design requests; later MVP implementation does not make their entire design active. Prompts 00–28 were added retrospectively after June work, and prompts 62–90 are diff-supported batches. Commit relationships must preserve those distinctions and cannot claim literal prompt execution without a transcript.

For each historical source link, verify the path exists at its cited commit and that line intervals match the excerpt. For current source links, use the locked HEAD and its current filenames. The historical docker-compose.yml became compose.yaml in HEAD; do not point a historical path at a current SHA. Associated implementation commits differ from prompt-introduction commits. The 0.3.0 tag points at the formatting-gate follow-up, while HEAD is a later documentation change. No local 0.2.0 tag exists in the reviewed corpus. Check release publication metadata separately when a date is claimed.

Validate internal anchors after the final heading normalization used by HTML and EPUB generation. Test chapter-to-solution links, diagrams' references, footnotes, table references and path-based asset links. Ensure PDF reference text is legible and online source links remain clickable. External documentation may change; record retrieval date and exact subject supported, prefer official primary sources, and do not let an unavailable network check masquerade as a successful fetch. Local Git object existence proves a repository anchor but not external HTTP reachability.

Write books/inside-orch/evidence/link-lock.json with origin, destination, type, SHA/line fields, local verification, network status and checked UTC time. Add reproducible link checks with explicit offline behavior. Publication downloads must be validated against actual build outputs and checksums, not prospective URLs.

Acceptance requires complete link inventory, zero mutable source-evidence links, correct historical/current path separation, valid local cross-references and a machine-readable distinction between local proof, fetched links and blocked network verification. Missing source objects, invalid anchors or fabricated release/download links block a complete edition.

Deliver books/inside-orch/validation/reviews/evidence-link-lock.md and books/inside-orch/validation/reviews/evidence-link-lock.json. The readable review must identify what was inspected, what was executed, what remains blocked, each finding's consequence, and the exact acceptance condition for its repair. The JSON must include source_sha, reviewed_paths, reviewer_scope, findings, checks and overall_status. Each finding needs a stable id, severity, target, relevant claim_ids, source evidence, recommended_action and resolution_status. Each executed check needs its command, working directory, prerequisites, UTC start/end, exit code and log path; distinguish passed, failed, blocked and not_run. Source inspection alone is not execution. Update chapter claim records using their schema: claim_id, statement, classification, source_path, source_sha, line_start, line_end, associated_commits, validation, evidence_log and limitations. Allowed claim validation values are expected_only, inspected, executed and blocked. Preserve the capability labels from BOOK_SPEC.md. Fix book defects within this scope, retain an audit trail and rerun only checks affected by changes. Update books/inside-orch/state/execution-tracker.csv with evidence paths; unresolved major findings require review_needed or blocked. A status of done requires this prompt's acceptance conditions, not merely delivery of a review file.
```


---

# 086. Create final metadata, cover and catalog material

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 085 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/RIGHTS.md; books/inside-orch/publication/book-metadata.json; books/inside-orch/manuscript/

## Output artifacts

books/inside-orch/publication/cover.svg; books/inside-orch/publication/cover.png; books/inside-orch/publication/catalog.json; books/inside-orch/publication/catalog-copy.md

## Work to perform

Create a publication cover from the existing orch vector identity and final title/subtitle. Use author Aleksandar Popovic consistently. Produce scalable SVG and a high-resolution export with verified aspect ratio and text legibility; inspect the result at cover and catalog-card sizes. Keep precise architecture diagrams outside decorative cover art. Derive all blurbs from completed chapters and validated capabilities.

Write a short catalog description, extended overview, learning outcomes, audience, prerequisites, reader paths and transparent edition/source metadata. Describe the book as a code-based engineering study of orch, including its current executable boundaries, not as a turnkey production HA platform. Populate real chapter/appendix counts, measured manuscript word count, actual lab status, source SHA and generated format paths. Never invent endorsements, bestseller status, ISBN, page count or review scores. Verify rights/attribution records and avoid relabeling source licensing. Include accessible alt text and short social metadata. The website can later use these assets through an adapter based on its real code.

## Acceptance and evidence

Cover visually checked; copy matches finished manuscript and real lab status; metadata measured; author/rights/source edition consistent; no unsupported marketing claims.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Final native metadata synchronization

Synchronize the final measured and reviewed edition metadata to canonical `books/inside-orch/book.json`, which scripts/book_catalog.py loads. Keep publication/book-metadata.json and catalog copy consistent with it. Replace planned/generation_pack status only when manuscript and required validations justify the final edition; do not leave a planned edition label in the release catalog or falsely mark incomplete work published. Preserve author, English language, source SHA, actual date, description and truthful rights.


---

# 087. Build a navigable print-quality PDF

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 086 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/manuscript/; books/inside-orch/examples/source-excerpts/; books/inside-orch/publication/cover.svg

## Output artifacts

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/publication/pdf-build/; books/inside-orch/validation/publication/pdf-build.json

## Work to perform

Assemble chapters and appendices from the canonical manifest order, excluding prompt workflow material and internal review notes. Choose available standard publishing tools and record versions and fonts. Build cover, title/rights pages, reader guidance, linked contents, bookmarks, numbered headings, code listings, figures and bibliography. Give chapter openers deliberate spacing and consistent headers/footers.

Ensure code, table and source-link layouts remain readable. Prefer short source-link labels with working PDF hyperlinks over printing 40-character URLs in every paragraph. Keep long listings in downloadable examples and avoid tiny fonts. Prevent headings orphaned at page bottoms, tables clipping the margin, overlapping text and broken glyphs. Export deterministic metadata and record the books/inside-orch/manuscript/source hashes used. Do not declare the PDF publication-ready before the next visual inspection task. Keep the build configuration with the manuscript so the edition can be regenerated rather than manually edited page by page.

## Acceptance and evidence

PDF contains complete canonical content, navigation and author metadata; build reproducible; no unresolved references; visual QA remains a separate required gate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Native publisher integration requirement

Implement `books/inside-orch/scripts/build.py` with metadata, safe nested selection, assemble, PDF, EPUB and explicit build entrypoints. Use available local dependencies and keep formats derived from one canonical 47-section manuscript. Reuse shared parsing primitives only after inspecting assumptions; never inherit Modern CI's hardcoded title, licenses or cover text. The native site build will call this publisher explicitly in prompt 092.


---

# 088. Render and inspect the actual final PDF

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 087 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/publication/pdf-build/; books/inside-orch/publication/DESIGN_SYSTEM.md

## Output artifacts

books/inside-orch/validation/publication/pdf-visual-review.md; books/inside-orch/validation/publication/pdf-pages.json

## Work to perform

Render the PDF to page images using available standard tools. Inspect cover, contents, every chapter/appendix opener, pages with tables/figures/code, and page endings; review every page at a legible resolution or systematically inspect all-page contact sheets followed by full-size suspect pages. Record page numbers checked and exact defects. Automated text extraction alone cannot establish visual correctness.

Check clipping, overlap, font substitutions, missing symbols, poor contrast, tiny listings, blank pages, inconsistent running headers, widows/orphans and broken table continuation. Test PDF links and bookmarks against the source/reference register. Compare selected extracted text with canonical Markdown to detect missing sections. Fix the typesetting source, rebuild and rerender affected pages and their neighbors; do not patch the PDF as the canonical manuscript. Record measured page count only after the final build. Keep internal screenshots as QA artifacts unless the user explicitly requests them as deliverables. Finish with a clear pass/fail list and actual evidence, not a generic assurance.

## Acceptance and evidence

All-page inspection coverage recorded; final rendered pages free of defects; links/bookmarks/contents correct; extracted content matches; measured page count and artifact hash captured.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 089. Build an accessible reflowable EPUB edition

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 088 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/manuscript/; books/inside-orch/publication/DESIGN_SYSTEM.md; books/inside-orch/publication/cover.png; books/inside-orch/editorial/REFERENCES.md

## Output artifacts

books/inside-orch/dist/inside-orch.epub; books/inside-orch/publication/epub-build/; books/inside-orch/validation/publication/epub-build.json

## Work to perform

Create a reflowable EPUB from the same ordered manuscript as the PDF. Include correct title/author/language/identifier/version metadata, cover designation, a linked navigation document, landmarks, chapter files and bibliography. Use semantic headings, meaningful link labels, figure text alternatives and table captions/headers. Keep reading order independent of decorative styling.

Code blocks must remain usable on narrow screens: consider horizontal scrolling, safe wrapping or downloadable complete listings, while preserving code meaning and indentation. Avoid fixed page numbers as the sole cross-reference; use chapter/section links. Convert exact diagrams to supported images plus accessible descriptions where a reader cannot render Mermaid. Package only required fonts/images with known rights; avoid large redundant assets. Test light/dark theme contrast and scalable type. Record tool versions, input hashes and output manifest. Do not declare validation complete because the ZIP container is readable; the next task verifies EPUB structure and reader behavior.

## Acceptance and evidence

EPUB content matches canonical manuscript; metadata/nav/reading order correct; code/tables/figures accessible; build inputs and rights recorded; validation pending explicit next gate.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Native EPUB contract

Record an explicit `epub_chapters` map for all 47 source stems when EPUB files use stem names. check-books otherwise guesses EPUB/text/chNNN.xhtml for new IDs. Package the exact catalog cover bytes at `EPUB/media/cover.png`, as required by the native cover check. Cross-section links and identifiers must be stable and source-derived.


---

# 090. Validate EPUB structure and real reading behavior

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 089 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/inside-orch.epub; books/inside-orch/publication/epub-build/; books/inside-orch/manuscript/; books/inside-orch/publication/book-metadata.json

## Output artifacts

books/inside-orch/validation/publication/epub-validation.md; books/inside-orch/validation/publication/epub-validation.json

## Work to perform

Run EPUBCheck if available and record the real version, invocation, exit code and report. If unavailable, record the missing tool and run structural checks without pretending they replace EPUBCheck. Inspect ZIP order and mimetype, OPF manifest/spine, navigation, missing images, duplicate IDs, unresolved internal links and metadata. Validate all asset paths without network assumptions.

Open the edition in available real readers or a documented preview and inspect cover, contents, chapter navigation, cross-references, source listings, tables, footnotes, diagrams and long URLs at small and large type. Compare word/section counts with the canonical Markdown; verify no chapter or appendix is missing. Check that accessibility alternatives communicate the diagram's actual code-based relationship. Fix the build source and regenerate before retesting. Report warnings separately from failures and declare any untested reader support rather than inventing compatibility. Preserve evidence for the exact final EPUB hash, not an earlier version.

## Acceptance and evidence

EPUBCheck outcome honest; structural/internal links pass; real preview reviewed where available; content complete; untested reader cases explicit; final artifact hash tied to validation.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

# 091. Implement the native Jekyll reader adapter

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Read scripts/book_catalog.py, scripts/build-books.py, scripts/check-books.py, _layouts/book.html, _layouts/book-overview.html and _plugins/site_features.rb. Read books/inside-orch/editorial/SITE_CONTRACT.md and books/inside-orch/manuscript/Book.txt. SITE is the repository root and BOOK is books/inside-orch. The complete reading order is 47 sections, beginning with a real preface. Do not create an unrelated static website or replace the existing reader.

Implement an orch-specific source adapter for metadata, safe nested selection, title/section classification, stable heading IDs, rendering, source-relative local reference rewriting, companion traversal and asset copying. Source paths may be nested under manuscript/chapters and manuscript/appendices; reject path escapes and duplicate stems. The Modern CI selection function requires direct child files, and its renderer has book-specific assumptions. Reuse only demonstrated compatible primitives. First H1s must match the inspected Chapter N - Title / Appendix A - Title grammar; index zero is Preface.

Preserve the native book, book-overview and book-license layouts. Code listings containing Liquid syntax must remain protected through build-books.write_page rather than being evaluated as templates. Reader URLs are /books/inside-orch/<source-stem>.html, public files /assets/books/inside-orch/, and downloads /assets/books/inside-orch/downloads/inside-orch.pdf and .epub. Exact source/commit links stay external immutable URLs. Resolve manuscript and companion links against their source parent and safely translate them to actual reader/companion/public-file addresses. Copy only referenced companion files; never publish the prompt corpus, entire research snapshot or private execution logs implicitly.

Add focused adapter tests for nested paths, renamed historical links, fragments, duplicate headings, companion documents, escaped paths and unsupported files. Keep an explicit epub_chapters map matching the generated EPUB rather than accepting the generic new-book chNNN guess. Record an interface/export manifest in books/inside-orch/publication/site-adapter/adapter-contract.json and actual test logs under books/inside-orch/validation/publication/. Tests can exercise the adapter directly before adding the catalog entry in prompt 092. Do not hand-author generated book-pages or _data/books.json.

Acceptance: all 47 source paths recognized in exact order, chapter/appendix counts correct, titles and slugs stable, local links round-trip to native addresses, referenced assets bounded to BOOK, and no raw workflow content exposed. Report actual executed tests and missing prerequisites. Update books/inside-orch/state/execution-tracker.csv for 091 with concrete evidence. Keep the implementation in books/inside-orch/scripts and a reviewable minimal native adapter patch; preserve existing books and do not publish live.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.


---

# 092. Wire the orch publisher and source catalog into the existing build

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

The target repository is already identified: alekpopovic/alekpopovic.github.io, inspected SHA 80801c8d3d97a4d8ff78e0fe69f3f902beda00c0. Reinspect current root AGENTS.md and actual sources; reconcile changes since that SHA without resetting the user branch. Use SITE_WORKSPACE.md and editorial/SITE_CONTRACT.md. This task integrates a native book, not a replacement site.

Add the new source record to scripts/book_catalog.py with id inside-orch; source ROOT/books/inside-orch; output ROOT/book-pages/inside-orch; files ROOT/assets/books/inside-orch; files_url /assets/books/inside-orch; metadata loaded from books/inside-orch/book.json; paths from safe books/inside-orch/manuscript/Book.txt selection; editions books/inside-orch/dist; filename inside-orch; chapter_group Chapters and chapter_label Chapter. Include truthful cover and licensing metadata and the explicit epub_chapters map. Configure cover bytes consistently between the catalog asset and EPUB/media/cover.png. The licensing page needs publication_notes or a real LICENSE.md; do not copy another book's public license claims.

Wire the actual orch publication build into scripts/build-books.py before its catalog copy loop. Registration alone cannot regenerate exports: current main explicitly calls only selected existing publishers. Import the new module safely without depending on current working directory or accidental mutable globals. Generate inside-orch.md, .pdf and .epub from the same complete 47-section canonical manuscript. Do not overwrite Modern CI, AgentPlane, LogBranik, Secret Contract Operator or Universal Tracking exports. Preserve and extend root renderer/companion-copy handling for orch based on prompt 091's adapter and concrete tests.

Confirm books/inside-orch is excluded in _config.yml so raw source/prompts are not copied by Jekyll. Preserve production origin, analytics and existing excludes. Keep book-pages/, assets/books/ and _data/books.json ignored. Canonical manuscript, scripts, metadata, final exports and meaningful validation records belong in books/inside-orch and Git. Generated public copies must not be force-added.

Prepare three chapter post drafts and the inside-orch glossary/update changes for the next task. Do not treat a half-completed registration as a release-ready site: all these source changes must be coherent before the full publication gate in 093. Run book-specific publisher/adapter checks and source exports with available toolchains. Verify 47 sections, 40 numbered chapters and 6 appendices, manifest paths, PDF/EPUB signatures, canonical/export consistency, license page inputs and existing-book preservation. Record actual commands, versions, outcomes and blockers under books/inside-orch/validation/publication/. Add focused tests for the new path; never weaken global completeness checks. Update the tracker and leave a concrete reviewable branch result. No main-branch push or deployment is authorized by this prompt.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.


---

# 093. Ship three original posts, glossary and updates with the native book

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Complete the source integration for inside-orch using the existing Jekyll/Tailwind reader. Read root AGENTS.md, _data/glossary.yml, _data/updates.yml, existing _posts front matter, scripts/check-books.py and scripts/check-site.py. Preserve shared includes and existing categories. All47 canonical sections and final PDF/EPUB exports must exist; a partial manuscript is not an edition.

Review the three prepared original posts under books/inside-orch/publication/site-adapter/prepared-posts/ against the now-completed chapters and actual source. Their topics are service resource propagation (Chapter05), default-server state/readiness (Chapter06), and partition/fencing limits (Chapter19). Revise to stand alone as substantive worked explanations; never copy chapter paragraphs or replace them with marketing summaries. Copy verified editorial sources into _posts/ with publication dates chosen at the actual release, stable filenames and required fields layout:post, title, description, category, book_id:inside-orch, real chapter_slug, allowed illustration and tags. Ordinary book builds must never regenerate these posts.

Add inside-orch to _data/glossary.yml with at least three useful definitions linked to real chapter slugs. The native check requires glossary keys to exactly match the catalog. Preserve all existing entries. Add a stable _data/updates.yml entry for the visible book change and accurate editorial dates. Extend a relevant learning path only when it has a real exercise and observable evidence; do not invent completed progress. Keep source IDs stable for bookmarks and backups.

From SITE run npm run build, then bundle exec jekyll build, then .venv/bin/python scripts/check-books.py (or configured CI Python). Run npm run check:site and npm run check:content. For shared/browser changes run npm run test:ui and npm run check:performance with the existing relevant compatibility checks. Missing dependencies are concrete blockers, not invented passes. Validate all 47 online sections, 40 chapter/6 appendix counts, native previous/next navigation, contents, code, companion links, three distinct numbered-chapter post links, reciprocal notes, glossary, search/feed/sitemap and full downloads. Compare PDF/EPUB/site text with canonical source and exact final hashes.

Confirm generated paths remain ignored and no raw workflow/evidence files leaked into _site. Produce books/inside-orch/publication/site-adapter/changes.patch, a source/generated file manifest and books/inside-orch/validation/publication/site-build.md with actual command logs. Inspect git status and stage only relevant canonical changes in the selected branch if committing. Do not push main or deploy. Acceptance is a complete, locally verified integration preserving existing books, not merely a new catalog card. Update the tracker with actual evidence and unresolved issues.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.


---

# 094. Verify native discovery, accessibility and publication behavior

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.


**Recommended reasoning:** high.

Review the complete built inside-orch edition in the existing site. Use actual _site output, native reader layouts, scripts/check-site.py, scripts/check-publication.py, package.json and root AGENTS.md. Canonical origin remains https://www.alekpopovic.com and book URLs /books/inside-orch/. Preserve current analytics configuration and exactly-one-tag behavior; never expose notes, selected text, search queries or contact values to tracking.

Verify landing/47section metadata, canonical URLs, author/title/source edition, accurate structured book data, social covers, search full text, feed, sitemap and post/chapter reciprocal links. Do not invent ISBN, reviews, page counts or ratings. Test PDF/EPUB download signatures and compare public copies to reviewed canonical books/inside-orch/dist files. Verify removed or nonexistent paths stay true404s; do not add catchall rewrites. The current post-deploy checker can be prepared locally without claiming a live check before deployment.

Review keyboard navigation, focus visibility, chapter selection, contents, copy-code controls, tables, heading hierarchy, image alternatives, source links, mobile layouts and no-JavaScript reading. Check reading progress, bookmarks, note export and versioned backups including storage failure. Existing IDs/URLs of other books must be unchanged. Retain local fonts/assets; ordinary builds should not fetch network assets. Use the native shared Google tag/layout conventions on any new rendered HTML.

Offline saving stays opt-in per section; do not precache whole orch chapters or PDF/EPUB files. Confirm local manifests contain correct asset versions and the worker preserves genuine network404s. If an offline downloadable ZIP is provided, it is an explicit download rather than a silent service-worker preload. Preserve CSS/conditional-JavaScript budgets from rootAGENTS and relevant browser/performance suites. Do not add analytics widgets or redesign shared navigation for this book.

Run npm run check:site and npm run check:content; run applicable Playwright tests and npm run check:performance after shared/browser changes. Record exact tested browsers, viewports, tool versions, timestamps and exit codes in books/inside-orch/validation/publication/site-quality.md and JSON. Automated audit scores complement manual reading checks. Fix defects in canonical source/build adapters, rebuild and retest affected outputs. Keep untested conditions explicit. Update books/inside-orch/state/execution-tracker.csv only when concrete acceptance is met. Leave a reviewable local integration; no publication action is implied.

## Baseline and progress record

Read `books/inside-orch/evidence/source-lock.json` before technical work. Record actual source SHA, prerequisites, commands, UTC timestamps, exit codes, checks and limitations. Update `books/inside-orch/state/execution-tracker.csv` with generated files and concrete validation paths; use blocked/review_needed for unmet acceptance. Inspected source is not an executed build or laboratory.


---

# 095. Create the offline edition and reproducible release inputs

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 094 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/dist/inside-orch.pdf; books/inside-orch/dist/inside-orch.epub; _site/books/inside-orch/; books/inside-orch/manuscript/; books/inside-orch/examples/; books/inside-orch/validation/; books/inside-orch/publication/

## Output artifacts

books/inside-orch/dist/inside-orch-offline.zip; books/inside-orch/dist/inside-orch-sources.zip; books/inside-orch/dist/SHA256SUMS.txt; books/inside-orch/publication/REPRODUCE.md

## Work to perform

Package the complete reader edition separately from editable publication sources. Include PDF, EPUB, offline HTML, code examples, lab instructions, answers, source/commit index, rights notices and source edition metadata. Editable sources include canonical Markdown, style/build configuration, asset sources and validation records, with credentials, ephemeral logs containing secrets and unrelated site files excluded.

Ensure offline HTML navigates without a server where supported; if an embedded local server is required for search or module loading, document the exact dependency and provide a simple working launch command. Include exact source SHAs and explain how to retrieve the application repo without confusing it with teaching extensions. Generate checksums only after final files exist and verify them independently. Use deterministic archive order/timestamps where feasible and record remaining nondeterminism such as PDF metadata. A reproducibility note must describe actual tool versions and commands, not an aspirational one-line build. Keep these archives reviewable before publishing.

## Acceptance and evidence

Reader/source packages complete and distinct; no credentials; hashes independently verify; offline behavior tested or clearly scoped; exact reproduction instructions available.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.

## Explicit offline reader producer

Prompt091 now produces the native adapter, not a standalone online/ directory. First build and validate the complete native site through prompts 092-094. Then explicitly create `books/inside-orch/dist/online/` for this offline edition from the finished native _site/books/inside-orch/ output or the book publisher's offline-export entrypoint. Copy only necessary reader styles, local fonts, images and code companions with an asset manifest; rewrite local navigation/assets safely for the packaged base and retain external source/commit links as online references. Preserve all 47 sections and title/source edition metadata. Validate the exported reader with a disposable loopback server, e.g. `python3 -m http.server 8765 --bind 127.0.0.1` from its own export directory, and scope/terminate only that owned process. Label any file-URL limitations. The explicit downloadable offline ZIP must not change the live service worker's opt-in per-section caching or precache complete books/downloads. Do not package a nonexistent online/ path or imply native adapter code itself is an offline edition.


---

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


---

# 097. Challenge the book as three skeptical readers

## Mandatory execution context

Execute this prompt from the root of **https://github.com/alekpopovic/alekpopovic.github.io**. Read root `AGENTS.md`, `books/inside-orch/AGENTS.md`, `books/inside-orch/BOOK_SPEC.md`, `books/inside-orch/SITE_WORKSPACE.md`, and `books/inside-orch/evidence/site-lock.json` first. The inspected site is Jekyll + Tailwind; preserve its shared layouts, existing books and source/build conventions.

`SITE` means the repository root. `BOOK` means `books/inside-orch`. All book-relative artifacts are inside BOOK; all site-source changes use the explicit root paths in SITE_WORKSPACE.md. Original orch paths named as source reads are relative to `books/inside-orch/evidence/orch/`, never to SITE. For Go/Docker/PostgreSQL experiments use a disposable application-source copy and record its working directory; do not run application commands against the website's code.

Canonical manuscripts, metadata, scripts and validation stay under BOOK. Do not edit generated `book-pages/inside-orch/`, `assets/books/inside-orch/`, or `_data/books.json` manually or force-add them to Git. No root AGENTS.md, README.md or existing scripts may be replaced by this pack. Live publication remains outside this prompt unless the current task authorizes it.

**Recommended reasoning:** high; use a deeper setting if available for cross-cutting review.

**Prerequisite:** Complete or explicitly resolve the gate from prompt 096 before dependent work.

## Workspace contract

Read `AGENTS.md`, `BOOK_SPEC.md`, `books/inside-orch/evidence/source-lock.json`, and the latest tracker before starting. Use the pinned application snapshot in `books/inside-orch/evidence/orch/` read-only. The application's 00–90 development prompts and this pack's 000–099 book-production prompts are separate sequences. Do not implement application changes to make the narrative true. Teaching additions live in `books/inside-orch/examples/teaching-extensions/` and need their own tests and attribution.

Use full-SHA source/commit links and actual code/test evidence. Mark observations as expected until executed. Record missing prerequisites as blocked; never fabricate passing tests, command output, timings, screenshots, citations or release status. After completion, update `books/inside-orch/state/execution-tracker.csv` with status, UTC time, generated paths, evidence and an optional local commit. Keep changes scoped to this prompt and preserve user work.

## Required inputs

books/inside-orch/manuscript/; books/inside-orch/validation/RELEASE_GATE.md; books/inside-orch/editorial/CAPABILITIES.md; books/inside-orch/evidence/orch/

## Output artifacts

books/inside-orch/validation/reviews/final-independent-review.md; books/inside-orch/validation/reviews/final-findings.json

## Work to perform

Perform independent developer, DevOps and architect reviews of the complete edition. If parallel reviewers are available, give each a distinct lens and exact source lock. Developer: can listings/examples be followed and compiled, are interfaces/state transitions correct? DevOps: do procedures state privileges, prerequisites, observations, recovery limits and cleanup? Architect: are persistence, concurrency, fencing, isolation, resource accounting and tradeoffs accurately scoped?

Give reviewers adversarial scenarios, not a request to praise the manuscript: two servers with memory state, conflicting claims, a node partition, a worker with unapplied limits, restart during rollout, a failed second GitOps manifest, advisory lock cancellation and a database suite silently skipped. Require findings with chapter/claim IDs and direct code or actual log evidence. Reconcile duplicate findings and fix material ones in canonical sources. Retest affected books/inside-orch/examples/labs/formats and update hashes. Record residual limitations without framing the book as a certification. The final recommendation must be based on readable teaching quality and inspectable evidence, not word count.

## Acceptance and evidence

Three lenses review actual final content; concrete findings source-backed; major issues resolved with revalidation; remaining limitations explicit; no invented external endorsement.

Report the concrete outcome, the checks actually run, skipped/blocked checks with reasons, and the next prompt. A generated document is not proof that its described experiment was executed.


---

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


---

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

