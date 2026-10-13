# Appendix C - Commit Atlas and Original Prompt Crosswalk

History is useful when it explains how a mechanism changed and what remained unresolved. It becomes misleading when a prompt title, a tracker mark or a release heading is substituted for executable evidence. This atlas keeps implementation, documentation and the original authoring requests separate while making their connections inspectable.

The pinned repository has **105 reachable commits and 91 original numbered prompts**. These counts were independently verified from a separate read-only bare Git clone, against the locked full SHA and tree object. Reachable means every ancestor, including merged side parents; the narrower first-parent count is not an interchangeable total. The book’s own 000–099 workflow is a different prompt sequence and is not included in the original 00–90 inventory.

The companion history contains every full commit SHA exactly once, its parents, authored and committed timestamps, subject, changed paths and immutable link. Every original prompt appears once with its complete filename, pinned blob URL, earliest containing addition commit, historical blob object ID and thematic chapter destinations. No author email addresses are copied into this reference.

## Reading the crosswalk honestly

Original prompt files entered the repository in two containing commits: [9f94bdad8bcf9f5bb819ec0b711440467a15da9b](https://github.com/alekpopovic/orch/commit/9f94bdad8bcf9f5bb819ec0b711440467a15da9b), which introduced thirty files, and [f0c526fafac58e7921e32ac314f594f7fe14b8b3](https://github.com/alekpopovic/orch/commit/f0c526fafac58e7921e32ac314f594f7fe14b8b3), which introduced sixty-one. First-containing means a Git addition was found and its blob presence checked; it does not mean the requested feature was first implemented then. In particular, June implementation can predate July prompt publication.

The crosswalk uses four evidence grades. A direct textual match requires explicit text connecting the records; it is not awarded merely because a title resembles another title. Strong path/diff correspondence means the associated implementation changed the named mechanism and the historical path exists. Partial relationship covers design/request material whose full executable delivery is not established. Unresolved records retain a specific missing evidence question instead of silently becoming support. The current mappings use strong correspondence or partial relationships; none is promoted to a literal execution transcript.

Associations can be many-to-one or one-to-many. The late quota/GitOps, jobs/storage and operations batches deliberately serve several prompts. Earlier docs and later corrections remain their own history entries even when they do not map neatly to an implementation request. Timestamps provide sequence context, not proof of the author’s private intent.

## Twelve checkpoints

Each excerpt below was retrieved from the named historical Git blob, with its exact bytes, line interval and checksum recorded. Short fragments illustrate the interface at that time; they are not complete replacement listings. Paths refer to that commit even when later code reorganized them.

### 1. Bootstrap: an executable shell

The scaffold introduced Go entrypoints, configuration validation and HTTP listener construction. Read the initial server run function before inspecting later controllers: its existence establishes a process skeleton, not the complete architecture promised in conventions. Later API construction selected an in-memory implementation. The enduring question is which constructor actually owns desired state.

Historical excerpt: [cmd/orch-server/main.go at 72f27ed1d81b](https://github.com/alekpopovic/orch/blob/72f27ed1d81b75e499ee65e0c9779e44b237f814/cmd/orch-server/main.go#L30-L35).

```go
func run(ctx context.Context, logger *slog.Logger, cfg config.ServerConfig) error {
	if err := cfg.Validate(); err != nil {
		return err
	}

	server := &http.Server{
```

### 2. Domain contracts: names become obligations

ServiceSpec collected typed workload inputs rather than leaving deployment intent as an unstructured map. Validation tests made malformed names, images and resources reviewable. Later versions expanded namespace, policy, security and workload fields. A field appearing in a struct is the beginning of its support trace; only its eventual runtime consumer establishes an end-to-end feature.

Historical excerpt: [pkg/types/types.go at c756f9d7f3a4](https://github.com/alekpopovic/orch/blob/c756f9d7f3a46e8bfe4d7bca291d67f6a783553d/pkg/types/types.go#L80-L85).

```go
type ServiceSpec struct {
	Name                 string                `json:"name"`
	Image                string                `json:"image"`
	Replicas             int                   `json:"replicas"`
	Env                  map[string]string     `json:"env,omitempty"`
	SecretRefs           []SecretRef           `json:"secret_refs,omitempty"`
```

### 3. PostgreSQL: a real package with a composition gap

The persistence commit added pgx-backed operations and integration tests. Its historical constructor accepts a pool explicitly, showing what a caller must supply. Subsequent migrations added optimistic concurrency, operational fields and attachment records. The default server never adopted this store as its live state owner; successful database package experiments therefore retain a narrower scope than a durable cluster.

Historical excerpt: [internal/store/postgres.go at 7eba6544ffe2](https://github.com/alekpopovic/orch/blob/7eba6544ffe2eba41b81faa811e899faf28b77a2/internal/store/postgres.go#L20-L25).

```go
func NewPostgresStore(pool *pgxpool.Pool) *PostgresStore {
	return &PostgresStore{pool: pool}
}

func ConnectPostgres(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	pool, err := pgxpool.New(ctx, databaseURL)
```

### 4. Agents: processes acquire an identity

Registration and heartbeat gave a worker a control-plane relationship and introduced a runner loop. Later issued credentials replaced using bootstrap authority for every control-plane call. Local task reconciliation, label ownership and drift cleanup refined execution safety. An enrollment mechanism can authenticate a worker without fencing a partitioned predecessor or protecting its Docker socket from local compromise.

Historical excerpt: [internal/agent/agent.go at 5cf921384916](https://github.com/alekpopovic/orch/blob/5cf9213849164ce1bebc4e042cc37bf5553c2427/internal/agent/agent.go#L46-L51).

```go
func (r *Runner) Run(ctx context.Context) error {
	if err := r.cfg.Validate(); err != nil {
		return err
	}
	if r.client == nil {
		client, err := NewHTTPClient(r.cfg.ServerURL, r.cfg.BootstrapToken)
```

### 5. Scheduler: planning meets persistence

RunOnce introduced a repeatable placement seam and tests around selection. Later property checks, resource accounting, public-port reservations and atomic claims expanded the contract. Follow both planning and write paths: ordinary MemoryService immediate placement still bypasses richer scheduler Plan constraints. A scheduler package’s correct algorithm does not imply every creation path passes through it.

Historical excerpt: [internal/scheduler/scheduler.go at fce0a657651c](https://github.com/alekpopovic/orch/blob/fce0a657651c00ffb697bf4a4aba12d0b171f463/internal/scheduler/scheduler.go#L45-L50).

```go
func (s *Scheduler) RunOnce(ctx context.Context) ([]Assignment, error) {
	if s.store == nil {
		return nil, fmt.Errorf("scheduler store is required")
	}
	if err := ctx.Err(); err != nil {
		return nil, err
```

### 6. Reconciliation: desired state becomes repeated work

The historical reconciler exposes ReconcileOnce and a store contract, making retryable convergence inspectable. Deletion and health refinements later changed which tasks count as active and when replacement is allowed. This package can reason about restarting from stored intent when explicitly wired to a durable store. The shipped memory binary instead uses its own integrated bookkeeping and loses live intent on process restart.

Historical excerpt: [internal/reconciler/reconciler.go at 208eb99758a5](https://github.com/alekpopovic/orch/blob/208eb99758a5dac15a3e083fce3fc3e0dcfdd2e3/internal/reconciler/reconciler.go#L121-L126).

```go
func (r *Reconciler) ReconcileOnce(ctx context.Context) error {
	if r.store == nil {
		return fmt.Errorf("reconciler store is required")
	}
	if err := ctx.Err(); err != nil {
		return err
```

### 7. Rollout: availability becomes a budget

The rollout controller added repeated deployment processing rather than treating an image update as a single synchronous mutation. Tests exercise surge and replacement sequencing; later rollback and operation-lock changes preserve terminal history and reject incompatible overlaps. Current old-task availability permits running or healthy, while new-version success specifically counts healthy. Read those predicates rather than translating every “running” observation into rollout success.

Historical excerpt: [internal/rollout/rollout.go at de5900bced92](https://github.com/alekpopovic/orch/blob/de5900bced92ad9d5786cd258ff7941d67369d33/internal/rollout/rollout.go#L59-L64).

```go
func (c *Controller) RunOnce(ctx context.Context) error {
	if c.store == nil {
		return fmt.Errorf("rollout store is required")
	}
	deployments, err := c.activeDeployments(ctx)
	if err != nil {
```

### 8. Node trust: credentials have a lifecycle

The issued-agent credential constructor defaults its TTL to fifteen minutes, then stores token hashes and validates expiry. Heartbeat rotation and revocation tests refine trust beyond the original bootstrap exchange. A rotation response can be lost after the server replaces its stored hash, leaving a worker with an obsolete credential. This is an engineering failure window, not evidence that enrollment is permanently reliable.

Historical excerpt: [internal/auth/agent.go at 4f25e78c229b](https://github.com/alekpopovic/orch/blob/4f25e78c229ba040c07a84801490485b5a0cbb2e/internal/auth/agent.go#L36-L41).

```go
func NewTokenAgentCredentialIssuer(ttl time.Duration) *TokenAgentCredentialIssuer {
	if ttl <= 0 {
		ttl = 15 * time.Minute
	}
	return &TokenAgentCredentialIssuer{ttl: func() time.Duration { return ttl }}
}
```

### 9. Namespaces, quotas and GitOps: a shared change batch

The quota/image/GitOps batch implements several thematic prompts together. GitOps receives a store and parser, checks a source out and applies bounded manifests; quota accounting operates within namespace mutation paths. Presenting that commit as one prompt’s exclusive result would erase the batch. Later job and operational surfaces require separate authorization checks, and digest syntax validation still does not resolve a registry’s remote digest.

Historical excerpt: [internal/gitops/gitops.go at f2836eabfff8](https://github.com/alekpopovic/orch/blob/f2836eabfff8e442d38984433f3e1f5c642667d1/internal/gitops/gitops.go#L182-L187).

```go
func (controller *Controller) Sync(ctx context.Context, id string) (types.GitOpsSource, error) {
	source, err := controller.store.GetGitOpsSource(ctx, id)
	if err != nil {
		return types.GitOpsSource{}, err
	}
	if err := ValidateSource(source); err != nil {
```

### 10. Finite and scheduled work: task semantics get another owner

The jobs/storage/DNS/notification batch adds CreateJob validation and task-derived bookkeeping. Cron selection, concurrency policy and occurrence records then coordinate finite work rather than ordinary service replicas. Job command/env/security fields require tracing to the agent; the Task-only dispatch path does not automatically consume every JobSpec field. Local volumes and DNS do not create replicated storage or an overlay network.

Historical excerpt: [internal/controlplane/workloads.go at 4d641bbe8913](https://github.com/alekpopovic/orch/blob/4d641bbe8913da568d6d9f4697a0144314e10b87/internal/controlplane/workloads.go#L114-L119).

```go
func (s *MemoryService) CreateJob(ctx context.Context, spec types.JobSpec) (types.Job, error) {
	if err := spec.Validate(); err != nil {
		return types.Job{}, fmt.Errorf("%w: %v", store.ErrInvalidState, err)
	}
	req, err := spec.ResourceRequirements.WithDefaults(types.DefaultResourceDefaults())
	if err != nil {
```

### 11. Operational hardening: useful controls, bounded evidence

The operations batch combines maintenance validation, retention, usage, migrations and release work. These controls add reviewable restriction and reporting surfaces, but their presence does not upgrade MemoryService into durable orchestration. The final schema includes sixteen migrations; the original test fixture applies only fourteen and misses agent_version introduced by migration sixteen. Separate full-schema teaching evidence repairs the fixture path without editing the historical application.

Historical excerpt: [internal/maintenance/maintenance.go at 7985b9ebe276](https://github.com/alekpopovic/orch/blob/7985b9ebe276f8447e1b8abfceb0d6b746ea6f2d/internal/maintenance/maintenance.go#L17-L22).

```go
func Validate(window types.MaintenanceWindow) error {
	if window.Name == "" {
		return fmt.Errorf("name is required")
	}
	if _, err := cronjobs.Parse(window.Schedule); err != nil {
		return err
```

### 12. Release and site packaging: descriptions remain claims to check

The locked final documentation commit links installation, CLI, API, deployment and security guides from a reader-facing project page. Formatting fixes and release metadata are legitimate history entries, as are dependency merges and tracker edits. They are not noise to remove from the 105-commit count. Publication polish improves navigation; it cannot establish that the default executable runs HA, autoscaling or a durable database-backed control plane.

Historical excerpt: [README.md at cbfc94ade5b5](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/README.md#L19-L24).

```html
  <a href="https://alekpopovic.github.io/orch/#INSTALLATION.md">⬇️ Install</a> ·
  <a href="https://alekpopovic.github.io/orch/#CLI.md">🖥️ CLI</a> ·
  <a href="https://alekpopovic.github.io/orch/#GITHUB_PAGES.md">📚 Docs</a> ·
  <a href="https://alekpopovic.github.io/orch/#API.md">🔌 API</a> ·
  <a href="https://alekpopovic.github.io/orch/#PRODUCTION_DEPLOYMENT.md">🚢 Deploy</a> ·
  <a href="https://alekpopovic.github.io/orch/#SECURITY.md">🛡️ Security</a> ·
```

## Surviving tensions and unresolved evidence

The original instructions are ambitious about persistence, HA, autoscaling and production operations. The current call path provides a more precise classification: PostgreSQL and leader election are implemented packages, autoscaling is an unwired package, several networking/storage improvements remain design work, and the default server constructs MemoryService. These are not interchangeable degrees of production readiness. Inspect the final composition after studying an earlier diff so a historical feature addition does not become a present-day wiring claim.

Nine design-oriented prompt associations retain partial grades: 54, 56, 63, 68, 69, 72, 75, 77 and 79. Their missing evidence is explicit: a design file and related path changes do not demonstrate the entire requested architecture running. Execution transcripts establishing exactly which prompt was sent, in which environment and with which results are absent for the wider historical mapping as well. The atlas preserves that causality uncertainty even when a mechanism clearly exists today.

Developers should start with the domain, scheduler and reconciler checkpoints, then compare interface seams and the tests that constrain updates. DevOps engineers should follow agents, rollout and operational hardening, asking which observed states survive a process boundary and which cleanup actions reach a worker. Architects should compare PostgreSQL, shared late batches and final composition, asking where an intended consistency property has an actual enforcing caller.

A useful diff study ends with a falsifiable question: which new path changed behavior, which test exercises it, and what input or failure still falls outside that scope? That method preserves both the value of the project’s history and the limits of what history alone can establish.
