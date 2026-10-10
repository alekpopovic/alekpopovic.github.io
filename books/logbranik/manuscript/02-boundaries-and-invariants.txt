# 2. Draw the trust boundaries

## Begin with actors, not ports

A visitor requests application content. A collector sends observations from an edge. A publisher distributes policy. An agent evaluates policy locally. An operator changes modes, allowlists, and manual decisions. Each actor needs a distinct authority. A valid certificate is proof of possession of a credential; it does not, by itself, prove permission to perform every action.

The companion mTLS server therefore checks a certificate fingerprint against an explicit role registry after the TLS handshake. The collector credential is accepted at ingestion. The publisher credential is accepted at policy updates. A different certificate signed by the same laboratory CA cannot publish just because its chain validates. The transport tests include this exact case.

In a managed deployment you will probably use a certificate identity with a registration database rather than manually maintained fingerprints. Preserve the second authorization step. Transport identity must map to a role and allowed scopes. Do not derive role from a visitor-controlled header or from a body field that happens to say `collector`.

## The local edge boundary

Nginx sends a deployment-configured site ID and a resolved client IP to the authorization handler. It overwrites the headers carrying those values. The handler must not receive arbitrary visitor headers or request bodies. Its socket permissions restrict which local users can connect.

A Unix socket avoids opening another TCP port, but it is not magical authentication. A compromised process with access to the socket can submit checks. A compromised edge root account can change Nginx configuration, replace agent state, or bypass the service entirely. This design does not claim protection against a hostile administrator of the enforcement host.

The lab has a loopback TCP option for hosts that cannot create Unix sockets. That option allows other local processes to connect and is for teaching. Use the Unix profile and operating-system permissions for the production boundary; verify it on the actual host.

## Central observations are scoped

Suppose collector A is registered for `site-demo`. Its certificate maps to `node-a` and that site. A body containing `site-other` is not permission to ingest for another site. A body containing a fake node ID should be rejected by the schema, which has no node field. In the companion server, node identity comes from the certificate registry and is passed separately to the ingestion function.

The event schema is strict because accidental flexibility becomes authority. Ignoring unknown fields permits an old client to believe a new field is being enforced. Interpreting unknown site IDs as global scope creates cross-site consequences. Treat unknown versions, sites, and mutation types as explicit errors.

## Decisions are data

A remote policy may describe an exact IP, a site, an expiry, and a reason code. It may not describe a shell command, executable path, firewall expression, arbitrary URL, or file to overwrite. The agent does not translate strings from a policy into commands. It evaluates a data structure.

This gives the control-plane compromise a defined blast radius. Someone who steals a signing key can still issue harmful valid decisions within the protocol's scopes and limits. They cannot obtain arbitrary code execution merely by adding a command field. Independent TTL caps, a local emergency bypass, and pinned site scopes reduce that damage without pretending it disappears.

## A small threat table

| Situation | Boundary that matters | Required response |
| --- | --- | --- |
| Visitor spoofs guard headers | Nginx to agent | Overwrite identity headers |
| Collector sends another site | Ingestion authorization | Reject or quarantine scoped record |
| Valid CA certificate has wrong role | mTLS application authorization | Deny endpoint access |
| Old signed policy is replayed | Agent revision state | Reject lower revision |
| Signed policy has excessive TTL | Independent agent validation | Reject the policy |
| Root on the edge is hostile | Host administration | Outside this protocol's guarantee |

## Exercise

You are told to save time by sharing one certificate between collector, publisher, and operator. Explain the failure this creates and identify one test that would expose it.

## Answer

A stolen collection credential would gain mutation rights, so a less privileged component could become an enforcement controller. Use separate credentials and role authorization. Connect to the snapshot endpoint using a CA-valid collector certificate and require denial. The companion's wrong-role test demonstrates the same boundary with a dedicated wrong-role certificate.
