## Chapter 23 - iOS Native Location Engine

iOS grants background execution according to declared capabilities, permission state, application behavior, and system policy. The design should use Core Location modes appropriate to the active product scenario and make limitations visible.

### Authorization states

The native module handles:

- not determined;
- restricted;
- denied;
- authorized while in use;
- authorized always;
- reduced accuracy;
- precise accuracy.

Ask for permissions incrementally and explain the benefit at the moment it is needed. A user who starts a live delivery shift understands the request better than a user prompted on first launch without context.

### Location modes

Core Location provides several strategies:

- standard location updates for active sessions;
- significant-change service for lower-frequency background awareness;
- visits for coarse arrival/departure behavior;
- region monitoring for limited geofence cases;
- deferred updates where supported.

The application chooses based on session policy. Standard updates with background capability are appropriate for active real-time tracking, but they consume more power. Significant-change updates are not a substitute for a live running route.

### CLLocationManager configuration

A native policy maps to properties such as desired accuracy, distance filter, activity type, pause behavior, and background update settings.

```swift
struct NativeTrackingPolicy: Codable {
    let desiredAccuracyMeters: Double
    let distanceFilterMeters: Double
    let allowsAutomaticPause: Bool
    let showsBackgroundIndicator: Bool
    let activity: TrackingActivity
    let batchSize: Int
}
```

The manager delegate validates each `CLLocation`. Discard invalid negative horizontal accuracy values. Record timestamp, altitude accuracy where relevant, speed accuracy, and reduced-accuracy state when available.

### Persistence and concurrency

Use a dedicated actor or serial queue for sequence allocation and SQLite writes. The delegate must not start overlapping network uploads.

```swift
actor LocationStore {
    func append(_ point: LocalLocationPoint) throws {
        // Begin transaction, allocate sequence, insert, commit.
    }

    func leaseBatch(limit: Int, now: Date) throws -> LeasedBatch? {
        // Select pending rows, mark lease, return immutable batch.
    }
}
```

The web bridge observes status events on the main thread, but durable writes stay native.

### Background relaunch

Certain location events can relaunch the application. Restore only the minimum state required to persist and synchronize. Do not assume the Angular web view is running.

The native module stores:

- active session identifier;
- device identifier and credential reference;
- sequence epoch and next sequence;
- effective policy;
- last successful sync;
- privacy and stop conditions.

When server state is uncertain, continue local persistence within policy and reconcile safely.

### Accuracy authorization

Reduced-accuracy locations may be sufficient for asset presence or city-level sharing but inadequate for route playback. The app should show the effective accuracy mode and let the server classify data accordingly.

Temporary full-accuracy requests require a declared purpose. Use them only for a clear user action, not as a silent recurring workaround.

### User visibility

Use system indicators and in-app status. A person should be able to see that tracking is active, why it is active, and how to stop or contact an administrator. For managed devices where stopping is restricted, the product must still communicate the policy honestly.

### Network and retry

The synchronizer uses background-capable URL sessions where appropriate, but it still relies on SQLite for durability. It applies server acknowledgements transactionally and respects retry limits and token rotation.

Avoid uploading tiny requests continuously when batching is acceptable. Radio wake-ups can dominate battery use.

### Test matrix

Field validation includes:

- foreground, background, and suspended states;
- while-in-use versus always permission;
- precise versus reduced accuracy;
- low-power mode;
- cellular loss and recovery;
- app termination and relaunch;
- device reboot;
- long stationary periods;
- navigation, fitness, and other apps using location;
- multi-hour route comparison against a reference device.

Record OS version, device model, battery health, environment, and policy. Anecdotal "it worked on one phone" is not evidence.

### Chapter checklist

The iOS engine should:

- select Core Location mode by session need;
- handle reduced and precise accuracy explicitly;
- persist in a native serial context before upload;
- restore enough state for background relaunch;
- remain useful without the web view;
- expose active tracking and policy;
- batch network work;
- pass a documented real-device test matrix.
