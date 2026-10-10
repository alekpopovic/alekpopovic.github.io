# 6. Move events without losing their meaning

## Retry is normal

A collector sends a batch, the database commits it, and the response is lost. The collector cannot know whether the commit happened. Resending is the correct action. The receiver must make that retry harmless. Network delivery and application effects are separate concerns; a transport's acknowledgement does not remove the need for application deduplication.

The production collector is Vector. It tails a known JSON access-log path, normalizes fields, and sends bounded NDJSON batches over authenticated HTTPS. Its HTTP sink offers retry-oriented delivery behavior, but durable end-to-end acknowledgement depends on the capabilities of the complete source-to-sink topology. Validate the exact file-source and buffer behavior you deploy rather than turning a sink label into a guarantee about every log line.

## A buffer has a physical size

Choose a capacity based on an outage you intend to tolerate. If normalized events average 800 bytes and you expect 100 events per second, one hour represents approximately 288 MB of payload before overhead. Filesystem metadata, collector records, variable event sizes, and operational headroom increase the real requirement. A capacity estimate is a planning calculation, not a measured buffer utilization figure.

Set a finite disk buffer and alert on occupancy and age. The oldest buffered event tells you how stale central knowledge has become. The buffer's percentage tells you how close you are to capacity. Both matter: a quiet site may have low occupancy while carrying hours-old observations.

Backpressure is not always loss-free. A collector that stops consuming may let the local log grow until rotation removes unread data. A collector that drops oldest records preserves freshness while losing history. A collector that drops newest records preserves old history while delaying knowledge of current activity. Make that tradeoff explicit and monitor the corresponding drops.

## NDJSON and batch boundaries

NDJSON is one JSON object per line. A JSON array is a different format. A final newline is harmless if the receiver supports it. Empty batches, oversized lines, and an oversized decoded body need a defined response. Keep collector batch limits below the API's limits, including normalization and framing overhead.

The lab contract caps the body at 1 MiB, the batch at 500 records, and a line at 16 KiB. The teaching HTTP handler accepts Content-Length framing and does not implement chunked bodies or gzip. That scope is documented rather than hidden behind a broad HTTP claim. A production ingress can support compression, but must enforce the decoded maximum to avoid a small compressed request expanding into unbounded work.

The original Vector configuration remains in `companion/production-design/examples/vector/`. It is an adaptation starting point for the production RFC3339 protocol. It is not directly connected to the lab's integer-time server. Use the finite normalizer or write an explicitly tested lab transform before connecting them.

## Log rotation

Rotation can rename the current file and ask Nginx to reopen a new one. A collector may track the old file by fingerprint while discovering the new file. Copy-and-truncate creates a different set of races. Your deployment test should keep traffic flowing through rotation and compare request IDs observed before and after it.

Testing a cold startup against one small file does not prove rotation behavior. Restart the collector with pending data, rotate a file while it is reading, and then restore the central endpoint after an outage. Count unique request IDs. Record duplicates separately from missing IDs. Duplicates are expected under retries; missing IDs are a different problem.

## Permanent failures

A retryable 503 and a malformed 400 must not look identical in dashboards. A permanently invalid batch can occupy a retry loop and starve valid traffic. The ingestion design quarantines individual invalid records while committing valid neighbors. Entire-request errors, such as an invalid content type or decoded-size violation, remain explicit request failures.

Check the deployed collector's handling of every response class in this contract. Do not assume it retries every non-2xx status or that every permanent drop generates an operator-visible signal.

## Exercise

Plan a ten-minute central outage at 100 events per second with 800-byte normalized events. What payload capacity does the arithmetic suggest, and what must a deployment measurement add?

## Answer

The payload estimate is 48 MB: 100 multiplied by 600 multiplied by 800. Add framing, buffer overhead, filesystem headroom, and the observed event-size distribution. Measure disk consumption and backlog-drain time. A nominal 48 MB setting would leave no margin and would not prove ten minutes of operational tolerance.
