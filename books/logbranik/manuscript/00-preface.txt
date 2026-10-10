# Nginx Log Security

## Build a local IP guard, signed policies, and a reliable analysis pipeline

**LogBranik - From logs to controlled action**

**Author: [Aleksandar Popovic](https://github.com/alekpopovic)**

Open-source publication candidate, edition 0.2. Prepared October 2026.

## Copyright and open licenses

Copyright (c) 2026 Aleksandar Popovic. The complete book text, exercises,
answers, prompts, and original LogBranik visual assets are licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
The [complete CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)
governs that grant. Original code, code snippets and configuration examples
are licensed under the [MIT License](https://opensource.org/license/mit).
The source package includes the full MIT notice and a detailed licensing map.

You may share, modify and redistribute these materials, including commercially,
under the applicable license. Attribute content to Aleksandar Popovic,
link CC BY 4.0, and identify changes. Retain the MIT copyright and permission
notice with code copies. Third-party fonts and dependencies retain their own
licenses. An optional paid reading edition does not restrict access to the
open sources. This edition has not yet been published to a public repository.

## MIT notice for original code

MIT License. Copyright (c) 2026 Aleksandar Popovic.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Introduction

An ordinary Nginx server already knows a great deal about the traffic reaching an application. Its access logs tell us which paths clients request, how the application responds, and how much work each request causes. Turning those observations into an automatic defense is possible without buying Nginx Plus. The difficult part is deciding what the observations mean, delivering a trustworthy decision, and keeping the application usable when a component fails.

This book builds that system from explicit contracts. An edge host keeps request checks local. A central service receives completed access events, identifies a narrow pattern of suspicious activity, and publishes short-lived IP decisions. An agent accepts signed policies and answers Nginx authorization subrequests. The design distinguishes an operator's intention from what an edge has actually applied.

The companion implementation is deliberately compact. Python and SQLite let you inspect persistence, deduplication, detection, signatures, revision ordering, and expiry without first operating several infrastructure services. Its live transport exercises use mutually authenticated HTTPS. The deployment design then extends those ideas to Vector, FastAPI, PostgreSQL, and a Go agent. That production design is a specification and migration path, not a claim that the small laboratory is production software.

## Who should read this book

You should be comfortable with Linux processes, HTTP, a basic Nginx configuration, and reading Python. You do not need to know public-key cryptography. The relevant operations are introduced through a concrete policy protocol. The PostgreSQL and Go lessons assume that you can read SQL and understand a simple service boundary; they explain the architecture rather than teach either language from scratch.

Work on servers you own or have permission to administer. All example addresses use documentation ranges or loopback. The traffic exercises target a local echo application. They are designed to study defensive behavior without contacting another organization's systems.

## What you will build

The laboratory includes a durable ingestion store, an explainable 404-path detector, a signed full-state snapshot, a local authorization handler, a separate mTLS control handler, and a periodic delivery process. You will observe allow, would-block, block, and revoke transitions. You will test old-policy rejection, duplicate ingestion, clock changes, and expiry without a central server.

Each of the twenty lessons ends with an exercise and an answer. The source of every lesson is a Markdown file in `lessons/`. The same content is exported to Leanpub manuscript files. The appendices contain a runbook, a bridge to the sixty-task implementation pack, a glossary, and source references.

## Evidence and edition status

The delivered verification directory records the actual Python test run and environment. The core and live loopback mTLS tests were executed during preparation. The host does not support creating an AF_UNIX socket, so that integration test is explicitly skipped. Nginx, Vector, PostgreSQL, and Go were unavailable in the preparation environment. Their configuration examples and production exercises therefore require execution on the reader's deployment host. No end-to-end Nginx performance measurement or production readiness claim is made.

This distinction is part of the engineering method. A plausible configuration is not a verified deployment. A unit test of a policy function is not a test of an Nginx access phase. A successful loopback HTTPS exchange is not a fleet rollout. The acceptance gates in later lessons tell you which evidence belongs to which claim.

## AI transparency

AI was used to generate the manuscript, companion code, exercises, and publishing materials. Automated checks were executed for the scope documented above. This candidate has not yet received an independent human technical review or an author's final editorial approval. Before commercial publication, the responsible author should review the text, reproduce the deployment exercises, and update this statement to describe the work actually completed. Do not replace this statement with a claim that AI was used only for proofreading.

## Reading route

Read lessons 1-3 for the system model. Run lesson 4 before changing a server. Lessons 5-12 cover trustworthy data and control. Lessons 13-17 cover operations and the production migration. Lessons 18-20 provide testing, troubleshooting, and a reproducible release workflow. The appendix runbook is useful at the keyboard, but it does not replace the explanations.

LogBranik is a proposed project brand. It is not an official Nginx product and does not imply endorsement by Nginx, Leanpub, or any dependency author. The name has not received trademark clearance. There is no fabricated author biography, endorsement, benchmark, or customer story in this edition.
