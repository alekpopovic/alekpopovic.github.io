# 13. Make expiry work without the central server

## Two clocks, two purposes

Wall time connects a policy to its UTC issuance and expiry. A monotonic clock measures elapsed time within one running process. Wall time can move because of a synchronization correction or a configuration mistake. Monotonic time does not provide a timestamp you can carry across a restart.

When accepting a ban, the lab computes a local monotonic deadline from its remaining wall-time lifetime. A check requires both wall-time and monotonic conditions to say that the decision is active. If the wall clock moves backward, the monotonic deadline prevents a running process from extending the ban indefinitely.

This is a useful local safeguard, not a complete time-service implementation. The lab also compares elapsed wall and monotonic time against an anchor and returns unavailable after a large divergence. A production agent needs monitored time health and a documented recovery policy. Simply having two clocks does not prove that the initial wall time was correct.

## Envelope freshness is not ban lifetime

An envelope may be eligible for delivery for two minutes. A contained decision may last fifteen minutes. The delivery interval limits when a new policy can be accepted. It does not invalidate already applied state at minute two. On restart, a saved signed policy can still contain a live decision even though its original delivery interval ended.

Conversely, creating a fresh envelope does not extend a decision. The ban's original expiry is carried forward. Reissuing the same address under a new decision ID is a new decision, with a separate detection and operator policy. It must not occur as an accidental side effect of delivery retries.

The test suite advances an injected clock without sleeping. It checks local expiry, refresh without extension, restore after delivery expiry, and unavailability after backward wall-time movement. These tests are deterministic because they do not depend on a fifteen-minute real wait.

## Restart with uncertainty

After a restart, the monotonic clock has a new origin. Reconstruct remaining lifetime only when wall time is trustworthy. The production design requires unavailable state and an alert if time health cannot establish remaining TTL safely. Central reconciliation can provide new policy, but the edge still needs a credible time basis for independently enforcing maximum lifetimes.

The compact Agent accepts a supplied clock and rejects saved policy issued too far in the future. It cannot independently certify NTP health. That responsibility belongs to deployment supervision or a fuller production agent. Do not convert the injected-clock tests into a claim that all host clock failures are handled automatically.

## Local policy precedence

Emergency bypass and locally provisioned emergency addresses come first. They exist so that an operator can recover a host even if a remote policy is harmful. Central exact-address allowlists come next. Active decisions are evaluated only after those exemptions. Monitor mode records a would-block rather than denying.

The lab exposes a process-local bypass flag for testing, not an unauthenticated network mutation endpoint. Production operations should expose a controlled local mechanism with ownership, audit, and visible health state. A forgotten bypass is a security configuration change that should remain obvious to operators.

## Prune without requiring delivery

Request checks ignore expired bans even if their entries remain in the saved policy. Background pruning can reduce memory and clean derived indexes, but expiry correctness must not depend on a successful pruning thread or a new central snapshot. This makes the behavior robust during network outages and scheduling delays.

An agent also needs limits on active policy size. Full snapshots simplify ordering at the cost of payload and memory use. The teaching limit is deliberately smaller than the source pack's production target. Measure both serialization cost and request-view size before increasing it.

## Exercise

Stop the delivery process after applying an enforced decision. Advance the test clock to its expiry. Then try a wall-clock correction backward while leaving the monotonic clock unchanged. What are the distinct expected outcomes?

## Answer

At ordinary expiry the address is allowed. After a large clock divergence, the lab reports unavailable because time health is uncertain. The deployment's Nginx availability profile decides how an unavailable guard affects the public request. Expired policy and unhealthy time should have separate metrics so operators do not mistake a clock incident for a normal ban ending.
