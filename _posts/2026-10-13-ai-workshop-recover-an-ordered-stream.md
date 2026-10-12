---
layout: post
section: ai
title: "AI workshop: recover an ordered tenant stream"
description: "Repair a reconnect reducer that trusts every message. Check snapshot identity, duplicate delivery, sequence gaps, and atomic recovery with eight acceptance tests."
category: Verification
tool: codex
surface: Codex CLI
format: Workshop
environments: [web, cli]
level: Intermediate
workshop_id: replay
verified_at: 2026-10-13
illustration: network
tags: [ai, workshop, tracking, tenancy, reconnect, idempotency]
sources:
  - title: Codex CLI workflows
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

A live view reconnects with a snapshot at cursor 10. Its buffered messages include event 11 twice and event 13 once. Applying every message produces a plausible screen while silently skipping event 12. The useful outcome is a request for a new snapshot, with no partial candidate state exposed.

[Try the browser workshop]({{ '/ai/workshops/?exercise=replay#workshop-lab' | relative_url }}) or [download the workspace]({{ '/assets/labs/ai-workshops.zip' | relative_url }}) and run `node verify.mjs replay`. Positions are synthetic finite numbers; the exercise is a pure reducer and opens no socket.

## Start from a trusted boundary

Validate the snapshot's tenant, nonnegative safe-integer cursor, and position map before processing the buffer. An invalid snapshot throws because there is no valid recovery base. A malformed event instead returns the valid original snapshot with `status: resync`.

Write down which data belongs to the snapshot and which data is merely a proposed update. Copy the position map before changing it. If event 11 is valid but event 12 belongs to another tenant, the final result must still contain the original position values.

For an optional Codex CLI session, use this ordinary prompt:

```text
Inspect replay/app.mjs and its acceptance tests without editing them.
Trace [11, 11, 13] and a buffer containing a foreign-tenant event.
Explain which partial values must never reach the caller.
Change only replay/app.mjs, then run node verify.mjs replay.
Keep tests and the reference solution unchanged; report remaining limits.
```

The [CLI workflow documentation](https://learn.chatgpt.com/docs/codex/cli) explains working on local changes; [repository instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) establish the permitted files. This exercise can also be solved manually without an AI account.

## Separate order from delivery identity

The next new event must have cursor 11. Event 12 can follow it. An exact repeat of event 11 has the same event ID, sequence, subject, and value, so applying it again adds no information. Reusing that event ID with a different payload instead requires resynchronization.

Events at or before the snapshot cursor are already represented by the snapshot. They can be ignored after validating their tenant and shape. A gap, an out-of-order buffer, or a conflicting identity makes the candidate state untrustworthy. The fixture chooses a fresh snapshot rather than trying to reorder an incomplete buffer.

## Make recovery atomic

Keep candidate state private until the whole buffer passes. On resync, return the original cursor and a fresh copy of the original positions. Preserve inputs and treat arbitrary subject IDs as data: a subject called `__proto__` must become an own property without changing the result's prototype.

Use the staged hints to examine one boundary at a time. After eight tests pass, save a timeline, the diff, and the final output. Explain what remains outside the exercise: server authorization, retention expiry, event persistence, transport backpressure, and obtaining an authorized replacement snapshot.

Follow the [realtime chapter]({{ '/books/universal-tracking/16-realtime.html' | relative_url }}) and the [multi-tenant tracking path]({{ '/learn/universal-tracking/' | relative_url }}) to connect this local contract with the wider system.
