// Book-only actual local Git, CLI parsers, injected reports/clock. No Docker/network server.
package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/alekpopovic/orch/internal/cli"
	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/internal/cronjobs"
	"github.com/alekpopovic/orch/internal/gitops"
	"github.com/alekpopovic/orch/internal/namespace"
	"github.com/alekpopovic/orch/pkg/types"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type Case struct {
	ID       string `json:"id"`
	Expected any    `json:"expected"`
	Observed any    `json:"observed"`
	Passed   bool   `json:"passed"`
}

var cases []Case

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func ck(id string, expected, observed any, pass bool) {
	cases = append(cases, Case{id, expected, observed, pass})
	if !pass {
		panic(fmt.Sprintf("case%s expected%v observed%v", id, expected, observed))
	}
}
func git(dir string, args ...string) string {
	command := exec.Command("git", append([]string{"-C", dir, "-c", "core.hooksPath=/dev/null", "-c", "user.name=Inside Orch Fixture", "-c", "user.email=book-fixture@example.test"}, args...)...)
	raw, err := command.CombinedOutput()
	if err != nil {
		panic(fmt.Sprintf("git%v:%v:%s", args, err, raw))
	}
	return strings.TrimSpace(string(raw))
}
func commit(dir, message string) string {
	git(dir, "add", "-A")
	git(dir, "commit", "-m", message)
	return git(dir, "rev-parse", "HEAD")
}

type failingFetcher struct{}

func (failingFetcher) Checkout(context.Context, types.GitOpsSource) (gitops.Checkout, error) {
	return gitops.Checkout{}, errors.New("book injected fetch unavailable; no remote request")
}

type clock struct{ now time.Time }

func (c *clock) Now() time.Time { return c.now }

type cronStore struct {
	item      types.CronJob
	jobs      []types.Job
	deleted   []string
	createdAt []string
}

func (f *cronStore) ListCronJobs(context.Context) ([]types.CronJob, error) {
	return []types.CronJob{f.item}, nil
}
func (f *cronStore) UpdateCronJob(_ context.Context, v types.CronJob) (types.CronJob, error) {
	f.item = v
	return v, nil
}
func (f *cronStore) CreateJob(_ context.Context, s types.JobSpec) (types.Job, error) {
	j := types.Job{ID: s.Name, Namespace: f.item.Namespace, Spec: s, Status: types.JobPending}
	f.jobs = append(f.jobs, j)
	f.createdAt = append(f.createdAt, s.Name)
	return j, nil
}
func (f *cronStore) ListJobs(context.Context) ([]types.Job, error) {
	return append([]types.Job(nil), f.jobs...), nil
}
func (f *cronStore) DeleteJob(_ context.Context, id string) error {
	f.deleted = append(f.deleted, id)
	for i, j := range f.jobs {
		if j.ID == id {
			f.jobs = append(f.jobs[:i], f.jobs[i+1:]...)
			break
		}
	}
	return nil
}
func fixtureCron(base time.Time, policy types.ConcurrencyPolicy) *cronStore {
	return &cronStore{item: types.CronJob{ID: "deterministic-cron-input", Namespace: "book-workloads", CreatedAt: base, Spec: types.CronJobSpec{Name: "atlas-minute", Schedule: "* * * * *", Timezone: "UTC", ConcurrencyPolicy: policy, MissedScheduleLimit: 2, JobTemplate: types.JobSpec{Name: "atlas-minute", Image: "busybox:1.36"}}}}
}

type captureClient struct {
	cli.Client
	cp      *controlplane.MemoryService
	ctx     context.Context
	lastJob types.Job
	cron    types.CronJob
	logTask string
}

func (c *captureClient) CreateJob(_ context.Context, s types.JobSpec) (types.Job, error) {
	v, err := c.cp.CreateJob(c.ctx, s)
	c.lastJob = v
	return v, err
}
func (c *captureClient) GetJob(_ context.Context, id string) (types.Job, error) {
	return c.cp.GetJob(c.ctx, id)
}
func (c *captureClient) ListJobs(context.Context) ([]types.Job, error) { return c.cp.ListJobs(c.ctx) }
func (c *captureClient) DeleteJob(_ context.Context, id string) error {
	return c.cp.DeleteJob(c.ctx, id)
}
func (c *captureClient) CreateCronJob(_ context.Context, s types.CronJobSpec) (types.CronJob, error) {
	v, err := c.cp.CreateCronJob(c.ctx, s)
	c.cron = v
	return v, err
}
func (c *captureClient) ListCronJobs(context.Context) ([]types.CronJob, error) {
	return c.cp.ListCronJobs(c.ctx)
}
func (c *captureClient) SetCronJobSuspended(_ context.Context, id string, b bool) (types.CronJob, error) {
	return c.cp.SetCronJobSuspended(c.ctx, id, b)
}
func (c *captureClient) StreamLogs(_ context.Context, _ string, task string, _ bool, _ string, out io.Writer) error {
	c.logTask = task
	_, err := fmt.Fprintln(out, "book fake log transport; no application logs")
	return err
}
func command(c *captureClient, args ...string) {
	root := cli.NewRootCommand(cli.Options{Out: io.Discard, Err: io.Discard, DefaultConfig: "/dev/null", NewClient: func(string) (cli.Client, error) { return c, nil }})
	root.SetArgs(append([]string{"--server", "http://127.0.0.1:1"}, args...))
	must(root.ExecuteContext(context.Background()))
}
func main() {
	if len(os.Args) != 2 {
		panic("pass canonical fixture directory")
	}
	fixtures, err := filepath.Abs(os.Args[1])
	must(err)
	ctx := context.Background()
	cp := controlplane.NewMemoryService()
	_, err = cp.CreateNamespace(ctx, "book-workloads")
	must(err)
	ns := namespace.WithContext(ctx, "book-workloads")
	dir, err := os.MkdirTemp("", "inside-orch-lab07-")
	must(err)
	defer os.RemoveAll(dir)
	git(dir, "init", "-b", "main")
	must(os.Mkdir(filepath.Join(dir, "manifests"), 0700))
	for _, name := range []string{"10-api.yaml", "20-worker.yaml"} {
		raw, err := os.ReadFile(filepath.Join(fixtures, name))
		must(err)
		_, err = cli.ParseDeploy(raw)
		must(err)
		must(os.WriteFile(filepath.Join(dir, "manifests", name), raw, 0600))
	}
	first := commit(dir, "add two Atlas manifests")
	unrelated, err := cp.CreateService(ns, types.ServiceSpec{Name: "manual-unrelated", Image: "nginx:1.27", Replicas: 0})
	must(err)
	source, err := cp.CreateGitOpsSource(ns, types.GitOpsSource{RepositoryURL: dir, Branch: "main", Path: "manifests", SyncInterval: time.Minute, Prune: true, DriftPolicy: types.GitOpsWarnOnly})
	must(err)
	controller := gitops.NewController(cp, nil, cli.ParseDeploy, nil)
	synced, err := controller.Sync(ns, source.ID)
	must(err)
	ck("git-real-revision", first, synced.LastRevision, first == synced.LastRevision && len(first) == 40)
	ck("git-managed-names-lexical", []string{"atlas-api", "atlas-worker"}, synced.ManagedServices, len(synced.ManagedServices) == 2 && synced.ManagedServices[0] == "atlas-api" && synced.ManagedServices[1] == "atlas-worker")
	services, err := cp.ListServices(ns)
	must(err)
	var atlas, worker types.Service
	for _, s := range services {
		if s.Spec.Name == "atlas-api" {
			atlas = s
		}
		if s.Spec.Name == "atlas-worker" {
			worker = s
		}
	}
	version := atlas.DeploymentVersion
	_, err = controller.Sync(ns, source.ID)
	must(err)
	unchanged, err := cp.GetService(ns, atlas.ID)
	must(err)
	ck("unchanged-sync-no-new-version", version, unchanged.DeploymentVersion, version == unchanged.DeploymentVersion)
	_, err = cp.ScaleService(ns, atlas.ID, 2)
	must(err)
	states, err := cp.GitOpsStatus(ns)
	must(err)
	var drift types.Service
	for _, v := range states {
		if v.ID == atlas.ID {
			drift = v
		}
	}
	ck("warn-manual-scale", map[string]any{"replicas": 2, "state": "drifted"}, map[string]any{"replicas": drift.Spec.Replicas, "state": drift.GitOps.Status}, drift.Spec.Replicas == 2 && drift.GitOps.Status == types.GitOpsDrifted)
	state := *drift.GitOps
	state.Policy = types.GitOpsAutoRevert
	_, err = cp.MarkGitOpsManaged(ns, atlas.ID, state)
	must(err)
	_, err = cp.ScaleService(ns, atlas.ID, 3)
	must(err)
	_, err = cp.GitOpsStatus(ns)
	must(err)
	reverted, err := cp.GetService(ns, atlas.ID)
	must(err)
	ck("auto-revert-on-status", 0, reverted.Spec.Replicas, reverted.Spec.Replicas == 0)
	_, err = gitops.NewController(cp, failingFetcher{}, cli.ParseDeploy, nil).Sync(ns, source.ID)
	ck("failed-fetch-preserves-services", "fetch failure and active known objects", fmt.Sprint(err), err != nil)
	alive, err := cp.GetService(ns, worker.ID)
	must(err)
	manual, err := cp.GetService(ns, unrelated.ID)
	must(err)
	ck("failed-fetch-no-prune", true, []types.ServiceStatus{alive.Status, manual.Status}, alive.Status == types.ServiceActive && manual.Status == types.ServiceActive)
	apiFile := filepath.Join(dir, "manifests", "10-api.yaml")
	raw, err := os.ReadFile(apiFile)
	must(err)
	must(os.WriteFile(apiFile, []byte(strings.Replace(string(raw), "replicas: 0", "replicas: 1", 1)), 0600))
	must(os.WriteFile(filepath.Join(dir, "manifests", "20-worker.yaml"), []byte("name: atlas-worker\nimage: nginx:1.27\nunknown_field: rejected\n"), 0600))
	invalid := commit(dir, "valid first file then invalid second")
	_, err = controller.Sync(ns, source.ID)
	if err == nil {
		panic("invalid manifest accepted")
	}
	partial, err := cp.GetService(ns, atlas.ID)
	must(err)
	alive, err = cp.GetService(ns, worker.ID)
	must(err)
	failedSource, err := cp.GetGitOpsSource(ns, source.ID)
	must(err)
	ck("partial-apply-not-atomic", map[string]any{"first_replicas": 1, "previous_worker_active": true, "last_revision": first}, map[string]any{"first_replicas": partial.Spec.Replicas, "worker_status": alive.Status, "last_revision": failedSource.LastRevision, "failed_checkout_commit": invalid}, partial.Spec.Replicas == 1 && alive.Status == types.ServiceActive && failedSource.LastRevision == first)
	must(os.Remove(filepath.Join(dir, "manifests", "20-worker.yaml")))
	final := commit(dir, "remove managed worker; retain Atlas API")
	synced, err = controller.Sync(ns, source.ID)
	must(err)
	removed, err := cp.GetService(ns, worker.ID)
	must(err)
	manual, err = cp.GetService(ns, unrelated.ID)
	must(err)
	ck("prune-preserves-unrelated", map[string]any{"worker": "deleted", "manual": "active"}, map[string]any{"worker": removed.Status, "manual": manual.Status}, removed.Status == types.ServiceDeleted && manual.Status == types.ServiceActive)
	for _, url := range []string{"https://robot:synthetic-private-value@example.test/repo.git", "https://example.test/repo.git?token=synthetic-private-value"} {
		err := gitops.ValidateSource(types.GitOpsSource{RepositoryURL: url, Branch: "main", Path: ".", SyncInterval: time.Minute})
		ck("url-credentials-rejected-"+fmt.Sprint(len(cases)), true, fmt.Sprint(err), err != nil && !strings.Contains(err.Error(), "synthetic-private-value"))
	}
	client := &captureClient{cp: cp, ctx: ns}
	command(client, "job", "run", filepath.Join(fixtures, "job-success.yaml"))
	success := client.lastJob
	ck("job-cli-success-manifest", map[string]any{"cpu": 100, "memory": 1 << 20, "command": true}, success.Spec, success.Spec.ResourceRequirements.Requests.CPU == 100 && success.Spec.ResourceRequirements.Requests.Memory == 1<<20 && len(success.Spec.Command) > 0)
	node, err := cp.RegisterNode(ctx, controlplane.NodeRegistration{Name: "book-job-node", AdvertiseAddress: "http://fixture-not-connected", Capacity: types.Resources{CPU: 4000, Memory: 1 << 30}, Allocatable: types.Resources{CPU: 4000, Memory: 1 << 30}})
	must(err)
	execute := func(job types.Job, status types.TaskStatus, exit int) types.Job {
		task, err := cp.GetTask(ns, job.TaskIDs[len(job.TaskIDs)-1])
		must(err)
		task, err = cp.AssignTask(ns, task.ID, node.Node.ID, nil, task.UpdatedAt)
		must(err)
		_, err = cp.ReportTaskStatus(ns, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: node.Node.ID, Status: types.TaskRunning, ContainerID: "injected-no-Docker"})
		must(err)
		_, err = cp.ReportTaskStatus(ns, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: node.Node.ID, Status: status, ExitCode: &exit, ContainerID: "injected-no-Docker"})
		must(err)
		updated, err := cp.GetJob(ns, job.ID)
		must(err)
		return updated
	}
	success = execute(success, types.TaskStopped, 0)
	ck("job-exit-zero", types.JobSucceeded, success.Status, success.Status == types.JobSucceeded)
	command(client, "job", "run", filepath.Join(fixtures, "job-failure.yaml"))
	failure := execute(client.lastJob, types.TaskFailed, 1)
	ck("job-nonzero-retry", map[string]any{"attempts": 2, "status": "pending"}, failure, failure.Attempts == 2 && len(failure.TaskIDs) == 2 && failure.Status == types.JobPending)
	latest := failure.TaskIDs[1]
	command(client, "job", "logs", failure.ID)
	ck("latest-attempt-log-selection", latest, client.logTask, client.logTask == string(latest))
	failure = execute(failure, types.TaskFailed, 1)
	ck("job-limit-terminal", map[string]any{"attempts": 2, "status": "failed"}, failure, failure.Attempts == 2 && failure.Status == types.JobFailed)
	command(client, "cronjob", "apply", filepath.Join(fixtures, "cron.yaml"))
	ck("cron-cli-manifest", map[string]any{"timezone": "Europe/Belgrade", "cpu": 100, "memory": 1 << 20, "policy": "Forbid"}, client.cron.Spec, client.cron.Spec.Timezone == "Europe/Belgrade" && client.cron.Spec.JobTemplate.ResourceRequirements.Requests.Memory == 1<<20 && client.cron.Spec.ConcurrencyPolicy == types.ConcurrencyForbid)
	base := time.Date(2026, 8, 21, 12, 0, 0, 0, time.UTC)
	clk := &clock{base.Add(3 * time.Minute)}
	allow := fixtureCron(base, types.ConcurrencyAllow)
	must(cronjobs.New(allow, clk).RunOnce(ctx))
	ck("cron-allow-missed-bound", 2, len(allow.jobs), len(allow.jobs) == 2 && allow.item.LastScheduleAt.Equal(base.Add(2*time.Minute)))
	forbid := fixtureCron(base, types.ConcurrencyForbid)
	forbid.jobs = []types.Job{{ID: "active-fixed-fixture", Status: types.JobRunning}}
	forbid.item.ActiveJobIDs = []string{"active-fixed-fixture"}
	must(cronjobs.New(forbid, clk).RunOnce(ctx))
	ck("cron-forbid-active", 1, len(forbid.jobs), len(forbid.jobs) == 1 && forbid.item.LastScheduleAt.IsZero())
	replace := fixtureCron(base, types.ConcurrencyReplace)
	replace.jobs = []types.Job{{ID: "active-fixed-fixture", Status: types.JobRunning}}
	replace.item.ActiveJobIDs = []string{"active-fixed-fixture"}
	must(cronjobs.New(replace, &clock{base.Add(time.Minute)}).RunOnce(ctx))
	ck("cron-replace-active", []string{"active-fixed-fixture"}, replace.deleted, len(replace.deleted) == 1 && len(replace.jobs) == 1 && replace.jobs[0].ID != "active-fixed-fixture")
	suspend := fixtureCron(base, types.ConcurrencyAllow)
	suspend.item.Spec.Suspended = true
	must(cronjobs.New(suspend, clk).RunOnce(ctx))
	ck("cron-suspend", 0, len(suspend.jobs), len(suspend.jobs) == 0)
	suspend.item.Spec.Suspended = false
	must(cronjobs.New(suspend, clk).RunOnce(ctx))
	ck("cron-resume-catches-backlog", 2, len(suspend.jobs), len(suspend.jobs) == 2)
	loc, err := time.LoadLocation("Europe/Belgrade")
	must(err)
	daily, err := cronjobs.Parse("30 2 * * *")
	must(err)
	springBase := time.Date(2026, 3, 28, 23, 0, 0, 0, time.UTC)
	spring := daily.Next(springBase.In(loc))
	springExpected := time.Date(2026, 3, 30, 0, 30, 0, 0, time.UTC)
	ck("dst-spring-missing-local-0230", springExpected, spring.UTC(), spring.Equal(springExpected))
	fallBase := time.Date(2026, 10, 25, 0, 0, 0, 0, time.UTC)
	fall := daily.Between(fallBase.In(loc), fallBase.Add(2*time.Hour).In(loc), 10)
	ck("dst-fall-repeated-local-0230", []time.Time{fallBase.Add(30 * time.Minute), fallBase.Add(90 * time.Minute)}, fall, len(fall) == 2 && fall[0].Equal(fallBase.Add(30*time.Minute)) && fall[1].Equal(fallBase.Add(90*time.Minute)))
	sixErr := error(nil)
	_, sixErr = cronjobs.Parse("0 30 2 * * *")
	ck("cron-exact-five-fields", true, fmt.Sprint(sixErr), sixErr != nil)
	for _, job := range []types.Job{success, failure} {
		must(cp.DeleteJob(ns, job.ID))
	}
	_, err = cp.GetJob(ns, failure.ID)
	ck("job-cleanup-metadata", true, fmt.Sprint(err), err != nil)
	if len(cases) < 12 {
		panic("too few cases")
	}
	must(json.NewEncoder(os.Stdout).Encode(map[string]any{"source_sha": "cbfc94ade5b57e449d6b73bf1485b1c5b1647022", "classification": "teaching extension", "namespace": "book-workloads", "source_id": source.ID, "fixture_revisions": []string{first, invalid, final}, "managed_object_set": synced.ManagedServices, "job_attempts": failure.Attempts, "job_statuses": []types.JobStatus{success.Status, failure.Status}, "clock_instants": map[string]any{"catchup_base": base, "catchup_now": clk.now, "spring_base": springBase, "spring_next": spring.UTC(), "fall_base": fallBase, "fall_due": fall}, "case_count": len(cases), "cases": cases, "scope": "real local Git and actual CLI parsers/control-plane methods; injected task reports/fake log transport and clock/store for cron; no containers or connected host", "limitations": []string{"same-name ownership-transfer prune not protected by current predicate", "partial apply and mutating auto-revert acceptance exception", "no timed Job backoff/deadline/parallelism/TTL/HA occurrence transaction", "latest log transport injected, not actual application log capture"}, "cleanup": "exact owned local repository removed; checkouts self-clean; in-memory jobs removed/state discarded"}))
}
