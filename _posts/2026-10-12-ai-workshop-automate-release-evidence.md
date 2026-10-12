---
layout: post
section: ai
title: "AI workshop: automate a reproducible release manifest"
description: "Build a deterministic artifact manifest, validate its inputs, and use byte-for-byte checks to evaluate an AI-assisted automation change."
category: Automation
tool: codex
surface: Codex CLI
format: Workshop
verified_at: 2026-10-12
illustration: package
tags: [ai, workshop, codex, automation, releases, reproducibility]
sources:
  - title: Codex CLI
    url: https://learn.chatgpt.com/docs/codex/cli
  - title: Repository instructions with AGENTS.md
    url: https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

Two release jobs describe the same artifacts, but their manifests differ because they enumerate files in different orders and insert the current time. Reviewers now have to separate useful changes from accidental differences. This workshop turns that problem into a small, repeatable automation task.

## Start with explicit artifact evidence

[Download and extract the workshop files]({{ '/assets/labs/ai-workshops.zip' | relative_url }}). Open `automation/app.mjs`, then run:

```sh
node verify.mjs automation
```

The starter intentionally fails. Each input artifact has a basename, a SHA-256 string, and a positive integer byte size. The exercise receives these values; it does not read files or calculate a real artifact hash. The repeated hexadecimal characters in the fixture are synthetic examples, not download verification results.

## Give the automation a deterministic contract

The output has exactly `version: 1` and a `files` array. Each file contains `name`, lowercase `sha256`, and `size`. Sort names using a fixed lexical comparison. Equivalent input orders must produce identical serialized JSON. Do not include timestamps or unknown input fields.

Reject duplicate names, directory paths, invalid hashes, and invalid byte sizes. The exercise accepts basenames of up to 80 characters, beginning with an ASCII letter or digit and continuing with letters, digits, dots, underscores, or hyphens. A narrow naming rule makes this small example easier to reason about; adapt it deliberately if your release system needs a broader contract.

## Ask for a bounded change

In Codex CLI, use this original prompt:

```text
Inspect automation/app.mjs and its tests.
Implement the documented manifest contract in app.mjs only.
Do not add dependencies, timestamps, network calls, or file access.
Reject invalid evidence before producing a manifest.
Run node verify.mjs automation and explain its exit status.
```

After the change, inspect whether the function builds new records instead of retaining arbitrary input objects. Check that sorting does not rearrange the caller's list. Validation should finish by throwing an error for an invalid artifact rather than quietly skipping it and producing a misleading partial release description.

```sh
node verify.mjs automation
node verify.mjs automation --solution
```

The tests cover fixed output fields, stable bytes across input orders, duplicate and path rejection, malformed evidence, and input ownership. Compare the separate worked solution after your own attempt. Save the patch and test output as evidence.

## Connect the result to a real release

In an actual pipeline, collect size and hash from the artifact bytes after the artifact exists. Store the manifest alongside those exact files. Recompute the checksum after downloading, and decide what authenticates the manifest itself. A checksum can detect changed bytes relative to a trusted value; generating JSON alone does not establish who published them.

For a useful extension, write a test that supplies an unknown `internal` field and confirms it is absent from the output. Then design a separate verifier that compares an on-disk file with its manifest record. Keep publication and signing steps outside this workshop until you have an explicit environment and authority for them.

Return to [all workshops]({{ '/ai/workshops/' | relative_url }}) or continue the [AI developer learning path]({{ '/learn/ai-workflows/' | relative_url }}).
