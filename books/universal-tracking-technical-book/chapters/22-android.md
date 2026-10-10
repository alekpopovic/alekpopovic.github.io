## Chapter 22 - Android Native Location Engine

Android background execution is policy-driven by the operating system. A production tracker uses a foreground service during active continuous tracking, requests permissions in context, persists locally, and treats process death as normal.

### Service lifecycle

A foreground tracking service can expose actions such as:

```text
START_SESSION
UPDATE_POLICY
PAUSE_SESSION
RESUME_SESSION
STOP_SESSION
SYNC_NOW
```

The service creates its notification channel before starting and calls `startForeground` promptly. The persistent notification explains that location tracking is active and opens the tracking screen.

The native plugin must make start and stop idempotent. If the web layer asks to start the already active session, return current state rather than creating duplicate listeners.

### Permission flow

Request foreground location first and explain the use. Background permission, where required by the OS version and product behavior, is a separate step. The UI must handle:

- precise granted;
- approximate granted;
- foreground only;
- background denied;
- permanently denied;
- location services disabled;
- notification permission denied;
- battery optimization restrictions.

Do not trap the user in repeated system prompts. Provide a settings path and a clear explanation of degraded behavior.

### Location requests

Use the platform location provider with explicit priorities and intervals. A policy can map to a request:

```kotlin
data class NativeTrackingPolicy(
    val movingIntervalMs: Long,
    val stationaryIntervalMs: Long,
    val fastestIntervalMs: Long,
    val minDistanceM: Float,
    val desiredAccuracyM: Float,
    val maxBatchDelayMs: Long
)
```

The effective interval may differ from the request. Record actual observation gaps and provider status.

Avoid holding wake locks continuously. Use bounded work and OS-supported callbacks. A dedicated tracker is better than a phone for requirements that demand second-by-second, twenty-four-hour operation under every power state.

### Persistence transaction

The callback performs minimum work:

1. validate finite values and timestamp;
2. assign point ID and sequence;
3. read lightweight battery/activity context;
4. insert into SQLite in one transaction;
5. schedule synchronization;
6. update status notification if needed.

Network requests do not run in the location callback. If persistence fails, surface a critical diagnostic because the device cannot honestly claim tracking is safe.

### Process death and reboot

The operating system may kill the process. Persist active session state, effective policy, and sequence epoch. On restart, reconcile with the server before resuming when policy allows.

After device reboot, automatically resuming person tracking may have legal and product implications. The rule must be explicit. For a managed vehicle tracker mode it may be allowed; for a personal session it may require user action and visible notification.

### Work scheduling

A background work scheduler can perform deferred sync when continuous service is not active. During an active foreground service, the synchronizer may run directly with network constraints and backoff. Prevent concurrent sync loops using a local lease.

The HTTP client enforces:

- TLS validation;
- request and response size limits;
- connect and read timeouts;
- access and device credential separation;
- idempotency headers;
- no sensitive body logging.

### Activity and sensors

Activity recognition can improve sampling but should be treated as a hint. Sensor availability and permissions vary. Record confidence and avoid changing privacy state solely because a classifier thinks the user is in a vehicle.

Optional signals include:

- motion activity;
- step counter;
- charging state;
- Bluetooth connection to a vehicle or beacon;
- ignition data from external hardware.

Each signal needs a documented battery and privacy purpose.

### Kotlin interface example

```kotlin
interface LocationRecorder {
    suspend fun append(point: LocalLocationPoint)
    suspend fun leaseBatch(limit: Int): LeasedBatch?
    suspend fun applyAcknowledgement(result: BatchResult)
    suspend fun releaseExpiredLeases(now: Instant)
}
```

Repository methods are tested against the actual SQLite implementation, including process-restart scenarios and schema migrations.

### Field validation

Test on multiple vendors and OS versions. Include:

- screen on and off;
- stationary and moving;
- Wi-Fi to mobile-network changes;
- airplane mode and recovery;
- low-power mode;
- app swipe-away;
- process kill;
- reboot;
- approximate location;
- permission revocation during a session;
- multi-hour battery study.

Emulators cannot prove real background behavior.

### Chapter checklist

The Android engine should:

- use a visible foreground service for active tracking;
- handle every permission state explicitly;
- persist before synchronization;
- recover from process death and expired leases;
- define reboot behavior by use case;
- treat activity recognition as a hint;
- expose honest diagnostics;
- pass real-device battery and reliability tests.
