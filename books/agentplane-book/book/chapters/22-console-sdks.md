# 22. Build Interfaces That Preserve Scope and Uncertainty

**Part VII — Product and Operations**

The console and SDKs should make safe platform behavior understandable. They must
not hide uncertain state, downgrade authorization errors into generic failures or
present a queued action as completed. A clear interface is part of the operational
safety design.

## Preserve organization and project context

Every authenticated page operates under an explicit scope. When a user changes
project, cancel or isolate in-flight requests from the previous scope. A late
response must not populate the new project's table. Cache keys include scope,
resource version and relevant permissions.

The same rule applies to live streams. Close terminal and event subscriptions
when their context is no longer active or authorized. Do not rely on a visually
changed project label while leaving an old privileged connection open.

## Show intent, observation and age

A session detail view should show desired state, last observed state, observation
age, active operation and safe reason codes. A disconnected cluster can retain a
last-known state, but the page must label it as such. A termination request should
show pending cleanup until confirmation arrives.

Capability warnings should identify what is missing: unsupported runtime,
unverified network enforcement, snapshot driver absent or policy version pending.
This is more actionable than a generic red banner and avoids encouraging users
to disable security controls blindly.

## Treat sensitive UI surfaces carefully

Enrollment tokens and API keys appear once and should not enter persistent browser
storage, analytics or screenshots collected automatically. Confirmation dialogs
for cluster revocation, destructive cleanup and permission changes must describe
the consequence, not merely ask “Are you sure?”

Terminal output, filenames, Git references and tool descriptions are untrusted
content. Use safe rendering and maintained components. Do not use arbitrary HTML
in tool descriptions. Accessibility matters especially in operational workflows:
keyboard access, visible focus, meaningful status text and non-color-only signals
help operators act correctly under pressure.

## Generate low-level clients, design high-level behavior

Generate transport types from the public API schema. Add idiomatic SDK methods
for waiting on operations, streaming execution, paging lists and handling typed
errors. Keep HTTP status, machine code, request ID and operation ID available to
callers without forcing them to parse human messages.

Cancellation must propagate through the SDK. Retries need operation-specific
rules. A helper named `execute_and_wait` must not silently repeat a script after
an unknown outcome. Preserve the original execution identity and return an error
that explains the uncertainty.

## Keep cross-language semantics consistent

Go contexts, Python cancellation and TypeScript abort signals are different APIs
for the same product requirement. Build a conformance suite around scenarios:
create with an idempotency key, conflict on changed input, wait timeout, stream
truncation, permission loss and unknown execution result.

A generated SDK can compile while implementing the wrong retry behavior. Test
observable semantics against a disposable service, not only type generation.
Package publishing is a separate release action requiring approved credentials;
a code-generation task should not publish packages automatically.

## Make the CLI safe for automation

Use explicit exit codes, JSON output and stable error envelopes. Accept program
arguments as arguments rather than a shell string. Keep binary file operations
separate from text output so progress messages do not corrupt downloads.

Read credentials from a secure credential store or environment under a documented
policy. Do not generate commands that put secrets in shell history. Avoid debug
logs that print full headers. Destructive actions require confirmation in an
interactive terminal and an explicit non-interactive flag in automation.

## Exercise

Prototype a session page for three situations: ready and fresh, last seen ready
but disconnected, and termination accepted but cleanup unconfirmed. Write the
screen-reader text as well as the visible labels. Then define an SDK result type
that preserves the same distinctions without relying on interface wording.
