# Prompt 000 — workspace and baseline evidence

Recorded at 2026-10-13T00:20:46.228710+00:00. Execution root:
`/home/popac/alekpopovic.github.io`.

## Outcome and ownership

Prepared a local, isolated workspace for **Inside orch: Building and Operating
a Docker Orchestrator in Go**, by Aleksandar Popovic, in English. The edition is
**1.0 planned**, with canonical metadata preserved in `../../book.json`.
The complete manuscript, application experiments, and final editions are pending.
The 85,000–110,000-word target and 47-section reading order are plans; no final
word count or typeset page count is claimed.

The initial checkout was `main` at
`80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`, with clean tracked files and only the
user-supplied `books/inside-orch/` pack untracked. Work now uses the separate
local branch `book/inside-orch-000`. No reset, local commit, push, deployment, or
application change was performed. The website origin identifies
`alekpopovic/alekpopovic.github.io`.

Read the root and book instructions, BOOK_SPEC, SITE_WORKSPACE, both locks, the
source snapshot's historical AGENTS, and prompt 000. The snapshot AGENTS is
source evidence; its application push rule does not authorize a website push.

## Immutable application baseline

- Repository: `https://github.com/alekpopovic/orch`.
- Locked commit: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`.
- Locked and reconstructed tree: `ff43cd85a88ab213c5c4fa76281d4811957b89aa`.
- **361 files** matched every locked size and SHA-256; membership also matched.
- **91 original development prompts (00–90)**, **105 commit records**, and
  **105 exported diffs** are present. All sixteen up/down migration pairs exist.
- Tags `0.1.0` and `0.3.0` are recorded in the source lock. No tag objects were
  fetched or independently authenticated during intake.
- The separate **100 book-production prompts (000–099)** and **508 pinned
  source/commit links** passed the supplied structural validator.

The exported snapshot contains tracked bytes and separately exported diffs,
**without a `.git` database**. Its file permissions do not preserve executable
bits. The read-only audit recovered original Git modes from the chronological
exported diffs, then computed Git blob/tree objects entirely in memory. The
result exactly matches the locked tree. No chmod, git init, build, or write was
performed in `evidence/orch/`. The commit SHA is present in the supplied lock and
history corpus; this does not independently authenticate a fetched commit object.

[`source-before.json`](source-before.json) and
[`baseline-audit.json`](baseline-audit.json) establish byte-for-byte source
preservation. [`audit_baseline.py`](audit_baseline.py) contains the actual audit;
its checks describe this intake baseline, rather than a permanent future CI
contract. The supplied pack files, including its sample, Book.txt and book.json,
were preserved; only its execution tracker is intentionally updated.

## Site contract and isolation

The current HEAD equals the locked site inspection revision. All twenty
supplied site-contract sources retain their locked hashes inside `evidence/site`.
Nineteen current site files match those sources exactly. The sole intended site
source change is adding `books/inside-orch` to `_config.yml`'s existing exclude
list **before the first build**. The production origin, existing excludes,
root AGENTS/README, publisher scripts, shared layouts, and existing books are
preserved.

Actual Jekyll output contains neither the raw canonical folder nor Inside orch
public assets. The generated catalog still contains the five existing books;
Inside orch remains unregistered. Existing ignore rules cover
`book-pages/inside-orch/`, `assets/books/inside-orch/`, and `_data/books.json`.
No generated book pages or catalog entries were hand-edited or force-added.

Canonical chapters, appendices, solutions, teaching extensions, validation
claims/lab results, and exports now have separate directories. The scope note is
[`../../manuscript/README.md`](../../manuscript/README.md). No placeholder prose
was created. Durable command records and results are beneath this validation
folder; the workspace manifest is
[`../../state/workspace.json`](../../state/workspace.json).

The empty disposable lab root is `/tmp/inside-orch-labs-cbfc94ade5b5`, outside
the website and canonical evidence. No application source copy or lab has been
started there. Recreate it if /tmp is cleared, copy the locked source before a
future experiment, and keep actual results under `validation/labs`. No history
clone was needed for intake; a later task requiring Git navigation must use a
separate clone and verify the full locked SHA.

## Actual local capabilities

| Tool | Observed version or availability |
| --- | --- |
| python | Python 3.14.4 |
| git | git version 2.53.0 |
| go | go version go1.22.5 linux/amd64; incompatible with source requirement Go 1.25.0 |
| docker | Docker version 29.8.2, build 7fc2dff |
| postgres-client | Not on PATH; command not run |
| postgres-server | Not on PATH; command not run |
| postgres-readiness | Not on PATH; command not run |
| pandoc | Not on PATH; command not run |
| weasyprint | WeasyPrint version 68.0 (site .venv) |
| pdflatex | Not on PATH; command not run |
| xelatex | Not on PATH; command not run |
| lualatex | Not on PATH; command not run |
| pdfinfo | pdfinfo version 26.01.0 |
| pdftoppm | pdftoppm version 26.01.0 |
| epubcheck | Not on PATH; command not run |
| java | openjdk version "25.0.4.1" 2026-08-18 |
| ruby | ruby 4.0.5 (2026-05-20 revision 64336ffd0e) +PRISM [x86_64-linux] |
| bundler | 4.0.6 |
| node | v26.4.0 |
| npm | 11.17.0 |

Docker daemon **29.8.2** was reachable through an authorized read-only socket
check. The initial sandbox attempt failed with permission denied; both actual
results are retained. No container was created or changed. Compose's version
was also checked. PostgreSQL executables were not on PATH, and no database
service or connection was tested.

An initial Python package probe incorrectly requested the `Markdown` distribution
and failed. A corrected probe of the actual publication dependencies passed:
PyYAML, Pillow, markdown-it-py, mistune, WeasyPrint and pypdf. Both outputs are
retained. `.venv/bin/weasyprint` is available even though `weasyprint` was not
on the ordinary PATH; the existing site's PDF-producing build passed.

[`tool-capabilities.json`](tool-capabilities.json) records exact paths, outputs,
and runtime scope. [`commands.jsonl`](commands.jsonl) records each executed
command's arguments, working directory, UTC start/finish, exit code, duration,
and stdout/stderr paths. [`record_command.py`](record_command.py) preserves the
recorder used for these executions; its initial phase refuses to overwrite an
existing intake inventory.

## Checks actually run

| Command | Exit | Finished at UTC | Actual output |
| --- | --- | --- | --- |
| `python3 books/inside-orch/scripts/verify_pack.py` | 0 | 2026-10-13T00:20:46.121222+00:00 | [verify-pack-final](verify-pack-final.stdout.txt) |
| `python3 books/inside-orch/validation/intake/audit_baseline.py` | 0 | 2026-10-13T00:19:11.966664+00:00 | [baseline-audit-final](baseline-audit-final.stdout.txt) |
| `npm run build` | 0 | 2026-10-13T00:16:08.683324+00:00 | [site-npm-build](site-npm-build.stdout.txt) |
| `bundle exec jekyll build` | 0 | 2026-10-13T00:17:34.775724+00:00 | [site-jekyll-build](site-jekyll-build.stdout.txt) |
| `.venv/bin/python scripts/check-books.py` | 0 | 2026-10-13T00:18:51.048537+00:00 | [site-check-books](site-check-books.stdout.txt) |
| `npm run check:site` | 0 | 2026-10-13T00:19:15.250402+00:00 | [site-check-site](site-check-site.stdout.txt) |
| `npm run check:content` | 0 | 2026-10-13T00:19:12.032690+00:00 | [site-check-content](site-check-content.stdout.txt) |

Pack verification returned **passed** with zero errors. The site publication
check verified **5 existing books, 157 sections, and 22,572 local references**;
those counts are not an Inside orch manuscript result. Site checks passed for
**247 indexable pages and 237 search documents**, and editorial checks covered
**18 entries and 24 source URLs**. No validation rule was weakened.

## Unrun work and dependent blockers

- **Go application execution is blocked:** installed Go 1.22.5 is below the
  source's `go 1.25.0` directive. No `go build`, `go test`, automatic toolchain
  download, benchmark, or application lint was attempted.
- **PostgreSQL labs are blocked until provisioned:** client/server/readiness
  commands are absent; a reachable Docker daemon is not database-test evidence.
- **The official EPUB conformance gate is blocked:** `epubcheck` is absent from
  PATH. Java alone does not provide an EPUBCheck result.
- Pandoc and the checked TeX engines are absent. They are optional alternatives;
  the site's current WeasyPrint renderer is available.
- No Inside orch PDF/EPUB, Docker/PostgreSQL experiment, eight-lab result,
  security/reliability conclusion, or complete-manuscript release check was
  produced. `check_manuscript.py --strict` is a later release gate and was not
  run against an unwritten manuscript.
- No UI or performance suite was rerun: prompt 000 changes no shared layout,
  browser code, or visible feature. Build/site/content checks cover the actual
  configuration change.

These gaps block their dependent execution or publication tasks, **not this
intake's source/workspace acceptance criteria**. Future tracker rows remain
pending. Existing shipped review documents describe pack creation, not new lab
runs; the execution tracker and this intake evidence record the current work.

## Handoff

Only task **000** is eligible for completion from this evidence. Print the next
unfinished prompt from the website root using
`python3 books/inside-orch/scripts/next_prompt.py --show`.
The next task is **001 — Inventory the implementation and its executable
entrypoints**. Printing its instructions does not execute it.

No publication or push is authorized. All application labs, chapter production,
rights decisions, native adapter integration, and final release gates remain
separate future tasks.
