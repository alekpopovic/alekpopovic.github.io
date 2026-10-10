# 4. Run the laboratory

## Set up an isolated working directory

Use Python 3.12 or a compatible newer release on Linux for the full laboratory. The preparation run used Python 3.12 and Cryptography 50.0.1. The requirements file provides a compatible major-version range, while the verification report identifies the version actually used. Reproduce tests with that recorded version before upgrading dependencies.

From the extracted book package:

```bash
cd companion
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m logbranik demo
```

The demo runs in a temporary directory. Its stable outcomes are:

```text
before (204, 'allow')
ingest {'accepted': 5, 'duplicates': 0, 'quarantined': 0}
monitor (204, 'would_block')
enforce (403, 'block')
revision 3
revoked (204, 'allow')
```

The request ID and decision ID are implementation data, not secrets in this example. Do not turn the example's fixed IP into a real-world allowlist or threat label. It is a documentation address used to make policy transitions reproducible.

## Move from functions to processes

Initialize persistent lab state and create disposable loopback certificates:

```bash
python3 -m logbranik init
python3 -m logbranik certificates
```

These commands refuse to overwrite an existing state or certificate directory. The state directory contains a central signing key and an agent's public verification key because this is a single-machine lesson. In a two-machine deployment, copy only the public key, agent identity, provisioned epoch, and authorized-site configuration to the edge. The central signing private key must not travel with it.

In terminal A, start the agent:

```bash
python3 -m logbranik agent
```

If your teaching host prohibits AF_UNIX sockets, use `python3 -m logbranik agent --tcp-auth`. That binds the authorization handler to loopback port 9101. It does not change the mTLS control listener, which uses loopback port 9443.

In terminal B, start ingestion:

```bash
python3 -m logbranik central-server
```

In terminal C, start periodic delivery:

```bash
python3 delivery_loop.py
```

The delivery process computes a full policy and sends it over mTLS. It checks the returned revision and payload hash. Its one-second loop is a teaching mechanism. The production design replaces repeated whole-state generation with durable desired-state changes, coalescing, a delivery outbox, and independent reconciliation.

## Feed real schema-shaped events

Generate local fixture events without accessing another server:

```bash
python3 - <<'PY'
import time
from pathlib import Path
from logbranik.__main__ import fixture_event
from logbranik.protocol import encode
Path('events.ndjson').write_bytes(
    b'\n'.join(encode(fixture_event(i,time.time())) for i in range(1,6)))
PY
```

Send them through the mTLS ingestion endpoint:

```bash
curl --cacert lab-state/tls/ca.crt \
  --cert lab-state/tls/collector.crt \
  --key lab-state/tls/collector.key \
  -H 'Content-Type: application/x-ndjson' \
  --data-binary @events.ndjson \
  https://localhost:9444/v1/events:batch
```

Inspect decisions with `python3 -m logbranik decisions`. Switch the registered site to enforce mode with `python3 -m logbranik mode enforce`. The delivery loop carries the updated mode to the agent. Check through the Unix socket:

```bash
curl --unix-socket lab-state/auth.sock -i \
  -H 'X-Guard-Site: site-demo' \
  -H 'X-Guard-IP: 198.51.100.23' \
  http://localhost/v1/check
```

For the TCP teaching profile, use the same headers at `http://127.0.0.1:9101/v1/check`. Confirm a 403 only after enforcement mode arrives. A 204 with `would_block` is correct in monitor mode.

## What this proves

The function demo proves the central-to-agent logic in one process. The process exercise proves transport, credentials, persistence, and live publication. Neither proves that Nginx calls the handler for every protected route. Lesson 8 adds that deployment gate.

## Exercise

Submit the same `events.ndjson` twice. Then edit one field in a record while preserving its request ID and submit it again. Compare the ingestion counters.

## Answer

The first retry is reported as duplicates and adds no evidence. The conflicting record is quarantined; it does not overwrite the original. The laboratory saves only the quarantine reason, avoiding a second raw copy of potentially sensitive input. A production quarantine should also have explicit retention, capacity, and access controls.
