// Teaching extension: real MemoryService, rollout controller and scheduler;
// explicit agent reports replace Docker and application health measurements.
package main

import (
	"context"
	"encoding/csv"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/internal/rollout"
	"github.com/alekpopovic/orch/internal/scheduler"
	"github.com/alekpopovic/orch/internal/store"
	"github.com/alekpopovic/orch/pkg/types"
	"io"
	"log/slog"
	"os"
	"strconv"
	"time"
)

var ctx = context.Background()

func must(e error) {
	if e != nil {
		panic(e)
	}
}
func require(ok bool, why string) {
	if !ok {
		panic(why)
	}
}

type fixture struct {
	cp         *controlplane.MemoryService
	node       types.Node
	service    types.Service
	controller *rollout.Controller
	scheduler  *scheduler.Scheduler
}

func fresh(name string) *fixture {
	cp := controlplane.NewMemoryService()
	nc, e := cp.RegisterNode(ctx, controlplane.NodeRegistration{Name: name, AdvertiseAddress: "http://127.0.0.1:1", Capacity: types.Resources{CPU: 300, Memory: 1 << 30}, Allocatable: types.Resources{CPU: 300, Memory: 1 << 30}})
	must(e)
	svc, e := cp.CreateService(ctx, types.ServiceSpec{Name: "book-rollout", Image: "nginx:1.27-alpine", Replicas: 3, ResourceRequirements: types.ResourceRequirements{Requests: types.Resources{CPU: 100, Memory: 1 << 20}}, RestartPolicy: types.RestartPolicy{Condition: types.RestartNever}})
	must(e)
	f := &fixture{cp: cp, node: nc.Node, service: svc, controller: rollout.NewController(cp, slog.New(slog.NewTextHandler(io.Discard, nil))), scheduler: scheduler.New(cp)}
	for _, t := range f.tasks() {
		f.report(t, types.TaskHealthy)
	}
	return f
}
func (f *fixture) tasks() []types.Task {
	ts, e := f.cp.ListTasks(ctx, controlplane.TaskFilter{ServiceID: f.service.ID})
	must(e)
	return ts
}
func (f *fixture) report(t types.Task, s types.TaskStatus) {
	_, e := f.cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: t.ID, NodeID: t.NodeID, Status: s, ContainerID: "synthetic-" + string(t.ID)})
	must(e)
}
func (f *fixture) begin() types.Deployment {
	d, e := f.cp.RolloutService(ctx, f.service.ID, controlplane.RolloutSpec{Image: "nginx:1.28-alpine", MaxUnavailable: 0, MaxSurge: 1})
	must(e)
	return d
}

type checkpoint struct {
	Stage         string           `json:"stage"`
	At            time.Time        `json:"at_utc"`
	Deployment    types.Deployment `json:"deployment"`
	OldActive     int              `json:"old_active"`
	TargetActive  int              `json:"target_active"`
	TargetHealthy int              `json:"target_healthy"`
	PendingStops  int              `json:"pending_stops"`
	Available     int              `json:"available"`
	Tasks         []types.Task     `json:"tasks"`
}

func (f *fixture) snapshot(stage string, id types.DeploymentID) checkpoint {
	d, e := f.cp.GetDeployment(ctx, id)
	must(e)
	c := checkpoint{Stage: stage, At: time.Now().UTC(), Deployment: d, Tasks: f.tasks()}
	for _, t := range c.Tasks {
		if t.DesiredStatus == types.TaskStopped && !types.IsTerminalTaskStatus(t.ActualStatus) {
			c.PendingStops++
		}
		if !types.IsActiveTask(t) {
			continue
		}
		if t.Version == d.FromVersion {
			c.OldActive++
			if types.IsAvailableTaskStatus(t.ActualStatus) {
				c.Available++
			}
		}
		if t.Version == d.ToVersion {
			c.TargetActive++
			if t.ActualStatus == types.TaskHealthy {
				c.TargetHealthy++
				c.Available++
			}
		}
	}
	require(c.OldActive+c.TargetActive <= 4, "surge bound")
	require(c.Available >= 3, "modeled availability gate")
	return c
}
func main() {
	require(len(os.Args) == 2, "provide timeline CSV path")
	f := fresh("book-rollout-baseline")
	d := f.begin()
	timeline := []checkpoint{f.snapshot("requested", d.ID)}
	repeat, e := f.cp.RolloutService(ctx, f.service.ID, controlplane.RolloutSpec{Image: "nginx:1.28-alpine", MaxUnavailable: 0, MaxSurge: 1})
	must(e)
	require(repeat.ID == d.ID, "idempotent rollout ID")
	negatives := map[string]string{}
	_, e = f.cp.RolloutService(ctx, f.service.ID, controlplane.RolloutSpec{Image: "nginx:other", MaxUnavailable: 0, MaxSurge: 1})
	require(errors.Is(e, store.ErrConflict), "different rollout conflict")
	negatives["different_rollout"] = e.Error()
	_, e = f.cp.ScaleService(ctx, f.service.ID, 4)
	require(errors.Is(e, store.ErrConflict), "active scale conflict")
	negatives["scale_during_rollout"] = e.Error()
	_, e = f.cp.RollbackService(ctx, f.service.ID)
	require(errors.Is(e, store.ErrConflict), "active rollback conflict")
	negatives["rollback_during_rollout"] = e.Error()
	must(f.controller.RunOnce(ctx))
	timeline = append(timeline, f.snapshot("target-created", d.ID))
	assigned, e := f.scheduler.RunOnce(ctx)
	must(e)
	require(len(assigned) == 0, "exhausted capacity must wait")
	timeline = append(timeline, f.snapshot("capacity-exhausted", d.ID))
	require(len(f.tasks()) == 4, "single target")
	must(f.controller.RunOnce(ctx))
	require(len(f.tasks()) == 4, "repeated pass duplicated target")
	_, e = f.cp.UpdateDeploymentStatus(ctx, d.ID, types.DeploymentFailed, d.UpdatedAt)
	require(errors.Is(e, store.ErrConflict), "stale deployment CAS conflict")
	negatives["stale_deployment_status"] = e.Error()
	_, e = f.cp.HeartbeatNode(ctx, controlplane.NodeHeartbeat{NodeID: f.node.ID, Capacity: types.Resources{CPU: 400, Memory: 1 << 30}, Allocatable: types.Resources{CPU: 400, Memory: 1 << 30}})
	must(e)
	assigned, e = f.scheduler.RunOnce(ctx)
	must(e)
	require(len(assigned) == 1, "capacity increase must assign target")
	for _, t := range f.tasks() {
		if t.Version == d.ToVersion && t.ActualStatus == types.TaskAssigned {
			f.report(t, types.TaskRunning)
		}
	}
	must(f.controller.RunOnce(ctx))
	slow := f.snapshot("running-but-not-healthy", d.ID)
	require(slow.OldActive == 3 && slow.PendingStops == 0, "slow health must not stop old")
	timeline = append(timeline, slow)
	for pass := 0; pass < 12; pass++ {
		for _, t := range f.tasks() {
			if t.Version == d.ToVersion && t.DesiredStatus == types.TaskRunning && (t.ActualStatus == types.TaskAssigned || t.ActualStatus == types.TaskRunning) {
				f.report(t, types.TaskHealthy)
			}
		}
		must(f.controller.RunOnce(ctx))
		c := f.snapshot(fmt.Sprintf("healthy-controller-pass-%02d", pass), d.ID)
		timeline = append(timeline, c)
		if c.Deployment.Status == types.DeploymentSucceeded {
			break
		}
		for _, t := range f.tasks() {
			if t.DesiredStatus == types.TaskStopped && !types.IsTerminalTaskStatus(t.ActualStatus) {
				f.report(t, types.TaskStopped)
				t.ActualStatus = types.TaskStopped
				f.report(t, types.TaskRemoved)
			}
		}
		must(f.controller.RunOnce(ctx))
		_, e = f.scheduler.RunOnce(ctx)
		must(e)
	}
	end, e := f.cp.GetDeployment(ctx, d.ID)
	must(e)
	require(end.Status == types.DeploymentSucceeded, "rollout failed to finish")
	_, e = f.cp.UpdateDeploymentStatus(ctx, d.ID, types.DeploymentRunning, end.UpdatedAt)
	require(errors.Is(e, store.ErrInvalidState), "terminal deployment immutable")
	negatives["terminal_revival"] = e.Error()
	// Separate failed rollout: the controller, not the harness, sets failed.
	bad := fresh("book-rollout-failure")
	failed := bad.begin()
	must(bad.controller.RunOnce(ctx))
	for _, t := range bad.tasks() {
		if t.Version == failed.ToVersion {
			t, e = bad.cp.AssignTask(ctx, t.ID, bad.node.ID, nil, t.UpdatedAt)
			must(e)
			bad.report(t, types.TaskFailed)
			_, e = bad.cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: t.ID, NodeID: t.NodeID, Status: types.TaskHealthy})
			require(errors.Is(e, store.ErrInvalidState), "late healthy must not revive failure")
			negatives["late_healthy_report"] = e.Error()
		}
	}
	must(bad.controller.RunOnce(ctx))
	failed, e = bad.cp.GetDeployment(ctx, failed.ID)
	must(e)
	require(failed.Status == types.DeploymentFailed, "controller failure status")
	rollback, e := bad.cp.RollbackService(ctx, bad.service.ID)
	must(e)
	require(rollback.ID != failed.ID && rollback.FromVersion == 2 && rollback.ToVersion == 1 && rollback.Status == types.DeploymentRollingBack, "separate baseline rollback")
	history, e := bad.cp.GetDeployment(ctx, failed.ID)
	must(e)
	require(history.Status == types.DeploymentFailed && history.CompletedAt == failed.CompletedAt, "failed history preserved")
	empty := fresh("book-no-history")
	_, e = empty.cp.RollbackService(ctx, empty.service.ID)
	require(errors.Is(e, store.ErrInvalidState), "rollback without predecessor rejected")
	negatives["no_previous_version"] = e.Error()
	deletion := fresh("book-delete")
	canceled := deletion.begin()
	must(deletion.cp.DeleteService(ctx, deletion.service.ID))
	canceled, e = deletion.cp.GetDeployment(ctx, canceled.ID)
	must(e)
	require(canceled.Status == types.DeploymentFailed, "delete cancels")
	out, e := os.Create(os.Args[1])
	must(e)
	writer := csv.NewWriter(out)
	must(writer.Write([]string{"stage", "at_utc", "deployment_id", "from_version", "target_version", "status", "old_active", "target_active", "target_healthy", "pending_stop", "modeled_available", "surge_bound"}))
	for _, c := range timeline {
		must(writer.Write([]string{c.Stage, c.At.Format(time.RFC3339Nano), string(c.Deployment.ID), strconv.FormatInt(c.Deployment.FromVersion, 10), strconv.FormatInt(c.Deployment.ToVersion, 10), string(c.Deployment.Status), strconv.Itoa(c.OldActive), strconv.Itoa(c.TargetActive), strconv.Itoa(c.TargetHealthy), strconv.Itoa(c.PendingStops), strconv.Itoa(c.Available), "4"}))
	}
	writer.Flush()
	must(writer.Error())
	must(out.Close())
	result := map[string]any{"status": "passed", "source_sha": "cbfc94ade5b57e449d6b73bf1485b1c5b1647022", "scope": "executed real MemoryService/controller/scheduler with explicit synthetic agent reports; no containers or external request-availability measurement", "timeline": timeline, "negative_cases": negatives, "identical_rollout_idempotent": true, "repeated_pass_did_not_duplicate": true, "failed_deployment": failed, "rollback_deployment": rollback, "preserved_failed_history": history, "delete_canceled_deployment": canceled}
	data, e := json.MarshalIndent(result, "", "  ")
	must(e)
	fmt.Println(string(data))
}
