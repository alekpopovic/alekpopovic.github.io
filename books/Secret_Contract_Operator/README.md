# Secret Contract Operator — Technical Book

**Designing a Safe Kubernetes Operator**  
Codepop Engineering · English edition 1.0 · October 10, 2026

The English edition contains **22 chapters, four appendices, three architecture diagrams, 30 development prompts, and 27 primary sources**. PDF, EPUB, and combined Markdown are generated from the same English manuscript. The preface and bibliography explain scope and limitations.

## Choose a Format

- [PDF edition](dist/secret-contract-operator-book.pdf): a typeset book with a clickable contents page, bookmarks, source links, and page numbers.
- [EPUB edition](dist/secret-contract-operator-book.epub): reflowable text for e-readers and EPUB 3 applications, with chapter navigation.
- [Combined Markdown](dist/secret-contract-operator-book.md): the complete editable text. Its diagram references use the accompanying `assets/` directory.

## Development Materials

`chapters/` contains 27 separate Markdown documents: the preface, 22 chapters, and four appendices. `prompts/` contains 30 numbered tasks with acceptance criteria. `tracking/` contains the initial CSV and JSON development registers; all operator tasks remain `pending`.

`examples/contractlab/` is a standalone, tested Go validator without Kubernetes dependencies. `examples/manifests/` contains five lab YAML templates. `examples/contract-gate.sh` is a reference generation-aware CI check. Read `examples/README.md` before starting.

`assets/` contains the cover and original diagrams in SVG and PNG formats, with English labels. `sources.json` is a machine-readable primary-reference list. `TEST_REPORT.md` distinguishes original-package checks from English-edition checks. Historical reports remain in `qa/`. `SHA256SUMS` records package-file checksums, excluding itself and temporary build files.

## What Is Implemented

This is a **book, design specification, and development package**, rather than a completed Kubernetes operator. It contains no finished manager, installable CRD, production Helm chart, or published container image. The development prompts guide their implementation.

The canonical `secrets.codepop.tech/v1alpha1` API and proposed repository name are project decisions, not confirmation that public resources with those names exist. The book consolidates earlier sketches, retains a read-only MVP, and separates the optional mutation phase.

The supplied package records successful local Go tests, a race check, vet, and a short fuzz run. Envtest, kind, real ESO, server-side CRD validation, Helm installation, and production integration **were not run**. Never use the synthetic example values as production secrets.

## Getting Started

Read chapters 1–5 and the security model first. Run the Go lab following `examples/README.md`. Then start with `prompts/001-task.md` and track operator development in `tracking/`. Medium/High labels describe task complexity, not automatic model configuration.

## Building the English Edition

From the website repository, install `requirements-books.txt` and run `npm run build`. The publisher under `tools/build.py` regenerates English PDF, EPUB, Markdown, cover, and diagram files locally, without fetching external assets. The site retains existing chapter filenames and reading URLs so previously shared links remain valid.

Original files whose names end in `_SR` are retained privately in the canonical package for reference. They are excluded from the website; public downloads use the English edition.
