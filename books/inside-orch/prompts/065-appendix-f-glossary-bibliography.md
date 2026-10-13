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
