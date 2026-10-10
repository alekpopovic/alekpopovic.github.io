# 12. Execute containers within explicit limits


## Define what the executor owns

The executor turns a compiled job into runtime operations. It owns workspace creation, checkout material, container lifecycle, resource limits, output capture, exit observation, and cleanup. It does not own project authorization or decide that a production credential is safe to release.

For the initial design, use dedicated Linux runner hosts with a container executor. Keep the control plane elsewhere. Docker documents important limits and the authority of its daemon; a container is not a complete hostile-tenant boundary merely because it has a separate filesystem view. [S08](e-sources.md#s08)

Job containers should not receive the host daemon socket, unrestricted host mounts, host networking, or privileged mode by default. Place the daemon control connection in the runner's authority boundary. Stronger public multi-tenant execution is separate work, not a configuration checkbox on this trusted-runner design.

## Build an execution envelope

The envelope includes image identity, working directory, command representation, environment, allowed mounts, network policy, CPU and memory budget, process limit, timeout, and output quota. Validate it against server and runner policy. A field absent from the plan must not silently inherit a permissive host default.

Resolve image aliases to immutable identities before execution and validate the allowed source registry. An image tag alone can change between runs. Store the selected platform when the image supports multiple architectures. Report pull and creation failures separately from a test command's nonzero exit.

Prefer explicit argument arrays for built-in actions. A shell step is a deliberate language boundary: document the shell, flags, working directory, and failure semantics. Do not concatenate a pull-request title or user parameter into shell syntax. Treat those values as data passed through a safe argument or environment mechanism, while still restricting which programs are allowed in privileged adapters.

## Observe exit before declaring completion

A timeout produces a termination request. Apply a configured grace period, then escalate within the runtime's supported operations if necessary. Observe that the managed container stopped. Record whether the outcome was command failure, timeout, cancellation, infrastructure loss, or uncertain termination.

A successful signal operation is not necessarily a successful cleanup. Mounted volumes, child containers created through unauthorized daemon access, or target-side commands can outlive the main process. The executor contract must explain which resources it controls and which observations it can actually make.

Use a new workspace per attempt. Different jobs exchange artifacts explicitly rather than relying on a previously used host directory. Within a job, step workspace sharing should be intentional and documented. Clear checkout credentials before user-controlled steps start whenever the fetch mechanism permits it.

## Cleanup must be conservative and repeatable

Assign ownership metadata at resource creation. Cleanup queries should filter by platform identity, runner identity, and attempt identity. Validate paths before recursive deletion, reject symlink escapes, and confine cleanup roots to configured directories. A faulty cleanup routine can be more destructive than the failed build it is trying to tidy up.

On disk pressure, stop admitting new work before exhausting the runner journal or control process. Report which budget is full. Artifact, cache, image, and workspace retention have different policies; deleting all four indiscriminately loses useful evidence and often hides the real capacity problem.

The executor should be testable behind an interface, but runtime integration tests remain mandatory. A mocked “container stopped” response does not establish that the selected runtime kills descendants or enforces a memory limit on the intended host configuration.

## Exercise

A runner times out a job, sends a termination signal, and immediately marks it cancelled. Its cleanup call fails because the runtime is unavailable. What status should be visible?

## Worked answer

Show that cancellation was requested and that physical termination is not confirmed. Preserve the attempt and quarantine affected capacity until reconciliation establishes what is still running. Do not release a deployment target lock based only on a signal request. A later observation can establish a terminal outcome while preserving the earlier uncertainty interval.

## Completion evidence

Test CPU, memory, process, disk, timeout, mount, and output limits against the actual runtime. Test restart recovery and ensure cleanup cannot target unrelated containers or paths.
