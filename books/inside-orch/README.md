# Inside orch - Codex Book Pack for alekpopovic.github.io

**Book:** Inside orch: Building and Operating a Docker Orchestrator in Go  
**Author:** Aleksandar Popovic  
**Language:** English  
**Execution repository:** https://github.com/alekpopovic/alekpopovic.github.io  
**Execution directory:** repository root  
**Install folder:** books/inside-orch

This is a complete 100-prompt book-generation pack adapted to the actual Jekyll + Tailwind website. It plans a preface, 40 chapters, 6 appendices and 8 progressive laboratories, with 47 native reading sections. It includes a source-reviewed sample chapter and 3 prepared original companion posts. The full manuscript and final book editions have not yet been generated.

Unzip directly into the website checkout so `books/inside-orch/START_HERE.md` exists. Open the repository root in Codex and begin with `books/inside-orch/prompts/000-workspace-and-baseline.md`. Read root AGENTS.md and the book's own AGENTS.md. Do not overwrite root files with package files. All prompt instructions name the site-root execution context and book-scoped artifact paths.

## Evidence and workflow

- 91 original orch development prompts mapped to actual changed source paths across 105 reachable commits.
- Immutable orch SHA cbfc94ade5b57e449d6b73bf1485b1c5b1647022, with 361 source files, diffs and exact excerpt seeds.
- Separate site-contract SHA 80801c8d3d97a4d8ff78e0fe69f3f902beda00c0 and 20 selected native publisher/configuration sources.
- 100 full book-production prompts; [ALL_100_PROMPTS.md](ALL_100_PROMPTS.md) combines their full texts, and [PROMPT_INDEX.md](PROMPT_INDEX.md) lists individual tasks.
- Source/claim policies, chapter contracts, worked-answer/lab templates, trackers and validators.
- Native catalog registration in root scripts/book_catalog.py, publisher wiring in scripts/build-books.py, 47 section ordering and exact chapter heading grammar.
- Three prepared substantive posts about different numbered chapters, plus glossary/update requirements and site build checks.

The default orch-server uses live in-memory state. The book distinguishes runtime behavior, standalone libraries, designs and teaching extensions, including actual persistence, placement/resource, HA and recovery limits. Go was unavailable during pack creation: application tests, Docker/PostgreSQL labs and benchmarks were not run. Sample Bash syntax and the source/package structure were checked. All 100 future book-production tasks remain pending.

See [SITE_WORKSPACE.md](SITE_WORKSPACE.md) for exact ownership: canonical books/inside-orch source is versioned; generated book-pages/inside-orch, assets/books/inside-orch and _data/books.json stay ignored. Read [START_HERE.md](START_HERE.md) for commands. Live deployment is separate from delivery of this pack; no website or application repository was changed.
