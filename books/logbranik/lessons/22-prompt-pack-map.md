# Appendix B. From lessons to sixty implementation tasks

The included Claude Code pack preserves all sixty original implementation tasks. The table below maps each task to its primary explanatory lesson. A lesson explains the design; it does not mark the production task complete. The original tracker remains pending and requires actual acceptance evidence.

Extract `companion/nginx-guard-claude-code-pack.zip`, read its `README_SR.md` and bootstrap instructions, and install it into your application repository according to the pack. Keep that repository separate from the book manuscript.

| ID | Implementation task | Lesson |
| --- | --- | --- |
| 000 | Repository inventory and project bootstrap | 20 |
| 001 | Version selection and reproducible dependencies | 20 |
| 002 | Typed contracts and golden fixtures | 11 |
| 003 | Local networks and development certificates | 4 |
| 004 | Database schema and initial migrations | 16 |
| 005 | Build commands and test foundation | 18 |
| 006 | Authenticated central service and role boundaries | 2 |
| 007 | Bounded NDJSON ingestion | 7 |
| 008 | Deduplication and durable processing queue | 7 |
| 009 | Structured Nginx access logging | 5 |
| 010 | Vector transport and disk buffering | 6 |
| 011 | First complete log ingestion demonstration | 4 |
| 012 | Go agent process and local listener | 17 |
| 013 | Immutable policy state and atomic persistence | 12 |
| 014 | Local authorization decision engine | 13 |
| 015 | Nginx auth_request integration | 8 |
| 016 | Availability profiles and local emergency bypass | 3 |
| 017 | Local expiry and offline enforcement milestone | 13 |
| 018 | Ed25519 signatures and cross-language vectors | 11 |
| 019 | Private mTLS snapshot receiver | 11 |
| 020 | Desired decisions and transactional snapshot outbox | 12 |
| 021 | Reliable push delivery and applied acknowledgements | 12 |
| 022 | Pull reconciliation and node heartbeat | 12 |
| 023 | Manual block lifecycle end-to-end milestone | 14 |
| 024 | Event-time aggregation and concurrency correctness | 16 |
| 025 | Sensitive-path scanning rules | 10 |
| 026 | Login-abuse rule with explicit endpoint semantics | 10 |
| 027 | Request-volume and error anomaly monitoring | 10 |
| 028 | Risk policy and safe automatic decision creation | 10 |
| 029 | Automatic detection-to-block demonstration | 4 |
| 030 | Operator roles and complete audit trail | 14 |
| 031 | Operator CLI for investigation | 14 |
| 032 | Operator CLI for bounded policy changes | 14 |
| 033 | Allowlist precedence and revocation race handling | 14 |
| 034 | Evidence search and decision explanations | 14 |
| 035 | False-positive recovery and emergency drills | 19 |
| 036 | Fleet membership and multiple sites per node | 2 |
| 037 | Snapshot coalescing and bounded delivery scaling | 15 |
| 038 | Raw-event retention and database maintenance | 15 |
| 039 | Metrics and structured cross-service diagnostics | 15 |
| 040 | Alert rules and operational health views | 15 |
| 041 | Measured throughput and latency baseline | 15 |
| 042 | Central outages, backpressure and collector recovery | 6 |
| 043 | Clock, TTL and restart fault matrix | 13 |
| 044 | TLS and signing-key lifecycle | 11 |
| 045 | Hostile inputs and cross-scope security tests | 18 |
| 046 | Nginx routing and existing-auth regression suite | 8 |
| 047 | Complete reliability regression gate | 18 |
| 048 | Production images and agent release binaries | 20 |
| 049 | Hardened systemd units and filesystem ownership | 17 |
| 050 | Idempotent installation and canary configuration | 20 |
| 051 | Database backup and tested restore | 12 |
| 052 | Upgrade, rollback and compatibility procedures | 20 |
| 053 | Deployment observability and recovery handbook | 19 |
| 054 | Continuous integration and release policy | 20 |
| 055 | Replay evaluation and production threshold calibration | 10 |
| 056 | Monitor-only installation readiness | 10 |
| 057 | Single-site enforcement canary | 20 |
| 058 | Staged fleet enablement and rollback drill | 20 |
| 059 | Final audit and release handoff | 20 |

## Milestone order

Start with repository and protocol foundations. Verify collection before detection. Verify local authorization before remote control. Verify signed control and expiry before automatic enforcement. Add operator recovery, then run reliability and deployment gates before enabling a canary. Fleet rollout comes after a single-site measured demonstration.

The compact Python lab covers behavior across several milestones using a smaller stack. It does not import its test result into the original production tracker. PostgreSQL worker correctness, Go race safety, continuous collector guarantees, real Nginx routing and staged deployment require their own evidence.

## Resume safely

Use the pack tracker and handoff document to resume work. Preserve unfinished prerequisites. Do not mark a task done because an assistant summarized it as successful. Record the executed command, observed result, and relevant artifact. When a prerequisite changes, reopen dependent work according to the tracker rules.
