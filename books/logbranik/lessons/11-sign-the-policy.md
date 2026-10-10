# 11. Sign policy, not transport assumptions

## Two different protections

mTLS authenticates both ends of a transport connection and protects data in transit. A policy signature authenticates the policy bytes independently of the connection that carries them. The two mechanisms answer different questions. A valid TLS connection does not prove that the receiver got the intended policy from the intended signing authority. A valid signature does not decide which network peer is permitted to use the update endpoint.

The laboratory uses Ed25519 signatures from the Cryptography library. It does not implement a signature algorithm. The central process holds the private signing key. The agent receives pinned public verification keys through provisioning. An incoming policy cannot introduce its own trusted verification key.

## Define the signed bytes

The envelope contains a key identifier, a base64 payload, and a base64 signature. The signature covers a fixed domain separator followed by the exact decoded payload bytes:

```python
DOMAIN = b"nginx-guard/snapshot/v1\x00"
signature = private_key.sign(DOMAIN + raw_payload)
public_key.verify(signature, DOMAIN + raw_payload)
```

The domain separates this use from other signed message types. The zero byte is part of the protocol. Changing it changes the message. Do not replace the payload bytes with a newly serialized JSON object before verification. Whitespace and key ordering can change the bytes even when an object seems equivalent.

The sender may choose a deterministic JSON encoding when generating a new policy. The receiver still verifies the received bytes. Deterministic generation helps produce reproducible fixtures; it is not permission for the verifier to rewrite an incoming message.

## Verification is only the first gate

After verifying the signature, validate the decoded policy. Check the version, agent identity, provisioned epoch, positive revision, issuance and delivery interval, complete authorized site map, mode values, allowlist scope, decision count, address syntax, and independent ban lifetime limits. A malicious but correctly signed policy remains possible if a signing credential is compromised.

Reject unknown fields. The teaching policy deliberately has no command field. Reject duplicate keys and ambiguous numeric types. Enforce byte limits before parsing and collection limits before constructing the live view. These are security and capacity boundaries, not merely convenient error messages.

The lab schema differs from the production protocol in timestamp representation and decision metadata. Both use the same signing concept and domain, but they are not interchangeable clients. A production implementation must match the full RFC3339 contract and use a shared test-vector suite. Do not advertise compatibility based only on a similar JSON shape.

## Key rotation

Provision a new public key before sending policies signed by its private counterpart. During a controlled overlap, the agent can pin both old and new key identifiers. Confirm that every intended agent accepts the new key before retiring the old one. Do not remove a key merely because new delivery succeeded on one edge.

Retiring a compromised key introduces a second concern: a saved policy may have been signed by it. Define how verified persisted state is refreshed and how the old key is removed without silently leaving an agent unable to restart. Local operator recovery and a new clean snapshot should be part of the rotation procedure.

A production signing key belongs in central secret storage with deliberate access and backup rules. The lab's raw key file is for an isolated example. The book package contains source that creates keys; it must not contain generated private keys or populated lab-state directories.

## Exercise

Save a valid envelope. Change one payload byte without updating the signature. Then generate another valid envelope with the same revision but a different site mode. Why are both rejected, and by which gates?

## Answer

The byte edit fails signature verification. The second envelope may pass signature verification because it was signed by the correct key, but fails the revision-conflict rule after a policy with that revision has already been applied. Cryptographic authenticity and safe state ordering are independent requirements.
