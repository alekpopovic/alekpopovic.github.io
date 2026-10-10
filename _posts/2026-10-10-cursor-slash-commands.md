---
layout: post
section: ai
title: "Cursor slash commands: ask, plan, and inspect"
description: "A complete snapshot of the documented Cursor CLI command families, including aliases, with a small workflow for investigating a UI bug."
category: IDE workflows
tool: cursor
surface: Cursor CLI; editor commands differ
format: Command reference
verified_at: 2026-10-10
illustration: queue
tags: [ai, cursor, slash-commands, cli, editor, debugging]
sources:
  - title: Cursor CLI slash commands
    url: https://cursor.com/docs/cli/reference/slash-commands
  - title: Cursor CLI overview
    url: https://cursor.com/docs/cli/overview
---

## Name the surface

This guide covers Cursor CLI. The editor and its custom commands are a different surface. Consult the [official CLI menu](https://cursor.com/docs/cli/reference/slash-commands) or `/help` for the installed version. Some entries depend on account features or rollout.

## Complete documented CLI menu

| Area | Commands |
| --- | --- |
| Model | `/model`, `/max-mode` |
| Modes | `/plan`, `/ask`, `/debug`, `/goal` |
| Execution | `/run-everything`, `/auto-run`, `/sandbox`, `/shell`, `/sh`, `/run` |
| Sessions | `/clear`, `/new`, `/new-chat`, `/newchat`, `/resume`, `/fork`, `/rename`, `/rewind` |
| Context | `/summarize`, `/compress` |
| Presentation | `/vim`, `/line-numbers`, `/show-thinking`, `/status-indicators` |
| Configuration | `/config`, `/setup-terminal`, `/bedrock` |
| Integrations | `/mcp`, `/plugin` |
| Navigation | `/open`, `/cursor` |
| Clipboard | `/copy`, `/copy-request-id`, `/copy-conversation-id` |
| Diagnostics | `/about`, `/logs`, `/feedback`, `/help` |
| Maintenance | `/update`, `/logout`, `/quit`, `/exit` |

Arguments include `/model [filter]`, `/plan [prompt]`, `/debug [prompt]`, `/goal [objective]`, `/help [command]`, and `/shell [command]`. `/run-everything` accepts `on`, `off`, or `status`. For MCP, the reference lists `list` and `list-tools`; `/plugin` and `/bedrock` have their own subcommands. This snapshot was checked on October 10, 2026 against [Cursor’s reference](https://cursor.com/docs/cli/reference/slash-commands).

## Investigate a UI bug before editing

Suppose a modal closes whenever someone clicks inside it. I would first ask a read-only question:

```text
/ask Trace the modal’s click handlers and show why a click inside the dialog
reaches the backdrop handler. Name the component and event path.
Do not edit the code yet.
```

The useful result is a concrete event path: the target element, its container, and the backdrop listener. “Event bubbling” is a diagnosis category, not enough evidence by itself. I would ask for the exact handler condition and compare it with a click on a button inside the modal.

My next brief would name three observable outcomes: clicking the backdrop closes the modal, clicking within the dialog keeps it open, and pressing Escape still closes it. I would also include one keyboard path: tab to an action in the dialog, activate it, then confirm where focus moves when the modal closes.

After the edit, I would reproduce those paths in the browser at a narrow width. A targeted test can check the handler, while the browser check reveals whether another element covers the backdrop or whether focus escapes into the page behind it. I would describe both observations in the result rather than saying only “fixed the modal.”

These are original investigation prompts. The [CLI overview](https://cursor.com/docs/cli/overview) explains the terminal’s interaction model; it does not make this modal scenario a built-in workflow.

## Treat speed settings as a separate decision

An execution setting should follow a clear task boundary. Before broad changes, write down which files and outcomes belong to the task. A small diff and an observable acceptance condition make a change easier to review than an unrestricted instruction to “clean everything up.”

Continue with [GitHub Copilot in VS Code]({{ '/posts/github-copilot-slash-commands/' | relative_url }}) or the [verification loop]({{ '/posts/ai-changes-need-a-verification-loop/' | relative_url }}).
