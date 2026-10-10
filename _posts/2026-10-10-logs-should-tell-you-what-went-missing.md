---
layout: post
title: "Logs should tell you what went missing"
description: "A reconnecting log stream needs ordering, ownership, and an honest answer when the missing bytes are no longer available."
category: Observability
book_id: modern-ci
chapter_slug: 13-live-logs
illustration: logs
tags: [logs, streams, reconnects, backpressure, retention]
---

A build page disconnects, reconnects, and starts showing output again. It looks healthy, but twenty seconds of logs have disappeared between the two connections.

If the interface simply joins the new text to the old text, the reader sees a continuous story that the system cannot support.

## Name the stream and its position

Log data belongs to a project, run, attempt, and stream. The attempt is essential: a retry should not append into its predecessor's output as though both came from one execution.

Within that stream, sequence bounded segments. A receiver can accept the next sequence, acknowledge an identical retry, and reject conflicting bytes for a sequence it has already committed.

This turns reconnect behavior into a concrete question: what is the last accepted position, and can the receiver provide everything after it?

## Store bytes before advertising them

An upload can write an attempt-scoped temporary object, verify its size and digest, and then finalize the metadata that makes the segment visible.

If the metadata commit fails, the object may become an orphan. That is a storage-cleanup problem. Publishing metadata before the bytes satisfy the durability contract creates a worse problem: readers are promised output that may not exist.

Keep ownership checks on finalization. A capability issued to one attempt must not let a stale runner write into a newer attempt's stream.

## Make gaps part of the interface

A browser transport can reconnect with a cursor, but the application still has to implement replay. If the requested range has expired under retention, say so. If a runner's bounded spool intentionally truncated output, show the gap and its reason.

The alternative is to manufacture continuity. That can conceal exactly the line an operator needs while investigating a failed deployment.

Backpressure needs an explicit policy too. Blocking output consumption, terminating the job, and recording truncation have different effects on the process being observed. Choose and test the behavior rather than allowing a full spool to silently drop bytes.

## Read output as untrusted data

Repository-controlled commands can print markup, control sequences, and misleading messages. Render their output as text under a defined terminal policy. A line claiming that a deployment was approved must remain a log line, not resemble an actual platform event.

Try a reconnect after retention has removed the requested segment. A useful log viewer should explain what it can recover and visibly mark what it cannot.
