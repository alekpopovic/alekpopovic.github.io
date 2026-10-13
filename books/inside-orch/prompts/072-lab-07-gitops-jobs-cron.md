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
