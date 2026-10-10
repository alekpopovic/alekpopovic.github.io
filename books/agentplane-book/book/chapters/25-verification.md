# 25. Build Evidence for Every Important Claim

**Part VII — Product and Operations**

A demonstration answers whether one path worked once. Verification asks whether
the implementation preserves a stated property across valid, invalid and
interrupted paths. AgentPlane needs both. A product demo makes the system
understandable; a verification record determines what a maintainer can honestly
claim about it.

## Classify evidence before collecting it

Keep four evidence classes separate: static review, local unit tests, component
integration tests and deployment acceptance tests. A Go state-machine test cannot
prove that a CNI enforces egress. A rendered Helm chart cannot prove that an
admission controller rejects a privileged pod. A scanned container is not proof
that its runtime cannot escape.

The companion repository runs small offline examples. SQL and Kubernetes labs
are procedures for an isolated environment, not implied successful experiments.
The validation report is a statement about specific commands in this edition.
Readers should create their own report after changing dependencies or deploying
to another cluster.

## Turn invariants into hostile tests

For each invariant, specify an attempted violation, expected observation and
measurement location. Consider: tenant A must not operate on tenant B's session.
Test reads, writes, batch requests, event subscriptions, download links, cached
objects and background jobs. The HTTP list endpoint is only one access path.

For command deduplication, run the handler twice, restart the handler between
attempts, change the payload while keeping the ID and lose the result after an
external effect. The last case cannot always be solved by another retry. A
correct implementation may expose an unknown outcome and require reconciliation.

## Test concurrency intentionally

A quota test with sequential requests does not test a quota race. Start more
concurrent reservations than the configured limit. Assert the final count, the
number of successes and the behavior of duplicate operation IDs. Release each
reservation twice and verify that the counter never becomes negative.

For approvals, two consumers should compete for the same approval. Only one
consumption may succeed. However, successful consumption still does not establish
exactly-once behavior at the downstream tool. Test that distinction explicitly so
future refactoring does not turn an uncertain effect into a blind retry.

## Fault injection needs an ownership boundary

Use a disposable cluster with an unmistakable context name. Before deleting a
pod or interrupting a dependency, assert the context and namespace. Never infer
that the current context is safe because the script lives in a directory called
`test`. Destructive tests should require a separate, explicit opt-in.

Interrupt the connector, worker, gateway and broker at different points. Record
whether intent was committed, whether the command was accepted, whether the
execution began and whether the final result was stored. Those observations help
locate the real ambiguity window.

## Measure with a workload description

Publish the machine, runtime versions, topology, request distribution, payload
sizes, concurrency, duration, warm-up and error criteria with a benchmark. A
single mean hides tails and excludes failed requests unless stated otherwise.
Record queue latency, provisioning latency and execution latency separately.

Do not transfer a local laptop result into a production capacity claim. Treat
capacity planning as a hypothesis refined by representative experiments. Include
resource ceilings and the cost of observability, metadata storage and idle warm
capacity when evaluating throughput.

## Decide what blocks a release

A release gate should be a small set of mandatory properties, not a wall of green
badges. Tenant isolation, credential protection, policy enforcement, safe retry
behavior and restore discipline deserve blocking tests. Cosmetic checks can be
useful without being confused with security assurance.

A failed mandatory check means the candidate is not ready for that advertised
scope. It does not mean all progress is worthless. Publish an accurate private
beta limitation or reduce the feature's availability rather than rewriting the
report to match the desired release date.

## Exercise

Choose five claims from the product homepage you would write for AgentPlane.
For each, identify the strongest available evidence and one counterexample the
test suite does not cover. Rewrite any claim that exceeds its evidence. Include
one claim about data location and one about recovery.
