# 10. Build a detector you can explain

## Begin with a narrow rule

The laboratory rule counts distinct paths that returned 404 from one site and one address in the last sixty seconds. At five distinct paths it creates a fifteen-minute decision. Those numbers are teaching defaults, not universal threat thresholds. A normal browser can encounter several missing assets after a broken release. A search engine may revisit old links. A customer behind a corporate proxy may share an address with a crawler.

The point of the rule is to make the decision observable. An operator can inspect the paths, times, address, and rule version. A more complicated rule without explanations is harder to calibrate and harder to revoke confidently. Add complexity after you can reproduce both valid and false-positive cases.

The lab deliberately excludes unknown and guard-generated outcomes. Only an allowed request contributes to the demonstration's evidence. This is conservative: an unavailable guard or an uninstrumented route should not silently become the same trusted observation as an allowed protected request.

## Event time and processing time

Event time says when the request completed. Processing time says when the analyzer receives it. A collector outage can separate them by hours. If the detector uses processing time for every arriving event, restoring a collector can turn old traffic into a new ban.

The teaching implementation stores old events but permits a fresh decision only from events within its freshness policy. It also rejects excessively future-dated events as detection evidence. The time-window query itself excludes events later than the current processing time. Events in the small future-skew tolerance are retained but do not immediately inflate the current window.

In production, make freshness and allowed clock skew explicit configuration with metrics. A high stale-event count can indicate transport backlog. A high future-event count can indicate clock configuration problems or a hostile producer. Both should be visible without automatically punishing visitor addresses.

## Deduplication precedes counting

The detector operates after event identity has been accepted exactly once for its effects. Counting then deduplicating raw history is too late: the earlier count may already have created a decision. A retry must not increment a counter, create another detection, or extend an active decision.

The lab's transaction handles this ordering directly. A production worker should mark a job's completion and commit its counter changes and decision creation together. If a worker crashes after updating a counter but before marking the event processed, repeating that job must not count it twice.

## Do not renew by accident

An active decision has an original expiry. New delivery messages carry the same expiry. Repeated activity does not automatically reset it in the teaching model. The detector also keeps a short persisted cooldown so that still-visible old window evidence cannot immediately create a replacement decision after a revoke or a very short TTL.

A production renewal policy, if needed, must be a separate decision rule. It should require fresh evidence after a defined boundary, have a maximum cumulative duration, and remain distinguishable from transport retries. Operators should be able to tell whether they are seeing a first decision, a deliberate renewal, or a delivery retry.

## Measure false positives in monitor mode

Before enabling enforcement, collect would-block outcomes and compare them with known application behavior. Review the top affected paths, addresses with many legitimate requests, shared network exits, and events around deployments. Monitor mode tests the rule's consequences without denying those requests.

Do not infer false-positive rate from a test fixture designed to trigger the rule. The fixture proves implementation behavior. It says nothing about your application's normal traffic. Use representative owned traffic and labeled operational cases for calibration.

## Exercise

Create five 404 events with different request IDs but the same path. Then create five with different paths. Retry both batches. Finally submit five events older than the freshness limit. What should create a decision?

## Answer

The single-path batch does not meet the distinct-path rule. The different-path batch can create a decision. Replaying either batch adds duplicates rather than evidence. Old events remain valid stored history but cannot create a fresh ban. To isolate each case, use a new state directory or different documentation addresses so that previous decisions and cooldowns do not affect the next scenario.
