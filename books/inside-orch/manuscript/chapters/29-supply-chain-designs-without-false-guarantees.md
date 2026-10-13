# Chapter 29 - Supply Chain Designs Without False Guarantees

Atlas API can now carry a digest through service intent, but an attacker could provide a digest for a malicious image. Precise identity is a prerequisite for a useful trust decision, not the decision itself. This chapter studies how the repository proposes to add signature and vulnerability evidence while keeping those proposals separate from the running application.

You already know the parser-only default resolver and built-in admission rules. Here you will define the artifact subject, place verification at explicit boundaries, and evaluate stale or unavailable evidence without pretending a scanner ran. The Atlas lab is a small executable book-side decision contract using supplied fake verdicts. It contacts no registry, verifies no signature and scans no image.

## Digest Identity and Signature Authenticity

A digest addresses content identity: the decision can name the same selected artifact across review, rollout and execution. A signature decision asks whether an accepted identity or key authorized that artifact under a particular trust policy. Even a valid trusted signature does not prove absence of vulnerabilities or malicious behavior. These are separate questions with different evidence and failure modes.

The source's implemented image policy checks registry, digest presence and mutable/latest rules. The default ParserResolver parses metadata without remote resolution. No signature verifier is called by that parser or the ordinary built-in admission evaluator. The signing document explicitly describes a design, including its goals and non-goals. [Claim ch29.baseline](../../validation/evidence/ch29.json).

[docs/IMAGE_SIGNING_DESIGN.md, lines 7–7](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/IMAGE_SIGNING_DESIGN.md#L7-L7) at the locked revision.

```text
This design does not implement signing, run a certificate authority, mirror registries, scan images for vulnerabilities, or make a signature prove that the image is safe. SBOM and vulnerability decisions are covered by `SUPPLY_CHAIN_SECURITY_DESIGN.md`.
```

For Atlas, define the threat before choosing a mechanism. The design addresses substituted tags, unauthorized publishers, stale results and artifact substitution between admission and execution. It does not protect a host already compromised at root, a deliberately malicious trust administrator or a compromised build identity that still satisfies the configured policy. Naming these exclusions prevents a signature badge from becoming a claim of universal safety.

A useful artifact subject contains the immutable digest plus relevant repository/platform interpretation. The trust decision also needs namespace and policy revision. Otherwise a result accepted for a development namespace could be replayed for production, or a success under an old policy could be reused after trust roots changed. The proposed verification evidence should bind those dimensions explicitly rather than storing an unqualified boolean verified.

Signed authenticity and registry access remain distinct. A registry credential permits retrieval; it should not become a signing credential or appear in a verification record. Likewise, the private signing key should not be sent to Orch so that it can verify signatures. The design describes public trust material and identity-based checks; actual key management and adapter behavior require a separate implementation and review.

The supplied-verdict lab intentionally avoids realistic-looking image digests. Its subject string says synthetic-non-executing-digest, because it will never be passed to an Engine pull. This makes the scope visible in both code and output. A future live verification exercise must use an available artifact and independently checked tool/version documentation rather than turning the teaching string into an operational reference.

## Trust Policy and Verification Placement

The signing design proposes verification at API admission, rollout creation and the agent before execution. Each point answers a different failure window. Admission gives early feedback, rollout ties a version to its exact subject, and the agent can refuse a stale or bypassed assignment at the final execution boundary. These are proposed enforcement points, not active hooks demonstrated by the current baseline. [Claim ch29.placement](../../validation/evidence/ch29.json).

An admission-only success can become stale before a delayed task starts. A rollout-only success does not prevent a direct agent path from bypassing that controller. An agent-only rejection gives late feedback after the control plane already accepted intent. Multiple checks can narrow those windows, but only if they bind the same digest and policy context and have a tested protocol for expiry and unavailable dependencies.

The design suggests short-lived assertions for agents. A complete assertion must bind subject, namespace, policy revision, expiry and issuer, and the agent must authenticate that binding. Copying a JSON object containing allowed:true is not equivalent. The book-side Verdict is deliberately just supplied test input, so its boolean signature_trusted demonstrates decision wiring only; it is not a cryptographic assertion implementation.

Trust-root rotation also changes the decision. If a previously accepted root is removed, cached results under the old policy cannot automatically remain valid forever. Record the policy revision and define how running and pending workloads are reevaluated. A grace period may be operationally necessary, but it needs an explicit scope and evidence rather than a silent exception.

Place audit evidence at the decision boundary. Useful records include digest, namespace, policy revision, verifier version, result reason and expiry. They should exclude registry passwords, raw identity tokens and full sensitive scanner payloads. A source event such as verification.succeeded is a proposed schema here; its name in a document does not mean the default server currently emits it.

The acceptance path should distinguish invalid evidence from unavailable evidence. An untrusted signature, wrong subject or expired assertion is not merely a transient network outage. Retrying those as though another HTTP attempt would make them valid can hide a policy error. Conversely, an unavailable verifier should not be mislabeled as proof of a malicious publisher. Stable reason codes support different operational responses.

## SBOM, Vulnerability Freshness, and Fail Modes

The supply-chain design proposes SBOM records and scan results keyed by immutable digest. It separates large documents from metadata, retaining document identity, producer, scanner/database version and timestamps. This is design material: the proposed image_artifacts, image_sboms and vulnerability_scans records are not evidence that the current migrations/API implement that data plane. [Claim ch29.scanning](../../validation/evidence/ch29.json).

[docs/SUPPLY_CHAIN_SECURITY_DESIGN.md, lines 34–34](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SUPPLY_CHAIN_SECURITY_DESIGN.md#L34-L34) at the locked revision.

```text
Admission runs after tag-to-digest resolution. Missing/stale data, active scans, scanner outage, and policy violation are separate structured results. Production defaults to fail closed for missing or expired evidence. Development may allow deployment while a scan is pending, but this produces an audit event.
```

An SBOM describes a claimed component inventory. Its existence is not proof that every component is accurately identified or that no vulnerability exists. A scanner verdict depends on the artifact, scanner behavior and the vulnerability database available at scan time. New information can make yesterday's clean result insufficient without any change to image bytes. Evidence freshness therefore belongs in policy rather than being inferred from an immutable digest.

A meaningful scan decision needs at least the subject, trusted producer/scanner, database version, completion state, scan time and expiry. Missing, pending, failed and expired results are different states. A critical finding is another different state. The proposed policy can choose how to treat each, but should not collapse all of them into a generic passed flag.

For Atlas production, the illustrative contract denies missing/unavailable or expired evidence and any critical finding. A narrowly selected development option allows a pending scan only after subject binding, signature trust and signature expiry have passed. That option returns allow_with_audit rather than an unqualified success. It does not override an explicitly untrusted signature or a mismatched namespace. [Claim ch29.contract](../../validation/evidence/ch29.json).

The contract's name matters: returning allow_with_audit does not actually persist an audit record. A future caller would need to perform that obligation and define what happens when the append fails. Similarly, signature_trusted is supplied by a fake, not computed by a real verifier. The executable test is useful precisely because it isolates the decision truth table without inventing external integration evidence.

| Supplied condition | Teaching decision | Scope |
| --- | --- | --- |
| Matching subject/policy, fresh trusted verdict, no critical finding | Allow | Supplied inputs only |
| Another namespace, digest or policy revision | Deny subject mismatch | Prevents modeled replay |
| Untrusted or expired signature verdict | Deny | No real signature verification |
| Pending scan with explicit narrow exception | Allow with audit obligation | Caller must implement audit |
| Unavailable scanner or expired completed result | Deny | Illustrative outage policy |

The decision table has a deliberate order. Subject mismatch and signature failure are checked before the pending-scan exception. A broad except-on-error rule placed first could accidentally bypass trust checks. The tests vary namespace, digest and policy separately, then exercise trust, expiry, findings and the narrow exception. The [actual teaching run](../../validation/labs/ch29/teaching-fixture.json) passed all five test methods and their subcases.

This observed success means the small Python contract behaves as asserted with injected time and fake verdicts. It does not establish real signature validity, SBOM parsing, scanner correctness, authenticated cache storage or a durable audit trail. Those adapters remain proposed. Keeping that limit explicit makes the test reusable when a real adapter is eventually introduced: its output must conform without changing the decision's meaning.

## What the Repository Proposes Rather Than Runs

The design includes proposed supply-chain API routes and CLI commands. They must not be copied into a current command reference as though implemented. A reader trying an absent scan command would be misled even if the architecture is sensible. The correct baseline description is implemented digest/reference policy plus separate signing/scanning designs.

History reinforces that boundary. [f2836eabfff8e442d38984433f3e1f5c642667d1](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1) adds the relevant image pinning and design material in a batch with other work. Its actual changed paths do not demonstrate a deployed verifier, SBOM service or vulnerability scanner. Original prompts 68 and 69 request design, and their existence should not be promoted to execution evidence.

A future integration plan should begin with versioned contracts and threat-model acceptance criteria. Pin the verifier/scanner version, verify commands against official documentation, and record a real artifact subject and expected rejection cases. Do not install a moving latest tool and then describe its output as historically representative of this source revision. The book does not need external installation to evaluate its current design boundary.

Cache design needs particular attention. Key results by subject, namespace or applicable trust scope, policy revision and verifier/database version, with explicit expiry. Authenticate stored results and avoid extending expiry simply because a cache entry was read. A fresh scan with the wrong policy context is not reusable evidence, and a cache outage should follow the same explicit fail mode as an unavailable backend.

Decide separately what happens to a running image when new findings arrive. Immediate termination can reduce availability without producing a safe replacement. Alert-only handling can preserve service while leaving known risk active. The design proposes a staged approach and future policies; the baseline does not implement an automatic quarantine guarantee. A rollout-blocking rule and a running-workload eviction rule require different tests and operator expectations.

For the safe Atlas lab, start in the book's teaching directory and run the deterministic tests. Python's standard library is sufficient. No Docker, registry, network, signing key, scanner database or application process is required.

```sh
cd books/inside-orch/examples/teaching-extensions/ch29
python3 -B test_contract.py
```

The clock is a fixed UTC instant. First predict each table outcome, including equality at expiry, which is denied. Then run and inspect the recorded output. Cleanup is process exit; -B avoids bytecode artifacts. A failed assertion should be investigated as a contract bug rather than weakening the expected denial to match an accidental result.

For a design extension, add a policy-revision change while a task waits to start, and decide whether its old supplied verdict remains acceptable. Keep that change visibly book-side and test it independently. A real adapter would additionally prove how it obtains and authenticates evidence. Until that exists, the correct release language is a tested illustrative decision contract accompanying an unimplemented supply-chain architecture.

## Exercises

1. Explain how a digest can identify malicious content precisely without proving a trusted publisher authorized it.
2. Identify the failure window addressed by admission, rollout and agent verification separately. Which are active in the baseline?
3. Why must a completed scan bind database version and expiry? Explain how new findings can change acceptance without changing the image.
4. A developer moves the pending-scan exception before subject/signature checks. Which modeled bypass becomes possible, and which test should catch it?

[Worked answers](../solutions/ch29.md) preserve the distinction between identity, trust and freshness. The book's concrete achievement here is a reviewed design and an executed supplied-verdict contract, with every external adapter and stronger operational guarantee still labeled as future work.
