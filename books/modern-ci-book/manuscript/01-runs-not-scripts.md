# 1. Think in runs, not shell scripts


## The misleading first demonstration

Imagine a web page with a repository selector and a Run button. The server clones a project, invokes a shell, and streams its output to the browser. A successful test suite produces a green badge. This is a useful demonstration, but it hides the hardest questions. What happens when the browser disconnects? Does restarting the server kill the command? Can a second click deploy twice? Which commit was cloned when the branch moved between the click and the checkout?

Start the design with records that survive these questions. A **definition** describes the work. A **run** is a particular request to execute an immutable definition against specific inputs. A **job** is a schedulable node in the graph. A **step** is an operation within that job. An **attempt** is one concrete execution of a job. A **deployment** is a separately tracked change to an environment. These terms let an operator distinguish a user's intention from a worker's observations.

Jenkins already has pipeline-as-code, durable pipeline execution, parallel work, and approval steps. Reimplementing those names is not a product advantage by itself. Its documentation is a useful reference for the existing concepts. Modern CI's design goal is a coherent contract and an understandable operational experience, not a claim to have invented pipelines. [S01](e-sources.md#s01)

## Follow one request through the system

A developer requests a run for source commit `c7`. The server authorizes the request and freezes its inputs. The compiler creates `test`, `package`, and `deploy` jobs with explicit dependencies. The scheduler makes `test` eligible. A runner receives attempt `a1`, reports its start, uploads bounded log segments, and submits a result. Only a committed successful result makes `package` eligible.

If `a1` fails because the execution host disappears, a retry does not erase it. The platform creates `a2`, preserving the first attempt and its evidence. A retry policy decides whether the failure is eligible. The job is the logical unit whose eventual outcome can satisfy a dependency; the attempt is the physical work whose history must remain inspectable.

Use identifiers rather than human names in internal relationships. Names are useful labels but can change. A deployment called `production` must still point to a specific environment record and artifact digest, even if someone renames a project halfway through the run.

## Desired, observed, and committed state

An operator can request cancellation without a worker having stopped. A worker can exit before its final result is committed. A target can receive a deployment before the network reply reaches the runner. Avoid turning these into one ambiguous status field.

A useful run detail page might show:

```text
Requested action: cancel
Attempt: a2
Last observed execution state: running
Control state: cancel requested
Last heartbeat: recorded server timestamp
Target side effects: not yet reconciled
```

This is less visually tidy than immediately displaying “cancelled,” but it is more truthful. An uncertain state is a supported outcome, not an embarrassing exception to hide.

Terminal results should be immutable within an attempt. Duplicate identical reports can be acknowledged. A conflicting later report should produce a conflict record, not overwrite the first committed outcome. Operator correction can create a separately authorized reconciliation event while preserving what the original worker said.

## Define success before breadth

The first useful milestone is one repository, one dedicated runner, an immutable checkout, a bounded command, durable result history, and a readable log. Add an artifact next. Add an approval-controlled deployment only after execution uncertainty has an explicit model. This path puts correctness before a plugin marketplace or a sophisticated visual editor.

Write success criteria as observable behavior. “Supports retries” is weak. “Creates a new attempt, preserves the earlier log, and rejects the earlier attempt's late result” is a testable requirement. “Secure secrets” is weak. “A project reader cannot retrieve plaintext, and a revoked attempt cannot redeem a credential” is a stronger starting point.

## Exercise

A user presses Retry while the previous attempt has lost contact with the server. A developer proposes replacing the old attempt row with a fresh `running` state. Identify three pieces of evidence that this destroys and the safer behavior for a deployment job.

## Worked answer

The replacement loses the old attempt identity, its execution timeline, and the association between its output and a particular claim. It also makes a late result difficult to distinguish from the new execution. Keep the attempt and mark its execution status uncertain. For a deployment, retain the target lock and reconcile the external state before authorizing another attempt. A new attempt is appropriate only after the retry policy and target-safety checks permit it. The old attempt remains part of the record.

## Completion evidence

A domain review should be able to explain every identifier and every transition in the request-to-result path. No API field should equate a cancellation request with confirmed termination.
