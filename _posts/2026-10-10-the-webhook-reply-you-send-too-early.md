---
layout: post
title: "The webhook reply you send too early"
description: "Returning success before an event is durable leaves a small failure window with a very expensive consequence."
category: Event processing
book_id: modern-ci
chapter_slug: 08-ingestion
illustration: network
tags: [webhooks, inbox, outbox, idempotency, transactions]
---

A webhook handler verifies the request, adds work to an in-memory queue, and returns success. The process restarts before a worker reads the queue.

The sender believes the event was accepted. The receiver has no durable record that it ever arrived. A fast response has turned a restart into lost work.

## Decide what success promises

The important boundary is the commit. Before acknowledging accepted work, persist the event receipt and the instruction that will cause it to be processed.

If creating a complete run is cheap enough, the transaction can contain the receipt, frozen run, and outbox entry. If compilation belongs off the request path, commit a durable inbox job first and let a worker do the expensive part later.

Both designs give recovery something to find. A process-local queue can still be a useful wakeup mechanism, but it cannot be the only place accepted work exists.

## A duplicate is a normal delivery

The receiver may commit successfully and lose its response. When the sender retries, the event has already been accepted.

Use a durable uniqueness boundary that includes the configured provider, installation, and delivery identity. An identical retry returns the existing receipt. It does not create another run simply because a different API instance handles the request.

Manual requests need their own identity. A project-scoped idempotency key plus a digest of the normalized request distinguishes a retry from accidental reuse of the key with different input.

## Authentication does not deduplicate

A valid signature tells you something about the received bytes. It does not make a second delivery disappear or prove that every field in the payload is authorized for your integration.

Verify the received body under the provider's contract, then apply the configured repository and installation boundaries. Keep byte limits and event-type validation close to the request boundary so that rejected input cannot consume unbounded work.

## Test both sides of the commit

Stop the process immediately before committing, then immediately after committing but before sending the response. Retry the same delivery after each restart.

The first case should allow the event to be accepted once. The second should recover the existing receipt and process the durable instruction without creating another logical run.

That experiment makes the response contract concrete. Success means the receiver has taken durable responsibility for the work, even when the connection cannot carry the reply back.
