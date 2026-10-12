---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "ChatGPT slash commands: know your composer"
description: "A complete snapshot of the documented desktop command menu, with a clear distinction between ChatGPT web, desktop actions, and custom shortcuts."
category: Chat assistants
tool: chatgpt
surface: ChatGPT desktop; web menu varies
format: Command reference
environments: [desktop]
level: Beginner
verified_at: 2026-10-10
illustration: network
tags: [ai, chatgpt, slash-commands, desktop, prompting]
sources:
  - title: ChatGPT app slash commands
    url: https://learn.chatgpt.com/docs/reference/slash-commands
  - title: Developer commands and web scope
    url: https://learn.chatgpt.com/docs/developer-commands
  - title: Prompting guide
    url: https://learn.chatgpt.com/docs/prompting
---

## First, check which ChatGPT you are using

Type `/` in the composer. ChatGPT web has its own action menu; the desktop command list below is not a promise that these commands exist in your browser. The [official developer reference](https://learn.chatgpt.com/docs/developer-commands) explicitly separates the two surfaces. Availability also depends on your account and environment.

## Desktop command reference

This snapshot covers every named command in the [official app reference](https://learn.chatgpt.com/docs/reference/slash-commands), checked on October 10, 2026.

| Command | Purpose |
| --- | --- |
| `/approve` | Retry approval |
| `/archive` | Archive chat |
| `/chat` | Unassigned chat |
| `/cloud` | Cloud execution |
| `/cloud-environment` | Cloud environment |
| `/compact` | Condense context |
| `/fast` | Fast tier |
| `/feedback` | Product feedback |
| `/fork` | Branch chat |
| `/goal` | Persistent objective |
| `/ide-context` | Editor context |
| `/init` | Project instructions |
| `/local` | Local execution |
| `/mcp` | Server status |
| `/memories` | Memory settings |
| `/model` | Model picker |
| `/new` | Blank chat |
| `/pet` | Desktop companion |
| `/pin` | Pin chat |
| `/plan` | Planning mode |
| `/project` | Project picker |
| `/reasoning` | Reasoning effort |
| `/rename` | Chat name |
| `/review` | Code review |
| `/side` | Side conversation |
| `/status` | Session information |
| `/usage` | Account usage |
| `/worktree` | Isolated workspace |

## Turn a vague task into a useful brief

Imagine you need to turn interview notes into a release announcement. Before choosing any action, write the result you want to receive:

```text
Draft a release announcement from the attached interview notes.
Audience: existing customers who use the reporting dashboard.
Length: 180–220 words.
Include: what changed, the first action to try, and known limitations.
Do not invent dates, customer quotations, or performance numbers.
Mark anything that needs confirmation as [CHECK].
```

For this task, I would ask for an outline before the draft. I would also keep a short list of unresolved facts next to the conversation. A polished paragraph cannot tell you whether the underlying release date is correct; that needs a separate check against the release owner’s information.

After the first draft, ask for one specific revision: shorten the opening, explain a technical term, or make the call to action clearer. Changing five things at once makes it harder to decide which change improved the result. Save the final brief with the draft so the next announcement starts from a repeatable process.

The [official prompting guide](https://learn.chatgpt.com/docs/prompting) is the reference for expressing intent and supplying useful context. The brief above is an original worked example, not a built-in command.

## Custom shortcuts are a separate layer

Enabled skills and `/prompts:<name>` entries can extend the desktop menu. Your own shortcut is not automatically available to another person. Share the underlying instructions and name the required setup when documenting a team workflow. The [app reference](https://learn.chatgpt.com/docs/reference/slash-commands) describes these menu extensions.

For terminal-specific controls, continue with the [Codex CLI reference]({{ '/posts/codex-slash-commands/' | relative_url }}). For a method that travels between tools, read [a useful AI handoff]({{ '/posts/a-useful-ai-handoff/' | relative_url }}).
