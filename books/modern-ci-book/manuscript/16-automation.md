# 16. Integrate source events, schedules, and matrices


## Keep trigger intent explicit

A run may be requested manually, by a push, by a pull-request event, by a schedule, or by another controlled automation. Record trigger kind, source identity, requester, event identity, and the policy decision. These fields help explain why a run exists and which restrictions applied.

A GitHub App integration should request only the permissions needed for repository discovery, source access, and status reporting. Keep installation identity separate from a human user's login identity. Revoking a user's access and uninstalling the integration are different lifecycle events. Handle both rather than treating the first successful OAuth or installation flow as permanent authorization.

Deduplicate provider deliveries using their delivery identity, as Chapter 8 describes. A manual rebuild of the same source commit is still a distinct intent when it uses a new idempotency key. Do not collapse the two through a global “commit already built” flag.

## Pull requests are a policy boundary

The same project may contain trusted branch builds and less-trusted contribution builds. Decide which source revision is tested: the contributor head, a provider-created merge revision, or a locally constructed merge. Record both the requested references and the actual checked-out commit. This is essential when a branch changes while a run waits in the queue.

Do not combine privileged workflow context with untrusted checked-out code. GitHub's secure-use reference discusses the hazards of privileged triggers and self-hosted execution. In Modern CI, the server must enforce the permitted pool, credential set, and cache namespace independently of the contributor's YAML. [S17](e-sources.md#s17)

A status check belongs to a specific run and commit. Give it a stable external identity for update retries. When an older run finishes late, update its own check rather than whichever check is currently most recent for the branch.

## Schedule occurrences, not timer callbacks

A scheduler process can restart, overlap with another instance, or miss a timer while the database is unavailable. Persist each schedule's timezone, expression, next intended occurrence, and catch-up policy. Use a unique occurrence identity such as schedule ID plus the scheduled UTC instant.

When daylight-saving rules produce a repeated local time, the design must specify whether both instants run. When a local time does not exist, it must specify whether the occurrence is skipped or moved. Do not let the behavior depend accidentally on which host happened to run the callback.

On recovery, apply a bounded catch-up rule. A monthly administrative job may need one missed occurrence; a job scheduled every minute should not necessarily flood the queue with thousands of runs after a long outage. Make the policy visible to operators and preserve skipped occurrences as meaningful scheduling decisions where required.

## Expand matrices before dispatch

A matrix creates multiple concrete jobs from declared dimensions. Calculate its maximum expansion before allocation and reject excessive size. Include each dimension combination in the compiled identity so its logs and artifacts cannot collide with another member.

Define aggregate success carefully. A cancelled member, an allowed-to-fail member, and a member that never started are not necessarily equivalent. A fail-fast policy may request cancellation of remaining members, but their physical termination still follows the normal runner protocol.

Reusable templates should be resolved to immutable versions when compiling the run. Avoid a template branch that changes silently between two jobs in the same run. Store a receipt of template source and resolved inputs alongside the frozen plan.

## Exercise

Two scheduler instances wake after an outage and each calculates that the 09:00 occurrence was missed. What durable key prevents duplicate scheduled runs, and why is a process-local mutex insufficient?

## Worked answer

Use a unique database key based on schedule identity and the intended occurrence instant, within the transaction that creates or enqueues the run. A process-local mutex coordinates only threads in one process and vanishes on restart. Both instances can legitimately calculate the same missed occurrence; only the durable uniqueness rule resolves which one creates it.

## Completion evidence

Test duplicate event delivery, changed branch heads, revoked installations, restricted pull-request execution, repeated and nonexistent local times, bounded catch-up, matrix limits, and out-of-order status updates.
