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
