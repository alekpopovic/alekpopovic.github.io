# Chapter 25 - Registry Credentials and Immutable Image Identity

Atlas API now needs an image from a private repository. Two questions must remain separate: which credential permits an agent to pull it, and which artifact should that pull retrieve? A password answers the first. A digest can identify the second. Neither fact alone establishes who built the artifact or whether its contents are safe.

This chapter builds on namespace-scoped secret handling and service versions. You will follow encrypted registry credentials into one assigned service task, calculate how the image parser separates a registry port from a tag, and distinguish supplied digest metadata from a registry lookup. The concrete failure window is a mutable tag changing between a reviewed manifest and an agent's pull. We will examine the implemented controls without claiming the default resolver contacts a registry.

## Registry Authentication Without Plaintext History

A service manifest references a credential ID through imagePullSecret. It does not need to contain the registry password. CreateRegistryCredential validates the ID, registry and username, requires a configured envelope, then encrypts the password before adding the credential to MemoryService. The stored record contains ciphertext and a key ID; the public metadata representation excludes the encrypted password. Updating an existing ID replaces the encrypted material within its namespace. [Claim ch25.credentials](../../validation/evidence/ch25.json).

The namespace is part of the lookup key. A credential named atlas-pull in one namespace does not satisfy the same reference in another. Service creation rejects a missing namespace-local credential before recording the service. This is a useful logical boundary, although it does not imply host-level tenant isolation. A node that receives authorized task execution material still becomes part of the trust boundary.

On assignment polling, ordinary service tasks take a specific path. The control plane finds the task's service, resolves its environment and resolves that service's imagePullSecret. The envelope decrypts the password into the transient RegistryAuth payload. The agent converts that payload into the runtime's authentication type, and PullImage passes the encoded credentials to the Docker client. Public service/event history should contain references and image metadata, not that transient password.

[internal/controlplane/controlplane.go, lines 854–873](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L854-L873) at the locked revision.

```go
func (s *MemoryService) resolveRegistryAuthLocked(ctx context.Context, namespaceName string, id string) (*RegistryAuth, error) {
	id = strings.TrimSpace(id)
	if id == "" {
		return nil, nil
	}
	credential, ok := s.registries[namespacedKey(namespaceName, id)]
	if !ok {
		return nil, fmt.Errorf("%w: registry credential %q not found", store.ErrInvalidState, id)
	}
	if s.envelope == nil {
		return nil, fmt.Errorf("%w: secret envelope is not configured", store.ErrInvalidState)
	}
	plaintext, err := s.envelope.Decrypt(ctx, secrets.Ciphertext{KeyID: credential.KeyID, Data: credential.EncryptedPassword})
	if err != nil {
		return nil, fmt.Errorf("%w: decrypt registry credential %q", store.ErrInvalidState, id)
	}
	return &RegistryAuth{
		Username:      credential.Username,
		Password:      string(plaintext),
		ServerAddress: credential.Registry,
```

Encryption at rest does not remove plaintext from execution. The server must decrypt for this protocol, the authorized agent receives the credential, and the Engine performs the pull. A debug dump of assigned-task payloads can therefore leak credentials even when list endpoints are metadata-only. Capture IDs, registry host and success/error shape for the lab; never capture the actual password or encoded authorization header.

The envelope key must remain available to decrypt stored material. Losing it is different from losing a registry token, and rotating one requires a distinct plan from rotating the other. In the default application, memory-owned credential records also disappear with a new server process. The existence of encrypted PostgreSQL fields is not automatic recovery of that state. Keep key custody, record durability and least-privilege registry access as separate operational decisions.

The service-specific path should not be generalized to every workload. The finite-job branch in ListAssignedTasks returns the task directly before the ordinary service environment/auth resolution. JobSpec does not expose imagePullSecret. A private-image Job therefore needs its own supported field and execution trace before documentation can promise the service credential behavior for it. Similar domain names do not establish identical delivery paths.

## Image References, Tags, and Digests

The parser first trims the requested reference and rejects an empty value. It separates an optional digest at the at-sign, then distinguishes a tag colon from a registry-port colon by comparing the last colon with the last slash. Consequently registry.example.test:5000/team/atlas:v2 has a registry port and a tag; it is not a repository whose entire suffix is a tag. [Claim ch25.parser](../../validation/evidence/ch25.json).

A first path component containing a dot or colon, or equal to localhost, is recognized as an explicit registry. Otherwise docker.io is used. An unqualified single-component Docker Hub name receives the library/ prefix. If neither tag nor digest exists, the parser supplies latest. These transformations explain the metadata fields without requiring any network communication.

[internal/image/reference.go, lines 30–50](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/image/reference.go#L30-L50) at the locked revision.

```go
	nameAndTag := requested
	digest := ""
	if before, after, found := strings.Cut(requested, "@"); found {
		if strings.Contains(after, "@") || !digestPattern.MatchString(after) {
			return types.ImageMetadata{}, fmt.Errorf("image digest is invalid")
		}
		nameAndTag = before
		digest = strings.ToLower(after)
	}

	lastSlash := strings.LastIndexByte(nameAndTag, '/')
	lastColon := strings.LastIndexByte(nameAndTag, ':')
	tag := ""
	namePart := nameAndTag
	if lastColon > lastSlash {
		tag = nameAndTag[lastColon+1:]
		namePart = nameAndTag[:lastColon]
		if tag == "" {
			return types.ImageMetadata{}, fmt.Errorf("image tag is empty")
		}
	}
```

The accepted digest pattern is broader than a cryptographic proof of image existence. It checks an algorithm-shaped prefix and a sufficiently long hexadecimal suffix, lowercases the digest, and rejects malformed repeated at-signs. It does not download a manifest and verify those bytes. Nor should this small parser be advertised as a complete implementation of every registry reference grammar or algorithm policy.

For a clearly non-executing explanation, imagine registry.example.test/team/atlas@sha256 followed by 64 repeated hexadecimal characters. That can demonstrate the syntactic shape and a policy branch. It is not an available image, a verified registry artifact or permission to run a pull. The parser tests intentionally use such synthetic values. Label them as test data instead of copying them into an executable deployment manifest.

| Input property | Parsed consequence | Remaining question |
| --- | --- | --- |
| Bare image name | Docker Hub/library and latest default | What bytes will the tag identify? |
| Explicit registry port and tag | Registry and tag separated by slash position | Is that registry reachable and authorized? |
| Supplied digest | Digest metadata can be populated locally | Does the artifact exist and match policy? |
| Successful authenticated pull | Registry access worked for that artifact | Is its publisher trusted? |

Keep RequestedImage for the operator's original request and the parsed registry/name/tag/digest for subsequent decisions. A rollout incident often requires both: the requested tag explains intent, while the actual immutable reference identifies the selected content. Showing only v2 can obscure whether two deployments used the same bytes; showing only a digest can obscure the user's original request.

## Immutable Policy Checks and Rollout Identity

Admission supports require_digest, allow_mutable_tags and the latest-tag denial names. A digest requirement rejects metadata without a digest. Disallowing mutable tags likewise rejects digest-free references, while latest denial addresses an implicit or explicit latest reference. These policies overlap but are not interchangeable. A version-looking tag such as release-2026 remains mutable unless the registry independently protects it or the deployment uses a digest.

The default ClusterPolicy permits mutable tags. Configuring a stricter policy is therefore part of the experiment, not a baseline behavior to assume. The service path calls its configured image resolver, stores metadata on the candidate and runs admission. RequireDigest also marks metadata Pinned. The task creation helpers then use PinnedReference for pinned images, producing registry/name@digest rather than silently returning to the mutable request. [Claim ch25.pinning](../../validation/evidence/ch25.json).

The focused image test uses an injected fixedImageResolver and a synthetic digest. It creates a service, performs a rollout, inspects stored image metadata and checks a current-version task's pinned reference. The test also explicitly completes deployment state through a test helper before requesting the subsequent task creation. Its passing result establishes those field transformations and paths under the fixture; it is not an actual image pull or a completed physical rollout.

The real [focused run](../../validation/labs/ch25/focused-tests.json) passed parser, pinned-reference and rollout-metadata checks. No private registry account was contacted. This is enough to support the chapter's deterministic observation gate: supplied metadata is retained and policy-directed task construction uses the expected identity. A live private-pull gate remains separate and needs an owner-provided accessible image and actual available digest.

Consider the failure window when Atlas is requested as team/atlas:v2. A review approves that tag at one time, then the registry changes it before the worker pulls. With the default parser, the server has not resolved the tag to content, so the worker can receive different bytes from those the reviewer imagined. Requiring a digest closes that particular mutable-name ambiguity only when a real digest is supplied or resolved by an actual trusted resolver. It does not establish that the content was built honestly.

The runtime must also receive the same pinned string for both pull and create. Pulling one reference and constructing a container from another would reopen the ambiguity. Trace the task image into the agent's PullImage and ContainerSpec.Image rather than stopping at the service metadata. Container inspection can then compare the intended reference with the selected local image identity during a separately scoped live experiment.

## Supplied Digests Versus Registry Resolution

ParserResolver.Resolve simply calls Parse. It has a context parameter to satisfy the interface, but does not use it for an HTTP registry request. The interface supports alternative resolvers, and the test injects one. That extensibility is not proof the default server performs tag-to-digest network resolution. [Claim ch25.resolver](../../validation/evidence/ch25.json).

A future remote resolver would need authentication, manifest/platform selection, bounded network behavior and a consistent decision about which digest it returns. An image index and a platform-specific manifest are different objects. A design would also need to carry the selected identity through service versions, rollout creation and worker execution. These are integration requirements, not missing details that can be filled with invented terminal output.

Digest identity is narrower than signature authenticity. An attacker can supply a digest identifying malicious content just as precisely as a trusted publisher identifies a legitimate release. Signing and vulnerability evaluation need their own trust policy and evidence. Chapter 29 treats the repository's proposals as design material; neither a successful Parse nor RequireDigest activates those proposed verifiers.

The development history makes this separation visible. [fe41c80f83b62a3c8ea8430046acf088ec4014a1](https://github.com/alekpopovic/orch/commit/fe41c80f83b62a3c8ea8430046acf088ec4014a1) adds registry credential support. [f2836eabfff8e442d38984433f3e1f5c642667d1](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1) batches image pinning with quotas and GitOps. The changed implementations support that history; they do not establish a separate deployment or verifier implementation for every original prompt title.

For the safe Atlas lab, use Go 1.25 and the disposable locked source copy. Run the following command there, with the environment contract's toolchain and caches. It has no Docker/database prerequisite and does not require a registry password.

```sh
go test ./internal/image ./internal/controlplane \
  -run 'TestParseImageReferences|TestPinnedReference|TestRolloutStoresDigest|TestRegistry' \
  -count=1 -v
```

Expected observations are accepted/rejected reference cases and the fixed-resolver pinned task assertion. The linked execution record preserves actual command, timestamps and output. Cleanup is process exit and removal of any run-owned teaching files. For an optional live experiment, obtain a genuinely accessible artifact, record its verified digest and registry/platform context, and use a scoped robot credential. Do not turn synthetic test digests into pull commands.

Before a release, retain requested reference, selected digest, service version and actual task identity together. If a pull fails, distinguish missing credentials, denied access, absent artifact and transport failure rather than assuming all are digest-policy violations. That separation lets an operator change the credential without silently changing artifact identity, or change the artifact through a deliberate new rollout rather than mutating an old observation.

## Exercises

1. Parse registry.example.test:5000/team/atlas:v2 into registry, name and tag. Why is the first colon not the tag separator?
2. A supplied synthetic digest passes the parser. List three operational claims this result does not establish.
3. Explain why requiring a digest with ParserResolver can reject a tag even when the registry could resolve it.
4. Design a private-image service pull observation without recording credentials, and explain why it cannot automatically certify private-image Jobs.

[Worked answers](../solutions/ch25.md) connect syntax, policy and execution evidence. The operational boundary is precise: encrypted credential delivery and supplied digest pinning are implemented paths; automatic remote resolution, artifact authenticity and vulnerability safety need additional independently verified components.
