---
layout: post
title: "A validation result can reveal a secret"
description: "Removing secret values from logs does not stop an untrusted rule author from learning through repeated pass/fail answers."
category: Security
book_id: secret-contract-operator
chapter_slug: 04-bezbednosni-model
illustration: shield
tags: [secrets, kubernetes, authorization, validation, security]
---

A secret validator prints no credentials. Its status contains only a reason code and a Boolean result. That sounds safe until someone can edit the validation rule for a secret they cannot read.

They ask whether the value starts with one prefix, then another. Each pass or fail answers a question about protected data. The output contains no raw value, yet the system has become a query interface to the secret.

## Authorizing a rule authorizes an observation

The important permission is broader than “may create a contract.” It is permission to evaluate particular properties of a particular secret and see the resulting evidence.

For an initial design, limit contract authorship to trusted administrators already authorized for the referenced secret. Keep references within the intended trust boundary and decide which status metadata readers may see.

A namespace restriction helps prevent cross-namespace mistakes. It does not prove that every person inside a shared namespace may inspect every secret there.

## Keep grants outside the request

If less trusted teams need to define contracts, a field such as `approved: true` inside their own object cannot establish authorization. They control the statement that supposedly grants their access.

Use a separately protected grant managed by another role. Bind it to the contract identity, target secret and allowed rule types. If mutation is introduced later, the workload target needs its own authorization too.

Deleting and recreating a contract with the same name should not inherit the old object's authority accidentally. Stable object identity matters whenever an approval outlives one request.

## Revocation changes future reads

Check the grant again during reconciliation. Revoking access must stop new secret reads and new workload changes, rather than merely hiding a button in the interface.

Also consider previously published status. Old validation details can remain informative after access changes. Replace them with the defined access-denied state when the current policy no longer permits their disclosure.

## Test information flow as well as log output

Use synthetic sentinel credentials to check logs, events, traces and parser failures. Then add a separate authorization test: an unauthorized contract must be rejected before the secret reader is called.

Try changing patterns repeatedly and observe which roles receive the answers. Test revoked grants and recreated contracts as distinct cases.

Clean diagnostic output is necessary. A complete review also asks who can choose the questions, which protected data those questions reach, and who can learn from the answers.
