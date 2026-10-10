## Appendix E - Operational Runbooks and Checklists

### Ingestion degradation

**Symptoms**

- increased `5xx` or retryable responses;
- rising database acquisition latency;
- old mobile queues reported by clients;
- commit latency above target.

**Immediate actions**

1. Confirm user impact and affected roles.
2. Check database CPU, I/O, WAL, locks, and pool saturation.
3. Check recent migrations or deployments.
4. Reduce non-critical worker concurrency.
5. Protect ingestion by pausing reports and exports.
6. Scale API replicas only if the database has headroom.
7. Communicate retry guidance and monitor recovery burst.

**Integrity checks**

- accepted batch count versus stored point count;
- duplicate rate;
- outbox lag;
- latest-state freshness;
- mobile acknowledgement behavior.

### WebSocket reconnect storm

1. Verify whether a deployment or proxy timeout triggered disconnects.
2. Confirm clients use jittered backoff.
3. Observe authentication and snapshot load.
4. Reduce optional realtime detail and increase coalescing.
5. Keep critical alert messages prioritized.
6. Drain or roll replicas gradually.
7. Run a post-incident reconnect benchmark.

### Disk pressure

1. Identify filesystem and growth source.
2. Protect PostgreSQL from reaching zero free space.
3. Pause non-essential exports and large reports.
4. Verify WAL archive health and replication slots.
5. Add capacity or safely remove verified expired temporary data.
6. Do not manually delete PostgreSQL data files.
7. Review retention and capacity alerts.

### Failed backup

1. Treat stale backup coverage as an incident.
2. Preserve the last known good backup and keys.
3. Diagnose storage, credentials, capacity, and WAL archive state.
4. Retry through the documented tool, not an improvised copy.
5. Run integrity verification.
6. Schedule an immediate restore drill when coverage is restored.

### Suspected credential compromise

1. Identify credential class and scope.
2. Revoke or rotate it.
3. Invalidate related sessions or token families.
4. Search security and audit events.
5. Check for false points, exports, public links, or commands.
6. Preserve evidence with access controls.
7. Notify affected parties according to policy.
8. Correct derived data through versioned workflows.

### Release readiness checklist

- [ ] All migrations tested from the supported previous release.
- [ ] Fresh database bootstrap passes.
- [ ] Cross-tenant suite passes with runtime role.
- [ ] Ingestion duplicate and partial-response tests pass.
- [ ] WebSocket reconnect and slow-client tests pass.
- [ ] Mobile field tests cover supported OS versions.
- [ ] Protocol fuzz corpus passes.
- [ ] Backup and PITR drill is within target.
- [ ] Image digests, SBOM, and signatures are recorded.
- [ ] Alerts and runbooks are enabled.
- [ ] Rollback has been rehearsed.
- [ ] Known limitations are approved and communicated.

### Daily operator checklist

- [ ] Ingest success and latency within objectives.
- [ ] Active-session freshness within objective.
- [ ] Critical job backlog age acceptable.
- [ ] Database disk and WAL archive healthy.
- [ ] Future partitions exist.
- [ ] Backup completed and verified.
- [ ] No unexpected dead-letter growth.
- [ ] No abnormal invalid GPS frame spike.

### Monthly resilience checklist

- [ ] Restore a backup into an isolated environment.
- [ ] Verify RLS and application smoke tests on the restore.
- [ ] Exercise one failure runbook.
- [ ] Review capacity forecast and retention.
- [ ] Rotate one non-emergency credential in a controlled drill.
- [ ] Review support and emergency access.
- [ ] Review public links and stale API clients.
- [ ] Re-run representative mobile battery tests after major OS updates.
