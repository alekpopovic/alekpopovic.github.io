## Chapter 29 - Privacy, Consent, Retention, and Legal Holds

Privacy controls must change system behavior, not merely produce a policy page. A person-tracking platform needs visible sessions, recorded purpose, access limits, private zones, data minimization, retention, export, correction, and deletion workflows.

### Visible tracking

For a person subject, the system records why tracking is active and exposes that status to the person through the mobile application or another appropriate channel. A tracking session can reference:

- work shift or assigned task;
- event participation;
- explicit consent record;
- guardian relationship;
- safety check-in;
- managed asset policy where the tracked object is not a person;
- emergency policy with additional audit.

Tracking outside the permitted interval is rejected, quarantined, or handled by a documented exception. It is never silently accepted because a device continued sending.

### Consent and withdrawal

Where consent is the chosen basis, it must be specific enough to connect to purpose and data use. Store policy version, scope, time, and withdrawal. Withdrawal affects future collection and sharing; deletion of existing data follows retention and legal rules.

The product should not force consent for unnecessary tracking as a condition of an unrelated service. Engineering cannot solve the legal validity of consent, but it can preserve evidence and enforce scope.

### Private zones

Private zones protect locations such as homes, schools, shelters, or medical facilities. They can apply policies such as:

- suppress exact points from normal views;
- replace points with a zone label;
- reduce precision;
- delay visibility;
- trim the beginning and end of shared routes;
- prevent public-link updates;
- restrict support access.

The raw point may still be stored for a narrowly defined operational purpose. If so, authorization and retention must reflect the higher sensitivity.

### Precision policy

Precision can be expressed as a server-side policy:

```text
exact
rounded_25m
rounded_100m
rounded_1km
zone_only
status_only
delayed_exact
hidden
```

The policy engine selects the most restrictive rule that applies. Responses include a precision descriptor so clients do not imply exactness.

### Retention engine

Retention is a planned workflow, not a nightly `DELETE`. A policy includes:

```text
policy scope
data category
retention duration
trigger event
archive behavior
anonymization behavior
legal-hold precedence
verification requirements
```

A retention planner produces candidate partitions, rows, files, and derived records. A reviewer or automated policy verifies that no hold applies. Execution occurs in bounded jobs with audit evidence.

For partitioned history, simple partition drop is possible only when every row shares an eligible policy. Otherwise, rows may need to move to policy-specific storage before the partition is retired.

### Anonymization

Removing a name is not enough when a route identifies a home and workplace. Effective anonymization may require aggregation, spatial generalization, time generalization, removal of unique trajectories, or deletion.

Pseudonymization preserves a reversible or linkable identifier and remains sensitive. Document which outcome the workflow provides.

### Legal holds

A legal hold prevents deletion for a defined organization, subject, time range, and data category. It requires:

- authorized creator;
- reason and case reference;
- effective interval;
- scope;
- review date;
- release process;
- complete audit.

Retention jobs consult holds before acting. A hold should not automatically grant broader viewing access.

### Data subject workflows

Support requests for:

- access and export;
- correction of profile data;
- explanation of tracking purpose and access history;
- restriction of processing;
- deletion where applicable;
- withdrawal of consent.

Identity verification must be proportionate. An export job captures a policy snapshot, generates a bounded package, encrypts or protects delivery, expires the file, and records access.

Raw location corrections need care. If a point was incorrectly associated due to an assignment error, preserve a correction record and recompute derived data. Do not silently rewrite history without provenance.

### Privacy review for new features

Every feature that adds data, sharing, or inference should answer:

- What data is collected?
- Why is it necessary?
- Who can access it?
- How long is it retained?
- Can the subject see and control it?
- What can be inferred by combining it with existing data?
- What happens when the feature fails?
- How is deletion propagated to files, summaries, and backups?

### Chapter checklist

Privacy is implemented when:

- person tracking has visible, recorded context;
- consent and withdrawal are enforceable states;
- private zones and precision rules operate server-side;
- retention is planned, reviewed, executed, and audited;
- anonymization claims match technical reality;
- legal holds override deletion without granting access;
- access, correction, and deletion workflows are tested;
- new features undergo privacy review.
