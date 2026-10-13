# Chapter 21 - Ingress, Host Networking, and the Overlay Roadmap

Atlas now has discoverable task endpoints, but visitors should use an application host name rather than track worker addresses and dynamic ports. The optional Traefik integration supplies that gateway. Its usefulness depends on understanding the actual packet path: a client reaches Traefik, Traefik selects a node-level published port, and Docker forwards to the container. A route definition is neither an overlay network nor a guarantee that every hop is reachable.

This chapter builds on endpoint identity from Chapter 20 and security-policy scope from Chapter 26 when following the operator/architect reading path. You will derive the generated router and service fields, identify failures at gateway and worker boundaries, and separate the executable host-port model from proposed networking improvements. Atlas remains the same stateless API; we change how clients find it, not the orchestrator's underlying runtime architecture.

## The Current Host-Port Packet Path

Docker's adapter maps container ports to published host ports in HostConfig.PortBindings. Ordinary exposure does not require host network mode: Docker port publication and explicitly selecting host networking are different configuration paths. The latter is a privileged policy choice considered in the admission chapter. Calling the whole current model “host-port networking” should not erase that distinction.

A routed Atlas task has a container port describing where the application listens and a public host port describing where a gateway can reach it. The node advertise address may include the agent's own port. That agent port is not the application backend destination; the Traefik builder extracts the host and combines it with the endpoint's PublicHostPort.

Unchanged source excerpt — [internal/traefik/config.go:143–156](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L143-L156):

```go
func endpointURL(endpoint discovery.Endpoint) (string, bool) {
	if endpoint.PublicHostPort <= 0 {
		return "", false
	}
	nodeAddress := strings.TrimSpace(endpoint.NodeAddress)
	if nodeAddress == "" {
		return "", false
	}
	host := addressHost(nodeAddress)
	if host == "" {
		return "", false
	}
	return "http://" + net.JoinHostPort(host, strconv.Itoa(endpoint.PublicHostPort)), true
}
```

This transformation is why a node advertised as http://192.0.2.10:8081 can produce a backend on another port. The documentation address is illustrative; it must never be used as a real experiment target. The builder emits an HTTP URL regardless of the route's client-facing TLS flag. That flag controls the router's TLS configuration, not an automatic HTTPS upgrade for the worker backend.

A complete path has four separately observable boundaries: client to gateway listener, gateway route match, gateway to published worker port and Docker to application listener. Test each one with the exact owned address and Host header. An API response that lists a healthy task cannot establish that firewall rules permit the gateway's connection, or that the application accepts the requested path.

## Traefik Routers and Services

BuildConfig first indexes endpoint sets by ServiceID and sorts a copy of services. It ignores non-active services, validates each route and gathers matching servers. A route without usable servers is skipped, so the output can omit both its router and service. This is preferable to imagining an empty configuration entry is a functioning route, but clients will still observe an unavailable application until a usable backend appears.

Each router contains a Rule and Service name, with an optional empty TLS configuration object. routeRule combines Host and PathPrefix using quoted values. The related service contains loadBalancer.servers and passHostHeader true. Server URLs are sorted, providing deterministic configuration output. These are concrete Traefik provider fields, not an implementation of a custom reverse proxy inside orch.

Unchanged source excerpt — [internal/traefik/config.go:71–85](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L71-L85):

```go
			serviceName := routerName + "-service"
			router := Router{
				Rule:    routeRule(route),
				Service: serviceName,
			}
			if route.TLS {
				router.TLS = &TLSConfig{}
			}
			config.HTTP.Routers[routerName] = router
			config.HTTP.Services[serviceName] = Service{
				LoadBalancer: LoadBalancer{
					Servers:        servers,
					PassHostHeader: true,
				},
			}
```

The endpoint selector requires matching container port, TCP protocol, actual running or healthy status and a positive published port with usable node host. Upstream discovery ordinarily already filtered desired-running work before the builder sees it. Preserve that caller relationship: BuildConfig's own input contract and the API's assembled endpoint set are different layers of protection.

The fixture TestBuildConfigIncludesOnlyHealthyTCPRouteEndpoints provides a useful adversarial mix: one running target, one healthy target, one unhealthy task, one wrong-port task and one UDP task. Only two HTTP backend URLs survive. The test asserts the exact router rule, a nonnil TLS object, passHostHeader and sorted URLs. TestBuildConfigSkipsRoutesWithoutHealthyServers asserts no routers/services for an unhealthy-only set.

A generated route key incorporates service name, host, port and route index after slugging. Readers considering broad multitenant compositions should inspect that naming scheme rather than assume it includes every namespace/UUID dimension. The current chapter does not claim arbitrary cross-namespace route-name uniqueness. That is a concrete integration review question, distinct from whether one Atlas route is generated correctly.

## Failures at Node and Gateway Boundaries

The provider endpoint is GET /v1/integrations/traefik/config. The upstream compose profile configures Traefik to poll it every two seconds. This creates another freshness boundary: an unhealthy task can disappear from the server's latest configuration before the gateway has fetched and applied that change. A previous gateway configuration can still send requests to a now-bad destination during the interval.

The two-second setting is an example poll cadence, not a universal routing-convergence promise. Gateway processing, transport errors, workload report timing and persistent connections can extend effective behavior. If user JWT authentication is enabled on the provider endpoint, the external consumer also needs a compatible authorized fetch path. The default demonstration's unauthenticated-user configuration cannot be assumed valid after security settings change.

Consider Atlas on node A and node B while the gateway loses access to node A's public port. Both agents may still report healthy probes because probes originate locally on the workers. The gateway receives a route containing A but cannot connect to it. This is a data-plane reachability failure that a local health report does not disprove. Record the failed gateway-to-A connection independently rather than changing desired replicas before understanding the hop.

A different failure occurs when all endpoints are filtered out: the provider output omits the route. Query the provider JSON first, compare current task versions/states and published ports, then inspect gateway behavior. A client using the wrong Host header can fail even when backends are present. That is why an experiment must preserve the request's actual host and path, not merely report that curl returned an error.

| Observation | Likely boundary to inspect | What it does not prove |
| --- | --- | --- |
| Provider has no route | Service status, route validation, endpoint filtering | Gateway itself is broken |
| Provider has backend, gateway refuses it | Node host/public port/firewall/app listener | Agent health report was forged |
| Direct backend works, host request fails | Router match, provider poll, gateway listener | Overlay networking is required |
| TLS router object exists | Client-facing TLS intent | Certificate issuance or backend encryption occurred |

The last row is especially important. A boolean in a workload route can request TLS configuration, but the builder does not issue certificates, distribute trust or encrypt every internal connection. Operators must know which external gateway configuration owns those responsibilities.

## An Overlay or CNI Design Is a Separate Step

The advanced networking document begins from these limitations: scarce public ports, exposed node topology, clients following rescheduling and missing workload network identity/policy. It proposes task addressing, IPAM, overlays such as VXLAN or WireGuard and possible CNI plugin integration. Those are design alternatives, not active branches hidden behind the existing route endpoint.

An overlay would need stable task address allocation, checkpointed lifecycle, route setup/removal, MTU handling and recovery after partitions. CNI integration would add plugin versioning, output validation, deadlines, privilege boundaries and repeatable cleanup. Network policy would require an enforcement mechanism tied to actual workload identity. Writing a namespace selector in a design does not make packets tenant-isolated in the current Docker host-port model.

These proposals interact with the ownership questions already studied. If a server loses task records, who reclaims an address? If an isolated worker continues serving, which generation may retain a route or tunnel key? If a plugin succeeds but its response is lost, how is cleanup repeated? A useful networking design answers these failure windows rather than only drawing a new subnet.

Atlas does not need an invented overlay to demonstrate ingress. Keep the baseline example small and inspectable, then write a separate architecture decision describing the missing mechanism you would add. A proposed feature gate must not appear in a source-derived command unless the pinned executable actually accepts it. The benefit of source-first study is knowing exactly where an extension begins.

Port pressure should be measured at the node boundary. Two containers can share the same internal application port while requiring distinct published ports on one host. Moving one replica to another node changes that collision domain, but it also changes the address the gateway must use. A capacity plan that counts only CPU and memory misses this constraint. Likewise, adding replicas cannot repair a gateway route whose selected destination port is wrong; more bad endpoints only multiply the same configuration error.

## Atlas Lab: Inspect Configuration Before Starting a Gateway

The deterministic stage uses the disposable pinned source copy with Go 1.25. It needs no external gateway or Docker daemon and proves the builder's transformation/selection contract.

```bash
go test ./internal/traefik -run 'TestBuildConfig(IncludesOnlyHealthyTCPRouteEndpoints|SkipsRoutesWithoutHealthyServers)$' -count=1 -v
go test ./internal/api -run TestTraefikConfigUsesHealthyServiceRouteEndpoints -count=1 -v
```

The [fresh package-test record](../../validation/reviews/ch17-24-fresh-source-tests.json) includes Traefik configuration tests with caching disabled. Those fixtures exercise generated data rather than a running gateway or encrypted client connection. Inspect the upstream traefik-demo manifest and compose profile, especially the listener mappings, provider URL and poll interval. Adapt only the service name to the owned Atlas case when creating a separately labeled teaching manifest; preserve supported fields and record the change.

For the real gateway variant, use an isolated daemon/network or explicitly owned compose project, verify free listener ports, and record the service/task/container identities. Do not start the upstream profile against an unrelated existing project just because it is convenient. Compare provider JSON, direct backend requests and gateway requests with the configured Host header. Induce a missing-endpoint case with the owned unhealthy workload rather than shutting down the host network.

Abort if any advertised backend is not run-owned, if compose would replace an existing service, or if the selected ports conflict. Cleanup stops only the chosen compose project and recorded Atlas workload objects; preserve unrelated volumes and daemon state. Save configurations and observations before cleanup. A successful gateway request demonstrates that concrete path at that time, not a service VIP, overlay, CNI implementation or comprehensive tenant network policy.

## Exercises

1. Why is a node's advertised agent port discarded when constructing an application backend URL?
2. A TLS route emits http:// backend servers. Explain why this is consistent with the builder and what must be configured separately.
3. A task is locally healthy but unreachable from the gateway. Give a hop-by-hop investigation that preserves both observations.
4. Select one proposed overlay/CNI mechanism and define the crash window its acceptance test must cover before it could replace the current host-port behavior.

[Worked answers](../solutions/ch21.md) separate generated intent, gateway configuration and actual packet effects. That distinction lets an operator use the current integration while an architect evaluates future networking honestly.

## Development history and source references

Original development prompts 36, 77 supply the requested scope. The inspected implementation history includes [ea0760e8201c](https://github.com/alekpopovic/orch/commit/ea0760e8201c842371caf6671a90bcfeb90197bb), [4d641bbe8913](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87). Their exported changed paths were compared with this chapter's implementation. These are topical associations; early prompts were retrospective and later work can share a commit. A tracker entry is not evidence that the described experiment ran.

- [internal/traefik/config.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config.go#L1-L197)
- [internal/traefik/config_test.go](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/traefik/config_test.go#L1-L147)
- [docs/TRAEFIK.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/TRAEFIK.md#L1-L75)
- [docs/NETWORKING.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NETWORKING.md#L1-L33)
- [docs/NETWORKING_DESIGN.md](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/NETWORKING_DESIGN.md#L1-L11)
- [deployments/examples/routed-api.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/routed-api.yaml#L1-L15)
- [deployments/examples/traefik-demo.yaml](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/traefik-demo.yaml#L1-L19)
