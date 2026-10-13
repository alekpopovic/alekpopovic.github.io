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
