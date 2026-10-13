# Chapter 40 - Release a System You Can Honestly Operate

Atlas has reached the end of the implementation tour with an operating local demonstration, a substantial set of packages, and several important limits. The release decision must account for all three. A successful workload demonstration does not erase memory-state loss on server restart, and an unwired durable store does not invalidate every useful scheduler or agent test. The task is to describe the system precisely enough that another operator can make a responsible decision.

This chapter assembles an operational dossier instead of a production-readiness slogan. You will connect actual test records with their prerequisites, read deployment manifests as conditional procedures, and interpret a database restore against the correct state owner. The final Atlas decision retains unresolved requirements and turns them into acceptance-oriented engineering work.

## Release Checks With Honest Coverage

The repository's CI runs formatting checks, vet, OpenAPI tests, lint, coverage tests, and a separate race job. The [workflow configures a PostgreSQL service for its quality job](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/.github/workflows/ci.yml#L12-L76). That is a source-defined procedure. It is not evidence that this exact workflow completed in the edition’s captured verification or that every integration fixture is compatible with the latest schema.

The actual book baseline built the four application binaries from the locked disposable source with Go 1.25.0. The [successful build record](../../validation/intake/orch-build-isolated-root.json) follows earlier failed attempts caused by the inherited toolchain environment. Preserve both the diagnosis and corrected environment. A command record's exit status is a better witness than a filename suggesting that an export succeeded.

The [baseline tests](../../validation/intake/orch-baseline-tests.json) and [race run](../../validation/intake/orch-race-tests.json) passed their reached paths, retaining explicit Docker/PostgreSQL skips. Named test pass events must be distinguished from package summaries when counting results. The separate owned PostgreSQL fixture run failed two store tests because it applied only migrations one through fourteen while current queries require a column added in sixteen. That failure remains part of the dossier.

Later full-schema and guarded Docker extensions supply additional evidence, but they do not rewrite the original test outcomes. A full-schema store experiment is not the default server using PostgreSQL. A real-Docker harness with owned cleanup is not an unmodified Compose deployment. A race detector passing selected executions is not proof that all possible interleavings are safe. Release language must preserve these qualifications.

The [Makefile lint target falls back to formatting checks and go vet when golangci-lint is absent](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/Makefile#L9-L17). That fallback is useful, but it is not equivalent to running the configured linter. Record which tool actually ran. Similarly, parsing OpenAPI checks document structure; comparing routes checks inventory; cross-layer request/response tests check behavior. None should claim the others' coverage automatically.

Commit [7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d](https://github.com/alekpopovic/orch/commit/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d) added operational hardening and release material. The current release notes explicitly retain the memory-control-plane boundary. Atlas should keep that honesty in its own deployment report rather than replacing it with a checklist whose final green box overrides the architecture.

## Deployment Manifests and Runtime Prerequisites

The production Compose file requests explicit server and agent image variables and requires several secrets. It creates PostgreSQL, server, agent, and optional monitoring services. The agent mounts the host Docker socket. These are starting points for an operator, not a managed platform installation. They depend on trusted nodes, chosen image identities, network restrictions, and a reviewed secret-delivery mechanism.

The [agent systemd unit joins the docker group and grants socket access](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/production/systemd/orch-agent.service#L9-L25). Host hardening options remain valuable, but Docker API authority can still amount to host control. Atlas should treat agent compromise as a node-compromise boundary, prevent workloads from receiving the socket, and restrict agent endpoints to appropriate networks. A non-root Unix username alone does not remove the authority granted by that socket.

The server unit runs as its own identity with a protected filesystem and environment file. Restart=always can restore process availability after failure, but it cannot persist MemoryService maps. A restart policy that makes the endpoint healthy again may therefore hide state loss unless the operational checks also compare expected services, tasks, credentials, and events. Process supervision and durable recovery are independent concerns.

The [Compose server environment supplies DATABASE_URL and TLS placeholders](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/deployments/production/docker-compose.yml#L22-L51). A database URL does not activate durable control-plane storage; TLS placeholders do not implement a native server TLS mode. The documented deployment assumes a reverse proxy or load balancer terminates TLS. Atlas must inspect actual network listeners and proxy configuration instead of assuming that mounted certificate files are being consumed.

Pin all deployment artifacts before a reproducible installation. Some optional monitoring images default to latest in the example. A future execution using those defaults can select different software from the reviewed run. Record digests or immutable tags, tool versions, configuration, and expected ports. This chapter does not fetch or launch those public images, install systemd units, create host users, or modify the machine's firewall.

Commit [18fcf32524007ba7d8a71acd70e5acc48f758e49](https://github.com/alekpopovic/orch/commit/18fcf32524007ba7d8a71acd70e5acc48f758e49) added the deployment examples. Their checked-in presence establishes a reviewable starting configuration. It does not establish that Atlas has a working TLS proxy, complete cross-node service networking, fenced stateful storage, or an approved production trust model.

## A Backup Drill With the Correct State Boundary

The backup script requires an explicit database URL and creates a PostgreSQL custom-format dump without owner or privilege restoration. The restore script requires an explicit target, an existing input file, and acknowledgment. The guard is visible in source:

```bash
if [[ "$yes" != true ]]; then
  cat >&2 <<'WARNING'
Refusing to restore without --yes.

Restore modifies the target database. If --clean is also supplied, existing
objects in the target database may be dropped before being recreated.
WARNING
  exit 2
fi
```

Exact source: [scripts/restore-db.sh:73–81](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/scripts/restore-db.sh#L73-L81).

Acknowledgment protects against accidental invocation; it does not inspect whether the selected target is safe. Atlas should restore into a newly owned disposable database, retain its exact name, verify that it was absent before creation, and remove only that target afterward. Never demonstrate destructive clean against a live database merely to show that the script accepts the flag.

The [backup runbook distinguishes database rows from external configuration and runtime objects](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BACKUP_RESTORE.md#L3-L36). A dump excludes Docker images, containers, volumes, process memory, TLS material, JWT signing secrets, bootstrap tokens, and the local envelope key. Encrypted secret rows without the matching envelope key remain rows that cannot yield their original plaintext. Backup success therefore needs both data verification and a separate secure key-recovery plan.

The actual [full-schema recovery record](../../validation/intake/full-schema-recovery-corrected.json) created owned source and restore databases, applied all sixteen migrations, inserted scoped records and synthetic encrypted canary data, dumped and restored, and verified the restored values. It rejected a wrong decryption key. It also retained migration idempotence and competing task-claim observations. Its program is a teaching extension around the store package, not an alternative executable silently substituted for orch-server.

That drill establishes useful package-level durability and restore behavior. It cannot restore active records created only inside a default MemoryService, because those records were never part of the database dump. The separate actual fresh-server experiment observed exactly that distinction: the second process was healthy enough to answer HTTP while its prior services, tasks, and nodes were absent. The surviving captured Docker container belonged to another state owner.

A recovery procedure should therefore specify what it intends to reconstruct. Database restoration recovers selected persisted records. Agent reconciliation inspects managed engine objects. Image registries supply images. Volume restoration recovers workload data. Configuration/key recovery restores identities and decryption capability. A single successful pg_restore command cannot certify all of those owners or their coordinated consistency.

Commit [64abe001e83932cba294831424557dfd16f77c8c](https://github.com/alekpopovic/orch/commit/64abe001e83932cba294831424557dfd16f77c8c) added backup scripts and guidance. The source remains useful when its conditional persistence premise is retained. Atlas's release dossier must say whether it is evaluating the store package, a proposed durable composition, or the actual default binary. Mixing those modes is the most consequential backup error in this case study.

## The Final Readiness Decision and Backlog

The [dossier verifier](../../examples/teaching-extensions/ch40/verify_dossier.py) checks selected evidence records exist, match the locked source, and retain their observed success status and output files. Its [actual corrected execution](../../validation/labs/ch40/dossier-integrity-corrected.json) passed. The initial inventory deliberately failed on an incorrectly selected failed build record; the corrected inventory points to the actual successful build. Both records remain visible.

Passing this verifier means the evidence inventory is internally connected. It explicitly reports production_decision as not approved. It does not certify application safety, replace independent review, or rerun every experiment. This distinction prevents the final book check from becoming an accidental production approval mechanism. The result is a reviewable local dossier, not a deployment action.

| Requirement | Evidence today | Acceptance work still needed |
| --- | --- | --- |
| Durable active state | Store, migrations, owned restore exercise | Compose a transactionally equivalent durable server |
| Exclusive controllers | Lease library and loss tests | Wire loops, repair session cleanup, verify topology and handover |
| Resource enforcement | Direct adapter works; normal path drops limits | Preserve requested fields through DTO and agent into engine |
| Autoscaling | Controller/provider interfaces and deterministic package tests | Supply observed metrics and explicit server composition |
| Node trust | Enrollment and credential policy mechanisms | Complete transport identity and operational rotation model |
| Networking/stateful recovery | Local and documented boundaries | Cross-node connectivity, fencing, and volume-aware recovery |

These backlog items should be ordered by the guarantee Atlas intends to offer. Durable active state precedes credible fresh-server recovery. Leadership composition follows shared authoritative state and must resolve retained advisory locks. Runtime resource propagation is a separate acceptance gate even for a single server. Complete node identity and networking cannot be deferred behind a claim that workloads are securely isolated across hosts.

Each improvement needs a negative case as well as a happy path. Durable transactions should survive an injected failure without partial service/event writes. Leadership should reject wrong cluster identity and stop mutating work after loss. Resource propagation should preserve explicit values and reject malformed inputs. Metrics providers should distinguish unavailable observations from low utilization. Networking tests should measure actual reachability rather than replay a diagram.

The Atlas case study demonstrated real guarded deployment, logs, scale, deletion, resource-boundary differences, actual memory-state loss after process restart, package-level database restoration, deterministic controller decisions, and scoped performance observations. The dossier also preserves harness corrections and explicit skips. That combination is more useful than either declaring everything ready or discarding every working component because production prerequisites remain incomplete.

An operator can now make a bounded decision: use the current system for the documented local learning and demonstration scenarios, with owned resources and understood failure boundaries; require further implementation and evidence before relying on durable production orchestration. The book ends with that concrete decision because an honest operating contract is part of the engineering, not a qualification added after the release is advertised.

## Exercises

1. Build a coverage table separating the ungated suite, explicit integration skips, original PostgreSQL fixture failure, full-schema extension, and guarded real-Docker flow.
2. Review the systemd restart policy and Compose database/TLS variables. Explain why they do not establish durable state or native TLS consumption.
3. Describe the owned restore drill, including database identity, canary verification, key handling, and cleanup. Identify the state a dump cannot recover from the default server.
4. Run the dossier verifier and select the next Atlas guarantee to implement. Define its failure case, evidence, and rejection criterion without changing production_decision merely because an inventory check passes.

Worked answers are in [Chapter 40 solutions](../solutions/ch40.md), with source and dossier classifications in the [claim ledger](../../validation/evidence/ch40.json).
