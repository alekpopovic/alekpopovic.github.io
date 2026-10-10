# 18. Test behavior at the boundary where it matters

## A useful test can falsify a claim

A test that repeats an implementation's constants is weak evidence. A test that retries the same event and observes no additional decision checks a real invariant. A test that injects a persistence failure and observes the old published state checks the acknowledgement boundary. Design tests around observable outcomes and failure mechanisms.

The companion's core tests cover duplicate and conflicting events, stale and future observations, guard-feedback exclusion, exact IPv4 and IPv6 behavior, monitor/enforce/revoke transitions, allowlist precedence, TTL expiry, refresh without extension, invalid signatures, epoch mismatch, stale revisions, equal-revision conflicts, malformed JSON, excessive input, restart, and concurrent checks.

Live loopback tests cover authenticated HTTPS push, acknowledgement identity, certificate-derived ingestion identity, missing client certificates, wrong-role certificates, and authorization routes that cannot mutate policy. The Unix-socket route test is explicitly skipped in the preparation environment because AF_UNIX creation is prohibited there. Run it without that skip on a Linux deployment host.

## Keep evidence levels separate

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| Core policy test | Function and state semantics | Nginx route coverage |
| Live mTLS test | Transport and role boundary | Production certificate lifecycle |
| Unix socket test | Local handler transport | Filesystem policy for all host users |
| Nginx integration test | Access-phase behavior | Fleet delivery reliability |
| Collector rotation test | Tested file/buffer topology | Unlimited outage tolerance |
| Load measurement | Recorded host/workload performance | Performance on every deployment |

One test can be valuable without proving the entire system. The mistake is attaching a larger claim to it than the observed behavior supports.

## Build the Nginx acceptance matrix

Test ordinary requests, special routes, named locations, redirects, static resources, existing authentication, and `satisfy` combinations. Confirm that a denied request never reaches the protected upstream. Confirm that permitted POST requests preserve their bodies. Confirm that application 403 and 500 responses are not confused with guard outcomes.

Kill the local agent and observe the public result under the chosen availability profile. Kill central services while leaving the agent live and verify local expiry. Spoof forwarding and guard headers from an untrusted client. Rotate logs while traffic continues. Restart the collector with pending records and compare unique generated request IDs.

These are deployment tests, not extra unit tests of a configuration string. The original pack's acceptance documents define the milestones and evidence expected from the real system.

## Test recovery, not only failure

After an outage, restore transport and check that stale log replay does not create fresh bans. Reconcile a newer policy and verify that old pending deliveries cannot restore a revoked decision. Restart an agent from saved state after envelope delivery expiry while a decision remains live. Restore central storage behind the edge's high-water mark and observe rejection instead of silent rollback.

Recovery paths often exercise a different state sequence from initial startup. A successful cold demo does not cover them. Use deterministic fixtures where possible so the test can identify whether a failure concerns time, ordering, or data identity.

## Record the environment

A useful verification record includes interpreter or compiler version, dependency version, operating system, configuration digest, workload, command, result, skipped cases, and limitations. For a performance claim, add hardware, concurrency, duration, distributions, and baseline conditions. Do not substitute a target number for measured evidence.

The delivered `verification/python-tests.txt` is an actual command log. The release report identifies unexecuted services. Updating the manuscript should regenerate its evidence after meaningful code changes rather than preserving an old green result beside new source.

## Exercise

A pull request changes only the fail-open Nginx profile. Existing Python policy tests all pass. Is the change sufficiently verified?

## Answer

No. The concrete remaining risk is Nginx's internal error routing and preservation of the main request. Run actual Nginx tests for backend availability errors, real 403 denial, application errors, and POST method/body behavior under that profile. Broader unrelated tests would not resolve the missing evidence.
