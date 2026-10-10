---
layout: post
title: "Accepted should mean committed"
description: "An ingestion response is a promise about durable observations, including the awkward case where the commit succeeds and the reply disappears."
category: Event processing
book_id: logbranik
chapter_slug: 07-durable-ingestion
illustration: queue
tags: [ingestion, deduplication, transactions, events, durability]
---

A collector sends a batch of access-log events. The receiver commits it, but the connection breaks before the collector receives the response. The collector retries.

That retry is not an exceptional situation. It is one of the normal consequences of moving durable data across a network, and the ingestion contract should handle it without inventing new observations.

## Bind identity to the authenticated producer

The book's deduplication boundary combines the authenticated node identity with the generated request ID. A node name supplied in the event body does not establish who sent it.

For a new identity, retain the validated event and a digest of its representation. An identical retry is a duplicate. A retry with changed content is a conflict that deserves quarantine and investigation rather than an update to the original event.

This preserves the first accepted observation while exposing a producer that has reused an identity incorrectly.

## Validate before allocating unbounded work

Bound request bytes, line bytes, event count, and field lengths near the boundary. Then validate the authorized site, address, method, path, numeric fields, and guard outcome.

Wire types need deliberate checks. In Python, a boolean can satisfy a loose integer type test. A protocol expecting an integer should reject a boolean instead of inheriting that language behavior by accident.

Duplicate JSON keys deserve the same attention. Different components can choose different values from the same ambiguous object. Rejecting ambiguity keeps producer and receiver interpretations aligned.

## Commit the next step with the event

In a production design that separates ingestion from detection, insert the observation and its durable processing job together. A notification can wake a worker, but the job row is what makes the work recoverable.

Return success after the transaction satisfies the chosen durability contract. A successful insertion into process memory cannot support that promise across a restart.

Also keep acceptance separate from detection. A valid stored event may be too old to create a fresh ban, or may not satisfy a rule. “Stored” and “action taken” are different outcomes.

## Lose the reply on purpose

Commit a controlled batch, interrupt the response, and send the same batch again. Then repeat with one changed value under an existing request identity.

The first retry should preserve one observation and report a duplicate. The second should preserve the original and expose a conflict. Those results make an ingestion response a useful contract rather than a hopeful acknowledgement.
