# Part IV - Web and Mobile Clients {.part}

## Chapter 19 - Build the Angular Operations Dashboard

The operations dashboard is a decision surface, not a database browser. Its architecture should separate domain state, map rendering, realtime transport, and user workflows.

### Workspace structure

A shared Angular workspace can contain:

```text
web/
  dashboard/
  public-tracking/
  shared/
    api-client/
    auth/
    ui/
    maps/
    realtime/
    models/
```

Use strict TypeScript and standalone components. Generated API types come from OpenAPI, while handwritten domain facades protect components from transport details.

Feature areas may include:

```text
shell
auth
organization
live-map
subjects
devices
sessions
history
geofences
alerts
tasks
reports
settings
audit
```

Lazy-load major areas. Keep map-heavy code out of routes that do not need it.

### State model

Avoid a single global mutable store containing every point. Distinguish:

- authenticated principal and selected organization;
- registry entities and list filters;
- current live state keyed by subject;
- ephemeral map viewport and selection;
- bounded history playback data;
- realtime connection and subscription intents;
- form drafts and server errors.

Signals or a disciplined state library can manage this. The choice matters less than explicit ownership and immutable updates.

### Snapshot and delta integration

A live-map facade performs:

1. fetch authorized snapshot;
2. normalize subjects and latest states;
3. open WebSocket;
4. subscribe with snapshot high-watermark;
5. apply deltas only when their version is newer;
6. resynchronize on a gap or protocol error;
7. expose freshness and connection state to the UI.

Do not let map components parse WebSocket frames directly. A protocol adapter validates messages and converts them into typed domain updates.

### Authentication

The web client uses short access tokens and secure refresh behavior. Prefer refresh tokens in secure, same-site HTTP-only cookies when the deployment model supports it. Keep access tokens in memory. Protect state-changing requests against cross-site request forgery when cookies are used.

The router applies authentication and permission guards for UX, but the server remains authoritative. A hidden button is not authorization.

### Operational list design

Dispatchers need dense, scannable information. A subject list can show:

- name and kind;
- movement and connection state;
- freshness;
- current task;
- team;
- battery and GPS quality;
- alert severity;
- last meaningful place.

Virtualize large lists. Filters should be reflected in URL state so a view can be shared or restored. The server handles large dataset filtering; the browser should not download every subject to search locally.

### Forms and concurrency

Administrative forms use optimistic concurrency. Include the resource version in updates. If another user changed the object, present a conflict with field-level context rather than silently overwriting.

Validate in the client for usability and again on the server for correctness. Map server error codes to stable form messages.

### Accessibility

A map cannot be the only representation. Provide:

- keyboard-accessible lists;
- meaningful status text;
- focus management for dialogs and panels;
- sufficient contrast;
- non-color alert indicators;
- reduced-motion support;
- table or textual alternatives to visual route data where practical.

Live updates should not constantly steal screen-reader focus. Announce only important changes through controlled live regions.

### Performance

Optimize measured bottlenecks:

- lazy-load maps and heavy charts;
- cluster or aggregate markers;
- update only changed features;
- avoid recreating map sources for every point;
- use web workers for expensive client transformations when justified;
- limit history windows;
- cache immutable reference data;
- cancel obsolete HTTP requests.

A live dashboard should remain responsive during a reconnect burst and while thousands of markers update.

### Error and degraded states

The UI distinguishes:

- authentication expired;
- realtime disconnected but REST available;
- stale snapshot;
- partial subject data;
- history unavailable;
- permission revoked;
- rate limited;
- server maintenance.

A visible "last updated" indicator is more honest than a map that silently freezes.

### Chapter checklist

The dashboard should have:

- feature-based Angular boundaries;
- typed API and WebSocket adapters;
- normalized live state separate from history;
- snapshot and delta recovery;
- server-driven filtering and virtualized lists;
- optimistic concurrency;
- accessible non-map representations;
- explicit degraded and stale states.
