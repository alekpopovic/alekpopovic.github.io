# Prompt 01 — Architecture and Threat Model

**Review level:** security-critical

**Read first:** [Chapter 1](../book/chapters/01-product-boundary.md) · [Chapter 2](../book/chapters/02-architecture.md) · [Chapter 3](../book/chapters/03-threat-model.md)

## Assignment

Design control and execution planes, data classifications and customer-owned policy bounds. Include compromised control-plane authority, hostile workloads, stream exposure, replay, restore and malicious cluster administrators.

## Required evidence and failure cases

For every threat, identify an enforcement point and adversarial test. Show that outbound-only connectivity does not remove remote execution authority.

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
