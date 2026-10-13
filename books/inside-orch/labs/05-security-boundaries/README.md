# Lab 05 - Secrets, Identities and Probe Boundaries

Atlas needs a secret without turning every metadata response into a secret-distribution channel. Its worker also needs an identity distinct from an operator's role. This lab exercises those boundaries using the unchanged local envelope, API handler, credential issuer and health checker. It creates no Docker workloads, queries no public host and uses no real credentials. The [complete teaching harness](../../examples/teaching-extensions/security/main.go) generates the key, signing material, bootstrap token and secret canary in process memory. Raw values are never written to the evidence files.

Read Chapters 14, 23, 24 and 27 first. Use [the environment contract](../ENVIRONMENT.md), the pinned Go 1.25 compiler and a verified disposable source copy. This is a teaching composition of actual packages, not a deployed production identity system. HTTP API requests run directly through httptest recorders. The only sockets are two disposable loopback healthcheck listeners, automatically closed on exit. If local listeners are unavailable, report the probe track blocked; do not silently replace observations with predictions.

## Reproduce Without Publishing Secrets

Copy the harness into .book-labs/security under the disposable Orch module after verifying its baseline files. Select a fresh evidence directory under your own temporary workspace. Do not direct output into another person's logs. With the environment's explicit pinned GOROOT and run-owned caches:

```sh
GOFLAGS=-buildvcs=false go run ./.book-labs/security /tmp/inside-orch-security-channels
```

The program prints a sanitized result and writes only channels already scanned for the generated canary. Capture its exit code and command independently. Its [actual successful command](../../validation/labs/lab05-security-local-probes.json) and [case matrix](../../validation/labs/lab05-security-local-probes.stdout.txt) document the author's run. Earlier attempts remain recorded: one exposed an invalid raw zero-resource JSON fixture, another assumed which of two randomly identified nodes would receive a task, and one was blocked by sandbox socket permissions. Correcting a teaching fixture is different from repairing the immutable application. The final fixture registers the intended assigned worker before creating the secret-bearing service.

The raw HTTP body uses empty resource request/limit objects where no quantity is intended. Directly marshaling a zero-value Go Resources struct emits cpu:0, which the strict quantity decoder rejects. The public CLI client's normalization avoids that boundary. This is why a source type and an accepted wire document must be checked separately rather than assumed interchangeable.

Cleanup closes the owned listeners and discards in-memory state. There are no host ports to retain, database schemas to reset or containers to remove. Delete only this run's temporary evidence and copied harness when finished. Keep sanitized hashes needed for review. Never place a real API token, database URL or envelope key in these examples.

## Follow Sensitive Data Across Owners

The harness creates a one-use canary and encrypts it with LocalEnvelope. A same-key round trip must recover the exact value; a different key must reject decryption. The ciphertext is scanned to ensure it does not literally contain the canary. The result contains the canary's SHA-256 and ciphertext hash, not their plaintext. These observations exercise this implementation, not cryptographic certification or a remote key-management service.

The API creates a secret in team-a, then returns metadata for create, get and list. Events, audits, captured logs and a cross-namespace missing-reference error are forbidden plaintext channels. Each is scanned before persistence. The scanner records file bytes and hashes so the acceptance script can detect later changes. Merely searching a final JSON report would miss a leak in an intermediate response; conversely, searching every payload without a visibility policy would incorrectly classify intended agent delivery as a leak.

An authenticated assigned worker receives the canary in its task environment, verified by an in-memory equality comparison. That raw response is discarded. The same secret name requested from team-b is hidden, and a service in team-b cannot resolve team-a's reference. This demonstrates namespace-scoped lookup, not kernel or network isolation. The server decrypts the value and the agent/application must receive it; anyone controlling those trusted processes can cross the confidentiality boundary.

| Producer | Consumer | Permitted sensitive data | Enforcement point | Residual assumption |
| --- | --- | --- | --- | --- |
| Secret writer | API/server | One-use plaintext input | User role and selected namespace | Transport and server process trusted |
| Local envelope | MemoryService | Ciphertext and key identity | AES-GCM/key identity check | Key remains available and secret |
| Metadata API | Viewer/operator | Name and timestamps | Metadata projection | Other fields do not become covert leaks |
| Server assignment | Authenticated assigned agent | Plaintext environment | Issued node credential and task node ownership | Worker host and process trusted |
| Agent/runtime | Application | Required plaintext environment | Intended workload setup | Docker socket owner has host-level power |
| API/handlers | Logs, audits, errors | Sanitized metadata | Channel-specific redaction and canary checks | A finite scanner does not prove every future log safe |
| Health checker | Local workload endpoint | Probe request, no canary | Input path validation and same-origin redirect guard | Chosen address/DNS require their own policy |

Losing the envelope key makes existing ciphertext unusable; changing a secret is not the same as rotating the encryption key. MemoryService ciphertext also disappears with the process. Encryption protects one storage representation while durable recovery requires an independently designed state and key lifecycle.

## Separate User Authorization From Worker Identity

The matrix observes 401 for a missing required user token, a successful viewer read, 403 for viewer mutation, an allowed team-a operator create and 403 for that operator in team-b. Audit reads require cluster administration: a namespace operator is denied, while an admin succeeds. Tokens are signed using the source's SignJWT interface with synthetic signing material, not hand-written strings that imply external identity-provider support.

Worker registration without the configured bootstrap token returns 401. Registration with it issues a credential. A second worker's credential cannot report status for the first worker: the handler returns 401 and the task state remains unchanged. A successful heartbeat rotates the first credential; replaying its old credential returns 401. The issuer separately rejects a token exactly at its expiry boundary and rejects a revoked record. These are distinct from user-role failures and therefore must not be flattened into a universal 403 expectation.

The empty user-JWT configuration is tested explicitly: an anonymous service metadata read succeeds. Agent credential enforcement is a separate path. The optional user JWT mechanism, static bootstrap credential and rotating node bearer tokens do not provide mutual TLS, public identity lifecycle integration or containment after a Docker socket compromise. A lost rotation response is also an operational concern; passing rotation tests does not establish a replay-safe recovery protocol.

## Keep Probe Traffic Local

Two loopback listeners provide a legal same-origin redirect, a cross-origin redirect, a slow response and a body larger than 64 KiB. The same-origin request succeeds. The cross-origin request is unhealthy and the second listener's request count stays zero. The slow endpoint exceeds a ten-millisecond timeout. The large response succeeds while the checker limits body consumption to its source constant; that observation does not claim the server wrote only 64 KiB or that allocation is globally bounded.

Input validation separately accepts /ready and rejects both a full absolute URL and a protocol-relative path. Those rejected examples never cause DNS or network access. The checker receives an already constructed target; validating a relative path and blocking redirects does not constrain every possible initially selected address or DNS answer. Do not probe cloud metadata or a production private service to illustrate that gap.

## Worked Questions

1. **Why is plaintext assignment allowed?** The trusted worker needs the application's value. Its credential and task ownership authorize a narrower distribution boundary than public metadata reads. The harness proves equality without saving the raw payload.
2. **Why distinguish 401 and 403?** Missing or wrong credentials fail authentication. A recognized viewer attempting a mutation fails authorization. Exact handler mapping determines the result; a generic denial label loses that evidence.
3. **Does zero cross-origin traffic prove SSRF safety?** It proves this redirect was blocked before contacting its target. Initial address choice, DNS resolution and trusted network placement remain separate questions.
4. **What does a clean canary scan establish?** The selected captured channels omitted this one generated value and still match recorded hashes. It does not prove universal redaction, absence of derived sensitive data, durable encryption or production-safe deployment.

The [acceptance record](../../validation/labs/05-check.json) checks the actual matrix, unchanged task, probe destinations and persisted channel hashes. Preserve those boundaries when applying the lesson to a live system.
