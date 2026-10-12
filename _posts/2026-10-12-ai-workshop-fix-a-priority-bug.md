---
layout: post
section: ai
title: "AI workshop: fix a priority bug without changing the input"
description: "Use a small failing test suite to separate numeric ordering, stable ties, and input ownership before asking a coding agent for a patch."
category: Coding agents
tool: codex
surface: Codex CLI
format: Workshop
verified_at: 2026-10-12
illustration: queue
tags: [ai, workshop, codex, javascript, debugging, tests]
sources:
  - title: Codex CLI
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

A queue displays a priority-2 job ahead of a priority-10 job. A tempting first request is “fix sorting.” That leaves another bug untouched: the function also rearranges the caller's array. This workshop gives the change a small, explicit contract so you can inspect both behaviors.

## Open the workspace

[Download the workshop files]({{ '/assets/labs/ai-workshops.zip' | relative_url }}) and extract them. Use Node.js 20+; there is no install step or API call in the exercise. From the extracted directory, run:

```sh
node verify.mjs bugfix
```

The supplied starter intentionally fails assertions. Read `bugfix/app.mjs` and `bugfix/test.mjs`. It compares priorities as strings and calls the mutating array sort method on the input. The examples contain valid finite numeric priorities; validating arbitrary external job records is outside this exercise.

## State the contract before asking for a change

The result must order larger numeric priorities first, keep arrival order for equal priorities, and leave the input array unchanged. Empty input should produce a fresh empty array. Negative and fractional priorities still use numeric ordering.

Start Codex CLI in the extracted directory so it can read the supplied `AGENTS.md`. The following is an original natural-language prompt, not a slash command:

```text
Inspect bugfix/app.mjs and bugfix/test.mjs.
Explain the numeric-ordering and input-ownership failures first.
Then fix only bugfix/app.mjs. Preserve stable ordering for ties.
Do not change the tests or use solution.mjs.
Run node verify.mjs bugfix and report its exit status.
```

The repository instructions keep the scope small. They do not prove the assistant followed it: inspect the diff yourself. You should be able to explain why the sorting operation now belongs to a new array and why subtracting finite priorities expresses numeric order.

## Check more than the happy path

The suite covers multi-digit priorities, input preservation, stable ties, negative and fractional values, and a fresh empty result. Read each assertion and predict its result before running it. A test that only checks `[3, 2, 1]` would have missed the original string-comparison bug.

```sh
node verify.mjs bugfix
node verify.mjs bugfix --solution
```

The first command checks your implementation. The second runs a separate worked solution and does not copy it over your work. Compare them only after making your own attempt. Keep the failing output, the patch, and the passing output as your evidence.

## Explain the boundary

Copying an array does not deep-copy its job objects. This solution changes the container's order without editing the objects, which satisfies this contract. If callers need an independent object graph, that is a separate requirement with different cost and identity semantics.

An additional useful experiment is to freeze the input array before calling your function. Your implementation should still work because it sorts its own array. Then ask what would happen if `priority` were missing or `NaN`. Decide whether to reject such data at this function or at the ingestion boundary before adding more behavior.

Continue with the [logging review workshop]({{ '/posts/ai-workshop-review-a-logging-change/' | relative_url }}) or browse [all workshops]({{ '/ai/workshops/' | relative_url }}).
