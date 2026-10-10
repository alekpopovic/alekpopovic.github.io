# Prompt 23 — Controlled Git Operations

**Review level:** security-critical

**Read first:** [Chapter 14](../book/chapters/14-execution-files-git.md) · [Chapter 16](../book/chapters/16-secrets-workload-identity.md)

## Assignment

Implement approved Git schemes, host-key verification, credential references and explicit network policy. Disable hooks and recursive submodules by default. Treat push as a separately authorized effect.

## Required evidence and failure cases

Test SSRF destinations, unsafe protocols, credential leaks in arguments/configuration, hooks, redirects and subprocess cancellation.

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
