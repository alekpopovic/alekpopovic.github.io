# Prompt 13 — PKI Rotation and Revocation

**Review level:** security-critical

**Read first:** [Chapter 8](../book/chapters/08-connector-pki.md) · [Chapter 24](../book/chapters/24-reliability-recovery.md)

## Assignment

Implement local key generation, CSR validation, URI identity binding, external signer integration and short-lived certificate rotation. Reject development signers in production mode.

## Required evidence and failure cases

Test proof of possession, CSR identity substitution, expiry, serial revocation, credential overlap and restoration from stale revocation state.

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
