---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "A useful AI handoff fits on one page"
description: "A practical context brief for moving a task between conversations or tools without losing decisions, evidence, and the next useful step."
category: Prompting & context
tool: workflow
surface: Across chat assistants and coding agents
format: Worked workflow
environments: [web, desktop, cli, ide]
level: Beginner
verified_at: 2026-10-10
illustration: queue
tags: [ai, prompting, context, handoff, workflow, agents]
sources:
  - title: OpenAI prompting guide
    url: https://learn.chatgpt.com/docs/prompting
  - title: Claude Code context controls
    url: https://code.claude.com/docs/en/commands
  - title: Gemini project instructions
    url: https://geminicli.com/docs/cli/gemini-md/
---

## Capture the decision, not the whole conversation

A long conversation contains discarded ideas, intermediate output, and repeated instructions. A useful handoff answers a smaller question: what does the next person or tool need to know to take the next correct step?

My handoff starts with the observable goal, followed by the constraints that still matter. Then it names the current state and the evidence behind it. I keep possibilities separate from decisions. “We considered moving the handler” is history; “the handler stays in the API service because the worker is deployed independently” is a constraint someone can act on.

The [OpenAI prompting guide](https://learn.chatgpt.com/docs/prompting) is useful background for supplying context and stating intent. The format below is an original template, intended to be edited for the actual task.

## A template you can reuse

```text
Goal
What should a user be able to observe when this is finished?

Boundaries
What can change? What contract or behavior must be preserved?

Current state
Which files, components, and decisions are relevant right now?

Evidence
What was run or observed? Include exact commands and outcomes.

Open questions
What has not been established? Do not turn guesses into facts.

Next step
What is the smallest useful action, and how will we check its result?
```

## Example: resume a search fix

Imagine the work stopped after implementing category URLs but before checking browser navigation. A handoff could read:

```text
Goal: A shared search URL restores its text and category.
Boundary: Keep the HTML directory usable without JavaScript.
Current state: The filter reads q and category on page load.
Evidence: Reloading ?q=proxy&category=Security restores both controls.
Open question: Back/forward behavior has not been checked yet.
Next step: Change a filter, navigate back, and compare controls and results.
```

This note makes the unfinished work visible. It does not imply that the feature is complete because one reload worked. It also gives the next tool a testable starting point without asking it to reconstruct every previous message.

Before sending the note, I would verify the file names and commands against the current workspace. A handoff written before the last edit can already be stale. If a command failed, include that outcome too; otherwise the next person may spend time repeating an unexplained failure.

## Keep persistent instructions small

Project-wide instructions should describe enduring conventions. A temporary request to investigate one bug belongs in the task brief. Mixing the two makes later tasks inherit a restriction that may no longer apply.

Different tools expose project context differently. [Gemini’s context guide](https://geminicli.com/docs/cli/gemini-md/) explains `GEMINI.md`, while [Claude Code’s command reference](https://code.claude.com/docs/en/commands) documents its context controls. Check the relevant tool’s behavior before assuming an instruction was loaded.

Use the [command guides]({{ '/ai/' | relative_url }}) to find the right control, and pair the handoff with [a verification loop]({{ '/posts/ai-changes-need-a-verification-loop/' | relative_url }}) before calling the task complete.
