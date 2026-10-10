# 6. Model identity, ownership, and permission together


## Scope every resource

An organization contains projects; a project owns pipelines, runs, artifacts, and secret-use policies. Runner pools and environments have explicit access grants. A request is authorized against both the action and the object being accessed. Hiding a button in Angular is not an authorization rule.

Use immutable organization and project identifiers in ownership relationships. Where practical, include them in compound foreign keys or lookup predicates so an accidental unscoped query is difficult to write. A run lookup should not retrieve a globally matching identifier and only sometimes check its organization afterward. Tests must deliberately attempt cross-project reads, writes, downloads, and websocket or streaming subscriptions.

Roles are named bundles of capabilities, not special branches scattered through the code. A viewer can inspect permitted history. A developer can author and request builds. An operator can manage runner availability. A release approver can authorize a particular environment transition. An administrator manages membership. Some organizations may combine these roles, but the model should not require them to be identical.

## Permission to write code is permission to influence execution

A person who changes build commands can cause actions using whatever the job receives. Treat secret use and privileged runner selection as separate permissions from pipeline editing. The server evaluates them after compiling the requested configuration and again before dispatch when revocations matter.

The YAML field `pool: production` is a request, not an entitlement. An authorized pool record must belong to or explicitly be shared with the project. Labels such as `linux`, `arm64`, and `gpu` further narrow eligible machines only after this authorization step. A label must never confer access to another tenant's host.

A shared runner pool needs rules for what happens when grants change. Already issued external credentials may remain valid until expiry. New claims and credential redemptions can be refused immediately. Make that distinction visible to administrators so “revoke” is not presented as retroactive erasure of all authority.

## Separate credential classes

A browser session, CLI token, one-use enrollment token, and long-lived runner identity are different credential classes. Do not accept one where another is expected. Give them different audiences, scopes, expiry policies, and storage conventions.

For browser cookies, use secure transport, `HttpOnly`, an intentional same-site policy, and a CSRF defense for state-changing operations. Avoid logging cookie headers or returning session secrets to frontend diagnostics. For CLI authentication, store credentials in a restricted local file or platform credential store, and keep normal command output free of tokens. These are proposed application controls, to be verified in its HTTP and packaging tests.

Runner enrollment should be a one-time action authorized for a particular pool. Exchange the enrollment credential for a revocable identity, then remove the enrollment secret. A runner rotation procedure must handle an overlap window deliberately; otherwise a routine key change can look like an unexplained loss of all workers.

## Audit decisions, not just mutations

An audit event should answer who requested the action, which resource was involved, which policy was used, and what decision was committed. Store actor and resource identifiers, request correlation, and a safe summary. Do not store plaintext secrets, full authorization headers, or uncontrolled payloads merely because they are useful during debugging.

Sensitive actions such as changing an environment policy, issuing a runner enrollment token, or reconciling an uncertain deployment deserve specific event types. A generic “settings changed” event leaves operators guessing during an incident.

Authorization tests should run at the service boundary as well as the HTTP boundary. A future background task or CLI adapter must not bypass checks simply because it calls the same underlying function without passing through a web middleware layer.

## Exercise

A developer may edit a staging pipeline and a project contains a production credential. The interface never displays that credential's value. Is the credential protected if the developer can add it to the staging job's environment?

## Worked answer

No. Code receiving the credential can use it or send it elsewhere, even if the interface is write-only. Enforce secret-use grants separately from secret visibility and pipeline editing. Restrict the production credential to an authorized environment and execution context, and recheck that policy at redemption. Log masking can reduce accidental disclosure but cannot safely grant a secret to malicious code.

## Completion evidence

Maintain an authorization matrix and negative tests for every resource family, including streaming endpoints, signed downloads, credential redemption, and runner pool selection.
