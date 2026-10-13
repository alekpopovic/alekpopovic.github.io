# Chapter 24 - Encrypted Secrets and Configuration Redaction

Atlas needs a database connection string, but its deployment manifest should name the secret rather than contain the real value. The control plane must protect its stored representation, supply plaintext to the authorized execution path and keep diagnostics from accidentally publishing it. These are three different obligations. Encrypting one map entry does not make the agent's environment encrypted, and printing a redacted configuration does not prove every log channel is safe.

You will trace namespace-bound secret resolution, inspect the actual local encryption envelope, compare configuration precedence with its redacted view and identify missing key-rotation mechanisms. Chapter 23 supplies identity scope; this chapter follows the value across the boundaries that remain after authentication. All examples use synthetic placeholders. No production secret belongs in a command argument, source file, exported transcript or chapter screenshot.

## Secret References and Namespace Resolution

The upstream secrets-api example shows an environment key with secretRef pointing to a named secret and a separate ordinary environment value. The YAML parser turns that reference into SecretRefs rather than embedding its plaintext into ServiceSpec.Env. The service retains the desired reference; the current value is resolved later when assigned-task data is assembled.

CreateSecret checks name and envelope availability, encrypts the supplied plaintext, then takes the memory-service lock. It verifies the namespace exists and stores encrypted bytes, KeyID and timestamps under namespacedKey(namespace,name). Creating an existing name updates its encrypted representation and timestamp; creating a new one also checks quota. The returned SecretMetadata excludes the encrypted payload and plaintext.

GetSecret and ListSecrets read only metadata within the namespace context. A user allowed to inspect secret names does not thereby receive their values through these endpoints. TestSecretsCreateRetrieveMetadataAndRedactPlaintext explicitly searches create/get/list/event response bodies for its synthetic value and asserts absence. That test establishes specific response channels, not a universal property of every diagnostic and integration.

resolveEnvLocked starts by cloning literal Env, then resolves each reference using the service's namespace and the referenced name. Missing references or unavailable envelope produce errors without embedding the plaintext. Decryption errors report the reference name rather than the decrypted value. A resolved secret then overwrites the selected environment key in the cloned map.

Unchanged source excerpt — [internal/controlplane/controlplane.go:821–837](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L821-L837):

```go
func (s *MemoryService) resolveEnvLocked(ctx context.Context, namespaceName string, spec types.ServiceSpec) (map[string]string, error) {
	env := cloneStringMap(spec.Env)
	for _, ref := range spec.SecretRefs {
		secret, ok := s.secrets[namespacedKey(namespaceName, ref.Name)]
		if !ok {
			return nil, fmt.Errorf("%w: referenced secret %q not found", store.ErrInvalidState, ref.Name)
		}
		if s.envelope == nil {
			return nil, fmt.Errorf("%w: secret envelope is not configured", store.ErrInvalidState)
		}
		plaintext, err := s.envelope.Decrypt(ctx, secrets.Ciphertext{KeyID: secret.KeyID, Data: secret.EncryptedValue})
		if err != nil {
			return nil, fmt.Errorf("%w: decrypt secret %q", store.ErrInvalidState, ref.Name)
		}
		env[ref.EnvName()] = string(plaintext)
	}
	if len(env) == 0 {
```

The agent task DTO receives this resulting plaintext Env, and ensureTask supplies it to ContainerSpec. Docker then constructs the container environment. This is necessary execution delivery, not a failure of encrypted control-plane storage. It does mean the authorized agent, Docker daemon administrator and application process become plaintext trust boundaries. A GET secret-metadata result cannot be used to infer that those administrators are unable to read the value.

Updating a secret's map entry does not mutate the already-created container's environment in place. Existing runtime objects retain their creation-time configuration until a separate workload lifecycle changes them. A rotation plan must identify which tasks should restart and how the application handles old/new credentials during transition. A successful secret update alone is not proof every workload now uses the replacement.

## The Local Encryption Envelope

Envelope is a small interface with Encrypt and Decrypt methods. LocalEnvelope implements it using an AES key and a key identifier. NewLocalEnvelope rejects empty key material, decodes supported base64 AES key lengths or derives a 32 byte key by SHA-256 of the provided string. That derivation is deterministic key construction, not an implemented external key-management service or a password-stretching subsystem.

The key identifier contains a prefix and the first eight bytes of a SHA-256 digest of the key. It identifies which local key representation is expected; it is not a remote lookup handle. The implementation creates AES-GCM, obtains a fresh random nonce for each encryption, prepends that nonce to ciphertext and authenticates KeyID as associated data.

Unchanged source excerpt — [internal/secrets/envelope.go:55–61](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L55-L61):

```go
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return Ciphertext{}, fmt.Errorf("generate secret nonce: %w", err)
	}
	data := append([]byte(nil), nonce...)
	data = gcm.Seal(data, nonce, plaintext, []byte(e.keyID))
	return Ciphertext{KeyID: e.keyID, Data: data}, nil
```

Decrypt rejects a nonempty mismatching KeyID, checks ciphertext length against nonce size and calls GCM.Open with the same associated data. Corrupt bytes or the wrong key fail rather than return plausible plaintext. TestLocalEnvelopeWrongKeyFails exercises that boundary; TestLocalEnvelopeEncryptDecrypt checks round-trip behavior and that stored bytes are not the literal synthetic value.

Those tests are deliberately narrow. They are not a cryptographic certification, a proof of secure key custody or a check that the current executable persists ciphertext across process restarts. In default MemoryService, encrypted secret records still belong to volatile maps. A new server process loses those records even if its local key remains available. Encryption and durability address different failures.

The envelope's key string can come from built-in development configuration unless the owner supplies another value. The default exists for local demonstration, not as a private deployment secret. A source review should name that default condition without publishing a user's effective key. Redacted configuration is appropriate evidence of which sensitive field exists, not of the secret's actual strength.

## Configuration Precedence and Redaction

LoadServerWithFile starts with defaults, applies a file, applies environment, applies explicit overrides and validates the result. Agent and CLI loading follow the same layered idea through their own fields. Therefore explicit command settings outrank environment, which outranks file, which outranks defaults. The relevant question in an incident is the resulting effective setting, not which source an operator remembers editing.

Unchanged source excerpt — [internal/config/config.go:95–107](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go#L95-L107):

```go
func LoadServerWithFile(path string, overrides ServerOverrides) (ServerConfig, error) {
	cfg := defaultServer()
	if err := applyServerFile(&cfg, path); err != nil {
		return ServerConfig{}, err
	}
	if err := applyServerEnv(&cfg); err != nil {
		return ServerConfig{}, err
	}
	if err := applyServerOverrides(&cfg, overrides); err != nil {
		return ServerConfig{}, err
	}
	return cfg, cfg.Validate()
}
```

String application helpers ignore some empty values, so “set an empty override to clear a secret” is not a universal supported operation. Registration-token environment selection also has explicit precedence over the older bootstrap setting. Inspect the exact loader path for the binary rather than assuming all environment names are interchangeable aliases.

ServerConfig.Redacted replaces the full database URL, bootstrap token, JWT secret, users and secret key with [REDACTED] when nonempty. It returns empty for empty values. It does not reveal a masked suffix or a credential hash that could become another identifier in evidence. Cluster policy has its own redacted view, while ordinary address/interval settings remain visible for diagnosis.

Agent redaction protects its bootstrap token, and CLI redaction protects its token. A value in a nonsensitive field is not magically sanitized by these views: server_url and node labels have their own meanings and should not be abused as secret storage. Audit metadata and notification text use different redaction routines, already examined in Chapter 15. There is no single blanket guarantee covering every arbitrary error string.

TestServerConfigPrecedence, TestAgentConfigPrecedence and TestCLIConfigPrecedence exercise actual loading order. TestRedactedConfigDoesNotExposeSecrets asserts the sensitive server keys equal the redaction sentinel. A meaningful additional diagnostic test should search for a unique synthetic canary across selected output channels and state exactly which channels were checked. An empty grep result from one config command is not proof application stdout never prints an injected environment variable.

The distinction mirrors runtime resources: declared fields and diagnostic output do not establish downstream enforcement. A separate captured Docker comparison in this edition found ordinary-agent Memory/NanoCPUs zero while a direct adapter populated the requested limits; that actual record is scoped to resource propagation, not secret confidentiality. Inspecting real runtime properties needs deliberate sanitized evidence, because a full Docker environment dump can itself disclose values.

## Key Custody and Rotation Boundaries

The local key is an authority required to decrypt stored secret bytes. Losing it while retaining ciphertext is a different incident from losing the default process's entire memory state. Copying it into every transcript to make a lab reproducible would destroy the confidentiality boundary. Record a synthetic fixture identifier or a redacted presence check, and store any real operational material through an owner's separate secret-handling process.

There is no external KMS provider, remote envelope-data-key wrapping or automated key-ring rotation in this source. Changing the configured local key makes existing ciphertext's key identity incompatible. A complete rotation extension would need to retain old decryption authority, re-encrypt records under the new key, verify completion and define rollback/retirement. That is a protocol with failure windows, not a configuration rename.

For Atlas, imagine the server encrypts secret V1, the worker starts container A, then the operator updates the stored value to secret V2. The current container can still use V1. Now imagine changing the envelope key without migrating stored records: a later assigned-task resolution can fail even though secret metadata remains visible. These timelines demonstrate why stored representation, current reference resolution and runtime environment must be observed separately.

Deletion has a related boundary. Removing a secret record does not erase plaintext already delivered to an existing container. It may instead make later reference resolution fail. Do not describe API delete as revocation of every external copy. Application credential revocation belongs to the downstream service's authority, with workload restart and orchestration cleanup as additional steps.

A threat model should therefore enumerate metadata readers, authorized task recipients, Docker administrators, application logs, audit events and backup material separately. Namespace-scoped secret lookup limits which record is chosen; it does not create kernel isolation or prevent an administrator of the shared daemon from inspecting execution. The engineering decision is to protect each owner explicitly and avoid transferring one boundary's claim to another.

## Atlas Lab: A Canary Without a Real Credential

Use the disposable pinned source copy with Go 1.25. The deterministic stage needs no database or Docker and covers encryption, wrong-key behavior, metadata secrecy, agent delivery and configuration precedence.

```bash
go test ./internal/secrets -run TestLocalEnvelope -count=1 -v
go test ./internal/config -run 'Test(ServerConfigPrecedence|AgentConfigPrecedence|CLIConfigPrecedence|RedactedConfigDoesNotExposeSecrets)$' -count=1 -v
go test ./internal/api -run 'Test(SecretsCreateRetrieveMetadataAndRedactPlaintext|SecretInjectedIntoAgentTaskEnv)$' -count=1 -v
```

The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) records envelope, configuration and API assertions with caching disabled. The [security laboratory](../../labs/05-security-boundaries/README.md) separately records a synthetic canary across permitted plaintext and forbidden metadata/log channels; it does not certify every possible application log. The injected sample value must be unique and obviously nonoperational. Generate it inside the fixture rather than place a real connection string in shell history. Retain only pass/fail channel names and sanitized diagnostics, not a full agent assignment payload containing plaintext.

For an optional owned Atlas deployment, add a reference using a supported teaching manifest and a disposable secret value. Prove metadata absence and intended application delivery through a boolean canary comparison, without printing the value or Docker's full environment. Compare a later secret update with the existing container identity to demonstrate that record updates and workload refresh are distinct. Use only run-owned namespace/service/container IDs.

Abort if the exercise reads real configuration secrets, logs bearer material or targets a user database. Cleanup removes the run-owned service before its secret reference and closes owned processes; preserve unrelated records. A useful result states which channel omitted the canary, which authorized recipient received it and which state remained volatile. It does not claim KMS integration, complete log sanitization or automatic credential revocation.

## Exercises

1. Why can secret GET safely omit plaintext while an assigned task legitimately receives it? Identify both trust boundaries.
2. Explain the nonce, KeyID and associated-data roles in the local envelope. What does the wrong-key test establish and leave unproved?
3. A file sets key A, environment sets key B and explicit overrides set key C. Which key is selected, and why is the redacted print unsuitable for proving its exact value?
4. Updating a secret and changing the envelope key are two different operations. Design an observation plan that avoids assuming existing containers refresh or old ciphertext remains decryptable.

[Worked answers](../solutions/ch24.md) connect confidentiality to concrete owners, configuration and recovery rather than a generic “encrypted at rest” slogan.

## Development history and source references

Original development prompts 37, 44 supply the requested scope. The inspected implementation history includes [ad738d1867ee](https://github.com/alekpopovic/orch/commit/ad738d1867eefb3c92cc4280659ae76943341426), [a4844c571a0d](https://github.com/alekpopovic/orch/commit/a4844c571a0ddf33879556413a62d49a408609e3). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/secrets/envelope.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L1-L108)
- [internal/secrets/envelope_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope_test.go#L1-L45)
- [internal/config/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go#L1-L780)
- [internal/config/config_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config_test.go#L1-L176)
- [docs/SECRETS.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SECRETS.md#L1-L65)
- [docs/CONFIGURATION.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/CONFIGURATION.md#L1-L129)
- [deployments/examples/secrets-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/secrets-api.yaml#L1-L14)
