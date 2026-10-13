# Inside orch — exact local edition gate

passed_local_edition_gate at 2026-10-13T04:18:21.013663+00:00.

Source `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`;40chapters,6appendices,preface;101,211meaningfulwords;546PDFpages;8actuallyexecutedboundedlaboratories.

PDF SHA256 `a734dd82a27fde589fd81cf9755693401f8b1abbe9a055d1ebe2e482916caee3`; EPUB SHA256 `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`.

The machine record [release-gate.json](release-gate.json) records every joined evidence hash, tracker-evidence path, exact export-input check, executed corpus/strict command and archive checksum result. A done tracker value was never accepted as sole proof.

## Critical boundaries

- Default MemoryService is process-local; PostgreSQL schema/store is not the active server state owner.
- Ordinary assignment is distinct from optional scheduler.Plan/store reconciler; task CAS is not a global resource fence.
- Ordinary resource values do not reach AgentTask/ContainerSpec/HostConfig; direct adapter limits and volume eligibility are distinct.
- Desired stop accounting, rollout success and drain completion can precede physical stop; partitions have no network fencing.
- HA advisory-lock cancellation can retain a pooled-session lock; HA/autoscaler packages are not wired default leadership.
- GitOps applies are partial; logical namespaces/local volumes are not hostile kernel isolation/distributed storage.
- Image digest parsing is not enforced supply-chain verification; plugins/billing/overlay designs remain proposals.
- The original PostgreSQL fixture still has two failures from its fourteen-migration setup; the separately labelled full-sixteen-schema extension passed.
- Baseline six external skips, fake-load measurements and optional unrun procedures remain explicitly scoped.

## Remaining limitations and publication boundary

- Local reviewable edition only: no push, PR, default-branch publication, live deployment or production fitness certification.
- Source/engineering/visual review was performed by AI agents with independent lenses; no external human endorsement is invented. Owner review remains the publication handoff.
- Browser evidence is actual installed Chrome on Linux; no proprietary e-reader or Safari/Firefox hardware compatibility claim.
- Full UI run had151passes/one stale five-book assertion; corrected six-book test passed separately. This is152distinct test coverage, not a fabricated zero-exit full rerun.
- All546 final PDF rasters match the actually reviewed edition; rebuilt PDF byte hash differs. No bit-for-bit PDF rebuild promise.
- Source/reader archive validation metadata is a timestamped snapshot; later gate/review records are carried separately in the final handoff.

## Decision

Ready for independent skeptical-reader review097 and a local release handoff; no deployment authorization.

Blocking findings: none.
