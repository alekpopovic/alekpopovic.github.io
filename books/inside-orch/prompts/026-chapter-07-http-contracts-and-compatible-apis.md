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
