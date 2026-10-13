# Chapter 8 - A CLI That Operators Can Automate

The Atlas operator wants a simple answer in a deployment script: does the server currently report the desired replicas available? A table meant for a terminal is a poor input format for that decision. The pinned CLI provides JSON output, predictable configuration precedence, and distinct local validation, but an automation script still needs to check the correct fields and preserve failures in its exit status.

We will build a small status checker as a book-side teaching extension. It calls the real CLI rather than guessing HTTP payloads, requires an explicit server address, and describes its result as server observation rather than a fresh host-health guarantee. A reproducible lab executes the same commands against an owned fresh server with synthetic configuration.

You will be able to predict configuration precedence, distinguish local validation from server acceptance, and automate current JSON output while retaining actionable failures and explicit scope.

## Cobra Composition and Local Validation

The root command is assembled with injected output writers and a client factory. This makes command behavior testable without hard-wiring a network implementation into every subcommand. [NewRootCommand registers](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go#L123-L194) version, validation, node, service, deployment, scaling, events, logs, namespace, and later feature groups. An available command group establishes CLI wiring, not a claim that every related package has complete end-to-end integration.

Persistent flags include `--server`, `--token`, `--namespace` with `-n`, `--output`, and `--config`. Output is restricted to table or json in the root pre-run check. Do not invent `--format`, `--wait`, or a default server flag because another orchestrator uses them. Read each current subcommand before illustrating an operator procedure.

The `validate <file.yaml>` command invokes ParseDeployFile directly, prints a local validity message, and returns its error. It does not construct the API client. Consequently a missing server URL does not prevent local deployment validation. The chapter 5 harness actually exercised that property while rejecting invalid fixtures.

`deploy <file.yaml>` uses the same parser but then constructs a client and submits the specification. Local parsing catches shape and quantity errors. Server admission can still reject namespace, authorization, policy, references, or quota. A successful validate followed by a failed deploy is not inconsistent: the commands cover different boundaries.

Service references can be names or UUIDs. [resolveService uses](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/root.go#L934-L947) GetService for a UUID and otherwise lists services and selects a matching spec name. A name-based `service inspect atlas-api` therefore has a list-and-select step, while an ID points directly at an identity. During deletion and recreation, reusing the same name can select a different service than a previously captured ID.

The CLI maintains its own APIClient wrapper and structured APIError formatting. The public client package contributes shared URL normalization, but the CLI is not simply an alias for every public-client method. Follow the injected client interface and actual implementation when adding an automation command; the existence of a similarly named method elsewhere does not connect it automatically.

## Configuration Precedence You Can Predict

CLI configuration begins as an empty configuration, optionally reads YAML, then applies nonempty environment values, then nonempty explicit overrides. The server, token, and namespace use the same order. Namespace falls back to default when still empty. Server URL does not receive an implicit localhost default.

```go
	if value := strings.TrimSpace(os.Getenv("ORCH_SERVER_URL")); value != "" {
		cfg.ServerURL = value
	}
	if value := strings.TrimSpace(os.Getenv("ORCH_TOKEN")); value != "" {
		cfg.Token = value
	}
	if value := strings.TrimSpace(os.Getenv("ORCH_NAMESPACE")); value != "" {
		cfg.Namespace = value
	}
	if strings.TrimSpace(overrides.ServerURL) != "" {
		cfg.ServerURL = strings.TrimSpace(overrides.ServerURL)
	}
	if strings.TrimSpace(overrides.Token) != "" {
		cfg.Token = strings.TrimSpace(overrides.Token)
	}
	if strings.TrimSpace(overrides.Namespace) != "" {
		cfg.Namespace = strings.TrimSpace(overrides.Namespace)
	}
	if strings.TrimSpace(cfg.Namespace) == "" {
		cfg.Namespace = "default"
	}
	return cfg, nil
}
```

Exact source: [internal/config/config.go:132–154](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/config/config.go#L132-L154).

For the Atlas experiment, imagine YAML naming `http://127.0.0.1:1` and namespace absent-config. Environment supplies another server value and absent-env. An explicit `--server` pointing at the owned server and `--namespace default` wins over both. Remove those flags and the nonempty environment values win over YAML. Remove the environment settings and YAML wins. These are precedence rules for nonempty values, so an empty flag is not a reliable way to erase a configured credential.

| Setting source | Priority | Atlas implication |
| --- | --- | --- |
| Explicit nonempty flags | Highest | Select the intended server and namespace for this command |
| Nonempty ORCH_SERVER_URL / ORCH_NAMESPACE / ORCH_TOKEN | Middle | Override values in the config file |
| CLI YAML | Lower | Provides persistent operator settings |
| CLI fallback | Last | Namespace defaults; server remains required |

The default configuration path comes from the operating system's user-config directory, under `orch/config.yaml`, with `.orch.yaml` as fallback if that directory cannot be determined. Automation should pass an explicit config path when it needs reproducible isolation. Do not repurpose HOME or dump the user's config file to prove which value was selected.

The implementation calls LoadCLI for server, token, and namespace separately. A malformed file can fail server selection before any request is made. That is different from successful configuration followed by 401. Report the failing boundary and preserve the command exit code, rather than telling the operator every problem is a bad token.

We tested server and namespace precedence with the actual CLI binary against the owned loopback server. Token precedence is source-inspected in the same loader; the lab does not claim an authenticated multi-token deployment because its fresh development server intentionally has user JWT enforcement disabled. Synthetic agent credentials used for reports are a separate internal contract and are never printed.

## JSON Output for Operator Automation

Read the output writer before selecting fields. [writeService emits](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/output.go#L174-L179) the service object directly in JSON mode, and [writeTasks emits](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/output.go#L191-L202) the task array. These are not the HTTP envelopes containing service or tasks. An automation script that uses `.service.spec.replicas` against CLI inspect output is reading the wrong shape.

The status checker is `examples/teaching-extensions/ch08/atlas_status.py`. It runs `service inspect` and `service ps` with `--output json`, an explicit server, and selected namespace. It validates service identity, deployment version, replica count, unique task identities, task ownership, and required task fields. It counts only tasks with desired_status running and the current deployment version. Reported availability follows the upstream lifecycle helper: actual status running or healthy.

That choice deserves a label. Running means the server accepted a runtime execution report; it does not prove a business endpoint is responding now. Healthy records a health result at an observation time. Neither makes two separate inspect and ps requests a transactional snapshot. The script's JSON result explicitly says server observation only, no fresh host probe.

Its success condition is an active service whose number of current-version intended-running tasks equals spec.replicas, with all those tasks reported available. A zero-replica active service can satisfy that condition with zero current tasks. A task from another service is a contract error, while a historical task desired removed is excluded from the active count. This prevents scale-down history from being mistaken for a missing or extra current replica.

The exact child commands have the following structure, with the lab's ephemeral origin substituted by the harness:

```bash
orch --server "$ATLAS_SERVER" --namespace default --output json --config "$ATLAS_CONFIG" service inspect atlas-api
orch --server "$ATLAS_SERVER" --namespace default --output json --config "$ATLAS_CONFIG" service ps atlas-api
```

ATLAS_SERVER and ATLAS_CONFIG here are task-specific variables, not an implicit CLI default. The actual executed command arrays and the selected generated loopback address are retained in the lab record. The script never prints a bearer token or forwards raw subprocess stderr into its user-facing failure text.

There remains a failure window between its two reads. A concurrent rollout or scale can change the deployment version or replicas after inspect but before ps. The conservative outcome is a non-converged result and another bounded check, not automatically changing desired state. A robust deployment pipeline can poll with a deadline, but this teaching script intentionally performs one check and leaves retry policy to its caller.

## Failures That Belong in Exit Status

The checker uses zero for reported convergence, one for a valid but non-converged observation, two for CLI/transport failure, and three for incompatible JSON shape. These are the teaching script's own statuses, not undocumented promises about every upstream CLI code. Upstream errors normally reach the executable's error path as a nonzero exit.

A two includes missing CLI, timeout, server rejection, and missing service resolution. Its concise instruction is to inspect CLI path, server reachability, namespace, and credential configuration. The reason for suppressing raw child stderr is specific: diagnostic strings can contain configuration details or URLs. Operators can run the corresponding CLI command in their own controlled terminal when they need the richer structured error.

A three means the script cannot safely interpret the current contract. It must not convert absent replicas or a renamed status field into zero and announce success. Likewise a malformed task row must not be silently skipped. Validating expected values after JSON decoding is the practical counterpart to chapter 7's renamed-field example.

The integration harness `examples/teaching-extensions/ch08/exercise_cli.py` verifies baseline hashes, starts one actual server on a newly selected loopback port, creates temporary config files, and executes the illustrated CLI/status procedures. Prerequisites are Python 3, the built pinned CLI/server, and local listener permission. No Docker daemon, database, or external endpoint is needed.

Run the actual lab procedure from the website root:

```bash
python3 books/inside-orch/examples/teaching-extensions/ch08/exercise_cli.py \
  /tmp/inside-orch-labs-cbfc94ade5b5/bin/orch \
  /tmp/inside-orch-labs-cbfc94ade5b5/bin/orch-server \
  /tmp/inside-orch-labs-cbfc94ade5b5/orch
```

`validation/labs/ch08/exact-cli.json` records a passed execution. Its stdout retains every real child command, exit status, and diagnostic. It covers flag-over-environment-over-file, environment-over-file, file-only configuration, missing server failure, local validation, deployment, inspect, ps, missing service, and connection-refused status checks. Intended failures are assertions within a successful harness, not discarded errors.

Before any node exists, Atlas's three replicas are accepted as intent but the status checker exits one. The harness then registers a synthetic worker and authenticates running reports for its three assigned tasks. The checker exits zero on those server observations. A separate semantic fixture run in validation/labs/ch08/status-semantics.json rejects duplicate task identities, missing contract fields, foreign-service rows, and boolean replica values; it also checks zero replicas and old-version cleanup history. These controlled fixtures complement the real CLI exercise without claiming host observations. No Docker containers are started, so the result cannot be described as three verified running host processes. This is an explicit and useful contract experiment rather than a simulated production deployment.

Cleanup stops only the process launched by the harness and removes its temporary config directory. The in-memory service disappears with that process. Captured evidence remains. The refused-connection case uses loopback port 1, not a remote URL or a previously running owner's endpoint. The chapter's commands deliberately avoid putting secrets on the command line.

The [initial Cobra CLI commit](https://github.com/alekpopovic/orch/commit/042a4a44ecfaa884d6173f9d93afafa81a24ea27) established command structure. [Configuration hardening](https://github.com/alekpopovic/orch/commit/a4844c571a0ddf33879556413a62d49a408609e3) later introduced shared config handling and related settings. Original prompts 05,43,44 explain the intended progression; the current parser, loader, command definitions, and actual child-command record establish the behavior we teach.

A shell caller should preserve the checker’s status immediately instead of piping its output into an unrelated success-producing formatter. It can retain the JSON on standard output for a report while using the exit code to decide whether to proceed. A non-converged result should not trigger an unconditional redeploy: assigned replicas may simply be waiting for a worker, and a transport error leaves acceptance uncertain. Keep observation and mutation as separate operator actions. If a pipeline adds retries, give them a deadline and retain the last failure category so a missing server or incompatible schema cannot become an endless wait that looks like deployment progress.

## Exercises

1. Predict the selected server and namespace when YAML, environment, and nonempty flags disagree. Explain the effect of removing each higher-priority source.
2. Explain why local validate succeeds without a server address but service ls fails. Identify which layer first needs an API client.
3. Modify your reasoning for an old-version healthy task alongside current-version assigned tasks. Should the status checker succeed, and which actual JSON fields decide?
4. An operator proposes grepping the table for running and treating any matching line as success. Explain the unsafe assumptions and how the exercised checker handles missing service, non-convergence, and transport errors.

See the [worked answers](../solutions/ch08.md).
