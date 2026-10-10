# Appendix C. Review Answers and Failure Scenarios

These notes are discussion guides, not a claim that only one architecture is
correct. A sound alternative identifies its assumptions and verifies its own
invariants.

## Why is an outbound connector still powerful?

Because a connection initiated inside the cluster can still carry commands from
the SaaS to the cluster. Direction controls reachability, not the authority of
messages after connection establishment. Constrain the command vocabulary,
identity, references, local policy bounds and workload lifetime independently.

## Why can RLS tests pass while isolation remains weak?

Tests may use the wrong database role or omit writes and association attacks.
An application role capable of changing tenant context is not a cryptographic
boundary against arbitrary SQL execution. Composite references, parameterized
queries, scoped caches and authorization checks address different failures.

## What happens after execution but before the result is saved?

The system may not know whether an effect happened. A durable execution identity
at the recipient can allow reconciliation. Without that support, a retry may
repeat the effect. Expose unknown outcome and resolve it through an explicit
procedure instead of claiming transport deduplication solved the problem.

## Does one approval authorize any retry?

No. Approval should bind the exact operation and inputs, with an expiry and
policy revision. A separate downstream idempotency contract determines whether
repeating the attempted effect is safe. A tool with no deduplication support
cannot inherit exactly-once semantics from the approval database.

## Does deny-all override every NetworkPolicy allow rule?

Not in the ordinary additive allow model of standard NetworkPolicy. Evaluate all
policies selecting the workload and prevent unreviewed broad grants. Ensure the
actual network implementation enforces the rules. A manifest by itself is not
proof of packet behavior. See [S04](../references.md#s04).

## Can a hash chain prove an audit log was not rewritten?

Only within its trust model. An attacker able to rewrite every record can also
recompute an unanchored chain. An independently protected checkpoint makes such
rewrites detectable relative to that checkpoint. Confidentiality, durable storage
and access controls remain separate properties.

## Can restoring an old database restore revoked access?

Yes, if restored authorization records are treated as current. A recovery plan
must reconcile revocations, active epochs, approval consumption and external
effects before reconnecting live workloads. An independent revocation record or
controlled re-enrollment procedure may be required.

## Where can customer data still reach the SaaS?

Output relay, file transfers, diagnostic bundles, tool arguments, telemetry and
exports are all possible paths. A policy of not fetching secret values from a
provider does not prevent a process from printing one. State default retention,
processing locations and optional direct-data-plane modes honestly.

## When should a feature be disabled?

When its mandatory enforcement capability is missing or cannot be verified.
Offer an explicit development-only mode only with a different assurance label.
Do not quietly replace gVisor with a default runtime or FQDN enforcement with an
unrestricted route while retaining the same product claim.
