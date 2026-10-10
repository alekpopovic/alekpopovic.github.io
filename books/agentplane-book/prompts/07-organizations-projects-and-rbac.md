# Prompt 07 — Organizations Projects and RBAC

**Review level:** security-critical

**Read first:** [Chapter 5](../book/chapters/05-tenant-data.md) · [Chapter 6](../book/chapters/06-identity.md)

## Assignment

Implement organizations, project scope, invitations and a centralized deny-by-default permission service. Define ownership transfer, last-owner rules, service delegation and granular sensitive operations.

## Required evidence and failure cases

Test cross-tenant resources, role escalation, mixed-scope batches, expired invitations and background-job authorization.

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
