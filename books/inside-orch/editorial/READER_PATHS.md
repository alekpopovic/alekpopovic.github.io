# Reader paths through one inspectable system

Shared foundation: **01 → 02 → 04 → 05 → 06 → 03**. Learn the state model and MemoryService boundary before starting or judging the default binary. Appendix prerequisites may be consulted without implying a feature is integrated. Every sequence below is a valid topological order of the dependency graph in [Learning objectives](LEARNING_OBJECTIVES.md). All40 chapters are assigned; overlap is deliberate.

## Developer

01 → 02 → 04 → 05 → 06 → 03 → 07 → 08 → 09 → 10 → 11 → 13 → 12 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 23 → 24 → 25 → 26 → 27 → 28 → 22 → 29 → 30 → 31 → 32 → 33 → 34 → 35 → 36 → 37 → 38 → 39 → 40

Focus on typed contracts, fields crossing interfaces, deterministic algorithms and independently tested extension seams. The broader prerequisites are retained because skipping them would hide a reliability boundary.

## Devops

01 → 02 → 04 → 05 → 06 → 03 → 07 → 08 → 09 → 10 → 11 → 13 → 12 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 23 → 24 → 25 → 26 → 21 → 27 → 28 → 22 → 29 → 30 → 31 → 32 → 33 → 34 → 35 → 36 → 37 → 38 → 39 → 40

Focus on explicit process/container ownership, operational observation, safe failure injection and recovery boundaries. The broader prerequisites are retained because skipping them would hide a reliability boundary.

## Architect

01 → 02 → 04 → 05 → 06 → 03 → 07 → 08 → 09 → 10 → 11 → 13 → 12 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 23 → 24 → 25 → 26 → 21 → 27 → 28 → 22 → 29 → 30 → 31 → 32 → 33 → 34 → 35 → 36 → 37 → 38 → 39 → 40

Focus on live state ownership, durable concurrency, composition, resource enforcement and the limits of fencing. The broader prerequisites are retained because skipping them would hide a reliability boundary.

## Checkpoints and optional deeper branches

| Checkpoint | Evidence to produce | Editorial time estimate |
| --- | --- | --- |
| Foundation01–06 | Pinned SHA, runtime/package diagram, parsed Atlas manifest, fresh-process state-loss prediction | 4–6 hours |
| Execution07–19 | DTO propagation trace, one exact lifecycle guard, IDs/logs for deployment and agent/container adoption | 8–12 hours |
| Isolation20–29 | Endpoint trace, policy/quota rejection and explicit limits/fencing caveat | 7–10 hours |
| Advanced30–35 | Partial GitOps apply, finite job identity, local storage boundary and two-session lease result | 6–10 hours |
| Verification36–40 | Named fake versus real experiments, measured telemetry scope and reviewable release checklist | 5–8 hours |

These are planning estimates, not measured reader completion times. Additional optional branches are packet-level ingress/overlay design after20/26, custom adapter implementation after33, and a bounded benchmark after39. They never replace the core resource propagation05/26, persistence06/09, or fencing19/34 chapters. Full numerical chapter order remains useful as a reference, but follow dependency order when running labs.

The running example is **Atlas API**, stable service name `atlas-api`, plus finite job `atlas-count`. Labs mutate the same service through deploy/scale/rollout/rollback, drift, node loss and isolated GitOps. A new execution gets a unique run namespace; evidence records IDs so a later run never assumes an old object still exists. [Case study](../labs/CASE_STUDY.md) defines all eight stages, expected observations and cleanup.

Readers can use plain Markdown links and tables without JavaScript. Navigation labels name chapters and outcomes, not unexplained icons; online controls must remain keyboard operable. Optional branches are pedagogical choices and not maturity badges.
