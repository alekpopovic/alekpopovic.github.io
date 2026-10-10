## Chapter 21 - Mobile Architecture with Angular, Ionic, and Capacitor

The mobile application is both a user interface and a sensor system. Web technology is effective for forms, tasks, session controls, and shared product code. Reliable background location requires native Android and iOS components.

![The native engine appends to SQLite first; synchronization removes only explicitly acknowledged points.](../assets/diagrams/mobile-offline.png){width=95%}

### Responsibility split

The Angular/Ionic layer owns:

- authentication and organization selection;
- device enrollment;
- shift and session workflows;
- task lists and proof-of-delivery screens;
- diagnostics and settings;
- secure display of tracking state;
- synchronization status;
- user-visible errors.

The native layer owns:

- OS location APIs;
- foreground/background execution;
- permission state;
- sampling and activity hints;
- battery-aware policy;
- local point persistence;
- wake-up and retry integration;
- platform diagnostics.

The bridge passes versioned commands and events. It does not stream raw positions through JavaScript before persistence.

### Local SQLite queue

The native engine writes every accepted local observation to SQLite before considering network delivery:

```text
mobile_location_points
  point_id
  sequence_epoch
  sequence_number
  session_id
  recorded_at
  latitude
  longitude
  accuracy_m
  altitude_m
  speed_mps
  heading_deg
  battery_percent
  activity
  sync_state
  attempt_count
  last_error_code
  created_at
```

Use transactions and migrations. Encrypt sensitive values when the threat model and platform capabilities justify it, but do not claim that application-level encryption protects a fully compromised device.

### Synchronizer

The synchronizer selects a bounded ordered batch, marks it as in-flight through a lease, sends it, and applies the server response transactionally.

State transitions can be:

```text
pending -> in_flight -> acknowledged -> deleted
                    \-> pending after retryable failure
                    \-> rejected after permanent failure
```

On app or process restart, expired in-flight leases return to pending. The client keeps rejected points for diagnostics until policy deletes them or the user submits a support report.

### Enrollment

A human user signs in and receives a short-lived enrollment grant. The native module generates installation identity and secure key material where possible. The app exchanges the grant for a device credential stored in OS-backed secure storage.

Reinstall and device replacement create a new installation. Do not silently reuse an old device record based only on a mutable hardware identifier.

### Session UX

When tracking a person, the active state must be unmistakable. The app shows:

- tracking active or inactive;
- session activity and purpose;
- start time and elapsed time;
- GPS and network status;
- unsent point count;
- battery impact information;
- stop or pause control when policy permits;
- support and privacy information.

Background tracking must not be disguised as a normal notification or hidden from platform privacy indicators.

### Policy adaptation

The server provides a requested sampling profile, but the native engine combines it with OS constraints and local conditions:

- moving versus stationary;
- battery level and charging state;
- accuracy availability;
- network availability;
- task urgency;
- session type;
- thermal or low-power mode;
- significant-location or activity events.

The app records the effective policy and changes so field diagnostics can explain battery use and gaps.

### Diagnostics

A support bundle can include redacted, bounded information:

- app and native module versions;
- permission state;
- background execution status;
- device clock skew estimate;
- queue counts and oldest pending age;
- last successful upload time;
- recent error codes;
- effective sampling policy;
- battery and network summaries.

It should not include access tokens, exact full route history, or raw personal data unless the user explicitly approves a controlled export.

### Bridge contract

Example commands:

```ts
interface StartTrackingCommand {
  contractVersion: 1;
  sessionId: string;
  deviceId: string;
  activity: 'driving' | 'delivery' | 'cycling' | 'running' | 'walking';
  policy: TrackingPolicy;
}
```

Example events:

```ts
interface TrackingStatusEvent {
  contractVersion: 1;
  state: 'starting' | 'active' | 'paused' | 'stopping' | 'stopped' | 'error';
  queuedPoints: number;
  lastRecordedAt?: string;
  lastSyncedAt?: string;
  errorCode?: string;
}
```

Generate or validate both Kotlin/Swift and TypeScript definitions from a shared schema where practical.

### Chapter checklist

A reliable mobile architecture:

- separates web UI from native location execution;
- persists before network delivery;
- uses leased queue states and explicit acknowledgements;
- enrolls each installation independently;
- makes tracking visible and controllable;
- adapts policy without hiding effective behavior;
- provides redacted field diagnostics;
- versions the native bridge contract.
