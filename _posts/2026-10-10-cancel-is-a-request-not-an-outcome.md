---
layout: post
title: "Cancel is a request, not an outcome"
description: "A useful deployment history records when cancellation was requested and what the running operation actually did."
category: Delivery
book_id: modern-ci
chapter_slug: 19-recovery
illustration: clock
tags: [cancellation, recovery, rollback, state, deployments]
---

An operator clicks Cancel just as a deployment finishes successfully. What should the interface show?

If the button immediately turns the run into a cancelled result, the history now says something the runtime never observed. The deployment happened. A cancellation request arrived too late to prevent it.

The interface should help the operator understand that timeline.

## Record intent and observation separately

Cancellation has several steps: the user requests it, the control service records it, the runner receives it, the runtime tries to stop, and somebody observes the result. Each step can be delayed or fail.

A queued job may be cancelled before execution begins. A running deployment may already have changed an external service. Giving both situations one instantaneous transition hides the difference that matters during recovery.

Record the request time separately from the observed terminal time. If the same authorized attempt reports a successful exit after the request, preserve that observation and explain that cancellation was requested too late.

## Uncertainty needs a reservation

Now change the scenario: the runner disappears after receiving Cancel. The control service cannot tell whether it stopped, finished, or is still applying a change.

Releasing the target reservation at this moment lets a new deployment overlap with an unknown operation. Keep the reservation while collecting evidence about the runner and the target.

A recovery record should identify who inspected the target, when they inspected it, which revision they observed, and what decision followed. A newly healthy runner connection is useful evidence, but it does not restore an expired attempt's authority by itself.

## Rollback needs its own plan

Restarting the previous image may reverse an application release. It may not reverse a data migration or a message already sent to another system.

Before deploying, identify the compatibility window for the previous binary and the recovery method for data changes. A rollback is another authorized operation with a target reservation and health checks. It deserves its own identity rather than an edit to the failed deployment's history.

## Exercise the race deliberately

Test cancellation before a job starts, during a slow target mutation, and immediately after a successful exit. Include a disconnected runner in the last two cases.

For every result, ask whether the interface distinguishes the user's intent from the evidence received. That small distinction makes a deployment history useful when the next operator needs to decide what is safe to do.
