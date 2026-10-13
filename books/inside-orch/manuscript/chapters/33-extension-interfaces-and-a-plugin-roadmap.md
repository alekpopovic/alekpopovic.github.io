# Chapter 33 - Extension Interfaces and a Plugin Roadmap

Atlas needs a second secret provider and a notification adapter. The tempting response is to build a plugin manager before understanding the interfaces already available. That would introduce process supervision, packaging, authentication, and compatibility work into an otherwise small integration. The first decision is therefore about the boundary: which side effect must vary, who calls it, and what survives a failed call?

By the end of this chapter, you should be able to locate existing extension seams, distinguish dependency injection from external plugin execution, and write a contract that rejects an incompatible adapter before it receives work. You will also learn why a runtime plugin remains privileged even when it lives in another process. The practical result is an executable fake adapter exercise and a deliberately unimplemented RPC proposal.

## Interfaces Already Present in the Code

The runtime interface is a useful starting point because its methods describe observable effects. Pulling an image, creating a container, starting it, and inspecting it are separate operations. This lets the agent recover after uncertainty between steps. A vendor adapter must preserve the meanings of those operations; merely returning successful HTTP responses would not satisfy the contract.

```go
type Runtime interface {
	PullImage(ctx context.Context, image string, auth *RegistryAuth) error
	CreateContainer(ctx context.Context, spec ContainerSpec) (ContainerID, error)
	StartContainer(ctx context.Context, id ContainerID) error
	StopContainer(ctx context.Context, id ContainerID, timeout time.Duration) error
	RemoveContainer(ctx context.Context, id ContainerID, force bool) error
	InspectContainer(ctx context.Context, id ContainerID) (ContainerStatus, error)
	ListManagedContainers(ctx context.Context, labels map[string]string) ([]ContainerStatus, error)
	StreamLogs(ctx context.Context, id ContainerID, opts LogOptions) (<-chan LogLine, <-chan error)
}
```

Exact source: [internal/docker/docker.go:47–56](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L47-L56).

The context on every method expresses cancellation and deadlines. It does not make an external operation transactional. If a create request reaches a remote engine but its response disappears, cancellation cannot prove that the container was never created. Task identity and a discoverable managed-container association are needed to resolve that uncertainty. The [fake runtime's task lookup illustrates the replay boundary](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/fake.go#L135-L166): repeated creation for the same task returns the existing identifier instead of adding another container.

Secrets expose a different seam. The [Envelope interface accepts encryption and decryption requests](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/secrets/envelope.go#L20-L24), while the server constructs a local envelope and injects it into its memory control plane. This is an implemented, runtime-integrated boundary. A replacement provider could implement the same Go interface, but the current constructor does not discover arbitrary remote secret plugins. Key selection, authenticated ciphertext, cancellation, and failure handling still need equivalent semantics.

The [notification sender owns delivery retries and signing](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go#L77-L115). Its HTTP client can be supplied through an option, and the dispatcher reads sinks through a narrow store interface. The server actually installs that dispatcher. An external webhook receiver is therefore a present integration surface, while an RPC notification plugin supervisor is a separate proposal. These distinctions matter when Atlas estimates the work: writing a webhook endpoint and building a secure executable loader have very different operational costs.

Autoscaling contains another instructive pair: a control-plane interface and a metrics-provider interface. The [provider returns service CPU utilization rather than exposing a monitoring vendor's client](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/autoscaler/autoscaler.go#L18-L36). That makes controller policy independently testable. However, a clean interface is not evidence that the default server starts that controller. Trace constructors and loops before labeling a seam runtime-integrated. A compilable package can remain an implemented library with no production caller.

| Boundary | Existing implementation | External-process status |
| --- | --- | --- |
| Container runtime | Go interface, engine adapter, fake adapter | RPC protocol is design only |
| Secret envelope | Go interface, local authenticated encryption | Remote provider requires new composition |
| Notifications | Dispatcher and signed HTTP delivery | Webhook delivery exists; plugin supervisor does not |
| Autoscaler metrics | Injectable provider interface | Default server composition remains incomplete |

The table follows the source, not a count of files named “plugin.” Commit [4d641bbe8913da568d6d9f4697a0144314e10b87](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87) added jobs, storage, DNS, and notifications together. Its notification implementation is useful historical evidence. It does not establish that every design described in the later plugin document became an executable subsystem.

## A Versioned External Plugin Handshake

The [plugin design document proposes isolated processes and versioned RPC](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/PLUGIN_SYSTEM_DESIGN.md#L3-L11). It specifies a handshake containing protocol version, plugin type, implementation version, capabilities, and supported orch range. These are design requirements, not fields decoded by an upstream supervisor. Atlas can use them to define a reviewable interface without claiming the transport already exists.

Protocol version and implementation version answer different questions. Protocol version determines whether the two sides understand request and response meanings. Implementation version identifies which adapter build is running. Supported orch range prevents a transport-compatible adapter from silently relying on a newer workload schema. Capabilities describe optional behavior, such as log streaming or secret-key rotation, which callers must explicitly require before use.

For Atlas, a runtime adapter must advertise cancellation and task idempotency. An adapter with a matching major protocol but missing either capability is rejected before any container request. Unknown additive capabilities may be ignored. A major mismatch fails closed. This avoids optimistic fallback that would turn an unsupported operation into a partially executed workload change. The [teaching test](../../examples/teaching-extensions/ch33/adapter_contract_test.go) implements only this small validation rule; it does not start processes or send RPC messages.

Capability names need precise definitions. “Cancellation supported” might mean that a client stops waiting, that a queued request is discarded, or that an operation is interrupted before an effect occurs. Those are different guarantees. Atlas's proposed contract should say that cancellation stops new work where possible, returns a recognizable error, and leaves completed effects discoverable by idempotency key. It must not promise to undo a container that has already started.

A request identifier is useful for diagnostics, while an idempotency key represents the logical effect. Retries can have different transport request identifiers but the same task-create idempotency key. The adapter must either return the previously created object or report a conflict when the repeated key carries a different specification. An interface that deduplicates only byte-identical requests needs an explicit canonicalization rule; map ordering and omitted defaults must not accidentally change identity.

Responses also need bounded size and stable error classes. Atlas should distinguish unsupported capability, invalid input, deadline exceeded, authentication failure, temporary unavailability, and unknown completion. A generic “retry” flag is insufficient when the effect may have happened. The caller's recovery decision depends on whether it can inspect by task identity, not merely on whether a network connection closed.

## Supervisor Lifecycle and Failure Containment

A proposed supervisor has a sequence: validate configuration, connect or start, handshake, become available, accept bounded calls, drain, and stop. Each transition needs an owner and a timeout. Availability should begin only after handshake acceptance. During drain, new requests are rejected while existing requests receive a bounded completion interval. Expiry then triggers cancellation and process termination according to a documented policy.

This lifecycle is a teaching design. There is no upstream plugin supervisor to launch in this chapter. An implementation would need to decide whether executable paths are trusted deployment configuration, whether artifacts are signed, how Unix socket ownership is checked, and how mutually authenticated TCP identities are bound to configured plugin instances. Accepting a path from an ordinary workload request would cross an entirely different trust boundary.

Process isolation contains crashes and dependency conflicts, but it does not remove authority. A runtime adapter with Docker access can change host workloads; a storage adapter can expose or destroy data. Both remain in the trusted computing base. Filesystem restrictions, network policy, resource limits, and secret scoping must match the actual operations. A process with unrestricted host access and a private RPC socket is still highly privileged.

Atlas's most dangerous failure window is a successful remote create followed by a lost response and adapter crash. The supervisor may restart the process, but restarting does not settle whether the create succeeded. A safe caller inspects using the stable task key before issuing another create. The recovery path must be tested with an adapter that forgets volatile state while the underlying engine retains the object. The fake exercise here tests replay within one fake runtime; it does not implement that stronger cross-process persistence guarantee.

Backpressure matters just as much as crashes. An unbounded queue can turn a slow secret provider into a control-plane memory failure. Atlas should bound concurrent calls and queued work per plugin instance, expose rejection counts, and avoid holding a global orchestration mutex while waiting on a remote provider. A timeout does not solve queue growth when every request is admitted first. Retries should consume the same bounded budget rather than bypassing it.

Logging belongs inside the contract. The current [notification redactor removes selected secret markers and sensitive detail keys](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/notifications/notifications.go#L118-L149), but pattern matching is not a universal secrecy guarantee. A proposed adapter should avoid accepting unnecessary credentials, return structured errors without secret values, and redact before writing process logs. Tests should use synthetic values and assert their absence without printing actual production material on failure.

## Contract Testing a Proposed Adapter

The Atlas exercise uses the upstream FakeRuntime through the upstream Runtime interface, plus the local envelope implementation. It creates one fake container twice with the same task identity, checks equal identifiers, rejects work with an already canceled context, starts and stops the object, removes it, and checks that no fake managed containers remain. Separate cases reject a new protocol major, a wrong plugin type, and a missing required capability.

The envelope case encrypts a synthetic value with one local key, confirms another key cannot decrypt it, and confirms an already canceled request is rejected. These assertions exercise concrete implementation behavior. They do not certify a cloud key-management service, a hardware security module, or a remote adapter's authorization policy. The distinction keeps a small contract test useful without allowing it to stand in for every provider's acceptance suite.

Run the teaching file from a disposable copy beneath the orch module, because Go's internal-package rules apply. Copy it into `.book-labs/ch33/`, then run:

```bash
go test ./.book-labs/ch33 -count=1 -v
```

The recorded execution in [adapter-contract.json](../../validation/labs/ch33/adapter-contract.json) passed. The command record retains its working directory, Go environment, UTC times, and output paths. It used no Docker daemon, database, network listener, external executable, or real secret. Cleanup means removing owned fake objects and letting test-local state disappear; it does not involve sweeping host containers.

To extend the experiment, first add a contract case, then build an adapter against it. A timeout adapter should distinguish a canceled wait from unknown effect completion. A malformed-response adapter should fail decoding before handing data to reconciliation. A crash adapter should leave a queryable operation record. These additional cases are proposed work, not results from the current run. Rejecting four handshake fixtures and replaying one fake create is narrower than supervising a production process through failure.

The chapter's boundary is therefore explicit: narrow Go interfaces and selected concrete adapters exist; the external RPC system remains a design. Atlas can adopt the tested seams today and use the proposal to estimate further engineering. It should not advertise third-party plugin support until transport, identity, supervision, compatibility, recovery, and provider-specific tests are implemented and observed together.

## Exercises

1. Locate one runtime-integrated seam and one interface whose controller is not started by the default server. Identify the constructor or missing composition that determines the classification.
2. Run the adapter contract and change the compatible handshake to omit task idempotency. Explain why rejection must happen before container creation.
3. Model a create that succeeds remotely but loses its response. Specify the identifier used for retry and the query needed after adapter restart.
4. Review a proposal granting a storage plugin unrestricted host access because it runs outside the server process. Identify the unsafe assumption and define three concrete acceptance checks.

Worked answers are in [Chapter 33 solutions](../solutions/ch33.md). The [claim ledger](../../validation/evidence/ch33.json) records source classification and execution scope.
