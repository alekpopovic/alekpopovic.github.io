# Detection and false-positive control

Implement deterministic, versioned rules; no AI dependency or paid reputation feed is required.
Aggregation key: site_id + normalized IP + rule ID + bounded time bucket. Event time drives
windows; received time measures delay. Reject implausible future timestamps from detection.
Default automatic eligibility: event age <= 120 seconds and future skew <= 30 seconds.
Late events stay searchable and cannot cause a fresh ban. Test boundary timestamps with
an injected clock. Use bounded fixed buckets as the MVP and document boundary limitations.

These defaults are starting points in monitor mode, not universal production thresholds:

| Rule | Candidate signal | Default action |
|---|---|---|
| Sensitive-path scan | >= 10 requests over 60s across >= 3 configured sensitive path families | 15m site ban after tuning |
| Login abuse | >= 30 401/403 responses over 60s on explicitly configured login endpoints | Monitor until application semantics verified |
| Error burst | >= 100 404 responses over 60s across >= 20 distinct paths | Monitor only |
| Request volume | >= 300 completed requests over 10s | Monitor only |

404, 403, high request rate or a user-agent alone is not reliable evidence of malicious use.
Login endpoints returning 200 on failed authentication require an application-level signal
or stay monitor-only. Shared NAT, crawlers, broken links and legitimate API bursts appear
in benign replay fixtures. Path matching excludes query strings and does not claim SQLi/body
inspection. Use bounded normalization; avoid catastrophic regex or repeated decoding.

Decisions include rule version, observed window, counters and bounded event references.
For a rule/site/IP/window, deduplicate the detection and avoid unbounded duplicate decisions.
Repeated delivery of the same event cannot increment a counter. Retries, backfills and logs
with enforcement=block cannot generate or perpetually extend their own ban. While a ban is
active, denied traffic is observability only; renewed TTL requires new independent eligible
evidence and a documented maximum cumulative duration/cooldown. Start with no automatic
renewal in the MVP. A revocation creates a configurable suppression period (default 15m)
to prevent instant recreation from the same evidence. All decision writes consult allowlists.

Limit active bans per site, new bans per minute, distinct paths retained per bucket, and
memory/database work per event. A circuit breaker suspends automatic enforcement on a
surge in ban creation or suspiciously broad impact, records the reason and alerts; existing
bans keep their original expiries. Global bans require manual action. CIDR allowlists are
manual and audited. Never automatically exempt a crawler based only on its claimed name.

Rollout: shadow/monitor -> replay review -> one enforce canary -> gradual fleet enablement.
Use precision on a labeled fixture set and operator-reported false positives as evidence;
do not publish a fabricated accuracy percentage.
