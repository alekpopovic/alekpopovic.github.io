# Source, provenance and execution policy

The baseline and file checksums are in `evidence/source-lock.json`. Preserve that edition. File links use the full baseline SHA. Historical links use the commit that actually contains the code under discussion. Use line anchors for exact excerpts. The historical patch corpus contains source changes; it is not a transcript proving the literal execution of a prompt or its acceptance checks.

## Evidence hierarchy

1. Current executable call path establishes current binary behavior.
2. Implementation plus callers establishes package behavior and integration.
3. Inspected tests establish intended assertions; only recorded runs establish executed results.
4. Current documentation helps explain intent and operation but can be stale.
5. Original prompts and designs establish requested scope, not delivery guarantees.
6. Commit subjects/tracker entries help navigation and do not prove a feature's correctness.

## Exact and adapted code

Extract exact snippets from immutable bytes, record raw SHA-256, source path, line interval, symbol and purpose. Printed line wrapping is a presentation transform; the copyable source stays exact. An adaptation must say what changed and be registered as a teaching extension with its own tests. Pseudocode is labeled and is never claimed to compile. A code block from an implemented library must explicitly say whether the running binary calls it.

## Claim schema

Use `templates/claim-record.json`. Allowed classifications: runtime-integrated, implemented package, partial integration, design only, teaching extension, future work. Allowed validation values: expected_only, inspected, executed, blocked. Record actual logs for executed claims. Null line/log fields are acceptable for an honestly unresolved claim; such a claim cannot establish a release guarantee.

The sample chapter remains a source-reviewed specimen; its own laboratory output must be linked to a matching run before it is called observed. The initial intake did not have Go, but exact Go 1.25.0 has since been downloaded and verified (validation/intake/go125-toolchain-network.json). Fresh disposable-copy baseline tests are recorded in validation/intake/orch-baseline-tests.json and its JSON event stream: 447 test pass events and six explicit external-suite skips. These results do not establish real Docker or PostgreSQL behavior. The separately executed original PostgreSQL store fixture failed two tests with missing agent_version (SQLSTATE 42703), because its migration list stops before the current query schema (validation/intake/postgres-store-owned.json). Preserve that failure; a separate full-schema teaching fixture cannot retroactively make the original suite pass. Do not infer any additional laboratory or benchmark run from these records.

## History caveats

All 91 prompt mappings were checked against actual changed historical paths. The first 29 development prompts were added retrospectively. Late changes batch several prompts in one commit. Preserve these relationships. HEAD is a documentation update after tag 0.3.0. Release publication time, tag commit date, author date and committer date are different facts. Exported GitHub release metadata is in `evidence/releases.json`.

## External references

Retrieve primary technical sources before using precise external claims. Record version, retrieval date and applicability. Do not fabricate references or assume current versions match this source edition. The site layout was inspected at https://www.alekpopovic.com/books/ on 2026-10-13 local time; its source repository is pinned separately in evidence/site-lock.json, with Jekyll + Tailwind native integration defined by SITE_WORKSPACE.md.
