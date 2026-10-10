## Chapter 27 - A Native GPS Protocol Gateway in Go

Dedicated trackers often use long-lived TCP or UDP connections and vendor-specific binary protocols. The gateway's job is to authenticate or map a device, parse bounded frames, normalize observations, send required acknowledgements, and pass canonical envelopes into the shared ingestion service.

![The gateway isolates network framing and vendor decoders from canonical ingestion.](../assets/diagrams/gps-gateway.png){width=95%}

### Listener architecture

Run the gateway as a separate role with configured listeners:

```text
:5001/tcp  Teltonika Codec 8/8E
:5002/tcp  GT06 family
:5003/udp  supported datagram protocol
:5055/http OsmAnd-compatible endpoint
```

Each listener has:

- connection and packet limits;
- read and idle timeouts;
- maximum frame size;
- per-IP and per-device rate limits;
- protocol-specific framing;
- graceful shutdown;
- metrics that do not expose device identifiers as labels.

Use Nginx stream proxying only when the build includes the required TCP/UDP modules and the operational team understands client address forwarding. Direct listeners behind a network load balancer are another portable option.

### Bounded frame readers

Never allocate based on an untrusted length field without a maximum. A protocol adapter first reads a fixed header, validates length and version, then reads exactly the bounded remainder.

```go
func readFrame(r io.Reader, max int) ([]byte, error) {
    var header [4]byte
    if _, err := io.ReadFull(r, header[:]); err != nil {
        return nil, err
    }
    n := int(binary.BigEndian.Uint32(header[:]))
    if n <= 0 || n > max {
        return nil, ErrFrameSize
    }
    frame := make([]byte, n)
    if _, err := io.ReadFull(r, frame); err != nil {
        return nil, err
    }
    return frame, nil
}
```

Real protocols have their own headers, checksums, and acknowledgements. The safety pattern remains the same.

### Adapter contract

A protocol adapter returns canonical messages:

```go
type LocationEnvelope struct {
    ExternalDeviceID string
    RecordedAt       time.Time
    Latitude         float64
    Longitude        float64
    AltitudeM        *float64
    AccuracyM        *float64
    SpeedMPS         *float64
    HeadingDeg       *float64
    Sequence         *int64
    Attributes       map[string]any
    RawReference     string
}

type Decoder interface {
    Identify(ctx context.Context, conn ConnectionInfo) (IdentityHint, error)
    Decode(frame []byte) ([]LocationEnvelope, Ack, error)
}
```

The adapter does not write database rows directly. It passes envelopes to an ingestion application service that applies device mapping, assignments, idempotency, quality, and transaction rules.

### Device identity mapping

Vendor identifiers such as IMEI are external identifiers, not secrets. A tracker may also use a password, shared key, or session handshake. Map the external identifier to an internal device within an organization and protocol profile.

Unknown devices are rejected or quarantined according to provisioning policy. Never auto-create an active device from an arbitrary packet on the public Internet.

### Protocol acknowledgements

Many trackers expect an acknowledgement indicating accepted record count or command state. The gateway should acknowledge only according to documented durability semantics. If the protocol allows, acknowledge after the batch is committed. If it requires earlier acknowledgement, document the risk and persist a raw frame or durable staging record first.

Commands from server to device need their own queue, expiry, capability check, and delivery receipt. A command such as immobilization is safety-critical and requires stronger policy, step-up authentication, and device-specific validation.

### OsmAnd-compatible HTTP

An HTTP protocol is a useful first adapter. It maps query or JSON fields to the canonical envelope, authenticates a device token, applies body and parameter limits, and calls the same ingestion service as mobile batches.

Compatibility should be documented precisely. Do not claim full protocol support when only a subset is implemented.

### Binary protocols

For Teltonika Codec 8/8E and GT06-family devices:

- implement framing from vendor specifications;
- validate CRC/checksum before parsing fields;
- cap record and IO-element counts;
- handle signed/unsigned conversions carefully;
- preserve unknown attributes in a bounded structure;
- normalize units explicitly;
- fuzz every parser;
- maintain binary fixtures from permitted test devices or specifications.

Protocol families contain variants. Identify supported versions and reject unknown frames safely.

### Raw packet handling

Normal logs never contain raw packets. A diagnostic quarantine may retain encrypted, redacted packets for a short period with strict access and size limits. Store a checksum and parser result. Provide deterministic replay tooling that feeds a packet fixture into a decoder without production network access.

### Abuse and load shedding

The gateway is exposed to malformed and slow clients. Defenses include:

- accept-rate limits;
- maximum concurrent connections;
- per-connection deadlines;
- bounded goroutines and buffers;
- slowloris protection;
- invalid-frame thresholds;
- temporary network and device bans;
- circuit breaking when the database is unavailable;
- graceful refusal rather than unbounded memory buffering.

### Chapter checklist

A safe GPS gateway has:

- separate bounded listeners per protocol;
- explicit framing and maximum sizes;
- canonical envelopes and shared ingestion rules;
- controlled device provisioning;
- durability-aware acknowledgements;
- versioned protocol support and fixtures;
- fuzzed decoders;
- restricted raw-packet quarantine;
- connection and abuse controls.
