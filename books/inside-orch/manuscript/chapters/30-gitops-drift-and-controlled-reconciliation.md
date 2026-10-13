# Chapter 30 - GitOps, Drift, and Controlled Reconciliation

Atlas API intent now lives in a Git repository. An operator can point to a committed manifest and ask which revision produced the service. That improves traceability, but it does not automatically make a repository apply atomic or every deletion safe. The controller still reads files, calls mutations and records progress across several failure windows.

This chapter assumes shared service parsing, admission and namespace scope. You will follow an actual local Git checkout into MemoryService, compare warn with auto_revert after manual scaling, and inspect the exact prune predicate. The safe lab uses real temporary commits and no containers. Its observations establish control-plane behavior for that fixture rather than a production deployment pipeline.

## A Source Revision You Can Trace

GitOpsSource identifies a repository URL, branch, path, sync interval, namespace, drift policy and prune setting. ValidateSource requires a nonempty repository/branch, positive interval and a supported drift policy. It rejects URL user information and credential-shaped query parameters. A relative configured path must remain inside the repository. [Claim ch30.source](../../validation/evidence/ch30.json).

CommandFetcher creates an owned temporary directory and invokes git clone with an argument slice, then resolves HEAD through rev-parse. The returned Checkout contains Directory, Revision and Cleanup. Sync defers that cleanup after a successful checkout. This gives the controller a concrete revision and a bounded checkout lifetime without mutating the pinned source or keeping an unmanaged checkout.

[internal/gitops/gitops.go, lines 73–85](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L73-L85) at the locked revision.

```go
	cleanup := func() { _ = os.RemoveAll(directory) }
	args := []string{"clone", "--depth=1", "--single-branch", "--branch", source.Branch, "--", source.RepositoryURL, directory}
	command := exec.CommandContext(ctx, "git", args...)
	if output, err := command.CombinedOutput(); err != nil {
		cleanup()
		return Checkout{}, fmt.Errorf("clone repository: %w: %s", err, strings.TrimSpace(string(output)))
	}
	revisionBytes, err := exec.CommandContext(ctx, "git", "-C", directory, "rev-parse", "HEAD").Output()
	if err != nil {
		cleanup()
		return Checkout{}, fmt.Errorf("resolve checkout revision: %w", err)
	}
	return Checkout{Directory: directory, Revision: strings.TrimSpace(string(revisionBytes)), Cleanup: cleanup}, nil
```

A branch name is still mutable. The important evidence is the checked-out commit, not an assumption that main always means the same content. Local clone depth behavior can differ from a remote transport, but the resolved HEAD identifies the actual fixture revision. Record that value in the lab rather than inventing a short placeholder commit or treating a previous source revision as the new checkout.

The canonical teaching fixture creates a temporary repository, commits atlas.yaml, synchronizes it and later commits its removal. Its [actual execution record](../../validation/labs/ch30/teaching-fixture.json) contains both full manifest-repository commit IDs in stdout. Those IDs identify this disposable content history; they are distinct from the pinned Orch source SHA used to execute the controller. The manifest commits belong only to the disposable fixture.

Credentials in repository URLs are dangerous because failure messages can include command output and source metadata. The implementation rejects obvious URL-userinfo and credential query forms, but that is not a promise to sanitize every possible secret-bearing remote string or Git configuration. The lab therefore uses a local path and no credentials. A real private-source integration needs a separate reviewed authentication mechanism.

## Fetch, Parse, Admission, and Apply

After checkout, manifestFiles selects the configured YAML file or walks a configured directory, collects .yaml/.yml paths and sorts them. Deterministic path order makes partial outcomes reproducible. It does not make all files one transaction. Sync reads, parses and applies each file inside the loop before moving to the next. [Claim ch30.apply](../../validation/evidence/ch30.json).

[internal/gitops/gitops.go, lines 218–235](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/gitops/gitops.go#L218-L235) at the locked revision.

```go
	syncCtx := namespace.WithContext(ctx, source.Namespace)
	managed := make([]string, 0, len(files))
	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("read manifest %q: %w", file, err))
		}
		spec, err := controller.parser(data)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("validate manifest %q: %w", file, err))
		}
		service, err := controller.store.ApplyService(syncCtx, spec)
		if err != nil {
			return controller.fail(syncCtx, source, fmt.Errorf("apply service %q: %w", spec.Name, err))
		}
		if marker, ok := controller.store.(managedStore); ok {
			relative, _ := filepath.Rel(checkout.Directory, file)
			policy := source.DriftPolicy
```

The server supplies cli.ParseDeploy, and ApplyService enters the checked service create/update paths. This is the ordinary shared parsing/admission boundary discussed earlier. Namespace context comes from the GitOps source, so manifests are applied within that selected scope. Successful services can be marked with source ID, checkout commit, relative path, desired spec, policy and last-check time.

Suppose atlas-a.yaml is valid and applied, while atlas-b.yaml contains an unknown field. The controller fails on the second file and records source.LastError, but the first service mutation has already happened. There is no repository-wide rollback in this loop. The incident record must inspect live services as well as the source status; a failed sync does not imply nothing changed.

Source.LastRevision is updated after the successful loop and optional prune. A failed sync can therefore leave prior revision metadata while an earlier file from the new checkout has already changed a service. This is an important provenance limit. A future all-or-nothing apply would need a deliberate validation/planning and transaction/operation protocol rather than merely changing the error message.

The failure helper records the error and sync-attempt time, then emits failure observations when source update succeeds. Event and audit appends in the emitter are best effort. A successful source update is not a durable mutation journal of every per-file action, especially with default MemoryService. Retain actual fixture output and service state before cleanup instead of relying on an assumed complete history.

Repeated application of an unchanged normalized spec should avoid creating unnecessary versions. The upstream local-repository test explicitly synchronizes twice and asserts the version does not advance. The [focused executed suite](../../validation/labs/ch30/focused-tests.json) passed that case alongside local prune and credential-URL rejection. It uses real Git commands and in-process state, with no external repository or Docker deployment.

## Warn Versus Auto-Revert Drift

MemoryService stores a GitOpsManagedState with DesiredSpec. GitOpsStatus compares current service.Spec against that stored desired value using DeepEqual. It marks missing sources unknown, stored errors sync_error, equality in_sync and differences drifted. The exact comparison is the code's normalized stored representation, not a semantic diff of every physical container. [Claim ch30.drift](../../validation/evidence/ch30.json).

With warn, a manual scale can remain live while status reports drifted and emits a drift observation. With auto_revert, that same status method restores DesiredSpec, increments deployment version, updates the timestamp and calls immediate service reconciliation. It then marks the service in_sync. This is a mutating status path, not merely a passive read or an independently proven continuously running drift controller.

The Atlas fixture begins with replicas zero in the committed manifest. It manually scales to two, checks warn and verifies two remain. It then changes the stored managed policy to auto_revert, manually scales to three and calls status. The returned service has replicas zero and in_sync. These values are actual assertions in the recorded run. No workload processes existed, so the result describes accepted service intent only.

The restoration branch does not call admission or quota checking again in the inspected method. A stored desired spec that was accepted earlier can therefore be restored through a different path from ordinary ApplyService. This matters if policy or quota changed since the original acceptance. Describe the exception openly instead of promising every state restoration reruns current acceptance rules.

| Operation | Current behavior | Boundary |
| --- | --- | --- |
| Ordinary source apply | Shared parser and service mutation | Admission on that path |
| Status with warn | Detects difference and retains live spec | Observation does not repair |
| Status with auto_revert | Restores stored desired spec and reconciles | Mutating status; no fresh Admit call there |
| Container manually changed | Separate agent/runtime drift question | Spec equality is not physical equivalence |

A manual rollback or emergency scale can conflict with auto_revert. If an operator changes live state and another process reads status, the status call can restore the old desired spec. Operational procedures should specify which source/policy is authoritative during intervention. A UI labeled read-only status should not obscure this behavior. A future design can separate detection from repair and require checked repair operations, but that is not the baseline method.

The failure window is between storing desired intent and later restoring it under changed constraints. A focused teaching test could tighten quota after scaling down, then ask status to restore a larger stored desired count. It should record whether current checks are re-run, not silently alter the baseline. This exposes an integration question that happy-path equality tests cannot answer.

## Prune Only What This Source Owns

The current prune loop constructs wanted names from the new manifest set and previous names from source.ManagedServices. It lists services in the source namespace and deletes a service when its name was previously managed and is no longer wanted. It preserves unrelated names. That is the exact implemented predicate; it does not compare the current service's ID or GitOps.SourceID before deletion. [Claim ch30.prune](../../validation/evidence/ch30.json).

The lab's unrelated service is intentionally never in the prior managed-name set. Removing atlas.yaml in a new real commit makes Atlas deleted, while unrelated stays active. This passed. It establishes the tested name-set boundary, not an unconditional guarantee that every currently unrelated object is immune to prune.

Consider replacement or ownership transfer under a previously managed name. Another source can mark the same service managed, or an operator can create a replacement after old state is removed under a different lifecycle. If its name still belongs to the first source's stale ManagedServices, that source's prune predicate does not independently check the new ownership marker. Names alone are weaker than stable object/source identity.

A safer teaching design would require namespace, current object ID and current source ownership to agree before deleting, with a conflict outcome when they do not. It would also define explicit transfer semantics and update managed inventories atomically enough for its intended guarantee. That guard is a proposal here, not a silent patch to the immutable controller. The real fixture deliberately avoids ownership replacement and does not claim to have tested that stronger predicate.

Prune also changes desired service lifecycle rather than directly sweeping daemon resources. Agent cleanup follows its own task ownership rules. A source removal should not trigger broad Docker container or volume pruning. For stateful workloads, data retention must be an explicit decision independent of whether a manifest disappeared. Chapter 32 examines why workload deletion and persistent data deletion are different operations.

Development history spans two batches. [f2836eabfff8e442d38984433f3e1f5c642667d1](https://github.com/alekpopovic/orch/commit/f2836eabfff8e442d38984433f3e1f5c642667d1) introduces the GitOps source/checkout path with other work. [4d641bbe8913da568d6d9f4697a0144314e10b87](https://github.com/alekpopovic/orch/commit/4d641bbe8913da568d6d9f4697a0144314e10b87) adds later drift behavior. These actual changes are more precise than attributing every capability to the original GitOps prompt alone.

For the safe Atlas lab, copy examples/teaching-extensions/ch30/main.go into book-gitops inside the disposable source module. Use the pinned Go toolchain and Git; no database, Docker daemon, server listener or external account is required. The fixture owns its temporary manifest repository and lets CommandFetcher own each temporary checkout.

```sh
go run ./book-gitops
go test ./internal/gitops ./internal/controlplane \
  -run 'TestControllerSyncsLocalFixtureRepositoryAndPrunes|TestSourceRejectsPlaintextCredentials|TestGitOpsManualChangesCreateDriftAndAutoRevert' \
  -count=1 -v
```

Predict both policy outcomes and the preserved unrelated name before execution. Success requires real full commit IDs, warn retaining two replicas, auto_revert restoring zero, Atlas deleted after the removal commit and unrelated active. The recorded teaching run passed those assertions. Cleanup removes only the fixture's exact temporary repository; checkout Cleanup handles its own directory. No external repository is modified.

## Exercises

1. Why must a lab retain both the Orch source SHA and the manifest repository's checked-out commit?
2. The second sorted manifest fails parsing after the first applied. What can LastError and LastRevision tell you, and what must be inspected separately?
3. Explain why GitOpsStatus under auto_revert is not a passive observation and why its acceptance path differs from ApplyService.
4. Design an ownership-transfer prune test. Which extra predicate is absent from the baseline, and what does the passing unrelated-name fixture actually prove?

[Worked answers](../solutions/ch30.md) keep provenance, drift and deletion scope distinct. Traceable Git intent is valuable when partial apply, mutating status and name-based pruning remain visible rather than being hidden under a blanket GitOps reliability claim.
