# Prompt 00 — Repository Assessment and Execution Contract

**Review level:** standard

**Read first:** [Chapter 4](../book/chapters/04-engineering-workspace.md) · [Chapter 26](../book/chapters/26-coding-agents.md)

## Assignment

Inspect the target implementation repository and preserve existing work. Create project scope, architecture decisions, security invariants, testing commands and a truthful execution tracker. Distinguish the application repository from this book repository.

## Required evidence and failure cases

Verify that the documented commands exist or are explicitly planned. Do not mark application features implemented because their documentation exists.

## Execution contract

Work in the separate AgentPlane **implementation repository**, not the book
repository. Read its `AGENTS.md`, current architecture, relevant book chapters and
execution tracker before editing. Inspect the working tree and extend valid
existing work instead of rewriting it blindly.

Preserve tenant boundaries, least privilege and explicit uncertainty. Use current
primary documentation for release-specific APIs. Never introduce fake success,
unchecked production fallbacks, secrets in logs or unverified model/version names.
Do not apply remote infrastructure, publish packages, push commits or deploy
workloads without separate human authorization.

## Completion record

Run the checks available in the current environment and report their exact
commands and outcomes. Add regression tests and documentation for the change.
Update the tracker to completed only when all mandatory criteria are met;
otherwise use partial or blocked with the missing evidence. Report changed files,
remaining risks and the next bounded step. A local commit requires authorization
and must not include unrelated work.
