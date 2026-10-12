---
layout: post
section: ai
title: "AI workshop: review a logging change for data exposure"
description: "Review a short request-event function, identify how new fields can leak into logs, and verify a deliberate output contract with regression tests."
category: Code review
tool: codex
surface: Codex CLI
format: Workshop
verified_at: 2026-10-12
illustration: shield
tags: [ai, workshop, codex, review, logging, data-boundaries]
sources:
  - title: Codex CLI review workflow
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

A small change makes request logs more convenient by spreading every property of a request object into an event. The current dashboard looks fine. The risk becomes visible when you inspect the serialized payload: headers, body fields, and query parameters now travel with it. This workshop practices a focused review with observable evidence.

## Run the review fixture

[Download and extract the workshop files]({{ '/assets/labs/ai-workshops.zip' | relative_url }}). In the extracted directory, run:

```sh
node verify.mjs review
```

The starter intentionally fails. All values in this example are synthetic. Read `review/app.mjs` as if it were a proposed patch, then inspect the test fixture. The useful operational fields are method, route path, status, and duration. Copying the whole request makes the output depend on everything a caller might add later.

## Ask for findings before edits

In Codex CLI, submit this original prompt:

```text
Review review/app.mjs without editing it.
Trace which values reach JSON.stringify(requestEvent(request)).
For each finding, name the trigger, exposed value, and minimal fix.
Focus on credentials, query parameters, request bodies, and future fields.
Do not claim a production incident: this is a synthetic exercise.
```

This is a normal task prompt. Codex CLI also has a dedicated review workflow; the linked official documentation describes its available review targets. The fixture itself needs no AI account and can be examined manually.

A useful finding connects a concrete input to a concrete output. “Logging may be unsafe” is too broad. “The spread copies `headers.authorization`, so serializing the event includes the sample bearer token” identifies the causal path and suggests a test.

## Implement an output contract

The event contract for this exercise has exactly five fields: `event`, `method`, `path`, `status`, and `duration_ms`. `path` is the local route before a query string or fragment. The input uses local request paths; parsing arbitrary URLs and protecting sensitive path segments are separate concerns.

Ask the assistant to change only `review/app.mjs`, retain the fixed event name, and leave the caller's request untouched. An explicit allowlist makes later additions to the request object stay outside the event by default.

```sh
node verify.mjs review
node verify.mjs review --solution
```

The tests check the exact field set, the route path, absence of synthetic secret values from serialized output, unknown future fields, and input preservation. A nested object that merely hides a value from the visible UI would still fail the serialization check.

## Keep the review useful

Save your findings beside the patch and passing result. Explain why an allowlist is easier to maintain here than deleting today's known sensitive fields. Also record the remaining boundary: route paths can themselves contain identifiers, and operational metadata can still be sensitive. This exercise establishes a small output contract rather than a universal logging policy.

For a follow-up, invent a new input field named `customer_note` and check that it stays absent without another code change. Then apply the same reasoning to a real analytics or audit event you own, using a synthetic fixture rather than copying private traffic.

Continue with [test design for retry timing]({{ '/posts/ai-workshop-design-retry-tests/' | relative_url }}) or [all workshops]({{ '/ai/workshops/' | relative_url }}).
