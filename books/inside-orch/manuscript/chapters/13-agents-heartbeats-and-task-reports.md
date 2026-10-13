# Chapter 13 - Agents, Heartbeats, and Task Reports

The server has decided that Atlas task T belongs on node N. Only the worker can observe whether Docker actually created its container. That split turns a simple deployment into a protocol: enroll the worker, maintain its identity, fetch assignments, apply local effects and report observations. Every network response can be delayed or lost, so the protocol must be read as a sequence of potentially ambiguous steps rather than one successful RPC.

This chapter assumes lifecycle guards, runtime adoption and the default server's state boundary. You will trace one enrollment and assignment, distinguish the agent's local authority from the server's desired-state decisions, and reason about a lost running report. The goal is a concrete delivery model with explicit trust and cancellation limits, not an invented exactly-once guarantee.

## Enrollment and Agent Credentials

The agent executable loads configuration, constructs its runner and starts the logging/runtime side of the process. Runner.Run validates configuration and creates an HTTP client or Engine runtime when they were not injected. It detects capacity, registers with the server and keeps the returned node identity for later heartbeat and task operations. [Claim ch13.enrollment](../../validation/evidence/ch13.json).

The bootstrap token authorizes initial registration. The server can issue an agent credential whose plaintext is returned to the worker while a hash, expiry and revoked flag are stored with node identity. The token issuer generates 32 random bytes and encodes them; its default lifetime is 15 minutes. The credential validator checks revocation, token/hash equality and expiry against the supplied current instant. It does not turn an HTTP connection into mutual TLS.

[internal/auth/agent.go, lines 44–57](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/auth/agent.go#L44-L57) at the locked revision.

```go
	raw := make([]byte, 32)
	if _, err := rand.Read(raw); err != nil {
		return AgentCredential{}, AgentCredentialRecord{}, fmt.Errorf("generate agent credential: %w", err)
	}
	token := base64.RawURLEncoding.EncodeToString(raw)
	expiresAt := time.Now().UTC().Add(i.ttl())
	return AgentCredential{Token: token, ExpiresAt: expiresAt}, AgentCredentialRecord{
		Hash:      HashAgentToken(token),
		ExpiresAt: expiresAt,
	}, nil
}

func (i *TokenAgentCredentialIssuer) Validate(_ context.Context, token string, record AgentCredentialRecord, now time.Time) error {
	if record.Revoked {
```

The HTTP client stores a credential returned by registration or heartbeat and reuses it on subsequent requests. Bootstrap and enrolled credential roles are therefore distinct. A copied development token in every operator example would hide that distinction and unnecessarily spread credentials into shell history. Lab commands keep disposable secrets in the process environment and execution evidence records only environment key names.

Identity is also bounded by state ownership. With the default MemoryService, the node's credential record lives in the server process. Restarting that process can invalidate the worker's relationship even if Docker containers continue running. Do not describe credential reuse as durable enrollment across arbitrary server loss; inspect the re-registration and rejection behavior separately.

A worker holding Docker access belongs to the trusted computing base. Even strong API authorization cannot prevent a compromised socket-capable agent from reading or altering its own host's workloads through Docker. The protocol authenticates supported requests; it does not create a kernel or daemon privilege boundary between the agent and the host. Production trust choices require more than changing a bootstrap secret.

## Heartbeat, Polling, and Assigned Tasks

Runner.Run uses a timer derived from HeartbeatInterval with jitter. On each timer event, it performs a heartbeat with retry, updates node state from the response and then reconciles assigned tasks. Assignment polling is therefore sequenced behind the heartbeat. A heartbeat operation that keeps failing can delay task reconciliation; the source does not start an independent perfectly reliable task stream alongside it.

The heartbeat advertises detected CPU/memory as both capacity and allocatable. CPU derives from runtime.NumCPU; memory reads MemTotal on Linux. This is host detection, not an administratively reserved budget after subtracting every unrelated process. The scheduler's declared accounting and the agent's capacity advertisement should not be confused with live cgroup utilization.

Retry behavior is specific. registerWithRetry and heartbeatWithRetry wrap operations in the retry helper. It starts from 250 milliseconds plus randomized delay, doubles backoff while below its threshold and exits when the context is canceled. It does not classify permanent authentication errors separately from transient network errors. A token rejection can therefore occupy the retry loop instead of immediately triggering a different recovery path. [Claim ch13.retry](../../validation/evidence/ch13.json).

[internal/agent/agent.go, lines 792–812](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L792-L812) at the locked revision.

```go
	for {
		err := operation()
		if err == nil {
			return nil
		}
		delay := backoff + time.Duration(rng.Int63n(int64(backoff)))
		timer := time.NewTimer(delay)
		select {
		case <-ctx.Done():
			timer.Stop()
			return ctx.Err()
		case <-timer.C:
		}
		if backoff < 5*time.Second {
			backoff *= 2
		}
	}
}

func DetectCapacity() types.Resources {
	return types.Resources{
```

After a successful heartbeat, reconcileAssignedTasks obtains the assignment collection. If listing fails, it returns before cleanup. On success it builds a map of assigned task identities, attempts each task and finally cleans up managed containers absent from that map. This distinction matters: no successful response is not the same as a successful response containing no tasks. Only the latter supplies the set used for cleanup.

The server owns assignment, desired stop/remove and lifecycle acceptance. The agent owns inspection and local Runtime calls. A task's reported running state is an observation about one container, not permission for the worker to choose arbitrary service intent. NodeID and task ownership checks at the API/control-plane boundary prevent one enrolled node from reporting another node's work as if it were its own.

## Local Container Convergence and Reports

For desired stopped or removed work, ensureTask takes the removal path. For desired running work, it first tries to rediscover a matching container. If a matching container is running, it can re-report running when the task record lacks the correct container ID or remains in an earlier transition state. This is the recovery path for an agent restart that loses local memory but retains server task identity and labelled runtime objects.

When no matching container exists, the agent reports pulling, pulls the selected image with supplied registry auth, creates a typed ContainerSpec, reports created, starts the container and reports running. Health observations happen after those execution steps. The request carries NodeID, status, ContainerID where known, failure reason where applicable and exit code for finite completion/failure. [Claim ch13.reports](../../validation/evidence/ch13.json).

Those reports are individual requests. reportTaskStatus itself does not call the generic retry helper; it sends once and increments a state-change metric on success. Recovery can occur through a later reconciliation pass, which re-observes the container and task state. Saying every status request is automatically retried with the registration backoff would misdescribe the implementation.

A failure after Docker create but before a successful created report leaves an ambiguity: the server may not know the container ID, while Docker already has the side effect. The label-based lookup from chapter 12 lets the next pass recover it. A failure after the server accepted running but before the client received the response can lead to another running report. Lifecycle guards and idempotent terminal duplicates determine which repeats are allowed.

| Boundary | Writer/observer | Relevant evidence |
| --- | --- | --- |
| Desired service replicas | Operator/server | Service mutation and reconciliation |
| Node readiness | Heartbeat/server monitor | LastHeartbeatAt and timeout handling |
| Actual container state | Agent/Docker | Inspect and status request |
| Acceptance of task report | Server | Ownership and lifecycle guards |
| Physical stop of an isolated old worker | Not established by missing heartbeat | Requires fencing beyond replacement |

The failure reason is also part of the trust boundary. Runtime errors can contain operational details, and generic log statements can spread those details if callers include credentials. The existence of redacted configuration views does not sanitize every arbitrary error string. Keep registry auth and bearer values out of experiment output, and inspect each report/log field rather than claiming universal secret redaction.

## Dropped Reports and Cancellation

Consider a concrete timeline. The agent starts container C for task T and sends running. The server accepts it, but the response disappears. The agent returns an error to the local reconciliation loop and logs a warning. On the next successful heartbeat/poll, it inspects C, compares task metadata and may recover without creating another container. This is repeated convergence under ambiguous acknowledgement, not exactly-once delivery.

Now insert an operator delete before that later report. Desired state becomes stopped or removed. The server's AgentCanReportTaskStatus guard must not let an old running observation resurrect work after that desired transition. The focused control-plane tests explicitly cover nonresurrection and terminal duplicate idempotence. A lifecycle rejection does not physically stop a partitioned old container; it prevents an invalid state update in the authoritative record.

Cancellation stops the main timer loop, and graceful shutdown attempts a final heartbeat using a new background context bounded by GracefulShutdownTTL. Failure to notify shutdown is logged but does not block termination forever. This is a best-effort notification, not proof that every container stopped or that the control plane observed shutdown before the process exited.

A subtle operational implication follows from sequential polling. If an external call ignores cancellation, cancellation of the top-level context alone does not prove every subordinate activity has ended. The supplied HTTP client has a 15-second timeout and request contexts, and runtime methods accept contexts, but each adapter's behavior still deserves its own test. Chapter 16 examines the log stream's additional goroutine and reader boundaries.

## Development History and Atlas Lab

[5cf9213849164ce1bebc4e042cc37bf5553c2427](https://github.com/alekpopovic/orch/commit/5cf9213849164ce1bebc4e042cc37bf5553c2427) introduced registration/heartbeat flow. [239eb6abab67773e20a18944ac38e2589802946a](https://github.com/alekpopovic/orch/commit/239eb6abab67773e20a18944ac38e2589802946a) connected task assignment reconciliation. [4f25e78c229ba040c07a84801490485b5a0cbb2e](https://github.com/alekpopovic/orch/commit/4f25e78c229ba040c07a84801490485b5a0cbb2e) changed credential reuse and agent authentication. Original prompts 07,08 and 19 are retrospective requested scope; the actual patches establish implementation history without proving a literal prompt execution transcript.

The source-only experiment runs agent restart/re-report, server heartbeat transitions, stopped-task nonresurrection and terminal duplicate cases. It uses injected clients/FakeRuntime and therefore does not need Docker or a database. The [focused record](../../validation/labs/ch13/focused-tests.json) passed with the exact package selection and test names in its raw output.

```sh
go test ./internal/agent ./internal/controlplane ./internal/auth \
  -run 'TestReconcileAssignedTaskReReports|TestAgentTaskStatusCannotResurrect|TestAgentTaskStatusTerminalDuplicate|TestAgentHeartbeat|TestAgentCredential' \
  -count=1 -v
```

Run this from the disposable pinned source with Go 1.25, the environment contract's GOROOT/caches and external integration flags unset. Examine the test's retained objects: agent reconstruction keeps the server task and runtime container fixture. Record that scope before explaining its success. A separate lost-response teaching fixture should inject failure after server acceptance, not merely return an error before any mutation; those two cases exercise different ambiguity windows.

For an optional process experiment, use one owned server and agent on loopback, save their PIDs and exact task/container IDs, then terminate only the agent. Observe the returned node and task reports after restart. Do not stop host networking to imitate a partition, and do not share the worker node identity with unrelated containers. Stop the agent before deleting its exact owned runtime objects. A fresh server restart remains the separate state-loss experiment from chapter 6.

A heartbeat and a task report should also be tested under different failure schedules. Suppose the heartbeat succeeds while reporting running fails. The server can reasonably consider the node reachable while its task state remains stale. Conversely, a workload may keep serving traffic while heartbeats are lost. Observing one channel cannot substitute for inspecting the other. In a fake-client experiment, record the method, node/task identity and error for each call; then compare the server-side task snapshot after the next reconciliation pass.

This distinction matters for an incident dashboard. A green node icon does not establish that every task transition arrived, and a stale task icon does not establish that the local process has stopped. Preserve the last accepted heartbeat time, last accepted task report and a separately scoped runtime observation. They answer three different questions. The existing stale-report guards protect accepted control-plane state; they do not remotely interrupt a process on a partitioned host. An operator deciding whether to start a replacement must understand that additional physical fencing or externally enforced ownership is still a separate requirement.

## Exercises

1. Identify which operations use the generic retry helper and which status-report operation does not. How can the latter still recover later?
2. Model a running report accepted by the server but not acknowledged to the agent. Which persistent identities make the next pass safe?
3. Explain why a rejected stale running report and an offline-node replacement do not establish physical fencing.
4. Design a cancellation test that distinguishes leaving Runner.Run from ending every transport/runtime activity. Include one observable resource that must close.

[Worked answers](../solutions/ch13.md) retain the distinction between authentication, delivery and physical side effects. Use the protocol to reason about bounded trust and recovery; do not promote a successful heartbeat or fake restart into a broader guarantee than its actual path supports.
