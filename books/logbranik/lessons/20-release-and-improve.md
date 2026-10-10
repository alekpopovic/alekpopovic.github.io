# 20. Release a reproducible system

## Freeze a reviewable edition

A release joins code, configuration, protocol version, tests, deployment notes, and operator procedures. Tagging code alone leaves readers uncertain about which manuscript and fixtures describe it. The book's release tooling exports lesson sources, checks structure, builds reading formats, records evidence, and creates a checksum manifest.

Each lesson is maintained in a Markdown file. Leanpub manuscript text is generated from those files, so there is one editorial source. The sample selects the preface and first four lessons. The full PDF and EPUB are built locally for review. Leanpub can generate its own preview when the manuscript repository is connected; that platform-specific output still needs inspection.

## Avoid the production-readiness shortcut

The teaching implementation is useful because it executes the central invariants. It does not implement every production requirement. It has one demonstration site, a compact integer-time wire format, a small rule, a simple periodic push process, and a SQLite store. It does not include a fleet operator API, independent pull reconciliation, mature retention, a complete Go port, or production load measurements.

Those are concrete next milestones, not vague warnings. The source pack provides sixty implementation tasks with acceptance evidence. Map each one to a lesson and complete it against your actual repository. A task is done when its criteria have evidence, not when a coding assistant emits a plausible patch.

## Assistants as implementation tools

The included Claude Code pack has native project instructions and progress tracking. Its tasks specify intended behavior and dependencies. Keep the application repository's existing instructions, review changes, and record commands and results. An assistant-generated summary should distinguish code written, tests executed, and deployment gates pending.

Model effort can help with complex reasoning, but it cannot replace real service execution. Use stronger reasoning for protocol ordering, threat boundaries, and concurrency review when available. Use ordinary effort for editorial cleanup and mechanical exports. The final evidence comes from the code, the environment, and human judgment about the observed behavior.

## Publish responsibly

Before commercial book publication, identify the actual responsible author or pen name, perform a human technical and editorial review, reproduce unexecuted deployment exercises, inspect PDF and EPUB, and complete the platform's author and payout setup. The package intentionally contains no invented biography or legal identity.

The Leanpub AI policy expects quality and human curation rather than mass-produced low-quality material. The manuscript's transparency statement describes the current preparation process. Update it honestly after review. Do not claim AI was used only for copyediting when it generated substantial text and code.

Pricing in the publishing notes is an editorial starting suggestion. It is not a revenue forecast, a market benchmark, or a platform fee quotation. Check the current account terms before selecting formats, payment details, and publication settings.

## Improve through evidence

The most valuable next changes are those driven by a observed limit. If rotation loses events, repair collection before adding more detectors. If false positives affect shared addresses, improve calibration and scope before lowering thresholds. If snapshots become too large, measure coalescing and fanout before creating a delta protocol. If concurrent workers miscount, fix state serialization before increasing worker count.

Keep release notes precise. Say that an epoch-recovery procedure was added and tested, or that a particular Nginx profile preserved POST bodies under specified errors. Avoid blanket statements such as "security improved" when the underlying behavior can be named.

## Exercise

Choose the next three implementation-pack tasks after finishing the laboratory. For each, name the remaining risk, the expected observable behavior, and the evidence required to mark it complete.

## Answer

A useful set is actual Nginx route integration, continuous collector recovery, and production worker transaction correctness. Their risks are bypassed access phases, lost or stale observations, and repeated or lost detection effects. Their evidence is a route/status/body matrix, unique request-ID reconciliation across outage and rotation, and a concurrent PostgreSQL crash/retry test. Completing those three would support stronger deployment claims than adding a cosmetic dashboard first.
