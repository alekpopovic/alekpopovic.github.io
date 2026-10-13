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
