---
layout: post
title: "An approximate marker needs an approximate payload"
description: "Location privacy belongs in the server's public projection, covering snapshots, live deltas, expiry, and revocation rather than only the marker shown on a map."
category: Security
book_id: universal-tracking
chapter_slug: 24-public-tracking
illustration: shield
tags: [privacy, location, capabilities, authorization, websockets]
---

A delivery page shows a large circle instead of a precise marker. The interface appears to protect the driver's location, but its network response still contains the exact coordinates. Anyone inspecting the response receives more information than the page intends to share.

Changing how a map draws data does not change what the recipient knows. The public response needs its own server-side projection.

## Define the capability before serializing a location

Treat each share link as a scoped capability. Its stored record establishes the subject or session, allowed fields, precision policy, validity window, and revocation state. The bearer token identifies that record; query parameters do not expand its scope.

For a worked example, suppose a delivery link permits status and an approximate area, with no history. A request asking for exact coordinates or a longer route should still receive only the fields allowed by the capability.

The projection can produce an approved area representation and an appropriate freshness indicator. It should omit precise coordinates entirely. An unused exact-coordinate field, a debugging object, or a hidden route array would defeat that decision.

## Apply the same policy to every delivery path

A correctly minimized REST snapshot can be undermined by the first WebSocket delta. If the live channel sends the internal event unchanged, it restores the precise data that the snapshot removed.

Use the public projection for both paths. Authorize the capability and apply field selection, precision, delay, and private-zone rules before serialization. A public subscriber should never depend on browser code to remove sensitive fields from an internal message.

Delayed sharing also needs a recoverable source. An in-memory timer alone cannot preserve the policy across a restart. Use durable data to select observations eligible for release, and keep the public freshness display consistent with that delay.

## Expiry is a request-time decision

Suppose a share expires at 18:00, but the cleanup worker is temporarily unavailable. A request at 18:01 must still fail its validity check. The worker can maintain records; it should not be the sole mechanism enforcing access.

Revocation needs attention on an already open socket as well. Publish the change through the durable event path and remove or downgrade affected subscriptions. Recheck policy as required when publishing, rather than treating the original handshake as permanent authorization.

## Inspect what the recipient can obtain

Create a test subject with a deliberately distinctive precise position. Fetch the public snapshot, connect its live stream, request disallowed history, and try query parameters that ask for greater precision.

Assert the allowed response shape and verify that precise coordinates never appear in the public payloads. Expire and revoke the capability while the socket is connected, then observe the documented access transition.

Finally, inspect logs, referrers, and cache behavior. A carefully reduced response still needs a delivery path that does not casually expose its bearer token or retain sensitive data in a shared cache. The map is only one of the places where a sharing decision becomes visible.
