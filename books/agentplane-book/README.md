# AgentPlane

## Building a Kubernetes-Native Platform for AI Agents

**An open engineering book · English · Edition 0.1.0**

Design a platform that runs and governs AI-agent workloads in customer-owned
Kubernetes clusters. Follow the boundaries between a Go control plane,
PostgreSQL, durable command delivery, an outbound connector, upstream sandbox
runtimes, network policy, workload identity and MCP tool governance.

**This repository is the book and its teaching material, not a released AgentPlane
SaaS application.** See [project status](NOTICE.md) and [validation](reports/VALIDATION.md).

### Read the book

| Edition | File |
|---|---|
| PDF | [AgentPlane-Book.pdf](dist/AgentPlane-Book.pdf) |
| EPUB | [AgentPlane-Book.epub](dist/AgentPlane-Book.epub) |
| Complete Markdown | [AgentPlane-Book.md](AgentPlane-Book.md) |
| Individual chapters | [Table of contents](book/index.md) |

The book contains 28 chapters, four appendices, original diagrams, seven labs and
45 implementation assignments. Chapters explain tradeoffs and failure modes;
they are not simply pasted coding prompts.

### The important engineering questions

How do you preserve tenant scope through SQL, queues and live streams? What can a
compromised SaaS still ask an outbound connector to do? Which component actually
enforces runtime isolation? How do you handle a command that ran but lost its
result? What does a one-time approval authorize, and what does it not guarantee?
How can a database restore accidentally revive authority?

The book answers these with proposed contracts, runnable small examples and
explicit integration exercises. The dependency-free Go and Python examples test
state, concurrency, approvals, quotas and tamper evidence. Real PostgreSQL and
Kubernetes validation require disposable infrastructure and are separately marked.

### Build and verify

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make verify
make book
```

Full export requires Pandoc and WeasyPrint's system dependencies. See
[BUILDING.md](BUILDING.md). To build only the website:

```sh
python scripts/build.py --format html
python -m http.server --bind 127.0.0.1 --directory _site 8000
```

### Repository map

```text
book/                 Chapter sources, appendices, sources and diagrams
examples/             Go, Python, SQL and Kubernetes teaching material
labs/                 Guided exercises and acceptance criteria
prompts/              45 assignments for a separate implementation repository
scripts/              Publication and local verification tools
dist/                 Generated PDF, EPUB and checksums
.github/              Validation, Pages workflow and contribution templates
```

### Publish and contribute

[PUBLISHING.md](PUBLISHING.md) explains how to create your own GitHub repository,
enable Pages and attach reading editions to a release. No remote repository,
Pages site or release has been created by this package.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting changes.

### License

Original narrative, diagrams and prompt prose: **CC BY-SA 4.0**.
Original code and configuration examples: **MIT**.
See [LICENSE.md](LICENSE.md) for material-by-material scope and third-party notices.
No upstream affiliation, independent audit or compliance certification is claimed.
