---
layout: post
title: "Reserve capacity before starting work"
description: "A concurrency quota needs a durable reservation before dispatch, plus a recovery policy for allocations whose outcome is unknown."
category: Reliability
book_id: agentplane
chapter_slug: 20-metering-budgets
illustration: queue
tags: [quotas, concurrency, reservations, agents, recovery]
---

A customer may run ten sessions. Nine are active when two API replicas receive a new request at the same time. Each counts nine, each starts a session, and the customer now has eleven.

The arithmetic is correct in both handlers. The decision was never coordinated.

## Reserve at one durable boundary

Store the allocation decision in a transaction shared by the replicas. A conditional counter update or a locked row can make the check and reservation one operation.

The first request reserves slot ten. The second observes that no capacity remains and receives a defined response before any create command is dispatched. An in-memory semaphore inside each API process cannot establish this organization-wide rule.

Give each reservation a stable identity tied to its operation. Retrying the same request should find the original allocation rather than consume another slot.

## Commit intent before contacting the cluster

Persist the reservation and the outgoing create intent together. After commit, a worker can dispatch the command and retry delivery if the connection fails.

Avoid holding the database lock while waiting for a remote cluster. A slow connector would otherwise turn one customer's provisioning delay into contention for unrelated requests sharing the allocation boundary.

The committed reservation means capacity has been promised. It does not mean a sandbox exists or that its execution environment is healthy. Track those facts separately so the interface can explain what is pending.

## Do not free a slot because a heartbeat vanished

The dangerous recovery case is a connector that starts the workload and then disconnects before confirming it. Releasing the reservation immediately creates capacity for another session while the original may still be running.

Represent the allocation as uncertain and reconcile it against observed workload state. Define who can override that uncertainty and what evidence the override requires. A timeout explains why the control plane stopped waiting; it does not establish that compute stopped.

## Separate capacity from consumption

A reserved slot is a concurrency obligation. CPU usage, allocated memory and a customer's spending budget are different quantities with different evidence.

Test those boundaries independently. Race two creates against one remaining slot, deliver the winning command twice, then lose its reply. Verify that one logical reservation exists, the duplicate delivery preserves its identity, and the unknown result remains visible until recovery resolves it.

Only release the reservation when its obligation is resolved according to the documented lifecycle. That makes the quota explainable during the failure cases where a simple count becomes least trustworthy.
