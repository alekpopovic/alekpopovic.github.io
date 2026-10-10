# Leanpub sales-page copy

## Title

Nginx Log Security

## Subtitle

Build a local IP guard, signed policies, and a reliable analysis pipeline

## Short description

Learn how ordinary Nginx can use completed access logs, a central analyzer, and a local authorization agent to apply short-lived IP decisions. Build an inspectable Python lab, then study the production path to Vector, PostgreSQL, and Go.

## About the book

Your Nginx access logs can support a useful defensive feedback loop. Turning that idea into a dependable system requires more than sending an IP address to a block endpoint.

This practical guide explains how to collect the right observations, deduplicate retries, keep request checks local, authenticate policy updates, reject replayed state, and expire decisions while central services are unavailable. You will build a compact Python/SQLite laboratory with signed policies and mutually authenticated HTTPS, and learn how the architecture extends to a production stack.

The book contains twenty lessons, exercises with answers, a laboratory runbook, editable Markdown sources, and a companion implementation pack. The design uses Nginx Open Source; it does not require Nginx Plus.

You will learn to distinguish desired, delivered, and applied state; preserve request bodies through authorization; avoid trusting visitor-supplied identity headers; start in monitor mode; and test the failure boundaries that matter.

The laboratory and production path are clearly separated. This candidate edition records the executed Python and mTLS tests. Real Nginx, Vector, PostgreSQL, and Go deployment exercises remain host-specific acceptance work; the book makes no unmeasured performance or production-readiness promise.

## What is included

- Twenty written lessons with practical exercises and answers.
- A Python/SQLite teaching implementation and behavioral tests.
- Signed-policy and mTLS transport examples.
- Nginx configuration generation for an isolated local lab.
- Production architecture documents and a sixty-task Claude Code pack.
- PDF and EPUB reading editions and a free sample.

## Audience and prerequisites

For DevOps engineers, Linux administrators, and backend developers who know basic HTTP and Nginx configuration. Familiarity with Python helps with the lab. PostgreSQL and Go appear in the production design, not as completed production services.

## Transparent edition note

Open-source publication candidate 0.2. AI generated substantial manuscript and code content. The preparation test scope is documented. Independent human technical review and the responsible author's editorial approval must precede commercial publication. Replace this edition note only after that review actually occurs.

## Open source and reader support

The complete Markdown manuscript, exercises, answers, prompts and original
branding are available under CC BY 4.0; original code and configuration are
available under MIT. Readers may share and adapt the material under those terms.
Open source access does not depend on an ebook purchase.

For an openly accessible Leanpub edition, use a USD 0 minimum when the chosen
publishing mode supports it, with an optional support price selected by the
author. A paid convenience edition is also compatible with the licenses.
This draft does not change account pricing. Add the actual public repository
link after publication; no source repository URL has been assigned yet.

## Search keywords

Nginx Open Source; access logs; IP blocking; DevOps; local authorization; auth_request; Ed25519; mTLS; Python; PostgreSQL; Vector; Go; reliability.

## About the author

Aleksandar Popovic is the author of Nginx Log Security and the maintainer of this
LogBranik book project. GitHub: https://github.com/alekpopovic.
 No endorsements, testimonials, customer counts, or benchmark claims are invented.
