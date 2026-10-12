---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "AI workshop: design retry tests before fixing the parser"
description: "Turn retry timing into a table of deterministic cases, inject the clock, and use failures to review an AI-generated implementation."
category: Testing
tool: codex
surface: Codex CLI
format: Workshop
environments: [web, cli]
level: Intermediate
workshop_id: tests
verified_at: 2026-10-12
illustration: clock
tags: [ai, workshop, codex, tests, retries, javascript]
sources:
  - title: Codex CLI
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

An implementation that reads the leading number from every retry value passes a simple “12 seconds” example. It also accepts `12garbage` and cannot calculate a future date correctly. This workshop practices describing boundaries before asking an assistant to produce code.

## Define the exercise's input language

[Download the files]({{ '/assets/labs/ai-workshops.zip' | relative_url }}) and inspect `tests/app.mjs`. The function takes a string and an injected current time in milliseconds. Its result is a nonnegative delay in milliseconds or `null` when the value is unsupported.

For this exercise, accept nonnegative integer seconds, optionally surrounded by whitespace, or a canonical GMT date such as `Mon, 12 Oct 2026 10:00:05 GMT`. Reject fractions, partial numbers, impossible dates, missing input, an invalid clock, and numeric values whose millisecond result exceeds JavaScript's safe integer range. A past date returns zero. This intentionally narrow contract is not a complete HTTP client or a promise to accept every historical HTTP date syntax.

## Predict the results

Write a small table before running the tests:

| Value | Clock | Expected delay |
| --- | --- | --- |
| `0` | Fixed valid time | `0` |
| `12` | Fixed valid time | `12000` |
| Future canonical date | Five seconds earlier | `5000` |
| Past canonical date | One second later | `0` |
| `12garbage` | Fixed valid time | `null` |
| `-1` or `1.5` | Fixed valid time | `null` |

The injected clock removes real waiting and makes the test independent of the machine's current date. Every assertion should run immediately.

## Use the assistant to challenge the cases

Start Codex CLI in the extracted workspace. This is an original prompt:

```text
Read tests/app.mjs and tests/test.mjs without editing.
Explain which contract cases the starter violates.
Suggest one missing boundary case and explain its expected result.
Then fix only tests/app.mjs and run node verify.mjs tests.
Do not weaken assertions or use solution.mjs as input.
```

You might add a wrong weekday, an impossible date, or an overflowing number. Explain why that case belongs to the chosen contract before extending it. A long generated test list is less useful than a few cases that expose distinct assumptions.

```sh
node verify.mjs tests
node verify.mjs tests --solution
```

The supplied starter should fail assertions; your completed implementation should pass. The second command checks a separate worked solution. Neither test suite needs an external service, real timer, or AI API call.

## Separate parsing from retry policy

A valid delay is not automatically an instruction to wait that long. A caller may have a smaller remaining deadline, a retry budget, or an operation that cannot be repeated safely. Keep these decisions outside the parser so each can have its own testable contract.

As an extension, design `chooseWait(parsedDelay, remainingDeadline)` on paper. What should happen when the parsed delay is unavailable or exceeds the deadline? Decide whether the operation should stop, use a bounded fallback, or report an explicit error. Keep that policy visible rather than hiding it in date parsing.

Continue with [reproducible release evidence]({{ '/posts/ai-workshop-automate-release-evidence/' | relative_url }}) or [all workshops]({{ '/ai/workshops/' | relative_url }}).
