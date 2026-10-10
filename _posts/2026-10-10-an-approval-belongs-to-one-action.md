---
layout: post
title: "An approval belongs to one action"
description: "Bind a human decision to the exact tool call, then preserve that identity through retries and uncertain results."
category: Integrations
book_id: agentplane
chapter_slug: 18-approvals
illustration: shield
tags: [agents, approval, authorization, idempotency, tools]
---

An operator approves an agent's request to export a report. Before execution, the agent changes the destination and expands the project scope. If the system checks only an `approved` flag, the human decision now authorizes an action nobody reviewed.

An approval needs an identity as precise as the operation it permits.

## Describe the decision before dispatch

Bind the request to the actor, organization, project, tool server, tool name, schema version, normalized input and policy version. Add an expiration and a stable execution ID.

For the report export, the destination and selected dataset are part of the decision. Changing either creates a different request. A friendly display title is useful to the approver, but it cannot substitute for this binding.

Define input normalization deliberately. Two clients can serialize the same object differently, while an apparently harmless default can change a tool's behavior. The approval service and executor need the same documented interpretation.

## Reserve authority atomically

Two workers may wake up after the approval arrives. A read followed by an unconditional write lets both believe they consumed it first.

Use a conditional transition from approved to reserved for the designated execution. A retry with that execution identity may observe its existing reservation. A different execution, expired request or changed input must fail before reaching the tool.

Keep the decision durable. Restarting the gateway must not restore a consumed approval or erase evidence of which execution claimed it.

## Plan for a missing result

Suppose the export succeeds, but its reply disappears. The reservation proves which execution had authority; it does not prove whether the external effect happened.

Retrying safely requires support at the destination, such as an idempotency key tied to the export, or a way to reconcile the operation's state. Otherwise, report the uncertain outcome and follow an explicit recovery procedure. Consuming an approval once does not make every downstream effect occur once.

## Test the route around the gateway

A perfect approval state machine offers little protection if the sandbox also holds credentials that can call the export service directly.

Verify that the authorized route is enforced at the tool boundary. Test changed inputs, concurrent consumption, expiry and a revoked approver. Record whether a rejected request reached the mock tool at all.

Finally, drop the successful reply and inspect recovery. The system should preserve the original decision and execution identity without turning uncertainty into fresh authority.
