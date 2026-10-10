# Modern CI

## Building a Reliable CI/CD Platform

**Aleksandar Popovic · Open edition 0.1 · October 2026**

A practical engineering book about designing a self-hosted CI/CD platform with
Go, Angular, PostgreSQL, dedicated runners, and independently versioned Git
repositories. Read the architecture, run a compact laboratory, and work through
the failure conditions that turn a build demonstration into a dependable system.

[Start reading](manuscript/00-preface.md) · [Full contents](manuscript/Book.txt) ·
[Uputstvo na srpskom](README.sr.md) · [Publishing](publishing/GITHUB.md)

### What is in this repository

The manuscript contains **24 chapters, five appendices, and 24 primary-source
references**. Every chapter includes an exercise, a worked answer, and completion
evidence. The appendix connects the reading route to **80 implementation work
items**, initially all planned.

The companion Go laboratory exercises graph validation, attempt fencing,
uncertainty, result idempotency, log sequences, webhook signatures and approvals.
Additional SQL, pipeline and message examples describe the production design.
They are clearly separated from the executable laboratory.

**This repository is a book and laboratory, not an implemented production CI/CD
platform.** It does not install a build service or deploy infrastructure. See
[verification](verification/README.md) for checks actually performed and checks
that remain for a deployment environment.

### Read the supplied edition

The release archive includes `dist/modern-ci-book.pdf`,
`dist/modern-ci-book.epub`, a PDF reading sample, and a complete static website
in `dist/site/`. Generated files are ignored by Git: commit the sources, rebuild
them in the publishing workflow, and attach reading editions to releases.

Markdown under `manuscript/` is the canonical source. `Book.txt` defines the full
order and `Sample.txt` defines the sample. Both sit beside the chapter files.
Do not edit HTML or PDF exports as the source of the next edition.

### Build the website and EPUB

Use Python 3.11 or newer and a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-site.txt
python scripts/check.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/build.py epub
python scripts/build.py site
python -m http.server 8000 --directory dist/site --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`. Stop the server with Ctrl+C. The site requires no
JavaScript, hosted database or tracking service.

### Build the PDF and run the complete checks

PDF export additionally needs WeasyPrint and its operating-system libraries:

```bash
python -m pip install -r requirements-print.txt
make check
python scripts/build.py all
```

`make check` also requires Go and a C toolchain for the race detector. See the
[build guide](publishing/BUILDING.md) for prerequisites and commands that do not
need Go. One invocation of `all` produces PDF, EPUB, sample PDF and the website.

### Repository layout

```text
manuscript/          Preface, chapters, appendices and reading order
examples/lab/        Executable Go laboratory with tests
examples/sql/        Illustrative PostgreSQL transactions
examples/pipelines/  Proposed pipeline language
implementation/      Eighty planned work items and evidence checklist
scripts/             Publishing tools and publication checks
styles/              Website, EPUB and print styles
publishing/          Build and GitHub publishing instructions
verification/        Recorded local checks and their limits
.github/             Contribution templates and publishing workflows
```

### Relationship to the application repositories

This book is a standalone repository. It describes a separate
`modern-ci-workspace` containing five application submodules (`server`,
`scheduler`, `runner`, `web`, `cli`) and two library submodules (`core`,
`contracts`). The book neither embeds those repositories nor changes their
commit history. Chapter 3 explains registration, release reachability and
cross-repository work. A book checkout does not need `--recurse-submodules`.

### Open licenses and contributions

The original book text and visual styling are offered under **CC BY 4.0**.
Original source code, snippets and configuration are offered under **MIT**.
Read the [licensing map](LICENSE.md), [book grant](LICENSE-BOOK.md), and
[code license](LICENSE-CODE.txt) before redistributing mixed material.
Third-party tools retain their respective licenses.

Corrections and reproducible examples are welcome through pull requests.
Follow [CONTRIBUTING.md](CONTRIBUTING.md), and report sensitive findings using
[SECURITY.md](SECURITY.md). There is no implied affiliation with Jenkins,
GitHub, Docker or the authors of the referenced tools.
