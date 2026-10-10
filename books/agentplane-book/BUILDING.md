# Building the Reading Editions

## Requirements

Python 3.11 or later, the direct packages in `requirements.txt`, and Pandoc are
required for all formats. Go 1.23 or later is needed only for Go teaching tests.
The edition was built using Python 3.13.5, Mistune 3.2.1, WeasyPrint 68.0 and Pandoc
3.1.11.1. Go teaching tests used Go 1.23.2. These are observed build versions,
not a recommended production Kubernetes application compatibility matrix.

WeasyPrint needs its platform's Pango/font system dependencies. The build uses
installed DejaVu fonts and distributes no font files. Different system fonts or
library versions can change pagination. This is a reproducible source workflow,
not a claim of byte-for-byte output reproducibility across operating systems.

On a Debian/Ubuntu development machine, the usual system prerequisites include
`pandoc`, `libpango-1.0-0`, `libpangoft2-1.0-0` and `fonts-dejavu-core`. Install them
through your reviewed system package process. On other platforms, follow the
WeasyPrint installation documentation for native dependencies.

## Install and build

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make verify
make book
```

`make book` writes `AgentPlane-Book.md`, `dist/AgentPlane-Book.pdf`,
`dist/AgentPlane-Book.epub` and a complete static site under `_site/`.
`dist/SHA256SUMS` records the reading-edition hashes. The command performs no
network access or deployment; dependency installation is a separate operation.

`make html`, `make pdf` and `make epub` build individual export types. Every build
also refreshes the assembled Markdown. Rebuild all formats before publishing a
new edition. `make serve` binds a local website server to 127.0.0.1:8000.

## Validation

`make verify` checks local Markdown links and anchors, source structure and the
teaching tests. `scripts/check_epub.py` checks archive ordering, XML, package
metadata, manifest/spine, navigation and local resources/anchors. It is not the
independent W3C EPUBCheck validator. Run EPUBCheck separately before a distribution
channel that requires it. See the shipped validation report for actual execution.

Render the PDF in a reader or with `pdftoppm` and inspect cover, contents, tables,
code, diagrams and final pages. The build does not guarantee reader-specific EPUB
layout or certify PDF accessibility. Test the target readers independently.

## Diagrams

Editable SVG sources and rendered PNG versions are under `book/assets/`. Normal
builds reuse them. To change diagram layout, edit `scripts/render_diagrams.py`,
install `requirements-artwork.txt` and run the renderer. The cover is edited in
`book/assets/cover.svg`; the same renderer refreshes its PNG version for EPUB.
No font files are distributed and no external image service is required.
