---
layout: post
section: ai
title: "AI changes need a verification loop"
description: "Turn a broad AI request into a small, observable change: define the behavior, inspect the diff, test the boundary, and record the evidence."
category: Practical workflows
tool: workflow
surface: Across coding agents and IDE assistants
format: Worked workflow
verified_at: 2026-10-10
illustration: shield
tags: [ai, testing, verification, review, workflow, debugging]
sources:
  - title: Codex review and diff commands
    url: https://learn.chatgpt.com/docs/developer-commands
  - title: Copilot testing examples
    url: https://docs.github.com/en/copilot/how-tos/chat-with-copilot/get-started-with-chat-in-your-ide?tool=vscode
---

## Define the result before asking for code

“Improve the reader” leaves too many choices open. “When I choose a chapter, keep the hidden site menu hidden and show the new chapter at the top” describes something a person can observe. The second request gives both implementation and review a common reference point.

For each task, I write one success example and one boundary example. In a chapter reader, the success example might be switching chapters while the menu is hidden. The boundary example might be navigation when browser storage is unavailable. These examples should come from the feature’s behavior, not from the structure of the proposed code.

## Use four separate checks

| Check | Question |
| --- | --- |
| Behavior | Does the visible result match the request? |
| Diff | Does every changed file help deliver that result? |
| Boundary | What happens when a dependency or input is missing? |
| Evidence | Can someone else repeat the useful check? |

These checks answer different questions. A clean diff does not demonstrate keyboard focus. A passing unit test does not demonstrate that a small-screen layout fits. A screenshot does not demonstrate that browser Back restores a filter. Choose the evidence that corresponds to the claimed behavior.

## A worked example: a command guide filter

Suppose an AI library has a tool filter, category buttons, and text search. I would define the combined result before implementing any of the controls:

```text
Selecting Codex + Coding agents + /diff shows the Codex guide.
The URL represents all three selections.
Reloading that URL restores the controls and the result.
An impossible combination shows an empty state with a working reset.
Without JavaScript, every guide remains available as an HTML link.
```

I would first try the valid combination, then deliberately select a category that cannot match the tool. After resetting, I would check that all guides return and that the search field receives focus. Finally, I would load the page with JavaScript disabled and open one of the reference articles.

This is a useful test sequence because a control can work alone and still fail in combination. It also exposes the difference between an empty result and a broken page. The empty state should explain the result and provide a next action.

## Ask for review with a target

The [Codex reference](https://learn.chatgpt.com/docs/developer-commands) documents `/diff` and `/review`; [GitHub’s practical guide](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/get-started-with-chat-in-your-ide?tool=vscode) describes Copilot testing prompts. These tools support review, while the acceptance conditions above define what to review.

My final note would say which combinations were checked, what happened without JavaScript, and whether any uncertainty remains. That is more useful than “all done” because it ties completion to repeatable observations. The workflow and examples here are original editorial guidance.

Keep the result with [a short handoff]({{ '/posts/a-useful-ai-handoff/' | relative_url }}) so the next change starts with evidence rather than an assumption.
