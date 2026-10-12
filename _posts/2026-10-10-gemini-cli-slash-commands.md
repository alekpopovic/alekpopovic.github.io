---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "Gemini CLI slash commands: context, tools, and sessions"
description: "The documented Gemini CLI command families and their subcommands, with a practical way to inspect project context before changing code."
category: Coding agents
tool: gemini
surface: Gemini CLI
format: Command reference
environments: [cli]
level: Beginner
verified_at: 2026-10-10
illustration: logs
tags: [ai, gemini, gemini-cli, slash-commands, memory, mcp]
sources:
  - title: Gemini CLI command reference
    url: https://geminicli.com/docs/reference/commands/
  - title: Custom commands
    url: https://geminicli.com/docs/cli/custom-commands/
  - title: Project context files
    url: https://geminicli.com/docs/cli/gemini-md/
---

## Use the terminal reference

These commands belong to Gemini CLI, not the Gemini browser app. `/help` shows your installed menu. The [official CLI reference](https://geminicli.com/docs/reference/commands/) is the source for this October 10, 2026 snapshot; configuration and extensions affect availability.

## All documented command families

| Area | Commands |
| --- | --- |
| Session | `/clear`, `/compress`, `/copy`, `/resume`, `/chat`, `/rewind`, `/restore` |
| Context | `/init`, `/memory`, `/directory`, `/dir` |
| Configuration | `/auth`, `/model`, `/settings`, `/permissions`, `/policies`, `/privacy` |
| Extensions | `/agents`, `/commands`, `/extensions`, `/skills`, `/hooks`, `/mcp`, `/ide`, `/tools` |
| Planning | `/plan` |
| Terminal | `/shells`, `/bashes`, `/editor`, `/terminal-setup`, `/theme`, `/vim` |
| Information | `/about`, `/help`, `/?`, `/docs`, `/stats`, `/bug`, `/upgrade` |
| Integration | `/setup-github` |
| Exit | `/quit`, `/exit` |

### Documented subcommands

| Family | Subcommands |
| --- | --- |
| `/agents` | `list`, `reload` / `refresh`, `enable`, `disable`, `config` |
| `/commands` | `list`, `reload` |
| `/directory` | `add`, `show` |
| `/extensions` | `config`, `disable`, `enable`, `explore`, `install`, `link`, `list`, `restart`, `uninstall`, `update` |
| `/hooks` | `disable-all`, `disable`, `enable-all`, `enable`, `list` / `show` / `panel` |
| `/ide` | `disable`, `enable`, `install`, `status` |
| `/mcp` | `auth`, `desc`, `disable`, `enable`, `list` / `ls`, `reload`, `schema` |
| `/memory` | `list`, `refresh`, `show` |
| `/model` | `manage`, `set` |
| `/permissions` | `trust` |
| `/plan` | `copy` |
| `/policies` | `list` |
| `/resume`, `/chat` | `list`, `save`, `resume` / `load`, `delete`, `share`, `debug` |
| `/skills` | `disable`, `enable`, `list`, `reload` |
| `/stats` | `session`, `model`, `tools` |
| `/tools` | `desc` / `descriptions`, `nodesc` / `nodescriptions` |

Refer to the [command reference](https://geminicli.com/docs/reference/commands/) for argument syntax and conditional entries, including nightly diagnostics and checkpoint-dependent restoration.

## Inspect context before a migration

Imagine a repository containing a public API and a legacy worker. Both use a shared model, but only one can be upgraded this week. I would start by making a small migration brief:

```text
The API can change in this task; the legacy worker must keep its interface.
Find all uses of the shared model and identify the worker-facing contract.
Propose a migration in two deployable steps.
For each step, explain which old and new versions can run together.
```

Before asking for changes, I would inspect the loaded instructions with `/memory show`. An instruction written for an older migration can be more misleading than having no instruction at all. I would compare what is loaded with the current brief and edit the repository instructions if they conflict. The [GEMINI.md guide](https://geminicli.com/docs/cli/gemini-md/) explains how those project instructions are discovered.

Then I would record the compatibility matrix as a four-cell table: old API with old worker, new API with old worker, old API with new worker, and new API with new worker. Any unsupported combination needs an explicit deployment condition. This exercise often reveals a missing transition step before a line of migration code is written.

The brief and compatibility exercise are original examples. They are useful regardless of which coding agent performs the change.

## Add your own command deliberately

Gemini CLI supports TOML command files. A project file such as `.gemini/commands/check-migration.toml` can provide a team shortcut; it is a custom command, not an entry installed for every user. The [custom-command guide](https://geminicli.com/docs/cli/custom-commands/) covers naming and reload behavior.

Compare [Cursor’s CLI menu]({{ '/posts/cursor-slash-commands/' | relative_url }}) and read [a useful AI handoff]({{ '/posts/a-useful-ai-handoff/' | relative_url }}) before passing a migration between tools.
