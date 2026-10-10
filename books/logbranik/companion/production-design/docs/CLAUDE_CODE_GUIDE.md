# Claude Code usage

## Project setup

Launch `claude` from the application repository root. The root `CLAUDE.md` imports the
pack's concise project contract with `@docs/claude-pack/CLAUDE.md`. Keep other project
instructions, and explicitly read AGENTS.md where present. Use `/memory` to inspect loaded
instructions when supported by the installed client. The 60-task export is not an automatic
memory import: read the individual current task to keep context focused.

## Model and effort

The pack does not pin a Claude model or install user settings. Select a model available to
your account. Prompt headers contain project recommendations, not automatic API settings:

| Metadata | Suggested use in this project |
|---|---|
| medium | Bounded documentation, status views and straightforward tooling |
| high | Implementation with meaningful integration and validation work |
| xhigh | Concurrency, signatures, identity boundaries, outages and final review |

Use `/effort` to inspect supported choices, or `/effort high` where that level is available.
Available levels depend on model, client and organization limits. If xhigh is unavailable,
use the highest appropriate supported choice and retain the task's acceptance tests.
Reasoning effort is not a substitute for runtime validation. The tracker only records a
recommendation; Markdown text cannot prove or force a model setting.

## Session continuity

Default: one prompt per implementation run. RUN_PHASE_PROMPT provides an explicit bounded
sequential alternative. Keep state.json as completion metadata and HANDOFF.md as the next
action summary. Write test evidence in the application repository. Before ending a session,
use CHECKPOINT_PROMPT. Use RESUME_PROMPT after interruption or context compaction.

`claude --continue` resumes the latest eligible session in the current directory; session
history still needs to be reconciled with the actual repository state. The plain resume
prompt works when a client session is unavailable. Run `claude --help` for the installed CLI.

## Tool access and truthful results

This package creates files and instructions; it does not authenticate Claude, install its CLI,
grant permissions, start a hidden prompt loop, or deploy infrastructure. A task needing a
missing binary is recorded as blocked until a legitimate installation/alternative resolves it.
If the client is in a mode that cannot edit, distinguish its plan from completed implementation.
Normal client permissions remain in force, and no bypass flags are included.

Official references checked on 2026-10-10 (Europe/Belgrade):

- https://code.claude.com/docs/en/memory — project instructions and imports.
- https://code.claude.com/docs/en/model-config — effort controls and model-dependent support.
- https://code.claude.com/docs/en/cli-reference — launch and continuation commands.

The project workflow, effort assignment and acceptance requirements are this pack's design.
