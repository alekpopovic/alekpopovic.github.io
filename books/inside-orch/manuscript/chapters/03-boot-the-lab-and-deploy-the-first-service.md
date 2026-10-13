# Chapter 3 - Boot the Lab and Deploy the First Service

## Pinned Prerequisites and Installation

Atlas has a source map and passing package fixtures. The next question needs actual processes: can an operator submit a service, distinguish accepted intent from task execution, and remove the resulting workload without touching somebody else's containers? This chapter follows the upstream local-development path and makes its assumptions visible before starting it. You will learn to build the pinned binaries, inspect node/service/task state independently, and keep cleanup tied to the resources the experiment owns.

Use a disposable checkout or copy of source revision `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. The immutable evidence directory is for reading, not running scripts or writing build outputs. Go 1.25.0 is the declared baseline. Docker Engine access and Docker Compose are required for the upstream local stack; curl is used by the startup script. PostgreSQL runs in Compose, but its presence does not make the default control plane durable. The three processes have different state owners even when their containers share one Compose project.

The [installation guide](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/INSTALLATION.md#L5-L13) documents platform archives for Linux, macOS and Windows on amd64/arm64. This edition's source lock establishes the code revision, not availability of every advertised release archive. Building from the pinned source avoids assuming a moving installer selects the same revision. Record the compiler version, command and source hash. An exact source build is a different evidence statement from “the installer downloaded the latest release.”

The source-only build command is straightforward, provided it runs in the disposable Orch root:

```bash
go version
go build -o ./bin/ ./cmd/orch ./cmd/orch-server ./cmd/orch-agent
./bin/orch version
```

For an exported snapshot without Git metadata, select the documented build environment with VCS stamping disabled. Do not edit go.mod to fit whatever compiler happens to be installed. The edition's build records preserve the exact downloaded toolchain and environment. Their successful compilation establishes that baseline on this host, not all supported platforms or real daemon operation.

Before starting Compose, reserve host ports 8080, 8081 and 5432 or stop and choose the separately scoped direct-process alternative. Do not kill unrelated listeners to force the example to run. Inspect the Compose file and startup script first. A running local website on another port is irrelevant; an existing database on 5432 is a concrete collision. The startup script has an unbounded readiness loop, so a failed server can otherwise leave an operator waiting indefinitely.

## One Local Server and One Worker

The [startup script](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-up.sh#L4-L14) changes to its own source root, copies .env.example when .env is absent, and starts postgres, orch-server and orch-agent with the local-orch profile. That script does not run migrations. It waits for the server's fixed ready endpoint, then prints listener addresses. Those messages describe intended endpoints; they are not proof the worker registered or the application is healthy.

The current main Compose fixture is `compose.yaml`; historical development commits used docker-compose.yml before a later rename. Use an explicit unique COMPOSE_PROJECT_NAME so project-level shutdown identifies your stack. The script's .env creation belongs in the disposable copy and should contain synthetic development settings only. Do not copy a real environment file into the manuscript or execution evidence.

```bash
export COMPOSE_PROJECT_NAME=inside-orch-atlas-local
./scripts/dev-up.sh
./scripts/migrate-up.sh
./bin/orch --server http://127.0.0.1:8080 node ls
```

The startup decision itself is small enough to inspect exactly:

```bash
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

docker compose --profile local-orch up --build -d postgres orch-server orch-agent

echo "Waiting for orch-server..."
```

Exact source: [scripts/dev-up.sh:7–14](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-up.sh#L7-L14).

A bounded wrapper is useful when executing this procedure unattended. The wrapper should enforce a deadline and preserve server/agent logs if readiness never arrives, rather than report the last printed message as success. It must also retain the unique project name so a timeout cleans up only the attempted stack. Adding a deadline is a book-side operational adaptation; it does not mean the upstream script already implements one.

The migration command is separate because database schema setup and active state ownership are separate operations. Read its URL/default behavior before invocation and ensure it targets the owned Compose database. The server environment contains DATABASE_URL, but ordinary startup still selects NewMemoryService. A successful migration demonstrates SQL setup against that database. It does not change which service implementation handles POST requests.

The worker container mounts the host Docker socket. Consequently, workload containers are created through that host daemon; they are not nested containers owned automatically by the Compose service lifecycle. The worker advertises its log-server address inside the Compose network so the server can proxy logs. This distinction matters during cleanup: removing the agent container is not itself a supported instruction to delete all previously created workload containers.

The fixture deliberately disables user JWT authentication and supplies development agent-registration/encryption values. These settings make a loopback learning environment convenient, but they are not production credentials or a deployment recommendation. Agent endpoints and user endpoints have different authentication paths. Keeping user auth empty does not mean an arbitrary token is valid for a node credential. Later identity chapters examine those paths; here, preserve the fixture's explicit trust assumptions.

Atlas first checks node state rather than deploy blindly. A successful node list request can return no nodes even while the API is ready. Inspect hostname, advertised address and ready status, then keep the returned node ID as part of the experiment record. If the agent never registers, investigate its server URL, Docker connection and bootstrap setting before treating a service's lack of containers as a scheduler problem.

## The First Deployment Timeline

The upstream [http-api fixture](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/examples/http-api.yaml#L1-L14) uses nginx:1.27-alpine, one replica, container port 80 and public port zero. Its label request is role=worker and its resource values are 100m and 128Mi. Public zero asks for a dynamic host port rather than binding every replica to one fixed host port. The upstream name stays `http-api` in this exact walkthrough; later Atlas manifests explicitly use `atlas-api` instead of silently pretending the source fixture had another name.

Validate locally before submitting it:

```bash
./bin/orch validate deployments/examples/http-api.yaml
./bin/orch --server http://127.0.0.1:8080 deploy deployments/examples/http-api.yaml
./bin/orch --server http://127.0.0.1:8080 --output json service inspect http-api
./bin/orch --server http://127.0.0.1:8080 --output json service ps http-api
./bin/orch --server http://127.0.0.1:8080 events --service http-api
```

Local validation proves that this parser accepts the file. Server admission still checks current policy, references, namespace and quota. A successful deploy response proves accepted service state; it does not prove nginx has started. Read desired replicas from the service spec and actual status from matching tasks. Keep task IDs, node IDs and container IDs distinct. A transition from assigned through pulling/created/running describes reported progress, while an independent Docker inspection confirms the local object.

Set explicit rejection criteria before the first deploy: reject a missing registered worker, a service whose accepted spec differs from the intended manifest, a task assigned to an unexpected node, or a container whose managed labels do not match the recorded task. Also reject cleanup evidence collected only after a broad daemon-wide deletion. A convincing empty list after destroying unrelated workloads is a failed ownership experiment. These criteria make the demo assessable even when the expected happy path is interrupted.

Save the pre-scale snapshot before issuing scale. Otherwise a later list containing two tasks cannot tell you whether the original task survived or both were replaced. Likewise, preserve the pre-delete IDs so an empty service response can be compared with the exact local objects that previously existed. The evidence is a relationship across snapshots, not the attractiveness of one final table.

The normal memory path may create an assigned task immediately. Do not insert an imagined pending state just because the architecture document describes a standalone reconciler followed by the scheduler. The agent then polls and acts. Depending on observation timing, a single service-ps request may miss intermediate states. Missing a short-lived state in a poll is not evidence the code skipped it. Use timestamped snapshots and accepted reports when reconstructing a timeline.

Scale only after establishing the first replica's identity:

```bash
./bin/orch --server http://127.0.0.1:8080 scale http-api --replicas 2
./bin/orch --server http://127.0.0.1:8080 --output json service ps http-api
./bin/orch --server http://127.0.0.1:8080 logs http-api --tail 20
./bin/orch --server http://127.0.0.1:8080 scale http-api --replicas 1
```

The dynamic published ports let two replicas use distinct host ports on one worker. That does not prove all placement/resource policies were enforced. The agent path omits resource limits even though the manifest declares them; Chapter 5 measures that boundary. Logs can legitimately be empty before traffic reaches nginx. An empty log stream is not a deployment failure by itself, and a successful log proxy is not a direct health request to every replica.

The motivating interruption occurs after Docker creates a container but before the server accepts its created report. The task record can lag behind the daemon. An agent retry should rediscover the same task identity, not create a new unrelated replica because the human saw stale status. The package fake/adoption tests address part of this scenario; a real runtime observation must correlate labels and IDs. Do not manually run docker rm merely to make a stale API response look consistent.

The [local environment commit](https://github.com/alekpopovic/orch/commit/f7e77377fbc8565d737ad2cdcf2f2e318b03e4fa) introduced scripts and fixtures; the [Cobra CLI commit](https://github.com/alekpopovic/orch/commit/042a4a44ecfaa884d6173f9d93afafa81a24ea27) introduced operator commands. The [final pinned documentation update](https://github.com/alekpopovic/orch/commit/cbfc94ade5b57e449d6b73bf1485b1c5b1647022) describes installation. These are engineering/history evidence, not stored proof that this complete demo ran in those commits. Original prompts 05,21,27,28 remain retrospective intent associations where appropriate.

## Cleanup and the Limits of the Demo

Remove the workload through the server while the worker is still available:

```bash
./bin/orch --server http://127.0.0.1:8080 delete http-api
./bin/orch --server http://127.0.0.1:8080 --output json service ps http-api
./scripts/dev-down.sh
```

Deletion marks desired cleanup rather than instantly proving every container disappeared. Wait for the owned task/container identities to reach removal, and independently inspect those IDs before shutting down the worker. The [shutdown script](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/dev-down.sh#L4-L7) performs Compose down for selected profiles. It does not enumerate and remove every container created through the host socket, and it does not use down --volumes. PostgreSQL volume retention and workload cleanup therefore need separate observations.

If the server fails before deletion, stop automatic experimentation and inspect only objects carrying your recorded task/node IDs. Do not run a broad command removing every orch.managed container on a shared daemon; that label can belong to somebody else's cluster. Preserve evidence of surviving objects and remove only your exact recorded IDs when authorized for the disposable lab. This is the same ownership principle used for process cleanup and database reset tests.

The upstream Compose commands above are source-checked expected steps until a matching execution record establishes their results. A successful package build or focused fake-runtime fixture does not count as a Compose run. If fixed ports or Docker are unavailable, keep the local validation and source trace, and use an owned ephemeral-listener/fake-runtime experiment for API transitions. Label that alternative accurately rather than replacing the missing daemon observation with an invented transcript.

A real-Docker alternative was executed for this edition and is retained in `validation/intake/docker-complete-flow-log-guard.json` with its complete JSON stdout. It connects the ordinary server handler to a real agent Runner and Docker adapter inside a guarded teaching harness. The wrapper requires a cached image and checks exact owned identities; it publishes no workload host ports. This is an observed component composition, not a claim that the upstream Compose commands above ran.

The observed sequence includes one accepted service-created event, an owned running nginx task, an HTTP request made with docker exec inside that captured container, and a log request traversing server, agent and Docker. The response matched the nginx welcome page, while the log response contained nginx output. Timestamped task snapshots then show active replicas changing one to two to one, followed by terminal deletion. Captured IDs and cleanup evidence allow those observations to be correlated without inventing an external public endpoint. The earlier failed guard attempt remains separate from the corrected passed run.

This alternative supplies runtime evidence for deployment, scaling, logs and removal while leaving upstream Compose startup as source-checked procedure. It also exposes the resource-limit propagation gap measured in Chapter 5. A passing demonstration must preserve both its working path and its limitation, rather than treating every declared specification field as enforced because nginx answered one request.

The demo's useful result is a correlated sequence: accepted service intention, identified tasks, worker reports, independently inspected containers, scale changes and owned cleanup. Its limits are equally concrete: default state is memory-backed, resource propagation has a known gap, and this small cluster has no demonstrated HA/fencing contract. These facts let Atlas continue into lifecycle reasoning with evidence instead of a screenshot of a green endpoint.

## Exercises

1. Explain why dev-up.sh succeeding does not prove the worker is ready or migrations ran.
2. Why can the example scale to two replicas on one host when public port is zero, and what changes with one fixed public port?
3. The agent container is stopped before service deletion. Explain the cleanup problem and the observations needed before removing anything.
4. A teammate reports “PostgreSQL started, therefore this demo survives server process loss.” Identify the wrong inference and design a narrow observation that tests it.

[Worked answers](../solutions/ch03.md) include the ownership and rejection criteria for each decision.
