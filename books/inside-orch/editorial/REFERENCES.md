# References and citation rules

## Repository evidence

The immutable application edition is **cbfc94ade5b57e449d6b73bf1485b1c5b1647022**. Exact listings cite full-SHA blob URLs plus original line intervals. The complete byte-derived list is [listing registry](../examples/source-excerpts/registry.json); [independent checksum review](../validation/intake/excerpt-check.json) verifies source slices. A stable listing ID is used across Markdown, HTML, PDF and EPUB.

A historical statement cites the full implementation commit and the actual changed file/diff at that commit, not baseline line numbers pasted into an older URL. Every SHA must occur in `evidence/commits.json`. Original development prompts are cited as requests at their baseline `prompts/NN-...md` path with their own full-SHA blob link, together with the topical association in `evidence/prompt-commit-map.json`. Retrospective prompts00–28 and batched late implementations must be identified; neither a subject nor the tracker proves literal prompt execution.

Design documents establish proposals. An inspected test establishes an assertion in source. An executed assertion additionally needs command, working directory, UTC timestamps, prerequisites, exit code and a stable local log. A teaching adaptation cites its source inspiration and names changed behavior and independent tests; it never inherits the exact listing checksum. An inference cites supporting code and explicitly says which conclusion is reconstructed rather than observed.

## Compact primary bibliography

The following sources were actually retrieved on2026-10-13. They explain concepts used in the manuscript and lab contract; they do not certify Orch integration. Versions are explicit where the provider offers them. Moving vendor documentation is labeled unversioned rather than disguised as an immutable implementation source. Dependency versions remain those in the locked `go.mod`, including Docker SDKv28.5.2 and pgxv5.10.0; an API documentation version is never silently treated as the negotiated daemon version.

- [The Go Memory Model](https://go.dev/ref/mem). 2022-06-06 specification revision. Use: Synchronization and the distinction between memory-race freedom and distributed durable concurrency. Retrieved2026-10-13.
- [Go context package](https://pkg.go.dev/context@go1.25.0). Go1.25.0. Use: Cancellation ownership and stream/loop cleanup vocabulary. Retrieved2026-10-13.
- [Docker Engine security](https://docs.docker.com/engine/security/). Unversioned official documentation, retrieved snapshot2026-10-13. Use: Docker daemon/socket trust boundary in the lab environment. Retrieved2026-10-13.
- [PostgreSQL16 Explicit Locking](https://www.postgresql.org/docs/16/explicit-locking.html). PostgreSQL16. Use: Distinguish transactional concurrency from session-owned advisory lock lifecycle. Retrieved2026-10-13.
- [RFC9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). RFC9110 June2022. Use: Separate HTTP request semantics and application-level replay/idempotency. Retrieved2026-10-13.
- [Prometheus instrumentation practices](https://prometheus.io/docs/practices/instrumentation/). Unversioned official guidance, retrieved2026-10-13. Use: Bounded metric label selection and distinguishing instrumentation from observed results. Retrieved2026-10-13.

Docker Engine APIv1.47 landing page was also opened, but the browser returned only its shell; no precise endpoint claim relies on that incomplete retrieval. For adapter fields use the locked SDK source/interface and recorded negotiated Engine behavior, or retrieve the relevant official endpoint before adding a precise external claim. No DOI, ISBN, issue link or absent release is invented.

## Offline evidence route

1. Open `evidence/source-lock.json` to identify the pinned source and file checksums.
2. Read the corresponding file under `evidence/orch/`; line numbers match the source blob.
3. Follow the stable listing ID into `examples/source-excerpts/`, comparing its raw file and SHA256.
4. For development history, open `evidence/original-prompts.json`, `evidence/prompt-commit-map.json`, and `evidence/commits.json`; read the full-SHA patch under `evidence/commit-diffs/`.
5. Inspect `validation/` for real execution records. Offline snapshots do not reproduce live external documentation or a historical test run.

The machine-readable [reference register](../validation/intake/reference-register.json) deduplicates repository anchors and primary sources. Keep new citations close to the claim. Rights and attribution review is separate: public repository visibility grants no assumed relicensing permission.
