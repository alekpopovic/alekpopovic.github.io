## Chapter 17 - Geofences and Alert Processing

A geofence converts a spatial relationship into a state transition: outside to inside, inside to outside, or remaining inside for a duration. The hard part is not drawing a polygon. It is producing stable transitions from noisy, delayed observations.

![Geofence evaluation combines spatial candidates, previous state, and a versioned transition algorithm.](../assets/diagrams/geofence-processing.png){width=94%}

### Geofence model

A geofence record contains:

```text
id
organization_id
name
shape geometry
shape_type
buffer_m
active_from
active_until
altitude_min_m
altitude_max_m
policy
version
```

Supported shapes may include circle, polygon, multipolygon, and route corridor. Normalize all shapes into documented geometry types and reject invalid or excessively complex input.

For circles, storing center plus radius can be clearer than approximating a polygon. Candidate queries can use `ST_DWithin`.

### Candidate selection

Never test every point against every geofence. First filter by tenant, active time, subject/team applicability, and a spatial index.

A polygon containment query can use:

```sql
SELECT id, version
FROM geofences
WHERE organization_id = $1
  AND enabled
  AND (active_from IS NULL OR active_from <= $2)
  AND (active_until IS NULL OR active_until > $2)
  AND ST_Covers(shape, $3::geometry);
```

Boundary semantics matter. `ST_Contains` excludes some boundary cases; `ST_Covers` often matches user expectations for "inside." Choose and document the rule.

### Accuracy-aware transitions

A point with 80-meter accuracy near a 20-meter boundary should not trigger rapid enter/exit alerts. Strategies include:

- require confidence that the accuracy circle lies inside or outside;
- add separate enter and exit buffers;
- require consecutive qualifying points;
- require a dwell duration;
- delay a transition until uncertainty resolves;
- mark low-confidence transitions for review.

Hysteresis is essential. The enter boundary can be tighter than the exit boundary, or vice versa depending on the use case.

### State table

Maintain state per subject and geofence:

```text
geofence_memberships
  organization_id
  subject_id
  geofence_id
  state
  entered_at
  last_evaluated_at
  last_location_id
  algorithm_version
  confidence
```

The worker processes accepted points in recorded-time order within a bounded lateness window. A late point may require reconciliation. Do not emit duplicate transitions when reprocessing.

### Event identity

A transition event should have a deterministic or idempotent identity derived from subject, geofence, transition type, source point, and algorithm version. This prevents duplicate alerts after retries.

```text
geofence.entered
geofence.exited
geofence.dwell_started
geofence.dwell_threshold_reached
```

Store source location ID, previous state, new state, confidence, and algorithm version.

### Alert rules

Geofence events feed a general alert engine. Other alert inputs include:

- speed threshold;
- offline duration;
- battery level;
- SOS;
- route deviation;
- task lateness;
- unexpected movement;
- sensor input from a dedicated tracker.

An alert rule defines scope, condition, schedule, suppression, severity, and delivery channels. Separate alert occurrence from delivery attempts:

```text
alerts
alert_notifications
notification_deliveries
```

The alert is a durable fact. Email, push, SMS, webhook, or in-app delivery may succeed or fail independently.

### Deduplication and suppression

Without suppression, a speeding subject can generate an alert every five seconds. Define an incident lifecycle:

```text
open -> acknowledged -> resolved
```

A rule may open an incident when the threshold is crossed, update its latest observation while still active, and resolve it after a clear period. Delivery policy can notify on open, escalation, and resolution.

Suppression examples:

- no more than one low-battery notification per six hours;
- group repeated offline subjects into an organization incident;
- suppress expected geofence entry during an approved task;
- respect quiet hours except critical safety alerts.

### Deterministic reprocessing

Algorithm upgrades and late data require reprocessing. A reconciliation job reads raw points for a bounded subject interval, calculates transitions with a named version, compares them with existing derived records, and writes a new generation.

Never silently mutate the history that was previously used for compliance or customer decisions. Mark superseded results and preserve explanation.

### Chapter checklist

Geofence and alert processing should include:

- validated, indexed shapes;
- tenant and applicability filtering before spatial tests;
- documented boundary semantics;
- accuracy-aware hysteresis;
- durable membership state;
- idempotent transition events;
- incident-level suppression and resolution;
- versioned, explainable reprocessing.
