# Verification scope — edition 0.1

The delivered edition was checked locally. These results apply to the book and
its teaching laboratory, not to an implemented production CI/CD platform.

| Check | Recorded result |
|---|---|
| Go tests | 31 passing named cases, including subtests |
| Go race detector | Passed for the exercised test suite |
| Go vet | Exit status 0, no diagnostics |
| Publication tests | 17 passed |
| Manuscript validation | 24 chapters, five appendices, 24 sources, 80 work items |
| PDF export | Completed; selected page renders reviewed |
| PDF geometry | No extracted text spans outside page boundaries |
| EPUB export | Completed; XML, resources, spine and internal links checked |

`report.json` records tool versions and page counts. `book-check.json` records
manuscript counts. The other files contain the unit output, demonstration,
race output, vet output, full-check output, and export paths. Export paths
record the preparation environment; they are not required installation paths.

The Go ledger is in-memory and single-process. The race detector reports only
behavior exercised by its test run. Publication checks are not formal EPUBCheck
validation or a complete e-reader compatibility test. Page counts can vary with
fonts and renderer versions. No font files are distributed in the source.

## Not executed

PostgreSQL integration, Docker/BuildKit isolation, Angular compilation,
multi-host runner communication, cloud deployment, GitHub-hosted workflows,
GitHub Pages publication, external store upload and official EPUBCheck were
not executed. No benchmark or production-readiness certification is claimed.
Run the book's acceptance gates in the intended deployment environment.

All eighty implementation items remain planned. Passing the laboratory tests
does not complete those product work items. The publication archive contains
sources and reading editions, but no existing remote repository or application
Git history.
