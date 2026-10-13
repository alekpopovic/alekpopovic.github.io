# Edition quality gates

These gates apply to the future book. Delivery of this pack does not mean they have run.

| Gate | Required evidence | Blocker examples |
| --- | --- | --- |
| Baseline | 361 file hashes; 91 original prompts; 105 commit records; source lock | Moving source revision, altered evidence file |
| Provenance | Exact excerpt registry; commit diff/source anchors; all prompt relationships | Invented commit, mislabeled adaptation, retrospective execution claim |
| Capability | Code-first ledger with constructor/caller/side-effect traces | Memory state called durable, unwired package called active, absent enforcement promised |
| Chapter | 40 complete chapters; specific outcomes, failure window, lab, 3–5 solved exercises, references | Filler, missing prerequisites, unexplained failure recovery |
| Appendices | Six useful appendices aligned with chapter definitions | Repeated unverified docs dump, missing worked answers |
| Examples | Exact source or independently tested extension; actual command/log evidence | Pseudocode claimed executable, copied output, unregistered adaptation |
| Labs | Eight isolated lab scenarios, actual logs, scoped cleanup, observed results | Skipped external suite hidden, production database used, unrun expected output called measured |
| Semantics | State/atomicity/fencing/isolation/resource limits accurately scoped | Exactly-once or zero-downtime claim without mechanism and tests |
| Review | Developer, DevOps, architect and security review with resolved findings | Major findings unresolved or hand-waved |
| PDF | All-page render inspection, functioning links/bookmarks, correct final content | Clipped code/table, tiny type, overlapping text, incorrect metadata |
| EPUB | EPUBCheck or explicit blocked gate, structure/link checks, actual reading preview | Missing spine chapter, inaccessible diagrams, false compatibility claim |
| Online | Complete reader navigation/search/mobile/keyboard checks | Missing chapters/downloads, guessed website schema, stale offline cache |
| Rights | Author/provenance/notices and explicit chosen publication terms | Unlicensed material relabeled, invented ISBN/endorsement |
| Release | Exact final hashes, reproducible inputs, truthful status, reviewable handoff | Old artifact validated then changed; pending work labeled complete |

Structural validators in this pack are deliberately limited: they catch missing files, altered corpus bytes and incomplete chapter records. They cannot certify technical truth, security or a polished layout. Human source review and actual experiments remain required. Missing tooling is reported as blocked, with a useful independent task continuing where possible.

## Verification record

Use `templates/verification-record.json`. Store the complete command, working directory, source SHA, tool versions, prerequisites, UTC start/end, exit code, sanitized output/log path and scope. Distinguish passed, failed, blocked, not_run and inspected. Inspect a suite's skip output and environment gates. Never claim all migrations tested merely because a fixture applied the initial migration.

## Critical review scenarios

- New default server process after a service/namespace was created.
- Ordinary service assignment compared with scheduler.Plan fixtures.
- Resource limits traced from YAML to DTO to Docker HostConfig.
- Two servers with independent MemoryService state.
- Advisory lock cancellation and failed unlock using actual PostgreSQL sessions.
- Worker partition after stateless replacement: late containers remain live without fencing.
- Partial GitOps apply, pruning ownership and path boundaries.
- Job retry/cron semantics and all-namespace controller behavior.
- Local volume claims after worker loss.
- Default green test suite with external tests skipped.
