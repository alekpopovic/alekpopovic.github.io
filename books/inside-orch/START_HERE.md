# Start in the website repository

1. Open the existing checkout of https://github.com/alekpopovic/alekpopovic.github.io.
2. Extract this ZIP into that checkout. It contains `books/inside-orch/`; it does not replace root AGENTS.md, README.md or scripts.
3. Open the repository root in Codex. Keep your selected model; the pack recommends high reasoning where available.
4. Give Codex this instruction:

```text
We are working in alekpopovic/alekpopovic.github.io.
Read root AGENTS.md and books/inside-orch/AGENTS.md.
Read books/inside-orch/BOOK_SPEC.md and books/inside-orch/SITE_WORKSPACE.md.
Execute books/inside-orch/prompts/000-workspace-and-baseline.md.
Write canonical book outputs under books/inside-orch.
Keep evidence/orch immutable and generated site paths ignored.
Update books/inside-orch/state/execution-tracker.csv with real evidence.
Do not publish or push the website's default branch.
```

From the website root, print the next task without executing it:

```bash
python3 books/inside-orch/scripts/next_prompt.py --show
```

Validate the package:

```bash
python3 books/inside-orch/scripts/verify_pack.py
```

The future book tracker starts pending. Begin a task with:

```bash
python3 books/inside-orch/scripts/update_tracker.py --id 000 --status in_progress
```

A done task requires existing evidence through `--evidence`, using a BOOK-relative path. The helper checks file presence; technical truth still requires review.

## Sequence

| Prompts | Output |
| --- | --- |
|000-019|Research, native-site binding, evidence, reading order and preface|
|020-059|40 English chapters, code, exercises, answers and claim records|
|060-065|6 appendices|
|066-073|8 labs with actual results|
|074-085|Source/code/security/reader/editorial review|
|086-095|Cover, PDF/EPUB, native Jekyll adapter, 3 posts, glossary, updates and site verification|
|096-099|Release checks, final archives and reviewable publishing handoff|

The original orch development prompts 00-90 are source evidence, not tasks to rerun against the application. These new 000-099 prompts create the book inside this website repository. Go/Docker/PostgreSQL labs run against a disposable orch source copy, not the Jekyll root.

The native edition has 47 sections: preface + 40 chapters + 6 appendices. It will read under /books/inside-orch/ with generated downloads under /assets/books/inside-orch/downloads/. Canonical source, scripts and exports belong under books/inside-orch; public generated copies stay ignored. Prompt 000 excludes the canonical folder from raw Jekyll copying before a build.

The plan targets 85,000-110,000 meaningful words. This is an editorial target, not content already written. Final page count is measured after typesetting. Missing tools remain blocked; do not invent build/lab results. The current delivery is the complete adapted pack and sample, not a finished 40 chapter book or a live site deployment.
