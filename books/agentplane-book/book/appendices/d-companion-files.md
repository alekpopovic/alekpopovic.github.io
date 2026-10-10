# Appendix D. Companion Files and Build Commands

## Companion files

The GitHub-ready ZIP is the complete companion repository. The PDF and EPUB are
reading editions, not executable software distributions. The assembled Markdown
is generated from the same chapters. No public repository URL is assumed.

| Path | Purpose |
|---|---|
| `book/chapters/` | The 28 source chapters |
| `book/appendices/` | Glossary, records, review notes and this guide |
| `book/assets/` | Original diagrams and cover artwork |
| `prompts/00-*.md` through `44-*.md` | Bounded implementation assignments |
| `prompts/TRACKER.csv` | Initial implementation tracker |
| `examples/go-core/` | State, approval and quota teaching programs |
| `examples/audit/` | Hash-chain example and tests |
| `examples/sql/` | Disposable PostgreSQL isolation lab |
| `examples/kubernetes/` | Local-only restricted manifest renderer |
| `labs/` | Guided exercises with acceptance criteria |
| `scripts/` | Publication, verification and artifact checks |
| `reports/VALIDATION.md` | Executed checks and known limitations |
| `.github/workflows/` | Validation and Pages publication workflows |
| `dist/` | PDF, EPUB and checksums for this edition |
| `AgentPlane-Book.md` | Assembled Markdown reading edition |

## Read without building

Open the PDF in a PDF reader, import the EPUB into an EPUB-compatible reader, or
start with `book/index.md` in a Markdown viewer. The chapter files work directly
on GitHub. Diagrams also have their editable source alongside the rendered images.

## Rebuild locally

The publication requires Python 3.11 or later and the pinned packages in the
requirements files. Full export also requires Pandoc and system libraries used
by WeasyPrint. See `BUILDING.md` for the tested tool versions and platform notes.
The standard build does not provision a cluster or contact a cloud account.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check.py
python scripts/build.py --format all
```

Generated files are disposable outputs. Edit chapter sources and rebuild them.
The website is written to `_site`, while reading editions are written to `dist`
and the root assembled Markdown file. `make verify` runs the teaching checks;
`make book` produces the complete publication.

## What publication does not do

The package does not create a GitHub repository, enable Pages, push a commit,
publish a release, deploy AgentPlane or certify runtime isolation. Follow
`PUBLISHING.md` to perform the account-side steps deliberately. The initial
implementation tracker remains not started because a book is not the application.
