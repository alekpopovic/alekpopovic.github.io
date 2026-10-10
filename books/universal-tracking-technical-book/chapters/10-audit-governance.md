## Chapter 10 - Audit, Classification, and Data Governance

A location platform must explain not only where data came from, but also who viewed it, who changed access, why data was retained, and which transformations produced a result. Audit is a first-class subsystem, not a log file.

### Audit events and application logs are different

Application logs help operators diagnose software. Audit records provide a durable history of security and business actions. Logs may be sampled or rotated; audit records follow a retention and access policy.

A useful audit schema includes:

```text
audit_events
  id
  organization_id
  occurred_at
  actor_type
  actor_id
  action
  resource_type
  resource_id
  outcome
  reason_code
  request_id
  source_ip_prefix
  user_agent_summary
  metadata JSONB
  previous_hash
  event_hash
```

Do not copy entire request bodies or location payloads into audit metadata. Record identifiers, field names, scopes, and policy decisions.

### What to audit

At minimum, record:

- authentication success, failure, MFA changes, and session revocation;
- organization membership and role changes;
- subject, device, assignment, and session lifecycle changes;
- credential issuance, rotation, compromise, and revocation;
- precise history views and exports;
- public-link creation, use, revocation, and scope changes;
- privacy-policy and retention changes;
- emergency access;
- legal holds and deletion workflows;
- webhook and API-client credential changes;
- administrative corrections to tracking provenance.

High-volume location ingestion is not copied into the audit table one point at a time. It already has durable provenance. Audit batch acceptance summaries and exceptional actions.

### Tamper evidence

A database administrator can ultimately change database content, so "tamper-proof" is an overstatement. Tamper evidence is achievable. One approach chains event hashes within a scope:

```text
event_hash = H(previous_hash || canonical_event_bytes)
```

Periodically export signed checkpoints to an off-site store or a separate security system. Verify the chain in a scheduled job and during audits. The mechanism must define canonical serialization and recovery from operational corrections.

### Data classification

Classify fields and datasets, not only tables. Example classes:

| Class | Examples | Controls |
|---|---|---|
| Public | product documentation | normal integrity controls |
| Internal | aggregate capacity metrics | staff access |
| Confidential | organization configuration, task details | tenant authorization and encryption |
| Sensitive location | exact current and historical coordinates | strict purpose, audit, precision controls |
| Secret | tokens, password hashes, private keys | no normal logs, restricted processes |

Classification drives export behavior, metric labels, support access, backup handling, and retention.

### Purpose and lawful basis records

For people, store the reason tracking is permitted. The exact legal terminology varies, but the engineering model can record:

```text
purpose
basis_type
policy_version
accepted_at
valid_from
valid_until
source
revoked_at
related_shift_or_event
```

The ingestion authorization path should be able to prove which active record or operational policy allowed tracking at `recorded_at`.

### Access history

A tracked person may need to see who accessed precise history. A separate access ledger can summarize:

- viewer identity and organization role;
- subject and time range;
- purpose or support ticket;
- export or screen view;
- precision returned;
- emergency-access indicator.

Avoid recording every map tile or marker refresh. Audit meaningful access sessions and sensitive operations at a useful granularity.

### Retention policy hierarchy

Retention may be defined at platform, plan, organization, subject type, and use-case levels. Resolve policies deterministically and store the effective policy ID with data when necessary.

Example:

```text
raw high-frequency points: 90 days
simplified routes:          1 year
trip summaries:             3 years
security audit:             2 years
public-link access logs:    180 days
quarantined raw packets:    7 days
```

These are examples, not universal defaults. A sports user may want long personal history; an employer may need much shorter retention for workers.

### Support access

Support engineers should not receive broad production access by default. Build controlled support tooling with:

- explicit customer approval where appropriate;
- time-limited scoped grants;
- reason and ticket reference;
- masking and reduced precision;
- complete audit;
- no secret or raw credential access;
- post-access review for sensitive cases.

### Chapter checklist

Data governance is credible when:

- audit and application logging are separate;
- sensitive access and policy changes are recorded;
- audit integrity has a verification procedure;
- fields and datasets are classified;
- person tracking carries a recorded purpose or basis;
- access history is meaningful and not noisy;
- retention resolves through documented rules;
- support access is scoped, visible, and temporary.
