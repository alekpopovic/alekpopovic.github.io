# Preface: A Platform Is a Set of Boundaries

An AI agent that only returns text is a different engineering problem from an
agent that can execute a program, inspect a repository and use a production API.
The second system must decide not only what the model says, but what software is
allowed to do after the model has said it. That decision belongs in infrastructure
and authorization systems, not in a reassuring system prompt.

This book develops **AgentPlane**, a reference architecture for operating and
governing agent execution in customer-owned Kubernetes clusters. It connects Go
services, PostgreSQL, an outbound connector, Kubernetes controllers and a web
console into a coherent design. Existing runtimes and gateways provide the
low-level machinery; the platform supplies tenant boundaries, lifecycle intent,
policy decisions and evidence.

The intended reader can already build a container, read a Kubernetes manifest
and write ordinary application code. You do not need prior experience with AI
training, GPU kernels or language-model research. You do need a willingness to
reason about retries, uncertain outcomes and security properties that are not
visible in a successful demo.

## Three kinds of material

**Design** means a proposed AgentPlane contract or architecture. It is not a
statement that this repository contains a working implementation.

**Teaching example** means an included, deliberately limited program that
illustrates an invariant. Its local test results are recorded in the validation
report. Passing those tests does not establish deployment security.

**Integration exercise** means work that requires a real database, cluster,
identity provider or cloud account. The book supplies a procedure and acceptance
criteria; a procedure is not an executed result.

This distinction applies even when a chapter uses confident imperative language.
“Reject a stale command” is a requirement for the application you build, not a
claim that every possible execution environment already rejects it.

## How to read

Read Chapters 1–4 before implementing anything. Chapters 5–11 establish the
control plane and its connection to Kubernetes. Chapters 12–21 examine execution,
networking, tool governance, storage and evidence. Chapters 22–25 address product
interfaces and operations. Chapters 26–28 show how to use coding agents, complete
a capstone and maintain an open publication.

Use the labs to turn claims into observations. Use the prompt pack as a sequence
of bounded implementation assignments, not as an unattended deployment script.
The same assignments can guide a human developer or another coding assistant.
Repository instructions never replace the assistant's actual permission model.

## The edition's promise

The promise is a useful, reviewable engineering book. It is not guaranteed
production readiness after a fixed number of prompts. The most important
outcomes are explicit trust assumptions, testable invariants and an honest record
of what has and has not been validated.

Start with the [table of contents](index.md), or run the offline checks described
in the [repository README](../README.md). The book is intentionally readable as
plain Markdown on GitHub and as a self-contained website.
