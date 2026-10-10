---
layout: post
title: "A lost reply should not erase a location"
description: "A mobile location queue needs stable point identities and explicit acknowledgements, especially when retries regroup the same observations into different batches."
category: Event processing
book_id: universal-tracking
chapter_slug: 12-idempotency-quality
illustration: queue
tags: [mobile, offline, idempotency, synchronization, durability]
---

A courier's phone records positions while its network connection comes and goes. It uploads a hundred observations, the server accepts most of them, and the connection disappears before the reply reaches the phone.

The phone now has uncertainty about delivery, rather than evidence of failure. Removing those observations would risk losing them. Giving every retry a new identity would risk storing them twice.

The useful design starts with the local queue, before an HTTP request exists.

## Give the observation an identity of its own

Assign each point a stable ID when it is persisted locally. Retain its original recording time and sequence context. Constructing a different upload batch must not change that identity.

Use a batch ID for the particular request payload. A retry of that payload keeps the same batch ID; a newly assembled payload gets another. The server can then distinguish an identical request from changed content presented under an old request identity.

Sequence numbers serve a third purpose: detecting ordering and gaps within a device stream. After a device reset, an explicitly established epoch separates new sequences from old ones. A smaller number arriving from a slow connection does not establish a reset by itself.

## Work through a partial response

Consider a small test batch with three points:

| Point | Server result | Local action after receiving the reply |
|---|---|---|
| `point-a` | Accepted | Remove from the upload queue |
| `point-b` | Already accepted, same content | Remove from the upload queue |
| `point-c` | Outside the authorized session | Retain a bounded diagnostic record |

The last row should not enter an endless retry cycle. It needs a terminal classification that is visible to the diagnostic workflow. A temporary service failure needs a different classification and can remain pending.

If this reply is lost, none of these local actions has happened yet. The phone retains the queued points and retries. The receiver recognizes the accepted identities and returns an explicit result again.

If a later synchronization groups `point-a` with new observations, point identity still prevents another stored observation. Batch deduplication alone cannot provide that protection because the batch has changed.

## Keep the live position from moving backward

An observation recorded at 10:04 may arrive after one recorded at 10:09. Accepting the late point into history does not require replacing the current position with it.

Define a deterministic comparison for the current-state projection. Keep recording time separate from receipt time, and apply the documented sequence and quality rules. Arrival order alone cannot describe movement when a phone has been offline.

## Interrupt the acknowledgement path

Test a commit followed by a lost reply. Retry the original batch, then regroup one accepted point into another batch. Verify that history contains one copy of each accepted observation and the local queue clears only after explicit acknowledgement.

Finally, send changed content under an existing identity. It should produce an identifiable conflict while preserving the original observation. These cases test the actual synchronization promise, including the gap between server commit and client knowledge.
