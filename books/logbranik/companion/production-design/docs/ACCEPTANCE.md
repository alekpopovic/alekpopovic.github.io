# Release acceptance and test matrix

No production-ready claim without evidence from the actual application. The pack itself has
only structural/tooling checks. The runtime tests below are implementation deliverables.

| Area | Required evidence |
|---|---|
| Normal request | Real static/proxied content passes and upstream sees original method/body |
| Block | A signed site/IP ban yields 403 on subsequent protected requests |
| Unblock/TTL | Revoke and expiry restore access without Nginx reload |
| Nginx lifecycle | Worker PIDs/start times stable during block/update/unblock cycle |
| Scope | Same IP on another site remains unaffected; spoofed Host cannot select scope |
| IPv6 | Native IPv6 and mapped address normalization match across Python and Go |
| Central outage | Saved decisions enforce only until original expiry; local check stays available |
| Agent outage | Fail-closed and explicit fail-open profiles behave exactly as documented |
| Identity | Forged visitor headers and wrong certificate role cannot bypass/mutate |
| Replay | Duplicates, wrong epoch/target, lower revisions and expired new messages rejected |
| Durability | Crash after DB commit/before response and agent persist/publish crashes recover |
| Log transport | Rotation, collector restart, backlog, 429/503 and permanent failures exercised |
| Detection | Duplicate/late events and Guard-denied events cannot inflate or renew bans |
| Routing | Static, regex, proxy, named/internal redirects, existing auth and exceptions tested |
| Restore | Database restore cannot silently roll back local enforcement revision |

Provisional lab targets: after enough fresh eligible completed requests cross a threshold,
p95 threshold-to-applied time <= 5 seconds at 100 events/s sustained. Report log flush,
collector batch, API commit, detector, delivery and agent publication components separately.
Pull-only recovery target <= 30 seconds under a healthy network. Local auth added p95
latency target <= 2ms at 1,000 protected requests/s on explicitly documented hardware.
These targets may require tuning; failures remain visible and no benchmark number is
invented. Re-run tests at the user's real traffic profile before fleet rollout.

Use only local/container/lab target hosts you control for generated traffic. Fixtures use
documentation IP ranges. A lab-only trusted proxy simulates client IPs; do not make arbitrary
internet X-Forwarded-For trusted in production to make a test pass.

CI checks include Python lint/type/unit/Postgres integration, Go vet/unit/race, contract vectors,
Nginx/Vector validation, end-to-end flows, dependency checks and reproducible packaging.
Per-prompt checks may use stubs before the real counterpart exists; replace them with real
cross-component tests at the explicitly scheduled integration gates.
