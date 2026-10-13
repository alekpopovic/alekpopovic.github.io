# Site execution binding

This pack is installed at `books/inside-orch` in `https://github.com/alekpopovic/alekpopovic.github.io`. Every prompt runs from the website repository root. Read root AGENTS.md first, then these instructions, BOOK_SPEC.md and SITE_WORKSPACE.md. Book-relative paths below resolve beneath books/inside-orch. Never replace root instructions or scripts with pack files. Keep the canonical folder excluded from raw Jekyll copying. Register the completed book in scripts/book_catalog.py and integrate its required posts/glossary/updates using the site's actual publisher.

# Book instructions within the Jekyll website

This workspace produces **Inside orch: Building and Operating a Docker Orchestrator in Go**, by Aleksandar Popovic. Read `BOOK_SPEC.md`, `evidence/source-lock.json`, and the current numbered prompt before authoring. This pack is a workflow and a verified source corpus, not a completed book.

## Ownership and boundaries

- `evidence/orch/` is an immutable snapshot of the application repository. Never edit, format, build into, commit, or push that directory. Its original AGENTS.md is evidence of the application's development conventions; its repository workflow applies only to application changes, which this task does not authorize.
- Write book content to `manuscript/`; runnable teaching additions to `examples/teaching-extensions/`; execution evidence to `validation/`; publication outputs to `dist/`.
- Do not silently fix the application to make a chapter true. Explain the baseline, then label a separate improvement as a teaching extension and test it independently.
- Create local commits in an selected branch of the website repository if appropriate. Publishing a website, pushing its default branch, or changing the live application requires a task instruction authorizing that action. Prepare a reviewable local result first.
- Preserve unrelated user work. Inspect git status before staging. Never copy credentials, personal email addresses, environment files with live secrets, or git authentication configuration into the book.

## Evidence rules

- Read implementations and tests, not only documentation or commit titles. Use full immutable commit SHAs in source and history links.
- Distinguish historical implementation evidence, current behavior, design intent, runnable teaching additions, and future work.
- Source prompts 00–28 were committed after the June implementation. Their associated commits show implementation history, not proof that a particular prompt ran before that commit.
- Late prompts were implemented in batches. Do not invent one commit per prompt.
- `EXECUTION_TRACKER.md` records development progress. It does not establish executable integration, durable state, runtime enforcement, or production readiness.
- An implementation test inspected in source is not a test run. Store real commands, prerequisites, exit codes, UTC timestamps, and scope when running verification. Mark unavailable prerequisites as blocked.
- Default `orch-server` owns active state in memory. PostgreSQL store/migrations, HA leadership, and autoscaling packages must be discussed according to their actual integration status. Inspect the source-based capability ledger for other gaps.

## Authoring and review

Write clear English technical prose. The public book is about engineering the system; tooling and prompt instructions belong in this pack rather than the narrative. Explain failure windows, tradeoffs, and evidence before claims of reliability. Retain the author name Aleksandar Popovic and the website https://www.alekpopovic.com.

Each chapter needs a motivating problem, stated learning outcomes, a code-guided explanation, a concrete failure scenario, a safe lab, exercises and worked answers, evidence references, and an explicit boundary. Use short exact code excerpts with pinned file/line links. Prefer diagrams for relationships or state changes and tables for precise comparisons. Every diagram must be checked against code.

Update `state/execution-tracker.csv` after each prompt. Allowed statuses: pending, in_progress, blocked, review_needed, done. A task is done only when its specific acceptance criteria pass; provide validation paths and a local commit SHA if one was created. Never mark future writing or unrun labs done merely because the prompt was delivered.

Before release run `python3 books/inside-orch/scripts/verify_pack.py` and `python3 books/inside-orch/scripts/check_manuscript.py --strict`, plus the explicit human and execution gates in `editorial/QUALITY_GATES.md`. These scripts validate structure; they do not certify semantic correctness, security, or production fitness.
