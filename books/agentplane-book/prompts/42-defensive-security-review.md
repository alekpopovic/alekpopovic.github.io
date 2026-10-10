# Prompt 42 — Defensive Security Review

**Review level:** security-critical

**Read first:** [Chapter 3](../book/chapters/03-threat-model.md) · [Chapter 25](../book/chapters/25-verification.md)

## Assignment

Review identity, SQL scope, connector authority, runtime profiles, egress, files, Git, approvals and CI. Map findings to the threat model and add regression tests for fixes.

## Required evidence and failure cases

Prioritize exploitable high-impact gaps. Record residual risk and independent-review status honestly; avoid claiming this assignment is a third-party penetration test.

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
