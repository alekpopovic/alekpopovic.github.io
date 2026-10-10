# 17. Give credentials to an authorized attempt, not a script name


## A secret reference is not a secret value

The pipeline snapshot stores a reference to a credential and the policy under which it may be used. It must not store the plaintext secret. The server resolves that reference only for an authorized active attempt and only within the permitted project, environment, and runner pool.

Make secret creation write-only through normal APIs. Return metadata such as name, scope, version, and last rotation time, not the value. A “show value” endpoint creates another sensitive access path and should not appear accidentally as part of a generic resource serializer.

Encrypt stored values with an established cryptographic library and an operator-managed key hierarchy. Store key version metadata so rotation and restore are possible. Keep encryption keys outside the database backup they protect. Losing the key while successfully restoring every database row is still losing the secret service.

## Credential redemption is a policy check

A runner presents its current attempt identity, fence, and the scoped capability named in its plan. The server verifies that the attempt is active, the pool is authorized, the project still has access, and the target policy has not been revoked. Only then does it return the permitted material or a short-lived external credential.

An expired lease must prevent new redemption. Previously delivered secrets cannot be retrieved from a worker's memory by revoking a database row. Previously issued external tokens can remain valid until their expiry or provider-side revocation. Design short lifetimes and narrow scopes around that reality rather than claiming immediate universal revocation.

Separate checkout credentials from deployment credentials. A build that can fetch one repository should not automatically be able to push to it or access every repository installed under an organization integration. Remove temporary fetch material before running contributor-controlled steps where possible.

## Use federation deliberately

OpenID Connect can let a workload exchange a signed identity assertion for short-lived cloud credentials instead of storing a long-lived cloud key. The provider trust policy must validate issuer, audience, and a suitably narrow subject. GitHub's OIDC documentation explains this federation pattern. [S19](e-sources.md#s19)

For a Modern CI implementation, start disabled. Enable it only after configuring the issuer, key distribution, trusted audience, subject claims, and provider policy. Bind claims to the project, environment, and approved workload identity. Do not let YAML choose an arbitrary role identifier and assume the provider will enforce your application's intention.

Use a maintained token library. Validate time bounds, accepted algorithms, key identity, and claim types. Keep signing-key rotation and stale-key caching in the runbook. A local mock token exchange is useful for contract tests but does not prove that the actual provider policy is correctly configured.

## Redaction is a secondary defense

Redact credentials from structured logs, error messages, traces, and support bundles. For streamed output, consider values split across chunks and encoded in common forms. But do not promise that masking prevents deliberate exfiltration. Code that receives a secret can transform or use it in ways a text filter cannot safely recognize.

The stronger control is deciding which code receives which authority. A deployment adapter that accepts an immutable release subject and a registered target can be narrower than giving a generic shell a cloud administrator token. The adapter still requires review and testing; a friendly function name does not establish least privilege.

Audit secret policy changes and redemptions with metadata only. Useful fields include project, attempt, credential version, requesting runner, policy decision, and expiry. An audit entry containing the secret defeats the purpose of encrypting the main table.

## Exercise

A secret is revoked at 14:00. A worker obtained an external token at 13:59 that expires at 14:09. The interface displays “all access removed.” What should it display instead?

## Worked answer

It should distinguish blocked future redemption from already issued authority. Show that the secret or policy is revoked for new requests, and record the latest known expiry of issued credentials where the platform can track it. Provider-side revocation may shorten that interval if supported, but the system must not claim it occurred without confirmation.

## Completion evidence

Test revoked leases, cross-project redemption, key rotation, backup without keys, restored keys, token audience and subject restrictions, expired assertions, and accidental leakage through diagnostics.
