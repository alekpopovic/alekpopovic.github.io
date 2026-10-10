# 9. Know whose address you are blocking

## Direct edges are the easy case

When a visitor connects directly to Nginx, the peer address is the simplest identity available. Ignore a visitor-supplied forwarding header unless an explicitly trusted proxy stands between the visitor and the edge. A header is data; it becomes identity only through a configured trust relationship.

When Nginx sits behind a load balancer or CDN, the peer address belongs to that intermediary. Blocking it would block many users. The correct solution is to identify the actual ingress topology and trust only the intermediary's legitimate peers when replacing the address. The real-IP module provides the mechanisms, but the deployment supplies the trust list.

## Model the complete path

List each hop in order: visitor, CDN, load balancer, edge, application. For each hop, write who can connect and which party sets or appends the forwarding field. If the origin is reachable directly from the internet, a visitor may bypass a CDN's header discipline. Restrict origin connectivity as part of the topology rather than relying only on the expected path.

A trust configuration with `0.0.0.0/0` or `::/0` says that every peer may choose the replacement address. That defeats the identity boundary. Similarly, trusting an entire private network can grant unrelated services the ability to impersonate clients. Use the actual ingress peers and maintain their changes as controlled configuration.

Preserve the original peer address where useful for audit. It helps distinguish a client identity resolved through a trusted chain from the TCP peer that actually connected. The request-time check should use the resolved address; investigation may need both.

## Normalize once

IPv6 addresses have multiple textual representations. The agent and detector should compare parsed addresses, not strings copied from separate serializers. The laboratory maps IPv4-mapped IPv6 addresses to their IPv4 identity. It rejects zone identifiers such as `%eth0`, hostnames, and malformed addresses.

A zone identifier is meaningful to local interface addressing, but is not an internet client identity for this protocol. Allowing it into an exact-IP ban key can create an address that the producer and consumer interpret differently. Document your normalization rules and use the same test fixtures across languages when migrating the agent to Go.

## An IP is not a person

Many clients can share one public address through NAT. A corporate proxy may represent an entire office. A mobile network can change a device's address. An attacker may distribute requests across many addresses. The system is controlling traffic attributed to an address, not proving a person's identity or intent.

This explains several conservative defaults: automatic decisions are site-scoped, exact-address, and short-lived. A global ban or a broad network ban has a larger blast radius. It requires separate operator intent and evidence. A detector that is accurate for one site's workload may be wrong for another site's clients.

## Detection and enforcement must agree

Suppose the collector stores the resolved client address, but the guard check receives the original load-balancer peer. Central can create a perfectly valid decision that never matches a local check. The opposite mismatch can accidentally ban the intermediary. The system's logs may look healthy while protection is ineffective or harmful.

Add a deployment test that records a known client's resolved address in both the access event and agent check. Include direct connections, trusted proxy connections, and malicious forwarding values from an untrusted peer. A unit test of `ipaddress` cannot establish Nginx's trust chain.

## Exercise

Your origin uses a CDN and is also reachable directly. A request arrives directly with a forwarding header containing an allowlisted IP. What address should be evaluated, and what other deployment control would simplify the boundary?

## Answer

The direct peer is not a trusted CDN peer, so its forwarding claim must not replace the client identity. Evaluate the actual peer. Restrict origin access to the intended ingress peers when the architecture requires CDN-only entry, then test both accepted proxy traffic and refused direct traffic. Keep an intentional management path separate from public visitor access.
