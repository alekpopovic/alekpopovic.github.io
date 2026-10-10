---
layout: post
title: "Before blocking an IP, trace the proxies"
description: "An address becomes a useful enforcement identity only after the ingress path and forwarding-header trust are clear."
category: Security
book_id: logbranik
chapter_slug: 09-client-ip-and-proxy-trust
illustration: network
tags: [nginx, proxies, client IP, ingress, trust boundaries]
---

The detector finds a burst of suspicious requests and bans the address it sees. Suddenly, many unrelated visitors lose access. The address belonged to the load balancer.

The rule may have counted requests correctly. The failure happened earlier, when the system decided what the address represented.

## Draw the path to the origin

Write down the actual hops: visitor, CDN, load balancer, Nginx, application. At each hop, identify who can connect and who sets or appends the forwarding field.

For a direct connection, the peer address is the starting point. A visitor-supplied forwarding header is data, not an instruction to replace that identity.

Behind a trusted intermediary, the resolved client address can come from the configured forwarding contract. The trust belongs to specific ingress peers and a known topology. Trusting every peer lets anyone who reaches the origin choose the address your detector believes.

## Test the path people are not meant to use

An origin reachable directly from the internet may let a request bypass the CDN that normally prepares its headers. Restrict origin connectivity where the deployment requires it, and test the direct path explicitly.

Preserve the original peer address for investigation when appropriate. Seeing both the connecting peer and the resolved client helps explain how the identity was derived.

The collection path and request-time enforcement path must use compatible resolution rules. Otherwise, the detector can ban one address while the guard checks another.

## Normalize before comparing

Different textual forms can represent the same address. Parse and normalize under a shared contract instead of comparing strings produced by unrelated serializers.

The book's laboratory maps IPv4-mapped IPv6 addresses to the corresponding IPv4 identity and rejects zone identifiers, hostnames, and malformed input. Shared fixtures become especially useful when separate components use different languages.

## Keep the decision's reach modest

Even a correctly resolved IP is not a person. An office, carrier network, or shared proxy can put many clients behind one address.

That is a reason to prefer short-lived, exact-address, site-scoped automatic decisions. A broader network or global restriction needs a different operational decision and stronger evidence.

Before enabling a blocking rule, send controlled requests through each supported ingress path, including an untrusted forwarding header. Check the identity recorded by the collector and the identity evaluated by the guard. They should agree for reasons you can explain.
