# 2. Draw control and trust boundaries


## Separate authority from execution

Modern CI has five applications: server, scheduler, runner, web, and CLI. The server handles user-facing APIs, identity, and integrations. The scheduler evaluates durable work. The runner performs authorized execution on a separate host. The web and CLI present the same control API through different interfaces. Shared code is not a sixth network service.

The server and scheduler must not execute repository commands. They do not need a build-host Docker socket. This follows a boundary already emphasized in Jenkins controller-isolation guidance: code that participates in a build must not inherit the controller's filesystem and administrative privileges. [S02](e-sources.md#s02)

```text
Browser / CLI / signed source events
                  |
             Go server
            /         \
      PostgreSQL    Object storage
            ^          ^
       Go scheduler    |
                  HTTPS initiated by runner
                       |
                 Dedicated runner
                  /           \
          Container runtime   BuildKit
```

This drawing describes authority, not a requirement for one machine per box. The server and scheduler can initially run as different processes on the same control host. PostgreSQL can be managed or self-hosted. What matters is that build execution is on a deliberately separate trust surface with controlled access back to the API.

## One database, different responsibilities

For the first release, PostgreSQL is authoritative for runs, jobs, attempts, permissions, leases, schedules, and audit events. Object storage holds bytes: logs, reports, and artifacts. The scheduler must not infer truth from a browser connection or from an in-memory event queue. Notifications merely wake it to reread committed state.

The server exposes an explicit migration command. A single migration tree lives in the shared core repository. Scheduler startup checks schema compatibility; it does not race another application's migration runner. This avoids independent repositories becoming independent and conflicting owners of the same database.

Avoid a generic “execute command” endpoint on the control plane. The runner receives a constrained execution description after authorization. The runner API accepts only messages tied to its current identity and authorized attempt. A compromised runner should not be able to turn the server into a filesystem browser or cloud administrator.

## Classify code by trust

A signed webhook proves something about a delivery, not about whether the repository content is safe to execute. A developer with permission to change a test can cause arbitrary actions inside the test process. A private repository is not automatically trustworthy if contributors have different privileges. GitHub's secure-use guidance specifically describes risks around self-hosted runners and untrusted pull-request content. [S17](e-sources.md#s17)

The initial supported model is a team operating dedicated runners for trusted projects. Production deployment uses another pool, with a narrower target set and credentials unavailable to ordinary build jobs. Untrusted public contributions require a separately reviewed isolation mode. Do not quietly enable that mode because the same YAML syntax happens to work.

An outbound runner connection simplifies network exposure, but it does not make every server instruction safe. Authenticate both ends, validate the protocol, constrain the received fields, and reject unknown privileged options. Network direction and authorization are different controls.

## Resource boundaries are security boundaries

A log upload, compressed artifact, report file, and matrix expansion can all consume unbounded resources unless the protocol sets limits. Record maximum request sizes, maximum uncompressed archive size, file count, graph size, and execution duration. A limit without a visible error becomes a debugging problem; a limit without server enforcement becomes a suggestion.

Separate the control plane's outbound destinations as well. A notification URL or repository URL must not become an unrestricted request proxy into metadata services or private administrative endpoints. Destination policy, redirects, DNS resolution, and credential forwarding need a design rather than one regular expression.

## Exercise

A build pool and a production pool use the same machine but different labels. Build containers can reach the host Docker socket. Does this establish the boundary required by this chapter?

## Worked answer

No. Labels describe eligibility, not isolation. A process controlling the host daemon may affect other containers and host resources. Docker documents the daemon's authority and the risks of exposing it. Separate deployment authority from build execution, remove the socket from job containers, and select an isolation design appropriate to the accepted code. Different labels on one uncontrolled host do not create separate trust zones. [S08](e-sources.md#s08)

## Completion evidence

Produce a threat model that names who controls repository content, who owns runners, which credentials cross each boundary, and what happens if one runner is compromised. Every arrow in the architecture needs authentication, authorization, and a bounded payload contract.
