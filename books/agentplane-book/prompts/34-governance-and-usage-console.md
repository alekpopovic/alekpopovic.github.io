# Prompt 34 — Governance and Usage Console

**Review level:** deep

**Read first:** [Chapter 18](../book/chapters/18-approvals.md) · [Chapter 20](../book/chapters/20-metering-budgets.md) · [Chapter 21](../book/chapters/21-observability-audit.md) · [Chapter 22](../book/chapters/22-console-sdks.md)

## Assignment

Build policy editing, effective-policy views, MCP discovery, approvals, secret-reference metadata, budgets and evidence downloads. Avoid secret reveal actions and unsafe optimistic security changes.

## Required evidence and failure cases

Test effective versus requested policy, expired approvals, unmeasured metrics labels, scoped exports and permission changes during a workflow.

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
