# Prompt 25 — Warm Pools and Suspension

**Review level:** deep

**Read first:** [Chapter 11](../book/chapters/11-upstream-adapters.md) · [Chapter 19](../book/chapters/19-workspaces-snapshots.md) · [Chapter 20](../book/chapters/20-metering-budgets.md)

## Assignment

Use supported upstream warm-pool primitives. Verify reset/isolation between claims and distinguish retained files from process checkpointing. Account for idle capacity and local policy ceilings.

## Required evidence and failure cases

Test exhaustion, late claims, suspend/execution races, unsupported resume and credential cleanup. Do not enable KEDA merely because it is available.

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
