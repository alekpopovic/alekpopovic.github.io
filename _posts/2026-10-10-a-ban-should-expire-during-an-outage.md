---
layout: post
title: "A ban should expire during an outage"
description: "The edge needs enough local time and policy state to end a temporary restriction without waiting for the central server."
category: Reliability
book_id: logbranik
chapter_slug: 13-time-expiry-and-offline-state
illustration: clock
tags: [expiry, TTL, monotonic clock, offline, edge agents]
---

A temporary ban reaches an edge, then its connection to the central service disappears. Fifteen minutes later, the ban should end.

If expiry depends on receiving another snapshot or running a central cleanup job, a temporary restriction can outlive the decision that authorized it. The edge needs to evaluate that lifetime locally.

## Separate delivery freshness from decision lifetime

A policy envelope may have a short window in which the agent can accept it. A decision inside that envelope may remain active longer.

Those times answer different questions. The first limits delivery of a new policy. The second limits enforcement of an accepted decision. Retrying delivery in a fresh envelope must not quietly extend the original ban.

The distinction also matters after restart: a saved policy can contain a decision that is still live even though the original delivery window has ended. Restoration needs its own validation path rather than a blind repeat of initial delivery rules.

## Use clocks for the jobs they can do

Wall time connects issuance and expiry to UTC. A monotonic clock measures elapsed time within one running process.

The laboratory derives a local monotonic deadline from the remaining lifetime when accepting a decision. While the process stays alive, that deadline helps prevent a backward wall-clock correction from extending the ban indefinitely.

This does not certify the host's time. A large divergence can make time health uncertain, and a restart gives the monotonic clock a new origin. Reconstructing remaining lifetime then requires a trustworthy wall-time basis and a documented recovery policy.

## Expiry must not depend on pruning

Request checks should ignore expired entries even if those entries remain in the saved policy. Background pruning can reclaim memory and clean indexes, but a delayed cleanup task should not make an expired decision active.

Keep normal expiry separate from an unhealthy clock in metrics and operational behavior. When the guard cannot establish a safe time basis, the deployment's explicit availability profile determines how that uncertainty affects requests.

## Advance a clock instead of waiting

Apply a short-lived decision with an injected clock. Stop delivery, advance to expiry, and check that the address is allowed. Then test a large backward wall-time correction while monotonic time continues.

These are different cases with different expected outcomes. Keeping them separate turns “temporary” into an enforceable lifetime contract, including when the central server is unavailable.
