# Chapter 20 - Endpoint Discovery and Internal DNS

After the worker experiment, Atlas API still has a stable service name but different task locations. A client that retained yesterday's node address cannot reach today's replacement merely because the control plane reports the desired replica count. Discovery must expose the current endpoint set, and the client must interpret that set correctly. Adding a DNS name improves naming, but it does not create a virtual network or eliminate published-port identity.

You will derive endpoints from task reports, compare the HTTP discovery builder with the optional DNS implementation, and analyze a stale-cache window after rescheduling. Chapters 14 and 19 supply health and node-loss vocabulary. The central question is which observed fields make an address useful, and which facts the response does not establish. This is the current host-port model, with no implied overlay or Kubernetes-compatible DNS service.

## Endpoint Sets and Health Filtering

BuildServiceEndpoints receives one service, tasks and nodes. It indexes nodes by ID, then ignores tasks for another service or tasks without a node assignment. Its includeTask helper requires desired running before interpreting actual status. Running and healthy are included by default; unhealthy is included only when the caller explicitly requests it. Pending, failed, stopped and removed are not useful service endpoints here.

Unchanged source excerpt — [internal/discovery/discovery.go:98–110](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery.go#L98-L110):

```go
func includeTask(task types.Task, includeUnhealthy bool) bool {
	if task.DesiredStatus != types.TaskRunning {
		return false
	}
	switch task.ActualStatus {
	case types.TaskRunning, types.TaskHealthy:
		return true
	case types.TaskUnhealthy:
		return includeUnhealthy
	default:
		return false
	}
}
```

For each accepted task the builder finds its node and iterates task ports. It prefers task-specific ports when present, falling back to service-spec ports otherwise. That distinction matters when dynamic host ports were assigned: the workload's container port can remain80 while different tasks publish on different host ports. An endpoint response must describe the actual task assignment rather than repeat a public-zero request from the service specification.

The emitted record carries service name/ID, task ID, node ID/address, public host port, container port, protocol, health status and service version. Sort order is deterministic by service name, task, container port, protocol and published port. Stable ordering is useful for diffing; it is not sticky load balancing or a guarantee that two sequential responses represent one atomic runtime snapshot.

Node presence is required, but this builder does not independently exclude a node merely because Node.Status is offline. The ordinary lost-node path changes task state, which usually removes it through the task predicate. Those are different claims. If a fixture deliberately supplies an offline node with a running desired-running task, inspect the builder's result instead of assuming an unstated node-health filter.

BuildAllServiceEndpoints additionally skips services with a nonempty non-active status. It sorts the services it receives. Developers embedding the helper should notice that it sorts that slice, whereas other helpers copy before sorting. The practical contract is about both visible records and inputs; do not add a concurrent caller that assumes the slice is untouched without testing ownership.

## Namespace Names and DNS Records

The optional internal DNS server is activated by ORCH_DNS_ADDR in default main. TTL defaults to thirty seconds, with a positive configured duration parsed by startup. The resolver supports service.svc.orch in the default namespace and service.namespace.svc.orch for an explicit namespace. It lowercases and trims a trailing dot. Other name shapes are rejected rather than interpreted as general Kubernetes search-domain behavior.

DNS Resolve selects the namespace context and finds an active service by its name. It lists that service's tasks and the available nodes, then extracts node advertise addresses from running or healthy tasks. This is a separate implementation, not a call to discovery.BuildServiceEndpoints. In particular, Resolve checks actual running/healthy but does not perform the endpoint helper's desired-running predicate. A task awaiting stop can therefore require separate analysis in the DNS path.

Unchanged source excerpt — [internal/dns/server.go:97–121](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server.go#L97-L121):

```go
	out := []net.IP{}
	seen := map[string]struct{}{}
	for _, t := range tasks {
		if t.ActualStatus != types.TaskHealthy && t.ActualStatus != types.TaskRunning {
			continue
		}
		host, _, err := net.SplitHostPort(addresses[t.NodeID])
		if err != nil {
			host = addresses[t.NodeID]
		}
		ip := net.ParseIP(host).To4()
		if ip == nil {
			continue
		}
		if _, ok := seen[ip.String()]; !ok {
			seen[ip.String()] = struct{}{}
			out = append(out, ip)
		}
	}
	return out, nil
}
func parseName(name, defaultNS string) (string, string, bool) {
	parts := strings.Split(strings.TrimSuffix(strings.ToLower(strings.TrimSpace(name)), "."), ".")
	if len(parts) == 4 && parts[1] == "svc" && parts[2] == "orch" {
		return "", "", false
```

The address conversion splits an advertise host/port where possible, parses the host as an IP and calls To4. Hostnames and IPv6-only addresses are skipped by this implementation. Multiple tasks on the same node contribute one deduplicated IPv4 address, not one DNS answer per replica. A client counting answers to infer replica count will therefore get the wrong abstraction.

ServePacket implements a small DNS response path: it expects one question, decodes labels and emits A answers with the configured TTL. Non-A questions receive no A records; this is not proof of a complete recursive resolver, SRV discovery or IPv6 service addressing. The server's query/error counters measure this component's work, not application request success.

## Node Addresses Still Need Ports

Suppose Atlas task A publishes container 80 as host 31081 on node 192.0.2.10, while task B publishes the same container port as 31082 on 192.0.2.11. These documentation addresses are illustrative, not reachable lab targets. The HTTP endpoint records preserve both pairs. DNS can return the node IPs, but an A record carries no task's host port. Resolving the service name and blindly connecting to port 80 can therefore fail despite a perfectly valid answer.

If every selected node uses one known fixed published port, a client can combine the DNS name with that configured port. With dynamic per-task ports, it needs the richer endpoint API or a gateway that consumes it. Naming and routing are separate mechanisms. A stable logical name does not guarantee a stable socket destination, and a successful lookup does not prove that the firewall, daemon binding or application permits the connection.

The upstream DNS compose example demonstrates a client configured to query the server's DNS address on an isolated compose network. It does not create a service VIP. It also does not supply a complete Atlas deployment by itself; the service, tasks and node advertisements still have to exist in the control plane. Treat the example as topology/configuration evidence and verify all prerequisites before calling it a working application network.

| Surface | Address identity | Port information | Important filter |
| --- | --- | --- | --- |
| HTTP endpoints | Per task/node record | Public and container ports | Desired running plus actual running/healthy; optional unhealthy |
| DNS A answers | Deduplicated node IPv4 | None | Actual running/healthy in separate resolver |
| Direct application socket | Specific host and published port | Required | Actual reachability tested independently |

These distinctions also explain why include_unhealthy is a diagnostic option rather than a request to route normal traffic indiscriminately. It expands the observed set; it does not fix an unhealthy application or make an offline worker reachable.

## Rescheduling, TTL, and Stale Clients

Consider a client caching node A at time zero with a thirty-second TTL. At second ten, the server replaces Atlas on node B and task A becomes obsolete. A new query may already return B, but the earlier client can retain A until its cache expires. Even that expiry does not guarantee an open connection moves: connection pooling, application-level retries and each client's resolver behavior are separate layers.

This timeline is hypothetical arithmetic, not a measured thirty-second recovery. Real effective staleness includes the task report delay, node-monitor cadence, DNS query time, intermediary caches and the client's policy. The TTL field is one bound offered to compliant caches, not a universal reconnection deadline. Lowering it trades query volume for freshness and does not repair a wrong node address or missing port.

A further ambiguity occurs while desired stop and actual running disagree. HTTP discovery can exclude the task through desired status while DNS Resolve still accepts its actual status. That divergence is source-derived and testable with a synthetic task. Do not silently claim both surfaces use identical filters just because documentation groups them under service discovery. A review can propose sharing the helper later, but that would be a change outside this pinned baseline.

For an operator, a useful incident record saves three snapshots: the control-plane endpoint list, the DNS answer with TTL and the direct socket outcome for the exact returned host/port. Keep task and service versions alongside them. A lookup failure, a stale answer and a refused application connection suggest different recovery owners and should not collapse into one message saying “DNS is broken.”

Namespace selection also differs from authorization. Encoding a namespace in the DNS name selects which service records to inspect; it does not present a user JWT or prove that the querying client has an API role. Bind the experimental resolver only where intended clients can reach it. Do not describe the namespace spelling itself as confidential tenant isolation.

## Atlas Lab: Compare Two Selection Functions

Use Go 1.25 and the disposable pinned source copy. The deterministic phase needs no real Docker or external DNS. Inspect the fixtures that build healthy/unhealthy tasks and verify task-specific assigned ports. The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) includes discovery and DNS cases with caching disabled. It records package assertions over fixture data, separately from the optional owned-listener experiment below.

```bash
go test ./internal/discovery -run 'TestBuildServiceEndpoints(FiltersByHealth|UsesTaskAssignedPorts)$' -count=1 -v
go test ./internal/dns -run 'TestResolve(HealthyEndpointsAndDNSPacket|RejectsUnsupportedName)$' -count=1 -v
```

Add an explicitly separate teaching fixture for desired-stopped/actual-running if you want to demonstrate the filter divergence. It should feed the same synthetic identities into each function and assert the source-derived difference, with no network dependency. Keep that fixture outside immutable evidence and distinguish its result from the existing upstream tests.

For a live owned Atlas environment, first save service/task/node records and exact published ports. Query the loopback API's endpoint surface, then query only the owned DNS listener. Configure a free nonprivileged local UDP port rather than assuming permission to occupy host port 53. Compare answers before and after a run-owned task's health transition. Request a direct application endpoint separately using the recorded host/port; never send test traffic to illustrative documentation addresses.

Abort if advertisements resolve to an unowned host, the DNS listener conflicts with an existing service, or the client configuration would change the host's global resolver. Cleanup closes the owned listener and restores only the disposable client configuration. Save answer bytes or parsed records, TTL, UTC times and command exits. Captured DNS names improve observability, but the experiment cannot establish an overlay, service VIP, universal cache behavior or kernel network isolation.

## Exercises

1. Two healthy Atlas tasks share a node but use different public ports. How many node-IP answers can DNS return, and why is that insufficient endpoint identity?
2. Predict HTTP discovery and DNS selection for a task with desired stopped and actual running. Which implementation difference controls the result?
3. An advertise address is an IPv6 literal or hostname. Explain what this DNS resolver does and why API endpoint presence does not contradict it.
4. A client still reaches the old worker after the new endpoint appears. Design evidence that distinguishes TTL caching, pooled connections and a wrong public port without claiming a universal recovery deadline.

[Worked answers](../solutions/ch20.md) retain the different filtering and addressing boundaries. Future networking designs can improve them, but the current book must describe the socket that actually exists.

## Development history and source references

Original development prompts 35, 78 supply the requested scope. The inspected implementation history includes [03f8c30f6df8](https://github.com/alekpopovic/orch/commit/03f8c30f6df8d6eb9abadb729b9a92cf7f460c4a), [4d641bbe8913](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/discovery/discovery.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery.go#L1-L117)
- [internal/discovery/discovery_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/discovery/discovery_test.go#L1-L68)
- [internal/dns/server.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server.go#L1-L222)
- [internal/dns/server_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/dns/server_test.go#L1-L79)
- [docs/SERVICE_DISCOVERY.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/SERVICE_DISCOVERY.md#L1-L50)
- [deployments/examples/internal-dns-compose.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/internal-dns-compose.yaml#L1-L20)
