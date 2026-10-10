---
layout: post
title: "Watch the age of the queue"
description: "A healthy process and a short queue can still hide stale security decisions. Measure the delay an operator needs to act on."
category: Observability
book_id: logbranik
chapter_slug: 15-observability-and-capacity
illustration: logs
tags: [metrics, queues, latency, capacity, policy delivery]
---

The dashboard is green. Collectors are running, ingestion returns success, and workers are alive. Yet a desired security decision has not reached one edge.

A process-health check cannot answer how long that edge has been operating with old state. To see the gap, the metrics need to follow the work.

## Start with an operator's question

For collection, ask how old the oldest pending observation is. For ingestion, ask whether commits succeed and whether duplicate or conflict rates change. For delivery, ask how long desired state has remained unapplied.

A queue's length is useful context, but age describes a different problem. A single stuck item can be operationally important even when the queue looks small. A large queue can be acceptable if it drains within the required time budget.

Connect each measurement to an action. An alert is easier to use when it points to a specific stage rather than reporting that the whole system is “slow.”

## Split the journey into delays

Measure request completion to ingestion separately from decision creation to application at the edge. Batching, worker scheduling, transport, persistence, and agent load can contribute differently to those intervals.

Measure request-check latency along the deployed Nginx path too. A fast in-process lookup does not include the socket, scheduling, and response-handling costs paid by a real request.

Compare distributions under a controlled workload rather than relying on a single average. An acceptance target is a hypothesis to measure against; it is not a performance result simply because it appears in a design document.

## Keep metrics bounded

Client IPs and request IDs are useful investigation keys. They are poor choices for unbounded metric labels because each new value creates more series and more memory pressure.

Use metrics for rates, capacity, state classes, and bounded dimensions. Keep detailed event identities in the systems designed to query them under access and retention controls.

Policy size, active decisions, assigned sites, retention, and fleet fanout are separate capacity dimensions. A deployment with little incoming traffic can still make delivery expensive if each update serializes a large full snapshot.

## Manufacture one stalled edge

Delay delivery to a single controlled agent while leaving the rest of the system running. Check that desired-to-applied age rises for that edge and that the active revision remains visible.

The useful dashboard is the one that shows the unfinished work despite healthy processes. It lets an operator trace a stale decision to the stage that needs attention.
