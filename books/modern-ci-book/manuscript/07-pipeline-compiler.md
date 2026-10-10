# 7. Compile a pipeline into an immutable graph


## Treat configuration as a small language

A pipeline file is an input language, not a trusted object. Give it a version, a strict schema, and predictable error locations. Reject unknown keys where silently accepting a typo would change execution. Bound file size, nesting, parameter count, and graph expansion. Define the meaning of strings, numbers, and booleans rather than depending on incidental parser coercions.

The following design example illustrates the intended syntax. It is not a file consumed by the included laboratory and is not a Jenkins or GitHub Actions configuration:

```yaml
apiVersion: ci/v1
name: library-check
jobs:
  test:
    pool: linux-build
    toolchain: go-supported
    steps:
      - run: go test ./...
  package:
    needs: [test]
    pool: linux-build
    toolchain: go-supported
    steps:
      - run: go build ./...
```

The toolchain alias is resolved to an allowed immutable image identity when the run is created. The frozen plan records that identity. Changing the alias later must not change an already compiled run.

## Build a bounded DAG

The graph compiler first creates a node table. Each identifier must be unique. It then verifies that every dependency exists, is distinct within its list, and is not the node itself. Finally, it performs cycle detection and emits a deterministic topological order. Sorting equally eligible nodes makes tests and plan hashes stable; execution can still run independent nodes concurrently.

A graph with `test -> package -> deploy` means that successful dependencies enable a later job. It does not imply that files automatically appear on another worker. Declare artifact edges separately. An environment approval may hold a job after all computational dependencies have succeeded.

Conditional behavior needs a small, safe expression model. Do not evaluate arbitrary Go, JavaScript, shell, or template functions while compiling. Begin with explicit comparisons against typed parameters and recorded source metadata. Secrets must not participate in a plan hash through their plaintext values, nor appear in compilation diagnostics.

## Freeze the decision inputs

A run snapshot should include the requested source commit, configuration content digest, compiler version, resolved toolchain identities, parameter values after validation, policy references, and the compiled graph. Store secret references rather than secret values. Record which policy decisions remain live and will be rechecked before execution.

This last distinction matters. The graph is immutable, but a revoked credential or disabled environment cannot be ignored merely because the earlier snapshot was valid. Freeze execution intent while allowing authority to become more restrictive. A policy change that expands authority should not silently add capabilities to a pending run.

A user-facing editor and a freestyle form should compile into the same intermediate representation. The form is a convenient authoring surface, not a second execution engine. Exporting and importing supported configurations should preserve semantics. Unsupported constructs should produce explicit errors instead of being dropped during a visual-editor save.

## Plan before scheduling

Store a failed compilation as a clear validation outcome rather than creating a partially runnable graph. A run cannot begin execution until its plan is committed in full. Hash the normalized plan using a specified encoding; do not hash an unordered map serialization whose output may change between runs.

Matrix expansion belongs before execution too. Calculate the resulting node count before allocating the complete product. A three-dimensional matrix with twenty values per axis has eight thousand combinations. Apply limits before the expansion consumes resources, and require a deliberate policy for failed matrix members and aggregate status.

The laboratory tests the graph invariant and deterministic order. Schema parsing, conditional evaluation, matrix limits, and frozen-plan storage are product work beyond that helper.

## Exercise

A job references `needs: [tests]`, but the defined job is `test`. A proposed convenience feature treats missing dependencies as optional. What operational failure could this cause?

## Worked answer

The package or deployment job could start without the intended tests, producing a success signal for work that never ran. Reject the missing dependency with a location-aware error and do not commit a runnable graph. Optional behavior should have explicit syntax and a documented aggregation rule, not arise from an unresolved name.

## Completion evidence

Compiler tests cover duplicate identifiers, missing dependencies, cycles, self-dependencies, unknown fields, expansion limits, deterministic plans, and policy changes between compilation and dispatch.
