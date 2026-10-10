# 5. Produce logs you can safely analyze

## Choose an observation contract

The analyzer needs an event identity, an event time, a site, a resolved client address, a query-free path, a method, a status, a duration, a byte count, and the guard outcome. It does not need authorization headers, cookies, request bodies, query strings, or arbitrary visitor metadata for the baseline detector.

That choice is both a privacy decision and an engineering constraint. A query string may contain a password-reset token. A body may contain personal data. A session cookie is an authentication credential. Collecting those fields first and promising to remove them later expands the number of systems that hold them. Start with a minimal record and require a reason for each addition.

Paths themselves may contain identifiers. A query-free path is therefore not automatically anonymous. Inventory your application's routes before enabling retention. If `/customers/123456/profile` is sensitive, replace selected path segments with a route pattern at a trusted normalization stage or exclude the route. Preserve enough information for the chosen detector without pretending all paths have equal sensitivity.

## Nginx format

The source-pack example uses `log_format ... escape=json` inside the HTTP context. Quoting variables without JSON escaping allows quotes and control characters in a request to damage the event boundary. The example emits numeric values as strings so that Nginx's variable expansion remains predictable; normalization converts those strings before application validation.

The essential shape is:

```json
{
  "schema_version": 1,
  "request_id": "00000000000000000000000000000001",
  "event_time": "2026-10-10T00:00:00+02:00",
  "site_id": "site-demo",
  "client_ip": "198.51.100.23",
  "method": "GET",
  "path": "/missing-one",
  "status": "404",
  "request_time_seconds": "0.002",
  "bytes_sent": "64",
  "enforcement": "allow"
}
```

Use Nginx's own request identifier, rather than accepting a visitor's `X-Request-ID` as the deduplication identity. You may forward the generated identifier to the application for correlation. If the application maintains its own identity, keep the two identities distinguishable.

## Original path and completed outcome

An internal redirect can change the current URI and the final logging location. The example derives a query-free original path from `$request_uri` and keeps it separate from routing variables. Test internal redirects, error pages, and any special application locations in your configuration. A top-level access log can be replaced by a location-specific logging rule, so reading only the server block is insufficient.

The guard outcome is equally important. An application 403 and a guard-generated 403 have different meanings. If the detector counts its own denied requests as fresh hostile evidence, a short ban can sustain itself through feedback. The production contract records `allow`, `block`, `would_block`, `bypass`, `unavailable`, or `unknown`. The teaching rule admits only events whose outcome is `allow`.

Disable authorization-subrequest logging. One public request should not become a second security observation merely because the guard performed a local check. The separate agent metrics can count checks without putting them back into the suspicious-traffic detector.

## Time units and normalization

Nginx's request duration is expressed in seconds. The ingestion contract uses milliseconds. Multiplying once by 1000 is correct; multiplying in both the collector and API is not. A two-millisecond request would otherwise become a two-second observation.

The production design keeps event timestamps as normalized UTC RFC3339. The compact teaching protocol uses integer Unix seconds. This is an intentional simplification and means that the two wire formats are not interchangeable. `normalize_logs.py` converts the Nginx example into the laboratory's format:

```bash
python3 normalize_logs.py guard-access.json > events.ndjson
```

Do not use that file as a production streaming collector. It reads a finite input and stops on invalid data. It is useful for inspecting a captured fixture and making a one-time lab submission. The Vector lesson addresses continuous collection and rotation.

## Exercise

Capture one local request whose path contains a quote and whose query contains a disposable token. Confirm that the resulting event parses as JSON, that the query is absent, and that the request duration has the expected units.

## Answer

The path should remain a single escaped JSON string. The query should not appear anywhere in the generated security event. After normalization, the duration should be milliseconds. If the event fails JSON parsing, inspect the log format before adding a tolerant parser. A tolerant parser can hide a broken producer and silently lose observations.
