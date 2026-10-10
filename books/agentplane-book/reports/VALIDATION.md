# Edition 0.1.0 Validation

Validation date: October 10, 2026. This report concerns the book and small teaching
examples, not a full AgentPlane application or production cluster.

## Executed checks

- Generated all 28 English chapters, four appendices and source references.
- Ran ten Go test functions, including concurrent transition, approval and quota
  cases, with the race detector; passed. Ran `go vet`; passed.
- Ran ten Python audit-chain tests; passed.
- Ran four Python Kubernetes-renderer tests; passed. These validate generated
  object structure only, not API acceptance, CNI enforcement or runtime isolation.
- Built Markdown, static HTML, a 106-page PDF and an EPUB reading edition.

- Ran `scripts/check.py`: 112 local Markdown documents, targets and anchors passed.
- Checked 113 generated HTML pages and 4,335 local references; no broken local
  targets or fragments were found.
- Ran `scripts/check_epub.py`: all 50 EPUB archive members, 42 XML documents,
  38 spine items and 314 local references passed the internal structural checks.
- Verified all 28 chapter titles in PDF text and the presence of PDF bookmarks.
  No extracted text spans extended beyond physical page bounds.
- Rendered the PDF for visual review; inspected the cover, contents, diagrams,
  body pages and final pages. Contact sheets covered the complete edition.

Detailed results and actual tool versions are in `reports/BUILD_RESULTS.json`.

## Explicitly not executed

PostgreSQL integration, real Kubernetes deployment, CNI traffic tests, upstream
sandbox execution, cloud provisioning, PKI integration and a full SaaS end-to-end
suite were not executed. The repository contains exercises and contracts for that
work, not a completed application. No external security audit was performed.

Independent W3C EPUBCheck was not available in the build environment. The included
internal checker validates packaging/XML/references but does not claim complete
EPUB specification conformance. No physical e-reader or commercial reading app
was tested. PDF/EPUB accessibility conformance is not certified.

GitHub workflows have not run on a user's repository. Their action commit
references were checked against the corresponding official repositories, but
account settings, runner packages and Pages deployment require separate validation.
No GitHub repository, remote commit, Pages site or release was created.

## Source review

The 24 primary-source references were consulted for the architectural discussion.
A linked upstream page is not an executed compatibility matrix. Release-specific
integration work must pin and test the exact controller, runtime, router, SDK,
network and storage combination. Earlier speculative tool-version and model-name
claims are not treated as application baselines in this edition.
