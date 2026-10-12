---
layout: post
section: ai
title: "AI workshop: reject stale deployment evidence"
description: "Build a deployment decision in three stages: check identity, reject stale observations, and keep the decision independent of sensitive diagnostics."
category: Code review
tool: codex
surface: Codex CLI
format: Workshop
environments: [web, cli]
level: Intermediate
workshop_id: gate
verified_at: 2026-10-13
illustration: shield
tags: [ai, workshop, kubernetes, secret-contracts, freshness, review]
sources:
  - title: Codex CLI workflows
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

A validation condition is green. A deployment starts. Between those two events, the Secret changes. The old condition still describes a successful check, but it no longer establishes that the current Secret satisfies the current contract. This workshop turns that distinction into a small decision function.

[Open the browser exercise]({{ '/ai/workshops/?exercise=gate#workshop-lab' | relative_url }}) or [download the files]({{ '/assets/labs/ai-workshops.zip' | relative_url }}) and run `node verify.mjs gate`. The starter intentionally trusts a positive condition too early. Eight acceptance tests describe the boundary; the exercise makes no Kubernetes connection.

## First establish identity

The proposed contract contains a namespace, a Secret name, and a positive safe-integer generation. The observation must be available and identify that same namespace and Secret. A missing observation produces `unknown`; evidence about another object produces `wrong-identity`. These are decisions about synthetic inputs, not a specification of a Kubernetes API.

Before editing, write a table with malformed contract, absent observation, wrong namespace, and matching identity. For each row, predict the result and connect it to a failing test. Use the first stage's hints only after you have named the counterexample.

In Codex CLI, you can submit this ordinary task prompt:

```text
Read gate/app.mjs and gate/test.mjs. Do not edit yet.
Explain how a satisfied observation can authorize the wrong object.
Propose a decision table with static reasons and an explicit unknown state.
Then change only gate/app.mjs and run node verify.mjs gate.
Keep the tests and reference solution unchanged.
```

The [official CLI guide](https://learn.chatgpt.com/docs/codex/cli) describes local editing and review workflows; repository instructions are documented in [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md). The prompt above is an original exercise instruction, not a slash command.

## Then establish freshness

Generation compares the observation with the requested contract revision. Resource version compares the observed Secret with the current Secret. Both matter: a Secret can rotate without a contract edit. Missing, old, or mismatched versions produce `stale`, even if the old observation says satisfied.

Work through a timeline: observe version 42, rotate to 43, receive the older successful observation, attempt deployment. The acceptance decision must remain negative until fresh evidence exists. The fixture compares resource-version strings for equality; it does not assign an ordering to Kubernetes resource versions.

## Make the result safe to consume

Return exactly `allowed` and a static `reason`. Raw errors and synthetic token fields must stay outside that output. Preserve both inputs so another caller cannot observe a hidden mutation. After the tests pass, inspect the diff and explain the order of your checks.

The remaining boundary is enforcement. A caller must actually stop deployment when the decision refuses it. This pure function neither implements admission control nor solves the race between checking and using a Secret. Keep that limitation beside your passing result.

Continue with the [deployment-gate chapter]({{ '/books/secret-contract-operator/14-gitops-i-deploy-gate.html' | relative_url }}) and the [secret-contract learning path]({{ '/learn/secret-contracts/' | relative_url }}).
