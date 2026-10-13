# Chapter 5 - Service Specifications, Resources, and Ports

Atlas API now needs three replicas rather than one. The deployment author proposes 250 millicores, 128 mebibytes, and the same public port for every replica. Each value looks reasonable in isolation. Together they describe capacity requirements and a possible host conflict that validation alone cannot settle. This chapter follows those fields from YAML into domain values, then checks which downstream paths actually use them.

The distinction matters immediately: a parser can accept a correctly shaped request while a placement path ignores its resource requirements, and a Docker adapter can support limits while its caller omits them. We will calculate the intended budget, reject malformed manifests through the actual CLI parser, and keep admission, scheduling, and runtime enforcement as separate claims.

You will be able to parse CPU and memory units, calculate replica budgets, predict node-scoped host-port conflicts, and identify the boundary between admitted specifications and runtime enforcement.

## From YAML to a Validated Service

The deployment file is a CLI-specific format. Its top-level `resources` mapping contains string CPU and memory quantities; `ports` entries contain `container` and `public`; placement labels are nested under `placement.labels`. These names do not match the domain JSON representation one for one. Inspect [DeployFile and its nested types in the parser](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go#L15-L36) before copying an HTTP payload into YAML.

The parser reads bytes, decodes them with known fields enabled, validates the deployment representation, converts fields to domain types, validates the resulting specification, and applies defaults. [ParseDeploy is the integration point](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/cli/deploy.go#L139-L201). Known-fields decoding means a misspelling such as `replica` is an error rather than an ignored suggestion. This is valuable operator feedback: silently interpreting a typo as zero replicas would be a materially different deployment.

Our valid teaching fixture is stored in `examples/teaching-extensions/ch05/atlas-valid.yaml`. It is original book-side input, not an upstream fixture or a change to the baseline:

```yaml
name: atlas-api
image: nginx:1.27
replicas: 3
ports:
  - container: 80
    public: 0
resources:
  cpu: 250m
  memory: 128Mi
placement:
  labels:
    role: worker
```

The parser maps this into both requests and limits. That equality is a behavior of the CLI deployment conversion, not a universal domain restriction. The domain can represent different requests and limits, provided validation accepts them. A direct HTTP client submitting the domain representation must therefore follow its own field names and validation rules.

The valid fixture is locally admissible. It does not prove a worker with `role=worker` exists, that the registry is reachable, or that three containers will fit on that worker. Those questions belong to later operations. Local validation also cannot check whether a referenced secret exists in the selected namespace or whether its operator may create a service there.

Four sibling fixtures deliberately replace one field. `atlas-invalid-cpu.yaml` uses `bananas`; the memory variant uses `1.5Mi`; the port variant uses container port 70000; the field variant misspells replicas. Their failures are distinct: quantity parsing, integer-suffix memory grammar, bounded port validation, and strict YAML field decoding. The retained actual responses make those distinctions observable instead of calling all invalid input a YAML error.

## CPU and Memory in Exact Units

The internal resource representation uses CPU millicores and memory bytes. For Atlas, 250m is 250 millicores, or one quarter of a CPU. Three replicas request 750 millicores, equivalent to 0.75 CPU. Memory 128Mi equals 128 × 1,048,576 = 134,217,728 bytes per replica. Three replicas total 402,653,184 bytes, or 384Mi. These are arithmetic budgets derived from declarations, not measurements of live utilization.

| Quantity | Per replica | Three replicas |
| --- | --- | --- |
| Requested CPU | 250 millicores | 750 millicores |
| Requested memory | 134,217,728 bytes | 402,653,184 bytes |
| CLI-converted limits | Same values as requests | Same aggregate values |

CPU parsing accepts a positive integer with `m`, or a positive finite decimal number of CPUs which it multiplies by 1,000. Memory parsing accepts positive integers with binary suffixes Ki, Mi, Gi; decimal suffixes K, M, G; or a plain byte count. Thus 128M means 128,000,000 bytes, which is less than 128Mi. Uppercase and lowercase spelling are part of this grammar, not stylistic choices.

The exact CPU implementation is short enough to examine directly:

```go
func ParseCPU(value string) (int64, error) {
	value = strings.TrimSpace(value)
	if value == "" {
		return 0, nil
	}
	if strings.HasSuffix(value, "m") {
		raw := strings.TrimSpace(strings.TrimSuffix(value, "m"))
		parsed, err := strconv.ParseInt(raw, 10, 64)
		if err != nil || parsed <= 0 {
			return 0, fmt.Errorf("invalid CPU value %q", value)
		}
		return parsed, nil
	}
	parsed, err := strconv.ParseFloat(value, 64)
	if err != nil || parsed <= 0 || math.IsNaN(parsed) || math.IsInf(parsed, 0) {
		return 0, fmt.Errorf("invalid CPU value %q", value)
	}
	return int64(parsed * 1000), nil
}
```

Exact source: [pkg/types/types.go:898–916](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L898-L916).

The HTTP resource decoder also distinguishes JSON numbers from strings: numeric CPU is already millicores, while a CPU string such as "1" passes through ParseCPU and means 1,000 millicores. A raw numeric 0 is rejected, whereas an absent field represents omission. Therefore copying a Go zero-valued struct into raw JSON is not equivalent to omitting resource fields.

An empty string returns zero so normalization can supply defaults. Explicit `0m` is rejected rather than interpreted as unspecified. Decimal CPU is converted with a floating-point multiplication followed by an integer conversion. Do not infer arbitrary precision or rounding guarantees from this small parser. Extremely small positive decimals can truncate to zero before defaulting, and arithmetic at extreme integer magnitudes is not comprehensively guarded here. For the lab we use ordinary, unambiguous quantities and retain those boundary questions for a robustness review.

The default resource requirements are 100 millicores and 128Mi for both requests and limits. [WithDefaults substitutes](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/types/types.go#L565-L602) zeros component by component, then applies strict validation. Requests cannot exceed a positive corresponding limit. Distinguish raw nonnegative validation from normalized strictly positive validation: the stages intentionally accept different representations of omission.

Suppose a direct API caller requests 250 millicores but leaves its CPU limit zero. Defaulting the limit to 100 would produce a request above the limit and fail strict validation. The CLI avoids that particular ambiguity by assigning parsed resources to both sides. Knowing where defaults apply prevents a seemingly similar YAML and HTTP example from silently teaching different behavior.

## Labels, Replicas, and Finite Host Ports

Placement labels restrict eligible nodes; they do not increase capacity. Three Atlas replicas constrained to one worker still share that worker's CPU, memory, and network bindings. A request for fixed public TCP port 8088 on every replica asks for the same host binding repeatedly. On one node, that is a conflict even though every individual port is within the allowed range.

Host port accounting is node-scoped and protocol-aware. Another worker may bind the same numeric TCP port on its own host. TCP and UDP with the same number are distinct keys in the scheduler's reservation model. A public port is not a globally unique cluster service address, and changing replica count does not automatically provide a reverse proxy or load balancer.

The scheduler package's [allocatePorts implementation](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/scheduler/scheduler.go#L511-L539) checks explicit ports against existing and newly planned reservations. For dynamic requests it scans the bounded range 30000–32767. Under that planner, two replicas with fixed TCP 8088 cannot both be planned on the same worker. A second eligible worker may allow placement; otherwise a task remains unplaced. Valid syntax and schedulability are different outcomes.

Here is the important active-path qualification. The memory control plane immediately creates assigned tasks using ready-node round robin. It invokes [assignPortsForNodeLocked instead of that planner](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L2552-L2573). The helper allocates a free dynamic port but does not reject an already-reserved explicit port. Therefore the planner's collision tests do not prove the immediate creation path prevents a fixed-port collision. A container creation error may expose the conflict later at Docker.

This is a source-confirmed integration gap recorded as DOC-014 in the contradiction ledger, not permission to improve the upstream implementation inside this book. Do not demonstrate it by binding arbitrary ports on a shared host. The safe teaching input uses public zero, and any experiment with fixed bindings needs disposable hosts, captured ownership, and explicit cleanup.

Even dynamic reservation has a boundary: the orchestrator's in-memory view does not know every unrelated host process. A number free in its task maps could already be occupied outside orch. Runtime creation remains a separate enforcement point. Successful allocation is a statement about the planner's known state, not a kernel reservation held before the Docker operation.

## When Admission Is Not Runtime Enforcement

Resources have a similarly revealing path. They are present in ServiceSpec and are used for admission/accounting. The Docker adapter supports memory bytes and NanoCPUs in HostConfig. Yet the server's AgentTask envelope does not contain resources, and the agent's ContainerSpec construction does not assign them. Follow [the envelope definition](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/controlplane/controlplane.go#L130-L137), [agent creation fields](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/agent/agent.go#L253-L265), and [Docker HostConfig conversion](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/docker/docker.go#L429-L438) together before asserting a live limit.

This gap was observed with real Docker. The guarded record `validation/intake/docker-resource-boundary-corrected.json` retains the exact command and scope. A service requesting limits of 250m and 128Mi reached Docker through the ordinary handler and agent Runner with inspected Memory=0 and NanoCPUs=0. A separate direct adapter call with supplied limits produced Memory=134217728 and NanoCPUs=250000000. The direct result demonstrates adapter capability; it does not repair the service path.

The harness used cached images, exact owned container IDs, and no host workload ports. Containers were removed and cleanup recorded. It was a teaching harness around real upstream components, not the upstream Compose deployment. The initial corrected-attempt history remains available rather than being replaced with a fabricated clean transcript.

Our local parser lab is independently reproducible without Docker. With the disposable baseline's built CLI and Python 3 available, run:

```bash
python3 /home/popac/alekpopovic.github.io/books/inside-orch/examples/teaching-extensions/ch05/check_manifests.py /tmp/inside-orch-labs-cbfc94ade5b5/bin/orch
```

The harness invokes the actual `orch validate` command on each checked-in fixture. It asserts valid input exits zero and each invalid input exits nonzero with its expected category of diagnostic. The record `validation/labs/ch05/parser-manifests.json` passed, with each child command, exit code, stdout, and stderr retained. The harness's success means the rejection assertions passed; it does not mean invalid manifests were accepted.

A useful failure window is between accepted intent and worker container creation. The server can count requests toward quota while the agent has not yet created a container, or while the eventual runtime limits are absent. Operators must therefore compare requested capacity with inspected enforcement rather than assuming accounting is usage or isolation. An admission success does not establish that a noisy replica is constrained.

History helps explain the separate layers. [Resource accounting](https://github.com/alekpopovic/orch/commit/44b60a210c5a17e444b02d622b6af0c1c11375e2), [host-port allocation awareness](https://github.com/alekpopovic/orch/commit/3bfcef82a54dec457cf9d4187705fa70cc7215cf), and [service validation](https://github.com/alekpopovic/orch/commit/6f7954b8d31b52a7909ebe20d1e22b384af19530) changed different packages. Their existence does not make all paths converge automatically. Original prompts 17,34,43 are intent records; current callers and actual observations decide the capability label.

No parser run changes application state. Keep the evidence and fixtures; there is no database or container cleanup for this local lab. The Docker experiment has its own explicit container cleanup evidence and must not be generalized into permission to remove unrelated host resources.

For the Atlas capacity review, retain three columns: declared request, placement decision, and runtime inspection. A declaration gives a reproducible budget; a placement decision names the actual node and its known reservations; inspection shows what Docker received. A disagreement between columns is actionable evidence. Changing a YAML value repeatedly until deployment succeeds obscures the cause, because it mixes parser rejection, scheduler eligibility, host binding, and adapter propagation into one symptom. Reproduce the smallest failing boundary first, then decide whether the implementation or the deployment requirements need a separately reviewed change.

## Exercises

1. Calculate CPU millicores and memory bytes for five replicas requesting 0.4 CPU and 64Mi each. Explain why 64M yields another total.
2. Explain the different rejection points for `cpu: bananas`, `memory: 1.5Mi`, and a misspelled replicas key. Run the fixture harness and identify each actual response.
3. Can two replicas publish TCP 8088 on one worker? Compare the scheduler planner's answer with the immediate memory assignment path.
4. A reviewer sees correct Docker adapter tests and claims Atlas has CPU isolation. Trace the missing fields and state which actual observation would be necessary to support that claim.

See the [worked answers](../solutions/ch05.md).
