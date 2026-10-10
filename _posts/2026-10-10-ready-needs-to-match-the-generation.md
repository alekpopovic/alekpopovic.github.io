---
layout: post
title: "Ready needs to match the generation"
description: "A deployment gate must distinguish a current validation result from a positive condition left by an earlier specification."
category: Delivery
book_id: secret-contract-operator
chapter_slug: 14-gitops-i-deploy-gate
illustration: package
tags: [gitops, deployment, kubernetes, conditions, validation]
---

A pipeline changes a SecretContract and waits for `Ready=True`. The wait returns immediately, so the pipeline deploys the application. A moment later, the controller reports that the new specification is invalid.

The positive condition belonged to the previous generation. Waiting for a Boolean did not establish which request had been evaluated.

## Capture the object you intend to validate

After applying the contract, record its UID and expected generation. A useful gate checks that the object still has that identity and specification generation, then checks both the overall observed generation and the generation attached to the Ready condition.

If the object is replaced or its specification changes again, the gate should stop treating it as the original request. Reusing a name is not the same as preserving the object's identity.

This gives a precise success statement: the controller reported Ready for this version of this contract. It does not establish an application-level connection to the credential provider.

## Bootstrap without a circular dependency

A contract that validates a running workload cannot become Ready before that workload exists. Requiring full workload readiness before the very first deployment creates a circular gate.

Separate preflight checks on the Secret from later checks on the consumer. Validate the preflight contract for its expected generation, deploy the workload, then verify its configuration references and rollout.

Keep the phases visible in pipeline output so a failure identifies whether the data contract, consumer wiring or application startup needs attention.

## Admit the remaining time gap

Even a generation-aware gate is an observation made before use. A Secret can change after validation and before a new pod reads it.

Define the gate's guarantee accordingly. Stronger handovers may require versioned inputs or a separately designed admission mechanism. A status object alone does not cause Kubernetes to reject an unrelated Deployment.

Do not treat an unimplemented admission design as an existing enforcement layer. The book's read-only contract workflow is a proposed validation boundary, with later enforcement work requiring its own implementation and tests.

## Make failure output safe and useful

Use a bounded deadline and report the reason for failure without dumping Secret objects or entire diagnostic payloads. Repeated API errors must eventually produce a clear failure, rather than an indefinite wait.

Test stale Ready, a changed generation, a recreated contract and controller unavailability. A successful test should show that old positive evidence cannot authorize the new deployment, while a current, correctly identified result can advance the intended phase.
