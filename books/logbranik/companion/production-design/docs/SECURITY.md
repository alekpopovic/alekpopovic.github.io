# Security invariants and threat model

Untrusted parties include visitors sending crafted headers/paths, unauthorized peers,
compromised collector credentials, delayed/replayed control messages and corrupt files.
Trust the provisioned central signing key, authorized operators and host root. A fully
compromised edge can lie about its own logs/enforcement; this protocol cannot fix host root.

| Threat | Required control |
|---|---|
| Forged client IP | Restricted ingress and explicit trusted-proxy policy |
| Cross-site poisoning | Certificate-derived node identity and node/site registry checks |
| Collector mutates bans | Separate collector, agent, dispatcher and operator roles |
| Unauthorized block message | mTLS peer authorization plus pinned Ed25519 signature |
| Replay/rollback | Agent-bound epoch/revision, persisted high-water mark and TTL |
| Partial write/corrupt state | Atomic fsync/rename, signature validation and readiness policy |
| Agent or API resource exhaustion | Byte/count/time limits, quotas and bounded concurrency |
| Log injection | JSON escape at Nginx; strict parsing and safe output rendering |
| Block feedback loop | Exclude Guard-generated denials from detection evidence |
| Compromised node callback URL | Operator-managed destination registry and egress limits |
| Secret exposure | No sensitive request data in logs; redact credentials and private keys |

Central application accepts verified peer identity only through a trusted private TLS ingress
that overwrites identity headers; it is not publicly reachable around that ingress. Document
the exact certificate-to-role mapping and reject an otherwise valid certificate with the wrong
role. Agent control uses Go TLS directly. Use short-lived certs where operationally feasible,
renew before expiry, and support emergency revocation through peer registry/CRL policy.

Operator access uses separately provisioned mTLS identities and roles: viewer, operator,
administrator. Bootstrap is local CLI/offline enrollment, not a public unauthenticated endpoint.
Audit state changes with actor, reason, scope, request ID, before/after revision and time.
An append-only table is not tamper-proof against a database administrator; export audit data
to separate storage if that guarantee is required.

The agent runs unprivileged, with no CAP_NET_ADMIN, no shell command execution endpoint,
no container socket, and no permission to reload Nginx. Its writable paths contain only
state; its auth socket is shared only with Nginx's group. Signing private keys live only in the
central signer/delivery trust boundary. Never store private keys in Git or test evidence.

Snapshot destinations are registered by administrators, not derived from logs or arbitrary
URLs in messages. Reject unapproved redirect destinations; enforce central egress policy.
Test invalid SAN, wrong CA, expired certificates, wrong role, wrong target and key rotation.
