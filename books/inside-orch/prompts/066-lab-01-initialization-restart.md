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
