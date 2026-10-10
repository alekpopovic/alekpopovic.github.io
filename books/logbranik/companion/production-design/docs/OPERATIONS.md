# Operations and deployment

Baseline: central Linux host plus one edge Linux host on a private network/VPN. The only
public edge listeners are existing HTTP/HTTPS services. Agent control port (example 9444)
accepts only central dispatcher peers over mTLS. The Unix auth socket is local. Central
private TLS endpoint accepts collectors, agents and operators according to their own roles.
No SSH remote commands are used for routine ban/unban updates.

## Installation sequence

Inventory Nginx topology and includes; provision certificates and pinned signing keys; deploy
central database/API/workers; register edge/site; install agent in monitor mode; obtain a
valid signed empty snapshot; verify local check readiness; configure Vector; validate and
canary Nginx includes; run nginx -t; reload once; verify true IP and scope; replay controlled
traffic; verify central desired state and agent acknowledgement; enable one tuned rule.
Snapshot updates and block/unblock commands never require a Nginx reload.

## Data retention

Default planning values: raw valid events 7 days, invalid redacted samples 24h, compact
aggregates 30 days, decision/audit history 90 days. Make values configurable and bound
quarantine per node. Reconcile retention with deduplication: retaining dedup keys for 14 days
prevents in-window replay double-counting; beyond that period historical events are too old
for detection anyway. Delete raw evidence only after retaining a small non-sensitive decision
summary. Partition raw events by received day when volume justifies it; global request-ID
deduplication must not be accidentally weakened by per-partition uniqueness.

Raw event storage estimate: events/s * 86,400 * days * measured stored bytes/event, plus
indexes, WAL, backups and headroom. At 100 events/s and 1,000 raw bytes/event this is
8.64 GB/day before overhead; 1,000 events/s is 86.4 GB/day. Do not size from compressed
network bytes alone. Measure the actual PostgreSQL footprint. Collector buffer sizing is
average encoded bytes/s * supported outage seconds with safety margin.

Vector disk buffer and file retention are finite. Alert before either fills. Prefer rotation by
rename plus Nginx log reopen, not copytruncate. Test checkpoint recovery and rotation during
outage. Backpressure may stop reading; old rotated files must remain long enough. Monitor
permanent HTTP errors because retry behavior differs by status. Do not promise zero loss
under disk failure or exhausted retention.

## Required runbooks

- Central outage: inspect pending deliveries/ingest queue, preserve edge state, restore service,
  drain backlog with stale-event detection disabled for old events, reconcile revisions.
- Agent failure: inspect socket/service/state, use the explicitly chosen fail mode, restore the
  agent, then reconcile. Local emergency bypass is authenticated via host permissions.
- False positive: revoke decision, add narrow temporary allowlist if needed, verify applied
  revision on affected nodes, preserve evidence and tune rule before reenabling it.
- Certificate/signing-key rotation: provision trust overlap, verify new use, then remove old
  trust after reconciliation. Saved states signed by old keys need a controlled replacement.
- Backup/restore: restore database in isolation, validate desired-state and revision continuity,
  resolve high-water conflicts, then reconnect agents; perform a real restoration drill.
- Rollback: preserve schema compatibility and state, disable enforcement per site, revert
  binary/config with nginx -t, and verify traffic. Never erase state simply to fix ordering.

Availability SLO and fail-open/fail-closed choices are site-specific and must be recorded.
Never interpret central HTTP success as confirmation that every edge has applied a block.
