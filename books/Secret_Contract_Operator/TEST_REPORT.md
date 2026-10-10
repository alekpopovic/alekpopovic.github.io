# Edition 1.0 Validation Report

Publication date: October 10, 2026. This report concerns the book and accompanying Go lab, not an unimplemented operator.

## English Edition

The English manuscript contains the complete preface, 22 numbered chapters, four appendices, and all 30 development prompts. The English cover and three diagrams are maintained as SVG sources, with PNG copies for EPUB and responsive website covers.

Run the website's publication checks after building the English edition:

```bash
npm run build
bundle exec jekyll build
.venv/bin/python scripts/check-books.py
npm run check:site
```

The publication check compares every reading section against its complete source and every EPUB chapter against the same text. It also checks PDF chapter coverage and attribution, EPUB language, structure, resources, and anchors, download consistency, linked posts, and local reading links. PDF pagination is generated from the English text; the original edition's 83-page count does not describe this edition.

## Checks Recorded in the Original Package

The following results are historical records supplied with the original edition, not claims that the operator was implemented or that the original pagination applies to the English export.

| Check | Recorded result | Scope |
|---|---|---|
| PDF generation and parsing | Passed | 83 original A4 pages; contents and bookmarks present |
| PDF visual inspection | Passed | Rendered pages, contact sheets, and enlarged cover, contents, prose, table, code, and diagram samples |
| PDF text-block bounds | Passed | No out-of-page blocks or replacement character U+FFFD found |
| EPUB archive and mimetype | Passed | First, uncompressed `mimetype`; `application/epub+zip` |
| EPUB XML/OPF/XHTML | Passed | XML parsing, manifest, spine, and navigation |
| EPUB local paths and fragments | Passed | 821 local references; no missing fragment IDs |
| YAML syntax | Passed | 15 fenced YAML blocks and lab documents in total; not server-side schema validation |
| Bash syntax | Passed | `bash -n examples/contract-gate.sh`; not executed against a cluster |
| Go unit tests | Passed | `go test -count=1 ./...` in `examples/contractlab` |
| Go race check | Passed | `go test -race -count=1 ./...` |
| Go vet | Passed | `go vet ./...` without findings |
| Bounded Go fuzz test | Passed | `FuzzValidator`, three seconds, two workers; 52,421 executions in the original environment |

The recorded Go environment was `go1.23.2 linux/amd64`. This short fuzz run is not exhaustive proof. It proves neither the absence of every bug nor every leakage channel. The security model discusses validation-oracle risk. Original execution logs and structural reports are in `qa/`.

## Checks Not Run

EPUBCheck and validation in every e-reader were not run. Structural EPUB checks are not formal EPUB certification.

The complete operator, envtest integration suite, kind E2E tests, actual External Secrets Operator, Helm installation/upgrade, Kubernetes admission webhook, cloud integration, and production rollout have not been implemented and executed. There is no confirmed support matrix for Kubernetes, ESO, or controller-runtime versions.

Server-side CRD schema/defaulting/CEL checks must run after the canonical API is implemented. YAML syntax does not prove cluster acceptance. Replace the workload example's image placeholder before use.

## Development Register

All operator prompts remain `pending`. A prompt or expected lab outcome does not prove implementation or execution. Each future task should record its commit, actual commands, results, limitations, and checks not run.
