# Prompt 15 — Durable Command Transport

**Review level:** security-critical

**Read first:** [Chapter 7](../book/chapters/07-asynchronous-api.md) · [Chapter 9](../book/chapters/09-durable-messaging.md)

## Assignment

Implement the outbox-to-JetStream pipeline, command acknowledgement, durable deduplication, active connection epochs, backpressure and operation results. Preserve PostgreSQL intent across broker loss.

## Required evidence and failure cases

Test repeated and reordered messages, stale owners, recipient fencing and crashes after external effects. Expose unknown outcomes when reconciliation cannot establish success.

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
