# Independent pack review

Reviewed UTC: 2026-10-12T23:47:13.926668+00:00. Source lock: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`.

**Decision:** technically coherent book-generation pack. All identified consistency findings are resolved and independently rechecked. No unresolved pack finding remains. This is not a completed manuscript or an application/lab execution certificate. PDF rendering is outside this review.

## Executed checks

- `python3 scripts/verify_pack.py`: exit 0; source hashes pass for 361 files; 100 sequential book prompts, 91 development-prompt mappings, 105 commit records, 40 chapters, six appendices and 508 prompt-level immutable link occurrences pass the supplied validator.
- Independent index/contract checks: all 100 prompt ids/paths exist, all word counts match current files, every prompt includes the source-lock/BOOK_SPEC/tracker contract, artifact/gate instructions are present, and each individual prompt appears exactly once in `ALL_100_PROMPTS.md`.
- Independent outline check: every chapter writing path matches its prompt; every chapter source path exists. All 91 original prompts are covered. Two appendix output-path mismatches are recorded below.
- Independent local Git link check: 1,494 source-link occurrences across pack text, 457 unique SHA/path targets and 683 commit-link occurrences resolve to local Git objects. Explicit line anchors are within their cited files. This establishes local object/anchor correctness, not network HTTP availability.
- Independent source-excerpt check: all six registry hashes and generated Go excerpt contents match exact locked line intervals. The extractor was read but not rerun, to keep this review read-only.
- `bash -n samples/runtime-boundary-lab.sh`: exit 0; syntax only. `python3 scripts/next_prompt.py` reports task 000 pending.
- Tracker inspection: exactly 100 rows; all statuses are pending. No book-production execution is falsely marked complete.
- `python3 scripts/check_manuscript.py --strict`: exit 1 with status incomplete; expected missing 40 chapters, six appendices and eight labs, zero narrative words. The separate sample is not counted as a complete chapter. This is the correct result for an unexecuted generation pack.
- Non-corpus artifact scan: no temporary scratch absolute paths found. Author/title/source metadata agree; publication metadata remains generation_pack, with null ISBN, page count and publication URL.

## Findings resolved by the main agent and independently rechecked

| Finding | Verified repair | Status |
| --- | --- | --- |
| Appendix C output mismatch | Outline/checker target is `manuscript/appendices/c-annotated-history.md`, matching prompt 062. | Resolved |
| Appendix D output mismatch | Outline/checker target is `manuscript/appendices/d-exercises-solutions.md`, matching prompt 063. | Resolved |
| Reasoning metadata differs | Prompts 077, 079, 080, 081 and index consistently recommend high; combined/index regenerated. | Resolved |
| Sample validation references old names | `validation/sample-static-review.md` names shipped `samples/runtime-boundary.md` and `samples/runtime-boundary-lab.sh`; old names absent. | Resolved |
| History seed names absent JSON | `editorial/PROMPT_HISTORY_SEED.md` references actual `evidence/prompt-commit-map.json`; absent scratch JSON name removed. | Resolved |
| Inconsistent writing_prompt representation | Chapters and appendices both use full relative writing_prompt file paths, each existing and matching its output contract. | Resolved |

Final recheck UTC: 2026-10-12T23:50:07.794253+00:00. `verify_pack.py` again exits 0; exact combined/index/outline/appendix checks pass with zero findings; all 100 tracker rows remain pending; sample Bash syntax again exits 0. The English README and START_HERE remain workflow instructions. No pack files were edited by this reviewer; only this external review report was updated.

## Truthfulness and chronology

The top-level README, AGENTS, specification, TOC, editorial brief and metadata clearly identify a generation pack with one sample. The sample lab's outputs remain expected, its application execution is unrun, and structural/Bash syntax checks are separately scoped. The source tree's development tracker is evidence of claimed progress and is not confused with the new 100-row tracker.

Retrospective prompt associations, late batched commits, design-only topics, MemoryService runtime ownership, unwired leadership/autoscaling, resource propagation, supplied-digest parsing, logical namespace limits, local storage and fake-load-test scope are required across the contract and review sequence. Historical links point to historical SHAs; current links use the locked HEAD. The old root docker-compose.yml path is retained only in historical evidence; current source is compose.yaml.

The history seed distinguishes 105 reachable commits from 99 first-parent commits and records 66 associated implementation/design/test commits. Local tags 0.1.0 and 0.3.0 are explicit; no 0.2.0 tag is invented. Exported GitHub release metadata provides publication times, separate from commit/tag dates. The 0.3.0 tag points to the formatting follow-up and HEAD to later documentation. The v0.1.0 CHANGELOG/date mismatch remains an explicitly reviewable historical fact, not a fabricated timeline.

**Limits:** this review inspected source evidence, pack contracts and structural consistency. It did not compile Go, run Docker/PostgreSQL labs, execute benchmarks, validate a completed manuscript, fetch every URL or inspect final PDF/EPUB/website behavior. Those future tasks remain mandatory under the supplied quality gates.


## Site-root adaptation review

The revised pack targets `alekpopovic/alekpopovic.github.io` at site contract SHA `80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`, with SITE as checkout root and BOOK as `books/inside-orch`. All 100 prompts contain the mandatory native execution context. Existing root instructions/scripts are preserved; canonical authoring and validation are book-scoped, and shared-site changes are explicitly identified. Go/Docker/PostgreSQL work is routed to disposable application copies rather than the Jekyll root.

The adapted validator passes 361 application files and 20 site-contract files. An independent byte comparison of all 20 copied site files against the inspected site checkout passes. The actual site checkout remains clean. This pack prepares future tasks; no site registration, post publication, main push or deployment has occurred.

`manuscript/Book.txt` has exactly 47 unique entries and matches the planned preface + 40 chapter paths + six appendix paths in order. Prompt 019 authors the real preface; numbered chapter and appendix clauses follow the site's actual H1 classifier. The native templates and selection contract acknowledge nested chapter/appendix paths rather than assuming Modern CI's flat selector can read them.

Prompts 091–094 address the actual source registry, explicit publisher call, bounded source selection, local-reference rewriting, companion traversal, EPUB map/cover convention, license-page inputs, canonical-folder exclusion, generated-copy ignore rules, source completeness, required posts, glossary, updates and native site checks. They preserve other books, existing reader layouts, analytics configuration, search/feeds, no-JavaScript/mobile/keyboard behavior and opt-in offline saving. They require concrete local validation and prohibit an implicit main push/deployment.

All three prepared posts have required front matter, `book_id: inside-orch`, real distinct chapter slugs 05/06/19, allowed illustrations and 514–574 prose words. No substantial paragraph is copied verbatim from the supplied sample. They are drafts under BOOK/publication/site-adapter/prepared-posts, not already-published site posts. Prompt 093 checks them against future completed chapters, chooses actual publication dates and copies canonical editorial sources only during final integration. It also adds the required glossary key/terms and stable update entry.

Native adaptation findings were sent to the main agent: explicit SITE-root helper commands and site-branch wording in BOOK AGENTS; fully prefixed START_HERE read command; final metadata synchronization to canonical book.json; and an explicit producer for the offline reader formerly created by replaced prompt 091. Those corrections have been inspected. Exact index/combined synchronization remains the final freeze check after editing prompts 086/095.

The strict future-manuscript gate now correctly reports 55 missing artifacts: one preface, 40 chapters, six appendices and eight labs, with zero completed narrative words. All 100 production tracker rows remain pending. Metadata remains generation_pack/planned until actual completion evidence justifies an edition. Source-reviewed sample, prepared posts and a section manifest do not establish completed manuscript or executed labs.
