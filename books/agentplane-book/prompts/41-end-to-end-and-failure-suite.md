# Prompt 41 — End-to-End and Failure Suite

**Review level:** deep

**Read first:** [Chapter 25](../book/chapters/25-verification.md) · [Chapter 27](../book/chapters/27-capstone.md)

## Assignment

Build a local two-tenant vertical-slice test with enrollment, execution, policy denial, approval, metering and cleanup. Inject failures before and after durable boundaries.

## Required evidence and failure cases

Record actual commands and environment. Include stale epochs, broker restart, disconnected termination and ambiguous effects; do not invent benchmark results.

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
