---
layout: post
title: "A slow map should not hold the stream hostage"
description: "Bound each WebSocket client's queue, coalesce replaceable marker updates, and give critical events a recoverable path when a browser cannot keep up."
category: Reliability
book_id: universal-tracking
chapter_slug: 16-realtime
illustration: network
tags: [websockets, backpressure, realtime, queues, recovery]
---

A dispatcher opens a live fleet map, then leaves the tab in the background on an unreliable connection. Location updates continue arriving at the server. If publishing waits for that browser to drain its socket, one slow consumer can delay everyone else.

Putting a queue in front of the socket moves the waiting elsewhere. It becomes a solution only when the queue has a limit and an explicit policy for reaching it.

## Separate state updates from events that matter individually

Imagine three messages waiting for the same vehicle:

```text
location version 210: first position
location version 211: newer position
location version 212: latest position
```

For a current-position display, the last update can replace the first two. History remains in durable storage; the browser does not need every intermediate sample merely to move a marker.

An alert transition has different meaning. Replacing “alert raised” with an unrelated newer position would lose information the dispatcher may need. Revocation and authorization changes also require their own handling rather than competition with marker traffic.

Classify messages before designing overflow behavior. A queue of interchangeable byte slices cannot decide which information is safe to replace.

## Put limits around every connection

Choose explicit limits for queued messages, queued bytes, and write time. Message counts alone provide weak protection when payload sizes vary.

When a client reaches the limit, discard superseded location updates first. Keep control and alert handling within a separate bounded policy. If the browser still cannot make progress, close the connection with a documented retryable reason.

Disconnecting a slow client is sometimes the correct outcome. Allowing it unlimited memory is a promise the process cannot keep. Calling a message “critical” also cannot justify an unbounded in-memory queue; its recovery path must live elsewhere.

## Make reconnection useful

The client begins with an authorized snapshot and retains a version or cursor for subsequent deltas. After reconnecting, it reauthenticates and requests replay from a supported cursor, or obtains another snapshot if that cursor is outside retention.

A durable event record supports this recovery. A database notification can wake a replica, but the notification is not the only copy of the event. Periodic reconciliation covers missed wake-ups.

Authorize the restored subscriptions against current policy. A connection that was allowed yesterday should not regain access today merely because its browser remembers a channel name.

## Measure the stalled browser

Create two test clients: one reads normally, while the other stops reading. Publish enough updates to reach the configured limits.

Verify that the healthy client's delivery continues, the stalled client's memory remains bounded, and the latest marker state can be reconstructed after reconnecting. Add an alert transition during the stall and verify its documented recovery path separately.

Then repeat during a rolling restart. Reconnect backoff and jitter should spread snapshot requests rather than making every browser immediately retry together. The successful result is controlled degradation with recoverable state, not the absence of every disconnect.
