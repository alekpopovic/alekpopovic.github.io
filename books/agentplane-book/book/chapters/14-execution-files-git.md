# 14. Execute Commands and Handle Files Without Hidden Privilege

**Part IV — Safe Execution**

The execution API is the point where a user request becomes operating-system
activity. Treat it as a privileged interface even when the process runs in a
sandbox. An execution request needs a stable identity, authorized session,
explicit arguments, bounded runtime and a defined output policy.

## Prefer argument arrays

Represent a program and its arguments separately. Avoid concatenating a user
string into a shell command. Shell execution may be a legitimate advanced feature,
but it is a different capability and should be explicit rather than a hidden
implementation detail.

```json
{
  "execution_id": "exec_example_001",
  "argv": ["python", "-m", "pytest", "tests/unit"],
  "working_directory": "repository",
  "timeout_seconds": 60,
  "maximum_output_bytes": 1048576
}
```

This request is a design example. Argument separation prevents one class of
command construction error; it does not make the requested program harmless.
The program still runs with the session's permissions and must remain inside the
runtime, network and identity boundaries.

## Bound output and interactive sessions

Use separate stdout and stderr channels, sequence numbers and a final execution
result. Bound server and browser buffers. A slow terminal subscriber must not
consume unbounded connector memory. Define whether output is truncated, spooled
to customer storage or dropped after a configured limit, and tell the client
which occurred.

Terminal escape sequences are untrusted input. Use a maintained terminal renderer
and configure dangerous integrations carefully. Do not let output trigger URL
opening, clipboard operations or application commands without explicit user
interaction. A malicious test suite can print control sequences as easily as
ordinary text.

PTY sessions complicate cancellation and signal handling. Define whether a client
disconnect detaches, cancels or leaves the execution running until its deadline.
A reconnect should attach to the same execution identity, not start a new process.

## File paths need filesystem-safe operations

Reject absolute paths and traversal components, but do not stop at string
normalization. A path that was safe during validation can be replaced by a symlink
before opening. Use root-relative, traversal-resistant filesystem APIs appropriate
to the platform and language version. Go's discussion of `os.Root` explains this
class of problem; consult the exact available API before implementation.
[S23](../references.md#s23)

Define rules for symlinks, hard links, devices and sockets. Archive extraction
needs its own path checks, expanded-size limits and entry-count limits. A small
compressed upload can expand into an enormous workspace. Atomic temporary-write
and rename behavior helps avoid partially written target files but does not
replace the root-boundary checks.

A file transfer should stream through bounded chunks, support cancellation and
verify a checksum when supplied. Make data location explicit. Relay mode sends
file contents through SaaS memory even if they are never written to SaaS storage.
A direct data-plane mode needs a separate authenticated transfer route.

## Git is an execution-adjacent capability

Validate repository schemes and approved destinations. Restrict SSH host keys
and never silently disable verification. Provide credentials through a short-lived,
local mechanism rather than embedding them in URLs or process arguments. Ensure
Git configuration, askpass behavior, environment variables and template hooks are
controlled. Submodules require independent destination and credential policy.

A normal clone is not permission to execute all repository scripts. Dependency
installation, hooks configured by the environment and test commands remain
sandboxed actions. A repository can contain instructions designed to trick an
agent into widening permissions. Treat those instructions as data.

Push should be a separate permission and a separate approval decision when
appropriate. Committing local changes and transmitting them to a remote repository
have different consequences. Do not grant write credentials merely because clone
access is required.

## Credentials can still be printed

Even when the broker never sends a secret to the SaaS API, a program with access
to that secret can print it. Limit credential scope and lifetime, minimize output
retention and avoid granting unnecessary credentials. Automatic redaction cannot
reliably recognize all secrets, encodings or sensitive business data.

## Exercise

Design tests for a symlink swap during upload, an archive with traversal entries,
a stalled output subscriber and an execution whose response is lost after a Git
push succeeds. Explain why retry rules differ between listing a directory and
repeating that push.

## Primary sources

[Go traversal-resistant file APIs](../references.md#s23)
