---
layout: post
title: "A cron tick needs an identity"
description: "Schedulers become easier to recover when an intended occurrence is durable data rather than a timer callback."
category: Integrations
book_id: modern-ci
chapter_slug: 16-automation
illustration: clock
tags: [scheduling, cron, timezone, automation, recovery]
---

A scheduled build runs every hour. During a database outage, the scheduler misses three callbacks. When it restarts, should it create three runs, one run, or none?

All three can be reasonable policies for different jobs. The mistake is letting a process restart choose the policy accidentally.

## Persist the occurrence you intended

A schedule needs an expression, a timezone, a next intended occurrence, and a catch-up rule. A useful occurrence identity combines the schedule ID with the intended UTC instant.

That identity gives two overlapping scheduler instances something they can agree on. They may both notice the same due occurrence, but a durable uniqueness boundary can ensure it creates one logical request.

It also gives an operator an explanation for why a run exists. The record points to a particular scheduled occurrence, rather than to whichever host's timer happened to fire.

## Make missed work a product decision

A monthly administrative task may need its most recent missed run. A minute-by-minute refresh job may become actively harmful if it floods the queue with a day's backlog.

Choose a bounded catch-up policy and make it visible. Record skipped occurrences when they matter to the job's history. A deliberate skip is more useful than a missing row nobody can explain.

The same care applies to local-time schedules. A daylight-saving change can repeat a local time or remove it entirely. Specify whether repeated instants both run and whether a missing local time is skipped or moved. Persist the interpretation rather than relying on an undocumented host default.

## Keep trigger intent separate from source identity

Two runs can legitimately build the same commit. One may be a scheduled check and another an operator's deliberate rebuild.

A global “this commit was already built” flag would collapse distinct intentions. Deduplicate the trigger delivery or occurrence instead, and record the actual source revision each run checks out.

## Recover from a manufactured gap

Pause the scheduler across several intended occurrences. Restart two scheduler instances together and inspect the resulting records.

You should be able to explain which occurrences ran, which were skipped, and why none were duplicated. Test timezone boundaries with an injected clock rather than waiting for a calendar transition.

Once occurrences are explicit, scheduling becomes a recoverable workflow. The timer is simply one way to notice that work is due.
