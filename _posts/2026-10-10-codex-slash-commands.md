---
layout: post
section: ai
title: "Codex slash commands: a terminal field guide"
description: "The documented Codex CLI menu, grouped by task, plus a practical plan, inspect, and review loop for a real code change."
category: Coding agents
tool: codex
surface: Codex CLI
format: Command reference
verified_at: 2026-10-10
illustration: package
tags: [ai, codex, slash-commands, cli, review, agents]
sources:
  - title: Codex developer commands
    url: https://learn.chatgpt.com/docs/developer-commands
  - title: Prompting guide
    url: https://learn.chatgpt.com/docs/prompting
---

## Start with the CLI menu

Type `/` inside an interactive Codex CLI session. This is the CLI reference, not the ChatGPT web menu. Features can depend on your installation and account. The [official reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) documents the command set below.

## Complete documented command menu

Grouped for lookup; aliases share a row. Windows sandbox commands are platform-specific, and experimental or account-dependent entries may be absent.

| Area | Commands |
| --- | --- |
| Model | `/model`, `/fast`, `/personality` |
| Planning | `/plan`, `/goal` |
| Approval | `/permissions`, `/approve` |
| Inspection | `/status`, `/usage`, `/debug-config` |
| Editing | `/diff`, `/review`, `/mention` |
| Context | `/compact`, `/ide`, `/memories`, `/init` |
| Sessions | `/new`, `/clear`, `/resume`, `/rename`, `/fork` |
| Side chats | `/side`, `/btw` |
| Session removal | `/archive`, `/delete` |
| Integrations | `/apps`, `/plugins`, `/skills`, `/hooks`, `/mcp`, `/import` |
| Agents | `/agent`, `/subagents` |
| Terminals | `/ps`, `/stop`, `/raw`, `/copy` |
| Presentation | `/keymap`, `/vim`, `/statusline`, `/title`, `/theme`, `/pets`, `/pet` |
| Environment | `/experimental`, `/setup-default-sandbox`, `/sandbox-add-read-dir` |
| Account | `/feedback`, `/logout` |
| Handoff | `/app` |
| Exit | `/exit`, `/quit` |

The source for this October 10, 2026 snapshot is the [built-in slash-command table](https://learn.chatgpt.com/docs/developer-commands?surface=cli). Custom skills and plugins can add entries beyond that table.

## A small change with an observable result

Suppose a search page forgets the selected category after a reload. I would start with a brief that names the current behavior, desired behavior, and boundary:

```text
/plan Make the search category survive reload through a URL parameter.
Inspect the existing search code first.
Keep combined text and category filtering.
An unknown category should fall back to All categories.
Preserve browser back/forward behavior and no-JavaScript navigation.
```

The important part of this brief is the behavior, not its length. It gives the implementation something concrete to demonstrate. An example URL, such as `?category=Security&q=proxy`, makes the acceptance condition easier to discuss than “improve search.”

After implementation, I would use `/diff` to inspect the changed files. I would look for a single source of truth for the selected category, a clear fallback for unknown values, and a URL update that preserves unrelated parameters. Then I would ask for a focused check:

```text
/review Look for regressions in combined filtering and browser navigation.
Pay attention to empty results, unknown categories, and HTML fallback links.
```

I would manually reload a filtered URL, change the filter, and navigate back. A passing test is useful evidence, but the visible URL and result list should also agree. Keep the final change small enough that those observations map directly to the diff.

These prompts are original examples. The [prompting guide](https://learn.chatgpt.com/docs/prompting) provides broader guidance on stating a task and its context.

## Keep the handoff short

A useful closing note says what changed, what was checked, and what remains uncertain. For a longer task, write that note before continuing into a new conversation. See [a useful AI handoff]({{ '/posts/a-useful-ai-handoff/' | relative_url }}) and compare the [Claude Code command menu]({{ '/posts/claude-code-slash-commands/' | relative_url }}).
