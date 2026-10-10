# Part III - The Location Data Plane {.part}

## Chapter 11 - Design the Location Ingestion Contract

The ingestion API is the highest-volume public contract in the platform. It must accept offline batches, distinguish duplicates from rejections, authenticate devices independently, and return enough information for a client to safely delete acknowledged data.

![A location batch passes through authentication, validation, one durable transaction, and realtime signaling.](../assets/diagrams/location-ingestion.png){width=95%}

### Batch instead of one request per point

Mobile devices should persist points locally and upload batches. Batching reduces radio use, TLS overhead, server request volume, and transaction overhead. A batch still has limits:

- maximum body size;
- maximum point count;
- maximum time span;
- supported schema version;
- maximum metadata size;
- maximum accepted age;
- compression policy.

A representative request is:

```http
POST /api/v1/location-batches HTTP/1.1
Authorization: Device eyJ...
Idempotency-Key: 0195f8c0-...
Content-Type: application/json
```

```json
{
  "schema_version": 1,
  "batch_id": "0195f8c0-...",
  "device_id": "0195d001-...",
  "subject_id": "0195a901-...",
  "session_id": "0195e442-...",
  "first_sequence": 4100,
  "points": [
    {
      "sequence": 4100,
      "recorded_at": "2026-10-10T10:00:01.125Z",
      "latitude": 44.81233,
      "longitude": 20.46112,
      "accuracy_m": 6.4,
      "altitude_m": 117.2,
      "speed_mps": 5.8,
      "heading_deg": 182.0,
      "battery_percent": 74,
      "activity": "cycling"
    }
  ]
}
```

The `device_id`, `subject_id`, and `session_id` are repeated in the authenticated context and validated. A client cannot select an arbitrary subject merely by changing JSON.

### Device authentication

A device token has a narrow audience and scope. Validation includes:

- token signature or opaque-token hash;
- credential version and revocation status;
- device status;
- organization binding;
- allowed ingestion schema;
- optional certificate or key confirmation;
- request size and rate policy.

The handler converts the credential into a `DevicePrincipal`. It does not reuse a human user principal.

### Validation order

Validate cheap, global conditions before database work:

1. method and content type;
2. body-size limit;
3. JSON syntax and schema version;
4. point-count limit;
5. finite numeric values and coordinate ranges;
6. timestamp parse and gross future limit;
7. sequence syntax and monotonic shape.

Then validate authenticated relationships and state:

8. active device and credential;
9. subject and organization binding;
10. assignment or session authorization at each relevant time;
11. activity compatibility;
12. batch and point idempotency.

Do not reject an entire useful batch because one point is malformed unless the contract explicitly uses all-or-nothing behavior. A partial result is often better for offline clients, but its semantics must be exact.

### Response semantics

A successful acceptance response can return ranges to remain compact:

```json
{
  "batch_id": "0195f8c0-...",
  "status": "accepted_with_rejections",
  "accepted": [[4100, 4147], [4149, 4152]],
  "duplicates": [[4148, 4148]],
  "rejected": [
    {
      "sequence": 4153,
      "code": "timestamp_too_far_in_future"
    }
  ],
  "next_expected_sequence": 4154,
  "server_received_at": "2026-10-10T10:03:12.031Z"
}
```

The client deletes only accepted and duplicate points. Rejected points move to a visible diagnostics state or are corrected according to a defined rule. They must not retry forever without explanation.

Return `202 Accepted` only when the durable contract supports later processing and the batch itself is safely stored. Return `201` or `200` for synchronous durable insertion. The status code is less important than documented durability.

### Transaction boundary

Within one transaction, the ingestion service should:

1. reserve or load the batch idempotency record;
2. validate assignment/session state consistently;
3. insert accepted location facts;
4. update sequence state;
5. update the latest-location projection conditionally;
6. append durable outbox events;
7. append a compact ingestion audit summary;
8. commit.

A `NOTIFY` executed in the transaction is delivered after commit. It is a wake-up, not the event itself.

### Backpressure

When the database is saturated, the API should fail safely rather than accept data into an unbounded memory queue. Use:

- strict body limits;
- request concurrency limits;
- database acquisition timeouts;
- bounded per-request work;
- clear retryable error codes;
- randomized client retry backoff;
- server hints such as `Retry-After` where appropriate.

The mobile queue is the durable buffer before server acceptance. The server's responsibility begins only after it confirms a durable commit.

### Go handler shape

A handler should be thin:

```go
func (h *Handler) IngestBatch(w http.ResponseWriter, r *http.Request) {
    principal, err := deviceauth.FromContext(r.Context())
    if err != nil {
        writeError(w, ErrUnauthorized)
        return
    }

    req, err := decodeLimitedJSON[IngestBatchRequest](w, r, h.maxBody)
    if err != nil {
        writeError(w, err)
        return
    }

    result, err := h.service.AcceptBatch(r.Context(), principal, req)
    if err != nil {
        writeError(w, err)
        return
    }
    writeJSON(w, http.StatusOK, result)
}
```

The service owns validation and transaction behavior. The handler owns HTTP parsing and rendering.

### Chapter checklist

A production ingestion contract has:

- independent device authentication;
- bounded batch size and schema versioning;
- cheap validation before database work;
- explicit accepted, duplicate, and rejected results;
- safe client deletion semantics;
- one durable transaction for facts and events;
- bounded concurrency and retryable overload behavior;
- no unbounded in-memory acceptance queue.
