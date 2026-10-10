## Chapter 18 - Trips, Stops, Routes, and Activity Analytics

Trips and stops are interpretations of observations. A delivery vehicle, runner, pedestrian, and asset beacon require different thresholds. The platform should provide configurable profiles and preserve the raw evidence behind each derived result.

### Segmentation

A basic segmentation pipeline considers:

- session boundaries;
- assignment changes;
- long reporting gaps;
- movement-state transitions;
- ignition or activity signals when available;
- maximum plausible distance jumps;
- explicit task start and completion.

A trip may begin after sustained movement and end after a dwell threshold. A stop is not simply a point with speed zero; GPS jitter and missing updates make that unreliable.

### Profile-specific thresholds

Example profiles:

| Profile | Start speed | Stop speed | Stop dwell | Gap split |
|---|---:|---:|---:|---:|
| Walking | 0.8 m/s | 0.3 m/s | 2 min | 10 min |
| Running | 1.8 m/s | 0.6 m/s | 1 min | 5 min |
| Cycling | 2.0 m/s | 0.8 m/s | 2 min | 10 min |
| Vehicle | 3.0 m/s | 0.5 m/s | 3 min | 15 min |
| Asset | policy based | policy based | 10 min | 1 h |

These values are illustrative. Field data and product expectations determine the real defaults.

### Trip model

```text
trips
  id
  organization_id
  subject_id
  session_id
  started_at
  ended_at
  start_location_id
  end_location_id
  distance_m
  moving_duration_s
  elapsed_duration_s
  max_speed_mps
  average_speed_mps
  algorithm_name
  algorithm_version
  generation
  quality_summary
```

Stops record center, radius, arrival, departure, dwell, and confidence. Use a robust centroid or representative point rather than averaging latitude and longitude blindly over large areas.

### Distance

Distance calculation should ignore obviously invalid segments and account for accuracy. For each segment:

1. ensure timestamps increase;
2. compute geodesic distance;
3. estimate implied speed;
4. apply activity and accuracy policy;
5. classify accepted or excluded distance;
6. accumulate both totals for diagnostics.

Store the algorithm and thresholds used. Map matching to a road network can improve vehicle distance and route display, but it adds external data, computational cost, and failure modes. It should be optional and never overwrite raw measurements.

### Elevation and pace

For sport activities, altitude from phones can be noisy. Elevation gain should use smoothing and thresholds. Document whether altitude comes from GPS, barometer, or a later terrain model.

Pace is inverse speed over meaningful intervals. Avoid presenting instantaneous pace from one noisy sample. Use a rolling window and show data quality.

### Route representation

A route can have several representations:

- ordered raw point IDs;
- a detailed polyline for close playback;
- simplified polylines for zoom levels;
- bounding box and start/end points;
- aggregate statistics.

Generate representations asynchronously after a trip is stable. A live route can be incremental and later reconciled.

### Playback

The playback API returns points or a polyline with timestamps in bounded chunks. The client interpolates between observations but indicates gaps. Do not animate smoothly across a twenty-minute network outage as if the exact path were known.

Provide controls for:

- speed multiplier;
- pause and seek;
- event markers;
- quality flags;
- task stops;
- geofence transitions;
- battery and network timeline.

### Late data and generations

A late batch can change a completed trip. Use a reconciliation window, such as several hours or a day, depending on device behavior. Recompute affected intervals into a new generation. The current generation is selected for normal views; older generations remain available for audit when required.

After the reconciliation window closes, very late points may be stored but not automatically change business reports without an explicit correction job.

### Activity summaries

Daily and session summaries reduce expensive repeated scans:

```text
activity_summaries
  subject_id
  period_start
  period_end
  activity_type
  distance_m
  moving_duration_s
  elapsed_duration_s
  trip_count
  stop_count
  max_speed_mps
  elevation_gain_m
  algorithm_version
```

Use jobs to update summaries idempotently. Reports read summaries for long periods and raw history only for drill-down.

### Chapter checklist

Derived mobility analytics should:

- use profile-specific, versioned thresholds;
- split on sessions, gaps, and provenance changes;
- account for accuracy and implausible segments;
- preserve raw observations;
- provide multiple route representations;
- expose gaps honestly in playback;
- reconcile bounded late data through generations;
- use summaries for long-range reporting.
