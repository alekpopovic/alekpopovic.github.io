---
layout: post
title: "A valid signature is only the first gate"
description: "Authenticating a policy's bytes does not make every authenticated policy appropriate for the receiving agent."
category: Security
book_id: logbranik
chapter_slug: 11-sign-the-policy
illustration: shield
tags: [signed policy, Ed25519, validation, keys, authorization]
---

An edge agent receives a correctly signed policy. The signature verifies. Should the agent replace its live configuration immediately?

Only if cryptographic authenticity were the whole contract. The policy can still belong to another agent, contain an unsupported version, exceed capacity limits, or conflict with a revision already applied.

## Authenticate the bytes you received

The book's laboratory signs a fixed domain separator followed by the exact payload bytes. The receiver verifies that same byte sequence under a provisioned public key.

Parsing JSON and serializing it again before verification changes the message. Whitespace or key ordering can differ even when the resulting object looks equivalent. Deterministic generation is useful for fixtures, but it is not permission for the receiver to rewrite an incoming signed payload.

The verification key must also come from provisioning. A policy that brings its own trusted key would let the sender choose both the claim and the authority for that claim.

## Validate the policy after verification

Once authenticity is established, check the version, intended agent, provisioned epoch, revision, timing fields, authorized sites, modes, address syntax, and decision limits.

Reject ambiguous encodings and unknown fields under the defined schema. Bound the received bytes before parsing and the collections before constructing a live view. These checks constrain what even an authenticated sender can ask the agent to do.

A compromised signing key makes this distinction particularly clear. Signature verification can succeed while the receiver still rejects a policy that violates its independent lifetime or scope rules.

## Treat transport and policy as separate contracts

Mutual TLS authenticates connection peers and protects data in transit. A policy signature authenticates the policy independently of that connection.

The endpoint still needs to decide which peer may deliver updates. The agent still needs to decide which signed policy is valid for its state. Neither mechanism removes the other's job.

Key rotation crosses both saved and live state. Provision a new verification key before using it, confirm the intended agents accept it, and plan how saved policies will remain verifiable through restart and retirement of the old key.

## Test a valid message you should refuse

Keep a fixture with a valid signature but the wrong agent identity. Add another with an already-applied revision and changed content.

The expected outcome is rejection at the appropriate validation or ordering gate. Testing only corrupted signatures would miss the most useful lesson: authentic data still needs a precise policy contract.
