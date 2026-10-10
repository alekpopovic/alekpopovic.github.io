---
layout: post
title: "A timeout is not a stopped deployment"
description: "A missing heartbeat changes what you know about a runner. It does not tell you what happened on the deployment target."
category: Reliability
book_id: modern-ci
chapter_slug: 10-fences
illustration: clock
tags: [runners, leases, fencing, retries, deployments]
---

A deployment starts, the runner loses its connection, and the dashboard stops receiving heartbeats. After a minute, the lease expires. It is tempting to put the job back in the queue and let another runner finish it.

But the first runner may still be changing production. The missing network connection is between the runner and the control service. The connection to the deployment target might be fine.

That distinction belongs in the state model before it becomes an incident.

## Separate permission from execution

A lease describes how long a runner is authorized to act as the current owner. A fence identifies the generation of that ownership. Together, they help the control service reject messages from a superseded attempt.

They do not automatically stop a remote process. Marking a database row as expired cannot reach through a broken connection and terminate a deployment command.

The useful state after losing contact is often **uncertain**. It tells an operator that the platform has lost evidence about execution and needs to reconcile before starting another mutation.

## Keep the old result in its own attempt

Suppose attempt A has fence 7. After its execution is confirmed stopped, a retry creates attempt B with fence 8. Then A reconnects and reports success.

The report may be worth recording, but it cannot complete B. Accepting a current result should check the job, attempt, runner, fence, and permitted state together. A late observation belongs to the attempt that produced it.

```text
attempt A, fence 7: stopped, then a late report
attempt B, fence 8: current execution
late A report: evidence about A, never completion of B
```

Keeping this history also explains disagreements between the dashboard and the target. Overwriting the current row would erase the evidence needed to investigate them.

## Protect the target boundary too

If the deployment adapter can enforce an operation identity or a target revision, use it. The target must actually check that contract; sending an extra fence field does nothing when the receiver ignores it.

For a target without that protection, retain its reservation while execution is uncertain. Inspect what is running, identify the applied revision, and record the recovery decision.

## Try the reconnect case

Disconnect a runner while its target operation remains active. Let its lease expire, then reconnect it with the original attempt identity. The test should show both that stale authority is rejected and that a second deployment has not quietly started.

This is the point where a timeout stops being a retry setting and becomes a question about what the system can prove.
