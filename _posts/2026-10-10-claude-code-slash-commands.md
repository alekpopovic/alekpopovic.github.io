---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "Claude Code slash commands: the command map"
description: "Navigate Claude Code’s documented commands, aliases, bundled skills, and retired entries without confusing the terminal with Claude web chat."
category: Coding agents
tool: claude
surface: Claude Code CLI
format: Command reference
environments: [cli]
level: Beginner
verified_at: 2026-10-10
illustration: network
tags: [ai, claude, claude-code, slash-commands, context, skills]
sources:
  - title: Claude Code commands
    url: https://code.claude.com/docs/en/commands
  - title: Skills and custom commands
    url: https://code.claude.com/docs/en/skills
  - title: Interactive mode
    url: https://code.claude.com/docs/en/interactive-mode
---

## Scope matters

This is Claude Code CLI, not claude.ai chat. Type `/` or use `/help` to inspect your installation. The [official command reference](https://code.claude.com/docs/en/commands) includes conditional features, bundled skills, aliases, and retired entries.

## The documented command map

Compact labels group the full reference snapshot checked on October 10, 2026. Check the linked reference for arguments and version requirements.

| Area | Commands |
| --- | --- |
| Workspace | `/add-dir`, `/cd`, `/init`, `/memory`, `/import` |
| Reasoning | `/advisor`, `/model`, `/effort`, `/fast`, `/plan`, `/goal` |
| Context | `/context`, `/compact`, `/autocompact`, `/recap` |
| Sessions | `/clear`, `/branch`, `/fork`, `/background`, `/resume`, `/rename`, `/rewind`, `/btw` |
| Review | `/diff`, `/code-review`, `/review`, `/ultrareview`, `/security-review`, `/simplify` |
| Running | `/run`, `/verify`, `/run-skill-generator`, `/autofix-pr` |
| Agents | `/agents`, `/list-agents`, `/subtask`, `/tasks`, `/stop`, `/batch` |
| Automation | `/loop`, `/schedule`, `/workflows`, `/workflow-authoring` |
| Extensions | `/skills`, `/skill-doctor`, `/reload-skills`, `/mcp`, `/ide`, `/plugin`, `/plugin-authoring`, `/reload-plugins`, `/hooks` |
| Permissions | `/permissions`, `/sandbox`, `/auto-mode-setup`, `/fewer-permission-prompts` |
| Artifacts | `/artifacts`, `/artifact-capabilities`, `/artifact-diagramming`, `/design`, `/design-login`, `/design-sync`, `/dataviz`, `/slides` |
| Browser | `/chrome`, `/claude-in-chrome`, `/deep-research` |
| Diagnostics | `/doctor`, `/debug`, `/heapdump`, `/insights`, `/status` |
| Preferences | `/config`, `/update-config`, `/output-style`, `/keybindings`, `/color`, `/focus`, `/scroll-speed`, `/statusline`, `/terminal-setup`, `/theme`, `/tui`, `/voice` |
| Remote | `/desktop`, `/mobile`, `/remote-control`, `/remote-env`, `/teleport` |
| Setup | `/install-github-app`, `/install-slack-app`, `/setup-bedrock`, `/setup-vertex`, `/web-setup`, `/team-onboarding` |
| Usage | `/usage`, `/cost`, `/stats`, `/usage-credits`, `/rate-limit-options`, `/upgrade`, `/passes` |
| Utilities | `/copy`, `/export`, `/help`, `/bug`, `/feedback`, `/login`, `/logout`, `/privacy-settings`, `/release-notes`, `/powerup`, `/radio`, `/stickers`, `/exit` |
| Retired | `/pr-comments`, `/vim`, `/ultraplan` |

Common aliases include `/bg`, `/new`, `/reset`, `/settings`, `/app`, `/checkup`, `/quit`, `/peers`, `/proactive`, `/allowed-tools`, `/rc`, `/continue`, `/routines`, `/tp`, `/ios`, and `/android`. The [command reference](https://code.claude.com/docs/en/commands) identifies their targets; do not treat retired commands as current instructions.

## Built-in actions and skills

Claude Code distinguishes fixed commands from prompt-based skills. For example, `/batch`, `/debug`, `/loop`, `/doctor`, `/code-review`, and `/claude-api` are documented bundled skills. `/claude-api` belongs to the command map too; its available arguments depend on the task. Custom skill and MCP prompt names can extend the menu. Read the [skills documentation](https://code.claude.com/docs/en/skills) for that separate mechanism.

## Work through one failing behavior

Consider an API endpoint that occasionally accepts the same payment notification twice. My first prompt would describe evidence rather than prescribe a patch:

```text
Trace how this endpoint identifies duplicate notifications.
Show the database constraint, the transaction boundary, and the response path.
Do not change code yet.
Use the two attached request IDs as examples.
```

I would write down three facts from the investigation: where the notification identity comes from, whether persistence has a uniqueness guarantee, and what happens when the same request arrives while another transaction is still open. If one fact is missing, I would investigate that gap before discussing a solution.

Next, I would ask for the smallest change that makes duplicate acceptance observable in a test. The test should exercise two attempts with the same identity and explain the expected response for each. A helper function called “deduplicate” is not evidence that concurrent requests are safe.

Before accepting the implementation, I would inspect the diff and run the scenario against the real database behavior used by the project. Finally, I would save the test command and expected result in the change description. This is an original debugging workflow; it does not require a particular model or an undocumented slash command.

Compare the [Codex reference]({{ '/posts/codex-slash-commands/' | relative_url }}) or continue with [a practical verification loop]({{ '/posts/ai-changes-need-a-verification-loop/' | relative_url }}).
