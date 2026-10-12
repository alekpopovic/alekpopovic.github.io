---
layout: post
section: ai
last_modified_at: 2026-10-12
title: "GitHub Copilot slash commands in VS Code"
description: "The commands in GitHub’s VS Code cheat sheet, practical prompts for fixing code and writing tests, and how to check commands supplied by extensions."
category: IDE workflows
tool: copilot
surface: GitHub Copilot Chat in VS Code
format: Command reference
environments: [ide]
level: Beginner
verified_at: 2026-10-10
illustration: shield
tags: [ai, copilot, github, vscode, slash-commands, testing]
sources:
  - title: GitHub Copilot Chat cheat sheet
    url: https://docs.github.com/en/copilot/reference/chat-cheat-sheet?tool=vscode
  - title: Copilot Chat practical examples
    url: https://docs.github.com/en/copilot/how-tos/chat-with-copilot/get-started-with-chat-in-your-ide?tool=vscode
  - title: VS Code AI features
    url: https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet
---

## Check the active editor

Type `/` in Copilot Chat to inspect the commands available in your VS Code installation. GitHub documents different menus for different IDEs. Extensions and saved prompts can add commands, so a web list cannot enumerate every locally installed shortcut. The [GitHub cheat sheet](https://docs.github.com/en/copilot/reference/chat-cheat-sheet?tool=vscode) is explicit about this variation.

## Commands in GitHub’s VS Code cheat sheet

| Command | Use |
| --- | --- |
| `/clear` | New conversation |
| `/explain` | Explain code |
| `/fix` | Suggest correction |
| `/fixTestFailure` | Investigate failure |
| `/help` | Discover features |
| `/new` | Scaffold project |
| `/tests` | Generate tests |

This is every command listed in the [VS Code version of GitHub’s cheat sheet](https://docs.github.com/en/copilot/reference/chat-cheat-sheet?tool=vscode), checked on October 10, 2026; the document describes common commands, not an exhaustive extension catalog. The [VS Code feature reference](https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet) also describes saved prompt files invoked with slash commands.

## Use a command with a concrete example

Suppose a function normalizes email addresses before a lookup. It trims whitespace and lowercases text, but crashes when given `null`. I would select the function and ask:

```text
/explain Walk through this function with " User@Example.com ", "", and null.
Show the return value or exception for each input.
```

Before asking for a fix, I would decide what the application should do with missing input. Returning an empty string, rejecting the request, and skipping the lookup are different product behaviors. The tool should not choose among them accidentally because one implementation is shorter.

Once the intended behavior is clear, I would request a bounded edit:

```text
/fix Reject missing input with the existing validation error type.
Keep valid-address normalization unchanged.
Do not change the caller’s error handling.
```

Then I would ask for tests that express behavior, rather than tests that repeat the implementation:

```text
/tests Cover whitespace, mixed case, empty input, and null.
Use the repository’s existing test framework and naming style.
Check the public function’s output or error, not private helpers.
```

I would review the expected values before running the tests. A generated test can agree perfectly with the same mistaken assumption as the generated code. Adding a boundary case that you chose independently gives the review another source of evidence. These prompts and the normalization scenario are original examples; GitHub’s [practical guide](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/get-started-with-chat-in-your-ide?tool=vscode) documents the relevant command behavior.

## Commands, participants, and context

The `/` menu is separate from `@` participants and `#` context references. Use the editor’s suggestions to see which are supported rather than pasting syntax from another IDE. Review [GitHub’s reference](https://docs.github.com/en/copilot/reference/chat-cheat-sheet?tool=vscode) when moving between environments.

For another editor-oriented tool, read [Cursor’s command guide]({{ '/posts/cursor-slash-commands/' | relative_url }}). For the acceptance checklist behind these examples, see [the verification loop]({{ '/posts/ai-changes-need-a-verification-loop/' | relative_url }}).
