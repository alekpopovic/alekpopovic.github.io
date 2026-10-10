# Prompt 03 — Disposable Development Environment

**Review level:** standard

**Read first:** [Chapter 4](../book/chapters/04-engineering-workspace.md) · [Chapter 25](../book/chapters/25-verification.md)

## Assignment

Create repeatable local PostgreSQL, JetStream and object-storage dependencies and an explicitly named local Kubernetes profile. Install only reviewed upstream releases in a disposable cluster after local authorization.

## Required evidence and failure cases

Use explicit contexts, bounded waits and local-only ports. Detect absent CNI, runtime and snapshot capabilities instead of silently inventing them.

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
