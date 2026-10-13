# Lab 03 — Reconciliation and ownership under drift

Atlas has three separate questions: how many task records should exist, which local containers belong to this agent, and whether the control plane will accept the agent's next status report. Predict each answer before running the fixtures. A container that disappeared is not sufficient permission to reset a running task to `pulling`.

This lab is an original **teaching extension** against source `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. Its observed track uses upstream `FakeRuntime`, the actual in-process `MemoryService` lifecycle, and the separate store-backed reconciler with its upstream test store. It uses no HTTP listeners, Docker daemon, PostgreSQL database, or external images. Source files copied for private-package access remain byte-identical; the only additions are two test files. The shipped server does not start the store-backed reconciler.

## Predict the two passes

Start with the five intent cases in [fixtures/cases.json](fixtures/cases.json). Write the expected new task count, ordered stop directives, service status, and transition-event count after two unchanged passes.

| Case | Initial state | First directive | Second unchanged pass |
| --- | --- | --- | --- |
| Below target | Three replicas, one running task | Create two pending records | No additional records/events |
| Failed, always | One replica, one failed record | Create one pending replacement | No additional records/events |
| Failed, never | One replica, one failed record | Preserve failed record, no replacement | Same failed record |
| Scale order | One desired replica, running + pending-a + pending-z + assigned | Stop pending-z, pending-a, assigned | No additional stop/events |
| Soft deletion | Deleting service, one running task | Desired stopped, actual still running | Service remains deleting |

The last case then receives explicit removed-task observations in the store fixture. Only the next pass marks the service deleted. This fixture is not a physical runtime acknowledgement transport. It isolates the reconciler's decision after that observation becomes available.

[The exact stop ordering](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L499-L540) prioritizes lifecycle state, then descending task ID. Desired stopped tasks stop counting as active immediately; this does not prove that their physical containers have already stopped. [Deletion logic](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/reconciler/reconciler.go#L240-L270) has the stronger terminal removed requirement.

## Run the isolated fixtures

Prerequisites are the locked Go 1.25.0 toolchain, its cached dependencies, Python 3, and a disposable copy of the locked application source. Do not execute against `evidence/orch`. The runner verifies all 361 baseline file hashes before making its two private `.book-labs/lab03*` package overlays. It never edits baseline files. Set the paths to your actual source copy and Go installation; the example values describe the generation environment.

```sh
python3 books/inside-orch/scripts/run_recorded.py \
  --id lab03-reader-run \
  --cwd /home/popac/alekpopovic.github.io \
  --output validation/labs/lab03-reader-command.json \
  -- python3 books/inside-orch/scripts/run_drift_lab.py \
  --source-copy /tmp/inside-orch-labs-cbfc94ade5b5/orch \
  --go-root /tmp/inside-orch-gomod/golang.org/toolchain@v0.0.1-go1.25.0.linux-amd64 \
  --output-prefix validation/labs/lab03-reader-observed
```

Use fresh output names: existing evidence is deliberately not overwritten. `run_recorded.py` captures UTC start/end, command, working directory, exit code and raw stdout/stderr. `run_drift_lab.py` copies unchanged agent/reconciler package and test files, adds the original tests, and executes only `TestBook*` with `go test -count=1`. The runner's fixed cache paths are generation defaults; adapt those environment locations for another host. The canonical tests contain executable fixture setup; the JSON fixture file describes and checks the exact case ID set.

## Observe lifecycle and ownership together

The ten agent cases all include an unmanaged container with a similar name and a managed container belonging to another node. Both must survive **each of the two passes**, including all cleanup cases. Matching uses labels, never name similarity. Exact [ownership predicates](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L689-L725) distinguish adoption from cleanup eligibility: matching additionally requires service, version and image consistency; cleanup eligibility requires managed, matching node and matching task identity.

| Case | Observed first-pass result |
| --- | --- |
| Missing, assigned task | Pull/create/start replacement; task becomes running |
| Missing, running task | `pulling` report rejected; no replacement created |
| Stopped, matching owned container | Start the existing container; report running |
| Image mismatch, running task | Remove owned mismatch, then reject `pulling`; no replacement |
| Version mismatch, assigned task | Remove owned mismatch and create replacement |
| Service-label mismatch, running task | Remove owned mismatch, then reject `pulling` |
| Foreign-node referenced container | Preserve it; reject attempted `pulling` reset |
| Unexpected owned orphan | Stop/remove orphan; unknown-task removed report is ignored by cleanup |
| Unmanaged referenced lookalike | Preserve it; reject attempted `pulling` reset |
| Soft-deleted owned task | Remove owned container; accepted removed report finishes service deletion |

The precise UUID-bearing rejection is retained per case in [the actual check](../../validation/labs/03-check.json). Its stable suffix is `cannot accept agent status "pulling"`. The running task remains running in control-plane state. This is a **passing test of an observed failure boundary**, not a successful recovery claim. Upstream agent unit tests use a more permissive fake client; connecting the unchanged agent to actual `MemoryService.ReportTaskStatus` exposes the invalid running-to-pulling transition.

Inspect [currentTaskContainer](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L357-L420), then [ensureTask](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L200-L355). Ordering matters: cleanup of an owned mismatch can occur before the later rejected lifecycle report. The lab leaves that result visible rather than modifying the agent or allowing an illegal transition. A second unchanged pass must add no transition events; repeated drift observations and rejected report attempts may still occur and are not transition-event duplicates.

## Optional reader Docker track

This track was **not executed for this lab**. Use a disposable host, inspect socket authority and `docker info`, and read the pinned [runtime integration test](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker_integration_test.go#L10-L120) before opting in. From the disposable application copy, the actual gate and test target are:

```sh
ORCH_DOCKER_INTEGRATION=1 go test -count=1 -run '^TestDockerRuntimeIntegration$' ./internal/docker
```

The daemon can grant host-level authority. Confirm the test's ownership labels, capture each created container ID, and retain the cleanup result. Clean only those captured IDs or an equally strict lab-owned label set. Never run broad container deletion or target another node's containers. A Docker runtime test still does not run this lab's MemoryService/agent lifecycle comparison; the fake track and daemon track establish different facts. The book's separately recorded real Docker flow is in Lab 01, with its own captured IDs and cleanup.

## Explain the boundary

| Question | Owner | Evidence in this edition | Remaining limitation |
| --- | --- | --- | --- |
| Desired replica task intent | Store-backed reconciler | Five actual cases, repeated no-op pass | Not composed into default server; fake store is not SQL |
| Local managed-container drift | Agent plus runtime and report contract | Ten actual FakeRuntime/MemoryService cases | No daemon behavior proven; running-to-pulling rejects recovery |
| Process restart | Binary lifetime and state owner | Separate [Lab 01](../01-initialization-restart/README.md) | Default active state is memory; container survival does not restore records |
| Database restoration | Migration/backup/store composition | Separate [Lab 08](../08-recovery-boundaries/README.md) | Restoring tables does not wire the default binary to persistent state |

Explain why changing only the fake client would hide the most useful finding. Propose a separate recovery design with legal lifecycle transitions, retry behavior and failure ownership; label it design work until tested. Do not patch the immutable baseline. Cleanup for this track is process exit plus the two owned overlay directories; it creates no external containers or database objects.
