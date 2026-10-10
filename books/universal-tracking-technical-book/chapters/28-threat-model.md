# Part VI - Production Engineering {.part}

## Chapter 28 - Threat Model and Security Architecture

A threat model connects assets, actors, trust boundaries, attack paths, and mitigations. It should be updated as the product adds public links, device commands, proof files, or new protocol listeners.

![Human, device, API-client, and public identities cross the same policy layer but never share credentials.](../assets/diagrams/security-boundaries.png){width=94%}

### Assets

High-value assets include:

- exact current and historical locations;
- person-subject identity and relationships;
- device and API credentials;
- authentication signing keys;
- private-zone definitions;
- task and recipient details;
- proof-of-delivery files;
- device commands;
- audit and access history;
- backup archives.

Availability is also an asset. A safety or delivery platform can be harmed by data loss, delayed alerts, or false positions even without confidentiality loss.

### Trust boundaries

Important boundaries include:

- public Internet to Nginx;
- browser to REST and WebSocket APIs;
- mobile web layer to native bridge;
- device networks to GPS listeners;
- Go processes to PostgreSQL;
- application to filesystem storage;
- worker to external webhook or email endpoints;
- primary database to backup destination;
- operator access to production systems.

Document what is authenticated, encrypted, rate-limited, and audited at each boundary.

### Principal separation

Different identities have different blast radii:

- a human user acts through organization membership and policy;
- a tracking device can submit only for authorized subject/session scope;
- an API client has organization and action scopes;
- a public capability has a narrow view scope;
- an internal process uses a database role and system policy.

Never transform one principal into a more powerful one because it is convenient in middleware.

### Attack scenarios

Representative scenarios include:

1. **Cross-tenant object reference** - an authenticated user changes a subject ID in a URL.
2. **Stolen refresh token** - an attacker attempts reuse after legitimate rotation.
3. **Compromised device credential** - false locations are uploaded for an assigned subject.
4. **Replay of old GPS frames** - a valid packet is resent to fabricate history.
5. **Public-link leakage** - a token appears in browser history or referrer headers.
6. **WebSocket subscription escalation** - a client subscribes to another team.
7. **SSRF through webhook URL** - the worker is induced to call an internal service.
8. **Malicious proof file** - an image decoder or spreadsheet export is attacked.
9. **Slow TCP client** - a connection consumes a goroutine and buffer indefinitely.
10. **Backup theft** - encrypted or unencrypted archives expose long-term history.
11. **Insider access** - support or operations staff view precise routes without purpose.
12. **Location inference** - even rounded public points reveal a home over time.

Every scenario receives preventive, detective, and recovery controls.

### Input validation

Validation is centralized by contract but remains defense in depth:

- HTTP body and frame limits at Nginx and application layers;
- strict JSON decoding with controlled unknown-field policy;
- finite numeric checks;
- file type and decompression limits;
- geometry complexity limits;
- URL and DNS validation;
- bounded metadata;
- parser fuzzing;
- database constraints.

Do not trust generated clients as a security boundary.

### Secret management

Use mounted secret files or Docker secrets with strict permissions. Configuration references file paths. Processes read secrets at startup or through a controlled reload mechanism.

Rotate:

- access-token signing keys;
- refresh and device credential policies;
- webhook secrets;
- database passwords;
- backup encryption keys;
- TLS keys.

A rotation runbook includes overlap, verification, rollback, and secure retirement.

### Network security

Only Nginx and explicitly required GPS ports are public. PostgreSQL binds to a private network and uses TLS where traffic leaves a trusted host boundary. Host firewalls allow only required paths. Administrative access uses separate accounts, MFA, and auditable elevation.

Container networks are not a substitute for firewall policy. The production Compose topology should not publish database ports to all interfaces.

### Supply chain

The release process should:

- pin dependencies and toolchains;
- verify checksums;
- run static analysis and tests;
- generate an SBOM;
- scan containers and source;
- build minimal images;
- sign release artifacts where practical;
- record provenance;
- prevent unreviewed generated changes.

A vulnerability scan is an input to risk decisions, not a guarantee.

### Security tests

Automate:

- cross-tenant endpoint and direct-SQL tests;
- token reuse and rotation tests;
- authorization parity across REST, WebSocket, exports, and jobs;
- fuzz tests for APIs and protocols;
- SSRF fixtures;
- malicious file fixtures;
- rate-limit and resource-exhaustion tests;
- secret scanning;
- dependency and container policy checks;
- backup restoration and key availability.

### Chapter checklist

The security architecture should have:

- a maintained asset and trust-boundary model;
- separate principal types and credentials;
- scenario-based controls;
- bounded input at every exposed parser;
- executable key-rotation procedures;
- private database and administrative networks;
- release provenance and SBOMs;
- automated tenant, protocol, and abuse tests.
