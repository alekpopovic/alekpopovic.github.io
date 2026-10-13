# Final skeptical developer review

Accepted for a local, reviewable edition after the actual 096 gate. No new blocking developer finding. Source revision `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`; PDF `a734dd82a27fde589fd81cf9755693401f8b1abbe9a055d1ebe2e482916caee3`; EPUB `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`; source ZIP `052901306f6e0b0073f45752193879df6f8c7bf88b46251f43d03c87a8699e06`.

This is a distinct developer lens, not an external endorsement. I authored Chapters 1–8 and 33–40; checks of those chapters are self-review. I independently reviewed Chapters 17–24 and Appendix D earlier, and this final pass deeply reread cross-author Chapters 9, 10, 27 and 30, their relevant answers, critical passages in Chapters 19, 34 and 37, exact current code, existing raw observations, examples guidance and reproduction instructions. The complete 40-chapter heading/claim/listing inventory and current source/input hashes are retained in the JSON. A fresh line-by-line reread of all prose or new execution of all programs is not claimed.

## Adversarial checks

### DEV97-01 — Put two default servers behind one load balancer and interpret readiness as shared durable state.

Chapter34 explicitly rejects two memory servers as HA; Chapter09 requires a new durable composition, not a constructor substitution.

Claims: `ch06.active-memory`, `ch06.restart`, `ch09.composition`, `ch34.default`. Direct code: `evidence/orch/cmd/orch-server/main.go:142–148`, `evidence/orch/internal/controlplane/controlplane.go:279–307`. Actual retained records: `validation/labs/ch06/combined-restart.json`.
Two simultaneously load-balanced servers were not executed. Their independent maps follow inspected constructors; the actual restart experiment is deliberately manual container association, not agent adoption.

### DEV97-02 — Use one successful task CAS to claim that two schedulers cannot overcommit different tasks or host ports.

Both chapters explicitly distinguish per-task ownership from cross-row CPU/port reservation and warn that ordinary immediate placement bypasses Plan. Worked answers identify the same predicates and limitation.

Claims: `ch09.assignment`, `ch09.transaction`, `ch10.claim`, `ch10.active-path`. Direct code: `evidence/orch/internal/store/postgres.go:892–936`, `evidence/orch/internal/scheduler/scheduler.go:170–218`. Actual retained records: `validation/intake/full-schema-recovery-corrected.json`, `validation/labs/lab02-concurrent-claims.json`.
No global reservation implementation or live two-planner overcommit experiment was invented; the broader race is source-derived analysis.

### DEV97-03 — Partition a worker, reschedule its stateless task, and infer that the old container has stopped.

Chapter19/37 distinguish server authority from host reality and eventual cleanup from fencing; stateful work and local volumes are kept separate.

Claims: `ch19.cutoff`, `ch19.drain-complete`, `ch37.return-cleanup`. Direct code: `evidence/orch/internal/controlplane/controlplane.go:681–699`, `evidence/orch/pkg/types/lifecycle.go:269–275`, `evidence/orch/internal/agent/agent_test.go:446–472`. Actual retained records: `validation/labs/ch37/fault-tests.json`, `validation/labs/03-check.json`.
No real network partition or simultaneous request-serving overlap was executed by this review. Fake cleanup is not network or disk fencing.

### DEV97-04 — Accept 250m/128Mi and cite direct Docker adapter support as proof that the ordinary agent enforces limits.

The book traces both missing data boundaries rather than assigning planner or direct-adapter guarantees to ordinary deployment. Requested accounting is distinguished from runtime measurement.

Claims: `ch05.resource-gap`, `ch06.envelope`. Direct code: `evidence/orch/internal/controlplane/controlplane.go:130–137`, `evidence/orch/internal/agent/agent.go:253–265`, `evidence/orch/internal/docker/docker.go:430–442`. Actual retained records: `validation/intake/docker-resource-boundary-corrected.json`, `validation/intake/docker-resource-boundary-corrected.stdout.txt`.
Cached-image/owned-ID teaching guards and no host-published workload ports are recorded; no production-kernel isolation certification.

### DEV97-05 — Restart during rollout or report deployment success and infer fresh-process persistence and physical stop completion.

Final Chapter 17 now explicitly says the next pass uses desired/store accounting before physical acknowledgement. Chapter37 names the retained-store test and separate fresh-process experiment.

Claims: `ch17.stop-limits`, `ch37.controller`. Direct code: `evidence/orch/internal/e2e/chaos_test.go:41–61`, `evidence/orch/pkg/types/lifecycle.go:269–275`. Actual retained records: `validation/labs/lab04-rollout-observed.stdout.txt`, `validation/reviews/ch17-independent-stop-accounting.json`.
The earlier overstatement was corrected before final formats and is independently visible in current text. No restart-during-real-production-rollout experiment claimed.

### DEV97-06 — Make the second sorted GitOps manifest invalid and assume a failed sync means the first service is unchanged.

Chapter30 walks exactly this failure: first mutation remains, LastError changes and LastRevision can still be the prior successful revision. The actual fresh Lab07 partial-apply assertion passed. Prune is explicitly a previous-name set, not a current stable ownership predicate.

Claims: `ch30.apply`, `ch30.drift`, `ch30.prune`. Direct code: `evidence/orch/internal/gitops/gitops.go:218–280`, `evidence/orch/internal/gitops/gitops.go:284–289`. Actual retained records: `validation/labs/review076/07-command.stdout.txt`, `validation/labs/07-check.json`.
Real local Git/in-process application methods; no external repository, daemon workload or repository-wide transaction.

### DEV97-07 — Cancel an advisory-lock lease, observe Done closed, and immediately allow a successor to assume the database lock and all old effects are gone.

Chapter34 explains pooled connection release versus session unlock and the Done-closed fast path. Cooperative callback cancellation, in-flight effects and absent default leadership wiring remain separate.

Claims: `ch34.session`, `ch34.wrapper`, `ch34.default`. Direct code: `evidence/orch/internal/leadership/postgres.go:67–109`. Actual retained records: `validation/intake/full-schema-recovery-corrected.json`, `validation/labs/ch34/leadership-tests.json`.
Observed package behavior on the owned PostgreSQL fixture; not a running replicated server or physical workload fencing demonstration.

### DEV97-08 — Treat the baseline 447 passes as evidence that the guarded database suite passed, then silently repair its fixture to get green results.

The final narrative and gate retain all skips and original database failures; separate full-schema teaching execution never overwrites that baseline.

Claims: `ch09.fixture-schema`, `ch36.fake-e2e`, `ch40.ci`. Direct code: `evidence/orch/internal/store/postgres_test.go:556–590`, `evidence/orch/migrations/000016_operations_safety.up.sql:1–8`. Actual retained records: `validation/intake/orch-baseline-tests.stdout.txt`, `validation/intake/postgres-store-owned.json`, `validation/intake/full-schema-recovery-corrected.json`.
This final review inspected existing raw records; it did not rerun destructive database tests or relabel their outcomes.

## Findings and followability

The prior material Chapter 17 stop-accounting overstatement is resolved in final canonical text. Desired stopped/removed tasks leave active accounting before physical acknowledgement; the actual rollout can succeed with one pending stop. The final chapter, source predicate and timeline agree. Its original independent correction record remains available. No canonical text or formats were changed during this final review.

The strongest teaching feature is the separation of a local computation, a persisted claim and an observed runtime effect. The worked answers retain those distinctions rather than repeating a general reliability claim. Listings can be followed using their immutable containing-package links and registered original overlays; `examples/README.md` makes the missing standalone package/import context explicit. `publication/REPRODUCE.md` clearly separates the source ZIP from a full application/site checkout.

Remaining limits are explicit: optional procedures are expected until run, fake cleanup does not prove network fencing, lexical GitOps path validation is not a tested hostile-filesystem sandbox, source fragments need their containing package, and PDF reproducibility means validated content rather than byte-identical future rendering. No new database/Docker experiment or format build was needed because this review found no new material defect.

Detailed evidence hashes, exact current source spans, all 40 chapter claim/listing coverage, eight concrete adversarial dispositions, current archive hashes and reviewer ownership are in `final-reader-developer.json`. Root must aggregate the other two independent lenses before closing 097 and preparing 098/099; deployment remains unauthorized.
