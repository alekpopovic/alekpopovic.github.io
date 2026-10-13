# Chapter 14 - Health Checks That Respect Trust Boundaries

Atlas API's container is running, yet requests to its application path fail. Treating running as healthy would send traffic to a process that cannot satisfy users and could advance a rollout too early. A probe gives the agent another observation, but it also makes the agent initiate network requests on someone else's behalf. Correctness and outbound trust must therefore be examined together.

This chapter assumes agent reporting and published-port handling. You will trace a configured path into the exact HTTP/TCP target, calculate when repeated results cross a threshold and distinguish a bounded health check from general network isolation. The examples use fake checkers and owned loopback listeners; none contact cloud metadata services or arbitrary private hosts.

## Running Is Not Healthy

Execution status and health answer different questions. Docker running means the process has started and has not yet been observed exited. An HTTP health result describes one request to one endpoint at one instant. Neither proves a complete business transaction, dependency availability or future responsiveness. Keeping these observations separate lets operators diagnose whether failure occurred before startup or after an application became reachable.

The agent only probes tasks whose actual state is running, healthy or unhealthy and whose healthcheck type is enabled. No configured check produces no new health report from this path. That absence should not be displayed as measured application health. A rollout or discovery component must interpret the task state it actually receives, rather than inventing a successful probe because a container exists.

A task can move healthy→unhealthy and later unhealthy→healthy according to the shared lifecycle guard. The server may also apply restart policy after unhealthy observations. Those downstream decisions must be traced independently: a probe returns an observation; it does not itself stop Docker, replace a node or select a rollout version. [Claim ch14.health-state](../../validation/evidence/ch14.json).

For Atlas, start from a path that serves successfully, then use the deliberately absent /atlas-deliberately-absent path in the lab fixture. Both manifests use the same image and service identity. The failed request isolates application-path health from image pull and process startup. Changing the image to a nonexistent reference would test a different failure phase and would not establish health threshold behavior.

## HTTP and TCP Probe Decisions

healthProbe does not accept an arbitrary hostname from deployment YAML. It finds a suitable assigned TCP published port, builds the target at127.0.0.1 and combines the validated scheme/path for HTTP. A requested health port can match an assigned public or container port; an unassigned port does not yield a probe. [Claim ch14.target](../../validation/evidence/ch14.json).

[internal/agent/agent.go, lines 562–585](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L562-L585) at the locked revision.

```go
	port, ok := healthcheckProbePort(check.Port, ports)
	if !ok {
		return health.Check{}, false
	}
	timeout := check.Timeout
	if timeout <= 0 {
		timeout = 2 * time.Second
	}
	target := "127.0.0.1:" + strconv.Itoa(port)
	switch check.Type {
	case types.HealthcheckHTTP:
		path := check.Path
		if !strings.HasPrefix(path, "/") {
			path = "/" + path
		}
		scheme := strings.ToLower(strings.TrimSpace(check.Scheme))
		if scheme == "" {
			scheme = "http"
		}
		return health.Check{Type: health.HTTPProbe, Target: scheme + "://" + target + path, Timeout: timeout}, true
	case types.HealthcheckTCP:
		return health.Check{Type: health.TCPProbe, Target: target, Timeout: timeout}, true
	default:
		return health.Check{}, false
```

This is a host-side probe of the task's published port, not a request inside the container's network namespace. A process bound on an unexpected port, a missing host binding or a wrong path can all make a running container unhealthy. If no assigned port matches, the agent skips probing; it does not magically discover an internal container address. That behavior is a useful source-reading checkpoint when a manifest looks valid but no health observations appear.

The domain/CLI validation requires a safe path and supported scheme. Absolute URLs and protocol-relative path forms must not turn a relative application path into a different target. The agent's target builder lowercases/defaults the scheme and ensures a leading slash, while the validation layer establishes stronger permitted-input constraints. A builder's small normalization step should not be mistaken for a complete independent parser.

DefaultChecker dispatches HTTP and TCP probes. HTTP creates a GET request with a context and timeout, follows only permitted redirects, drains at most64KiB of response body and evaluates status. Statuses from200 up to but excluding400 are considered healthy after the client's redirect behavior. TCP merely establishes and closes a connection. A successful TCP connect does not prove the HTTP route or response body is correct.

The response body cap limits how much content is read; it does not reject a large response purely because more bytes exist. The huge-body test checks bounded reading rather than an invented payload-validation policy. This distinction prevents a security improvement from being oversold as a content guarantee. Application-specific health semantics, such as checking a JSON field, would need a separate supported checker or teaching extension.

## Timeouts and Repeated Health Reports

Each check has a timeout, defaulting to two seconds when unset or nonpositive at the checker boundary. HTTP uses both a request context and client timeout; TCP uses a context-aware dial. A connection refusal, timeout or blocked redirect generally becomes a result with Healthy false and a message, while malformed configuration or an unsupported probe type can return an error. The agent handles those categories differently.

For an ordinary unhealthy result, the agent increments consecutive failures and clears successes. For a healthy result, it increments successes and clears failures. These are in-memory agent counters keyed by task identity. They are not persisted failure history and do not survive arbitrary agent reconstruction. [Claim ch14.threshold](../../validation/evidence/ch14.json).

When successes reach HealthyThreshold, the agent reports healthy if the task is not already healthy. When failures reach UnhealthyThreshold, it reports unhealthy with the probe message. Defaults are one success and three failures when the relevant threshold is nonpositive. A returned checker error increments the failure metric but returns early before the normal threshold-counter update. Do not count every possible checker error as one accumulated unhealthy observation without following that branch.

Consider Atlas configured with healthy threshold one and unhealthy threshold two. The first successful observation can report healthy. One later404 resets successes and records one failure but does not cross the unhealthy threshold. A second consecutive404 reports unhealthy. A subsequent success resets failures and can report healthy again, unless a server-side restart/deletion transition has already changed the task's admissible state.

| Moment | Observation | Agent counter effect | Possible report |
| --- | --- | --- | --- |
| t0 | Container starts | No probe result yet | Running |
| t1 | HTTP200 | successes1, failures0 | Healthy |
| t2 | HTTP404 | successes0, failures1 | None at threshold 2 |
| t3 | HTTP404 | failures2 | Unhealthy |
| t4 | HTTP200 | successes1, failures0 | Healthy if lifecycle still allows |

These labels are a logical timeline, not measured elapsed seconds. The loop schedules probes alongside heartbeat/task reconciliation and adds health jitter; it does not run a perfectly periodic independent probe every configured interval. Slow requests and other task work can affect observation timing. A threshold of two means two counted observations, not a promise of failure detection within exactly twice the interval.

## SSRF Protection With Explicit Limits

The SSRF hardening is a chain of controls: safe scheme/path input, assigned-port selection, a loopback-generated initial target and same-origin redirects. sameOriginRedirect compares lowercased scheme and host, including the port, against the original URL. It also bounds the redirect chain. A redirect to another loopback port is still another origin and is blocked. [Claim ch14.redirect](../../validation/evidence/ch14.json).

[internal/health/health.go, lines 97–110](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/health/health.go#L97-L110) at the locked revision.

```go
func sameOriginRedirect(origin *url.URL) func(*http.Request, []*http.Request) error {
	originScheme := strings.ToLower(origin.Scheme)
	originHost := strings.ToLower(origin.Host)
	return func(req *http.Request, via []*http.Request) error {
		if len(via) >= 10 {
			return fmt.Errorf("stopped after 10 redirects")
		}
		if strings.ToLower(req.URL.Scheme) != originScheme || strings.ToLower(req.URL.Host) != originHost {
			return fmt.Errorf("healthcheck redirect blocked: %s", req.URL.Redacted())
		}
		return nil
	}
}
```

Use owned local handlers to test this. Handler A can redirect to handler B on a different port; the result should be unhealthy and B should not be treated as the approved target. A same-origin redirect can reach another path on A. There is no need to contact a real metadata address to establish that cross-origin behavior. A fake HTTP transport is also appropriate when testing request construction without listeners.

The generic DefaultChecker accepts a Target string and is not itself a universal address allowlist. The safe initial target described here comes from the agent's builder. Another caller using the checker directly would need its own trusted-target policy. This is why source claims must include both the package and its current caller rather than attributing all target protection to one function.

Loopback targeting is also not tenant network isolation. The agent runs on a host where other processes can listen, and a permitted published port must correspond to the intended container binding. Host-network mode and daemon access introduce broader risks that a redirect check cannot remove. The book's lab avoids arbitrary host probing and keeps workload exposure explicitly separate from operator-facing loopback listeners.

## History and Atlas Lab

Task probing was introduced in [ee067bd0f02566eb600031a0cb81f25919d52445](https://github.com/alekpopovic/orch/commit/ee067bd0f02566eb600031a0cb81f25919d52445). The later hardening commit [f92f0a4fcfd760cbc9f850ab4c2e3e6d5dc8a081](https://github.com/alekpopovic/orch/commit/f92f0a4fcfd760cbc9f850ab4c2e3e6d5dc8a081) changes scheme handling, validation, redirects and body reading. Original prompt 11 is retrospective intent; prompt 53 requests the SSRF work. The inspected tests and changed hunks define the actual controls, not a blanket claim that the agent cannot make any dangerous network request.

The experiment needs Go 1.25 and permission for temporary owned loopback listeners. Docker and PostgreSQL are unnecessary. The first attempt in the restricted environment failed because opening the test listener was denied; that [failure record](../../validation/labs/ch14/focused-tests.json) is preserved. The same pinned tests then ran with the approved loopback capability and [passed](../../validation/labs/ch14/focused-tests-loopback.json). This is an environment restriction followed by an actual successful run, not a source repair.

```sh
go test ./internal/health ./internal/agent \
  -run 'TestHTTPHealthCheck|TestTCPHealthCheck|TestHealthProbeRequiresAssignedPort|TestReconcileAssignedTaskReportsHealth' \
  -count=1 -v
```

Execute from the disposable source copy with the environment contract's toolchain/caches. Inspect the raw output for healthy/unhealthy HTTP cases, timeout, same-origin and external redirect cases, huge-body bound, TCP behavior, assigned-port construction and agent thresholds. The allowed external-redirect test uses local fixtures; no real metadata endpoint is contacted.

All listeners belong to httptest or the local test fixture and close when the tests complete. No system networking configuration is changed. If adding an Atlas process experiment, use the owned unhealthy manifest, record actual conditions and restore the healthy fixture afterwards. Report timings only if measured; preserve image, task and probe configuration with the observation. Stop the exact owned agent/server before removing container IDs.

Choose the probe endpoint as deliberately as its timeout. An Atlas root page can return200 from a cached handler even while the dependency required by the API is unavailable. A readiness endpoint can instead check the minimum dependency needed to accept useful traffic, but it should avoid expensive or destructive work. If every probe performs a costly database operation, the health mechanism can amplify an outage. These are application-level design choices; the orchestrator sees only the resulting observation.

A safe local experiment can expose the distinction with two handlers in an owned loopback server. Keep one endpoint returning200 and make the other return503 under an injected dependency flag. Predict the resulting counters for each chosen path before sending a probe. This exercise requires no real database and does not justify probing a remote service. Record which path was configured and the exact response sequence, because otherwise a healthy result says little about what was actually tested. When the dependency recovers, require the configured consecutive success threshold before expecting a healthy report. Counter reset behavior, endpoint semantics and downstream replacement policy must all agree before an operator can interpret recovery accurately.

## Exercises

1. Starting from running with both healthy and unhealthy thresholds set to two, predict reports for 200,404,200,404,404. Explain why total failures are not the deciding count.
2. Why does a TCP success not establish HTTP health? Give an Atlas failure that separates them.
3. Compare a redirect to another path on the same origin with a redirect to another port on127.0.0.1. Which source check decides?
4. An engineer calls DefaultChecker directly with an arbitrary Target and cites this chapter as proof of an address allowlist. Identify the missing caller boundary and propose a safe local test.

[Worked answers](../solutions/ch14.md) retain each counter transition and trust boundary. Choose health checks for an explicit observation, preserve bounded network behavior, and avoid presenting successful probing as evidence of complete availability or host isolation.
