# 1. Understand the feedback loop

## Start with the event that actually exists

Imagine that a client requests five nonexistent paths from your application. Nginx proxies each request, the application returns 404, and Nginx writes an access record. An analyzer can now see five completed observations. It cannot travel backward and prevent those requests. Its first useful action affects a later request from the same address.

That timing determines the system's scope. Access-log analysis can interrupt repeated activity after evidence accumulates. It does not inspect a request before it starts, and it does not terminate an already established stream. A slow response delays the corresponding access event. A long-lived connection may not produce its terminal record for a long time. Network capacity can be exhausted before this application-level loop has enough evidence.

Instead of promising instant protection, define a measurable reaction interval. Start it when the detector has enough eligible events to create a decision. End it when the edge has persisted and published the policy containing that decision. Separately measure the delay from request completion to ingestion. Those two intervals reveal whether collection or control delivery is the bottleneck.

## Three different things called a block

An IP decision in a database is desired state. A signed message containing it is delivery state. A revision published by an agent is applied state. Calling all three "blocked" makes an operator dashboard misleading. A central service can create a ban while an edge remains disconnected. An HTTP sender can finish transmitting while the receiver rejects an epoch mismatch. An agent can accept a policy whose decisions are already expired.

The first vocabulary rule is to name the state precisely. A decision may be active centrally and unapplied locally. A delivery may be pending, retrying, or acknowledged. A local policy may be applied, but contain no active bans. The edge's answer to a real check is the ultimate observation of request-time enforcement.

The laboratory exposes this distinction in its demo:

```bash
cd companion
python3 -m logbranik demo
```

The command prints an initial allow, an ingestion result, a monitor outcome, an enforcement outcome, and an allow after revocation. It uses a temporary directory and generated keys, so it does not alter an existing Nginx configuration or retain credentials after completion.

## The two paths

The request path contains Nginx, a local authorization check, and the protected application. It should remain usable when the central analyzer is unavailable. The analysis path contains logs, transport, storage, detection, and policy delivery. It is slower, retryable, and permitted to touch disks and databases.

Moving a database query into every authorization check joins those paths. A database maintenance operation then becomes an application outage. Moving signature verification into every check creates unnecessary CPU work and makes verification latency part of every request. Perform those operations when a policy changes. Publish a complete in-memory view afterward.

The architecture diagram in the exported edition shows both paths. Arrows represent actual information transfers, not an assumption that all transfers succeed. Every arrow across a machine boundary needs authentication, a maximum size, a timeout, and a definition of success.

## Write the first invariants

An invariant describes behavior that must remain true despite retries and failures. For this system, expired decisions must stop denying requests even while central services are offline. A replayed older policy must not resurrect a revoked decision. A collector must not choose another node's identity by putting it in a JSON field. A repeated event must not be counted as additional evidence. A lost acknowledgement must not force a decision's lifetime to restart.

These statements are more useful than a feature list because they tell you what to test. "Supports retries" says little. "An exact duplicate policy returns its existing acknowledgement without reapplying or extending bans" defines a reproducible behavior.

## Exercise

Write a timeline for five suspicious requests, an event retry, a central decision, a failed delivery, and a later successful delivery. Mark the earliest request that could be denied. Which interval should an operational alert measure?

## Answer

The five original requests finish before their access observations exist. A retry adds no evidence after deduplication. The earliest denied request is one arriving after the agent has published the policy, assuming the site is in enforce mode and the decision has not expired. Alert on excessive desired-to-applied delay and on collection lag independently. Combining both delays into one number hides the failing component.
