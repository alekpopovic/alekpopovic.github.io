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
