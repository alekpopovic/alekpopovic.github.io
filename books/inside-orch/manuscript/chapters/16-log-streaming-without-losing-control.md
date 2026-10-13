# Chapter 16 - Log Streaming Without Losing Control

Atlas API is running, but an operator needs to see what it wrote before a failed request. The CLI opens a stream through the server, which contacts the worker, which reads Docker logs. Each hop owns a connection or reader, and the operator can disconnect at any moment. A useful log feature must therefore do more than print lines: it must identify the right task, preserve meaningful error boundaries and stop work when its consumer disappears.

This chapter assumes agent identity, Docker runtime methods and the difference between events and application output. You will trace the actual files, distinguish stdout/stderr framing from the text the operator receives, and reason about slow consumers and cancellation. This path is an on-demand stream, not an invented persistent centralized collector.

## The Client-to-Server-to-Agent Stream

The command is logs <service-name-or-id>, with optional --task, --follow and --tail. The CLI resolves the service before requesting its log stream; selecting a task makes the target explicit during a rollout or scale change. The client forwards a request to /v1/logs. These are current CLI shapes, not commands inferred from a planned package named logs.

On the server, the handler resolves a task, requires a known container ID and obtains its node. Offline or unknown node state is rejected before contacting the worker. The server sets a plain-text response and passes the task ID, advertised agent address, follow/tail values and configured bootstrap token to AgentHTTPLogStreamer. [Claim ch16.proxy](../../validation/evidence/ch16.json).

The streamer builds /v1/agent/logs with URL-encoded query parameters, attaches the supplied bearer token and creates the outbound request with the incoming context. A non-success agent status becomes an error with a bounded response-body read. Successful response bytes are copied to the operator's writer. The public stream therefore depends on both API authorization and the separate server-to-agent credential path.

[internal/api/logs.go, lines 33–51](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/logs.go#L33-L51) at the locked revision.

```go
	baseURL := normalizeAgentURL(req.AgentURL)
	values := url.Values{}
	values.Set("task_id", req.TaskID)
	if req.Follow {
		values.Set("follow", "true")
	}
	if strings.TrimSpace(req.Tail) != "" {
		values.Set("tail", strings.TrimSpace(req.Tail))
	}
	httpReq, err := http.NewRequestWithContext(ctx, http.MethodGet, baseURL+"/v1/agent/logs?"+values.Encode(), nil)
	if err != nil {
		return fmt.Errorf("create agent logs request: %w", err)
	}
	if req.Token != "" {
		httpReq.Header.Set("Authorization", "Bearer "+req.Token)
	}
	resp, err := client.Do(httpReq)
	if err != nil {
		return fmt.Errorf("request agent logs: %w", err)
```

The worker's log handler accepts its configured token, finds a managed container by task ID and calls Runtime.StreamLogs. At this baseline the worker log handler uses the bootstrap token configured at startup; it is not automatically the same short-lived enrolled credential used for node reports. Conflating those credentials would conceal an important operational trust boundary.

An advertised agent address is also an outbound destination used by the control plane. Treat worker enrollment and allowed worker endpoints as part of trusted configuration. The health-check target restrictions from chapter 14 apply to their own caller path; they do not automatically constrain the server's log proxy. Each outbound facility needs a separate source trace and network policy.

## Docker Frames and Application Output

Docker can multiplex stdout and stderr in its log transport. The Engine adapter obtains a reader and uses stdcopy.StdCopy to split it into stdout and stderr pipes. Separate scanner goroutines turn each pipe into LogLine values tagged with Stream and a read-time UTC timestamp. This structured intermediate representation carries information that the final plain-text handler does not preserve. [Claim ch16.frames](../../validation/evidence/ch16.json).

[internal/docker/docker.go, lines 326–335](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L326-L335) at the locked revision.

```go

		stdoutReader, stdoutWriter := io.Pipe()
		stderrReader, stderrWriter := io.Pipe()
		copyErr := make(chan error, 1)
		go func() {
			_, err := stdcopy.StdCopy(stdoutWriter, stderrWriter, reader)
			_ = stdoutWriter.Close()
			_ = stderrWriter.Close()
			copyErr <- err
		}()
```

The agent sends line.Line with Fprintln and flushes when the writer supports flushing. It discards the LogLine.Stream field and timestamp in that response. The operator sees newline-delimited text, not a structured record that reliably identifies stderr versus stdout. A displayed timestamp should not be invented from the intermediate read time when the output did not include it.

The two scanner goroutines also do not establish one globally ordered sequence across both streams. Each stream retains its reader's order, but their shared-channel interleaving depends on scheduling and arrival. If precise cross-stream ordering matters, the application should emit its own correlation/timing fields or a future structured transport should expose an explicitly defined ordering model. The current text output cannot reconstruct information that was discarded.

Application stdout/stderr differs from orchestration domain events. A task.failed event explains a control-plane observation and related task identity; an application error line explains the workload's own execution. A deployment can generate domain events without ever starting a container, and a healthy container can write errors without changing service intent. Combine both records during diagnosis rather than searching one as a substitute for the other.

The scanner uses its default buffer behavior without a custom Buffer configuration in this source. Exceptionally large unbroken lines can therefore surface scanner errors. That is a bounded parsing concern, not an unlimited-log guarantee. A teaching structured-log extension should choose and test its line/frame limits explicitly, including what the operator sees after the limit is exceeded.

## Tail, Follow, Disconnect, and Cancellation

Tail selects how much prior output Docker should return, while follow keeps reading later output. The CLI passes a string; the worker's tailValue accepts integer text and otherwise falls back to all. This is permissive normalization rather than strict validation of every nonnegative bound. A malformed value can therefore request more history than the operator intended, and a negative integer is left for downstream behavior.

Runtime.StreamLogs forwards follow, tail and optional runtime fields such as since/until/timestamps to the Engine request. The public CLI discussed here exposes only its current subset. Do not document unimplemented CLI switches merely because the lower-level LogOptions structure has those fields. [Claim ch16.options](../../validation/evidence/ch16.json).

The handler selects between incoming lines and request-context cancellation. If the operator disconnects and the request context is canceled, it can return promptly. The outbound proxy request also carries context, so cancellation can propagate to the worker connection. At the runtime layer, scanLogStream checks cancellation before sending a scanned line to the channel.

[internal/docker/docker.go, lines 612–623](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L612-L623) at the locked revision.

```go
func scanLogStream(ctx context.Context, reader io.Reader, stream string, out chan<- LogLine, done chan<- error) {
	scanner := bufio.NewScanner(reader)
	for scanner.Scan() {
		select {
		case <-ctx.Done():
			done <- ctx.Err()
			return
		case out <- LogLine{Stream: stream, Line: scanner.Text(), Timestamp: time.Now().UTC()}:
		}
	}
	done <- scanner.Err()
}
```

Those checks are useful but not identical to proving every reader and goroutine closes under every blocked-I/O state. A scanner can be waiting in reader.Scan before it reaches the select, and a copy goroutine can be blocked on a pipe. Engine StreamLogs coordinates both scanner completions and the framing copy before its deferred reader close. A complete transport shutdown test must exercise those blocked states, not only a cooperative fake that immediately notices context cancellation.

This is the chapter's failure window. The client disappears while one stream writer or reader is blocked. The HTTP handler may return, yet a subordinate goroutine can remain if the cancellation path does not unblock its specific I/O operation. Source inspection identifies the risk and the tests establish their actual scope; neither permits a blanket assertion that all possible real Engine streams are leak-free.

Slow consumers create related backpressure. The adapter's line channel is unbuffered, and the HTTP writer can block while the operator reads slowly. Buffering everything would merely move the problem into memory growth. A deliberate design chooses a bounded queue, a cancellation/deadline strategy and an observable error/drop policy. That would be a separately tested teaching extension, not a configuration switch already present in this stream.

Transport errors after streaming starts have another limit. The server flushes headers before copying worker output. If the worker later fails, the server cannot replace the already-started plain-text response with a fresh structured JSON error status. It logs the failure and the client can receive a truncated stream. A successful initial HTTP status is therefore not a receipt that the complete requested history arrived.

| Failure point | Operator-visible possibility | Additional evidence |
| --- | --- | --- |
| No task container known | Request rejected before streaming | Task/container state |
| Worker returns non-success | Proxy logs error after headers may start | Agent/server diagnostic logs |
| Client disconnects | Stream ends/cancels | Handler and runtime cleanup assertions |
| Docker disappears mid-follow | Partial output, transport error | Runtime reader/copy error |
| Task/container deleted | Existing reader may end or fail | Exact task/container IDs and deletion timeline |

## Boundaries of Log Retention

The stream reads whatever the configured Docker logging path can supply. The orchestrator does not persist a duplicate central log archive in MemoryService, PostgresStore or an external collector through this implementation. Removing a container or changing daemon logging/rotation can change what remains available. An older task's log request cannot be guaranteed after its runtime object disappears.

A service name is particularly ambiguous during a rollout. Multiple tasks may exist across versions, and a default task selection can differ from the operator's failing replica. Record service ID, task ID, container ID, node ID and deployment version when saving a diagnostic excerpt. Use --task when reproducing a specific failure. A screenshot of generic service logs without those identities is weak evidence about which version actually emitted a line.

The text stream also does not universally redact application output. The workload can print a password or selected user value, and the handler writes that text. Audit metadata redaction and notifier sanitization are different code paths. Use deliberately nonsecret fixtures, redact copied evidence where required and keep the raw sensitive data out of the manuscript rather than claiming a sanitizer that is absent.

For a centralized retention design, define collector ownership, authentication, bounded storage, rotation, tenant scoping, correlation and restart behavior. Test the failure case where collection stops while the workload continues. Calling the existing log proxy a collector would skip all of those contracts and create an operational expectation the source does not meet.

## History and Atlas Lab

[39e2359653e0e8790feda86eb5fbee3eb5ae509f](https://github.com/alekpopovic/orch/commit/39e2359653e0e8790feda86eb5fbee3eb5ae509f) introduced the agent HTTP handler, API proxy and basic streaming integration. Its patch also adds cancellation-related test structure. Original development prompt 12 is retrospective intent, not a timestamped claim that the described test ran when that prompt first appeared. Follow the actual internal/agent, internal/api and internal/docker files rather than the planned package tree.

The source-only lab uses a FakeRuntime whose log stream intentionally blocks until cancellation. TestLogHandlerStopsOnCancellation starts the handler with a request context, waits until streaming begins, cancels and requires handler completion. The runtime's own fake-stream fixture drains its channels after cancellation. The [actual focused run](../../validation/labs/ch16/focused-tests.json) passed both. It does not exercise a real Engine reader blocked in stdcopy or every proxy hop.

```sh
go test ./internal/agent ./internal/docker \
  -run 'TestLogHandlerStopsOnCancellation|TestFakeRuntimeStreamLogsCanBlockUntilContextCancellation' \
  -count=1 -v
```

Run from the disposable pinned source with Go 1.25 and the environment contract's GOROOT/cache settings. The fixtures create no host container and require no PostgreSQL or external network. Their cleanup is context cancellation, goroutine completion and process exit. Reading the completion assertion is essential: a test that only calls cancel without waiting would establish almost nothing about cleanup.

The separate [actual Docker flow](../../validation/intake/docker-complete-flow-log-guard.json) verifies deploy, HTTP access, bounded logs, scaling and deletion for the owned lab workload. That proves a useful end-to-end path in its environment, but it is still not the targeted blocked-stream disconnect experiment. Keep those claims separate. An optional real follow/disconnect test should record reader/goroutine completion and task identity while removing only the exact owned container after the agent is stopped.

## Exercises

1. Which stdout/stderr information exists in LogLine but disappears in the final text response? Why can line order not recover it?
2. Compare tail and follow. What does a malformed tail string become in the worker handler?
3. Explain why the passing fake cancellation test does not prove every Engine pipe/scanner exits after a client disconnect.
4. Design a bounded slow-consumer extension with an explicit overflow/deadline policy and a test involving a disappearing task.

[Worked answers](../solutions/ch16.md) separate the observed fake cleanup, the real bounded log path and the still narrower blocked-I/O question. Preserve that evidence budget when deciding what operators can safely expect from streaming and retention.
