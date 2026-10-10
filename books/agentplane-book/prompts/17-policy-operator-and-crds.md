# Prompt 17 — Policy Operator and CRDs

**Review level:** deep

**Read first:** [Chapter 10](../book/chapters/10-reconciliation.md)

## Assignment

Build AgentPlane-specific intent CRDs and idempotent reconciliation. Use conditions and observed generation, explicit namespace bounds and safe ownership checks. Do not duplicate upstream Sandbox resources.

## Required evidence and failure cases

Use envtest for reconciliation, validation, finalizers and status. Treat watches and list permissions as data-access decisions.

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
