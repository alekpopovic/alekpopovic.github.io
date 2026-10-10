# Prompt 38 — Production Helm Design

**Review level:** security-critical

**Read first:** [Chapter 23](../book/chapters/23-deployment-upgrades.md)

## Assignment

Package control and customer components separately with least privilege, resource bounds, probes, network controls and compatible upgrade paths. Use approved external dependency references and migration discipline.

## Required evidence and failure cases

Lint and render charts, validate schemas and run install/upgrade tests in disposable clusters. Never deploy remotely as part of this assignment.

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
