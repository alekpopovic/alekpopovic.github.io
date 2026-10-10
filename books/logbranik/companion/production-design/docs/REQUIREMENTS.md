# Requirement traceability

This is the planned implementation map. Completion evidence is produced in the application
repository during execution; all prompts are initially pending.

| Requirement | Main prompts | Release proof |
|---|---|---|
| Ordinary Nginx OSS | 001, 009, 015 | Module inspection and real Nginx tests |
| Continuous remote log delivery | 007–011 | Correlated request IDs in PostgreSQL |
| Disk buffer and reconnect | 010, 042 | Outage/rotation/restart test |
| Central risk analysis | 024–029 | Labeled replay and detector evidence |
| IP block without reload | 014, 015, 023, 029 | 403 plus stable worker identities |
| Local-only request checks | 012–017 | Offline-central check tests |
| Signed private control requests | 018–022 | mTLS and cross-language crypto tests |
| TTL and automatic unblocking | 014, 017, 043 | Frozen-clock/restart boundary tests |
| Revoke without stale resurrection | 020–023, 033 | Out-of-order push/pull tests |
| Explicit agent failure behavior | 016, 046 | Fail-open/closed routing matrix |
| Real IP behind trusted proxies | 009, 015, 045, 046 | Forged-header and multi-hop tests |
| IPv4/IPv6 parity | 002, 014, 023 | Shared address fixtures |
| Site isolation | 006, 007, 014, 036 | Same IP, different site results |
| No detector feedback loop | 026, 028, 029 | Blocked events cannot extend bans |
| Duplicate-safe ingestion | 008, 024 | Retry/concurrent worker tests |
| Allowlist and emergency bypass | 016, 033, 035 | Precedence and recovery drill |
| Audited operator controls | 030–035 | Role matrix and audit evidence |
| Multiple edge servers | 036, 037 | Full fleet convergence test |
| Measured performance | 041 | Hardware-qualified benchmark |
| Bounded retention and resources | 007, 013, 038, 039 | Capacity/retention tests |
| Backup and upgrade recovery | 051, 052 | Restore and rollback drill |
| Reproducible deployment | 048–050, 054 | Clean install and CI |
| Monitor-first rollout | 055–058 | Calibration and canary evidence |
| Honest release status | 047, 059 | Requirement-to-evidence matrix |
