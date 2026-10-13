# Manuscript workspace

This workspace will produce **Inside orch: Building and Operating a Docker
Orchestrator in Go**, by Aleksandar Popovic, in English. The planned first
edition is a new source-based engineering book. The installed pack and its
sample are preparation material; the complete manuscript has not been written.

`Book.txt` preserves the planned 47-section reading order: a preface, forty
numbered chapters, and six appendices. Its entries are a writing plan, not proof
that those sections exist. Keep canonical prose in `chapters/`, `appendices/`,
and `00-preface.md`; put worked answers in `solutions/`. Do not create placeholder
chapters or copy the supplied sample into a completed chapter during intake.

The immutable application snapshot is `../evidence/orch/`, pinned to commit
`cbfc94ade5b57e449d6b73bf1485b1c5b1647022` and tree
`ff43cd85a88ab213c5c4fa76281d4811957b89aa`. It contains tracked file exports and
separate commit records/diffs, without a `.git` database. Never build into or
edit that snapshot. Run future experiments in the separate disposable directory
recorded in `../state/workspace.json`; persist actual commands and results under
`../validation/`. Label unrun experiments as expected results.

Read the root and book `AGENTS.md`, `../BOOK_SPEC.md`, and
`../SITE_WORKSPACE.md` before authoring. Teaching extensions belong under
`../examples/teaching-extensions/`; canonical publication outputs belong under
`../dist/`. Generated site pages, public downloads, and the generated catalog
remain ignored. Intake leaves this incomplete book unregistered in the site.

The target is 85,000–110,000 meaningful words, subject to editorial review.
Neither a final word count nor a rendered page count has been measured. Source
rights and the manuscript's publication license still require the dedicated
rights review; this scope note grants no new public license.
