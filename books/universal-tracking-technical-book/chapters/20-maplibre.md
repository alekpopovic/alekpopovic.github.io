## Chapter 20 - Map Rendering and Route Playback with MapLibre

MapLibre GL JS renders vector maps and dynamic layers in the browser. The tracking platform should treat the basemap provider, geocoding provider, and routing provider as adapters so the core product remains portable.

### Layer architecture

A live map can use separate sources and layers for:

- current subject points;
- selected subject highlight;
- movement heading symbols;
- subject clusters;
- geofence fills and outlines;
- active route lines;
- task stops;
- alerts and SOS markers;
- privacy masks;
- playback cursor.

Update GeoJSON source data incrementally or in bounded batches. Do not create one DOM marker per subject at high scale. Symbol and circle layers are more efficient.

### Marker semantics

A marker should communicate more than category color. Encode:

- shape or icon for subject kind;
- border or badge for alert state;
- opacity for freshness;
- heading only when speed and quality support it;
- motion animation sparingly;
- explicit stale and offline labels in details.

Avoid implying precision the data does not have. An accuracy circle can be shown for selected points. Public views may display a larger privacy radius.

### Clustering

Cluster when the viewport contains more points than can be usefully distinguished. Clusters show count and optionally aggregate status, such as the number of active alerts. Clicking a cluster zooms or opens a bounded list.

Server-side aggregation may be necessary for extremely large fleets or historical heatmaps. The client should not download millions of points and rely on browser clustering.

### Route history

A route query is bounded by subject and time. The server can return:

```json
{
  "route_id": "0195...",
  "from": "2026-10-10T08:00:00Z",
  "to": "2026-10-10T10:00:00Z",
  "segments": [
    {
      "quality": "observed",
      "coordinates": [[20.4611, 44.8123], [20.4614, 44.8126]],
      "timestamps": ["...", "..."]
    },
    {
      "quality": "gap",
      "from": "...",
      "to": "..."
    }
  ]
}
```

Longitude precedes latitude in GeoJSON. Keep the distinction visible in shared types.

### Playback engine

A playback engine maps virtual time to route segments. It can interpolate position between consecutive observations for animation, but should not fabricate path across gaps or implausible jumps.

```ts
interface PlaybackState {
  status: 'idle' | 'playing' | 'paused' | 'ended';
  currentTime: number;
  speed: number;
  selectedEventId?: string;
}
```

Use `requestAnimationFrame` for visual updates. Keep domain time independent from frame rate. The route timeline can mark stops, geofence transitions, alerts, task events, and periods of low accuracy.

### Geofence editor

A geofence editor must validate more than drawing:

- minimum and maximum vertices;
- self-intersection;
- maximum area and complexity;
- unsupported dateline crossing;
- circle radius limits;
- team and subject applicability;
- active schedule;
- enter, exit, and dwell policy.

Display the effective buffer and uncertainty behavior so an operator understands when alerts occur.

### Basemap portability

MapLibre is the rendering engine, not the tile license. Configure style URLs and attribution. Cache policy must follow provider terms. For self-hosted maps, plan separate storage, tile generation, and update operations rather than hiding them inside the tracking database.

Geocoding and routing are optional integrations. Store their results with provider, version, time, and confidence. Do not make the ingestion pipeline depend on reverse geocoding.

### Privacy rendering

Precision reduction can happen server-side before coordinates reach the browser. Options include:

- rounding to a grid;
- replacing with a geofence or neighborhood centroid;
- delaying by a time interval;
- hiding points inside private zones;
- showing only ETA and status.

Client-side hiding alone is not a security boundary because the precise data has already been delivered.

### Chapter checklist

A useful tracking map:

- uses efficient vector layers rather than many DOM markers;
- communicates freshness, quality, and alerts;
- clusters at appropriate zoom levels;
- represents route gaps honestly;
- validates geofence geometry and policy;
- treats tiles, routing, and geocoding as adapters;
- applies privacy reduction before data reaches unauthorized clients.
