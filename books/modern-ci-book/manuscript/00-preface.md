# Preface

A CI/CD system is easy to demonstrate and difficult to trust. Starting a command is a small part of the job. The platform must know which source revision it is running, who authorized the work, where credentials may be used, whether a disconnected worker is still changing a target, and which result belongs to the current attempt. A useful interface makes these distinctions visible instead of compressing them into a green or red badge.

This book develops an original, self-hosted-first platform named **Modern CI**. The target is not a cosmetic wrapper around Jenkins. It has its own control plane, scheduler, runner protocol, pipeline compiler, web application, and command-line client. Nor does it promise compatibility with every historical plugin or dynamic pipeline program. The intended first release serves teams with trusted repositories and dedicated Linux runners. Its scope is to build, test, publish artifacts, and coordinate controlled deployments without requiring Kubernetes.

The architecture uses Go for the server, scheduler, runner, and CLI; Angular with Tailwind for the browser; PostgreSQL for durable state; Docker and BuildKit for execution and image construction; and local or S3-compatible storage for binary objects. Each application has its own repository. Shared domain libraries and wire contracts have two additional repositories. A superproject pins the combination that has been tested together.

## A book, a laboratory, and a product design

These are three different deliverables. The manuscript explains the engineering decisions. The companion laboratory contains small, runnable Go examples for graph compilation, attempt fencing, idempotent results, webhook signatures, bounded log segments, and approval identity. The production design describes the additional persistence, identity, infrastructure, and operational work required to turn those ideas into a platform.

The laboratory is deliberately in memory. It does not start containers, provide a production API, connect to PostgreSQL, or implement an Angular application. SQL and pipeline files are separate teaching examples. Their presence is not evidence of a deployed product. The verification directory records which checks were actually executed for this edition. Production claims require the acceptance gates described later in the book.

## Intended reader

You should be comfortable reading Go, SQL, HTTP requests, and shell commands. Experience maintaining build servers will make the failure scenarios familiar. The text explains the domain rather than teaching Go or Angular from the beginning. Chapters about privileges assume that you control the systems being configured. Use disposable infrastructure for experiments and do not give the laboratory production credentials.

Read Chapters 1–4 to understand the boundaries, then run Chapter 5. Chapters 6–10 establish identity, compilation, transactions, and ownership. Chapters 11–17 turn those records into controlled execution. Chapters 18–21 cover deployment and operator interfaces. Chapters 22–24 explain operations, upgrades, and release management. The appendices provide a laboratory runbook, an eighty-work-item implementation map, acceptance gates, a glossary, and primary references.

## How examples are labeled

A **laboratory command** runs the included Go module. A **design example** explains an interface or schema that a complete implementation must build. An **operator procedure** describes actions to adapt and review on a deployment you own. Example repository names and resource identifiers are not evidence that those resources already exist.

The source files under `manuscript/` are the canonical edition. The website, PDF, EPUB, and reading sample are built from those files. Corrections should be made there, accompanied by a test or a reproducible explanation when behavior changes. The book repository is independent of the eight application/workspace repositories described in Chapter 3. Reading the book does not require cloning them.

## Open licenses and attribution

Copyright (c) 2026 Aleksandar Popovic. Original prose, exercises, answers, and original publication styling are offered under Creative Commons Attribution 4.0 International. Original code, snippets, scripts, and configuration examples are offered under the MIT License. The repository contains the licensing map and MIT notice. Third-party dependencies keep their own licenses. The Creative Commons license permits sharing and adaptation with its attribution conditions; the MIT notice governs reuse of the code. [S23](e-sources.md#s23) [S24](e-sources.md#s24)

Modern CI is a working project title, not a trademark-clearance claim. References to Jenkins, Go, Angular, PostgreSQL, Docker, GitHub, and other projects identify the technologies being discussed; they do not imply affiliation or endorsement. There are no measured product benchmarks or customer claims in this edition.

## Evidence before confidence

A unit test of a lease model does not prove that two database transactions coordinate correctly. A valid configuration file does not prove that a container runtime enforces it. A local book build does not prove that a hosted publication has been deployed. Throughout the book, the question is not merely “does this look plausible?” but “which observation would make this claim defensible?”

That habit is the real foundation of a reliable CI/CD platform.
