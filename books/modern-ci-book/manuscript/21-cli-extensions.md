# 21. Keep the CLI precise and extensions constrained


## A CLI is another client, not an administration back door

The CLI should use the same versioned API and authorization decisions as the browser. Give it explicit contexts for server, organization, and project. Display the selected context before dangerous operations and avoid guessing an environment from a similar name.

Machine-readable output needs a stable contract. Send data to stdout and diagnostics to stderr. Use documented exit statuses to distinguish success, invalid input, authentication failure, authorization denial, remote failure, and an operation that remains uncertain. A successful HTTP submission is not necessarily a successful deployment.

A command such as `runs watch` should reconnect using the documented cursor and stop according to an explicit terminal-state rule. A command such as `deployments reconcile` should require a specific deployment identity and recorded evidence. Avoid broad wildcard mutation by default.

## Make automation reviewable

Support a read-only plan or preview for changes that can be described before mutation. The preview should identify the actual resources and the version being changed. Use conditional updates to detect that a resource changed between preview and apply.

Interactive confirmation is useful for a human but not sufficient for scripted use. Provide an explicit noninteractive flag only when the request fully identifies its scope and desired action. Keep approval and authorization checks on the server even if the client has a `--yes` option.

Store credentials with restricted permissions. Do not accept a token in a command-line argument when a safer input path is available, because arguments may be visible in process listings or shell history. Support reading from a protected file or environment under a documented policy, and exclude secrets from debug output.

## An extension contract is a permission contract

An action definition should declare its version, inputs, outputs, runtime identity, required capabilities, and supported protocol. Resolve it to an immutable identity during compilation. The manifest requests capabilities; it cannot grant them to itself.

Run extension code outside the control-plane process. For the initial product, a small built-in action set is easier to secure and support than a broad marketplace. Add a signed catalog or publisher-verification process only when there is a real need and a defined trust policy.

A containerized action still inherits whatever the executor gives it. Review mounts, credentials, network reachability, and output channels. Isolation boundaries come from the execution design, not from naming something a plugin.

## Import Jenkins narrowly and honestly

The migration analyzer can inspect exported configurations and recognize a bounded subset of static stages, commands, credentials references, triggers, and artifact declarations. It should produce a translation report with supported, partially supported, and unsupported items.

Do not evaluate arbitrary Groovy while importing. Do not copy credential values into generated YAML. Map credential references and require an operator to establish the equivalent policy in the new system. Dynamic shared-library behavior may need manual redesign rather than a mechanical conversion.

Run the new pipeline in a non-production comparison mode before switching the authoritative deployment path. Compare source identity, outputs, test counts, and target behavior. Prevent both systems from deploying to production simultaneously during the transition.

## Exercise

A migration tool can translate every shell command but drops an unsupported approval plugin. It reports “100% command coverage.” Is that enough to activate the imported pipeline?

## Worked answer

No. The missing approval changes who may authorize a deployment. Migration coverage must include control and security semantics, not just executable commands. Mark the pipeline blocked until the environment policy and approval behavior are represented and tested. A mechanically complete command list can still be an unsafe migration.

## Completion evidence

Test CLI exit statuses and output stability, stale previews, restricted credentials, version mismatch, action capability denial, and migration reports that never silently discard unsupported security controls.
