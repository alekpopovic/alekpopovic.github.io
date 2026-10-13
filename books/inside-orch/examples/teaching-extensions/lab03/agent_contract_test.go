// Original teaching extension. Tests unchanged agent code with real MemoryService lifecycle validation.
package agent

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"os"
	"strings"
	"testing"

	"github.com/alekpopovic/orch/internal/api"
	"github.com/alekpopovic/orch/internal/config"
	"github.com/alekpopovic/orch/internal/controlplane"
	orchdocker "github.com/alekpopovic/orch/internal/docker"
	"github.com/alekpopovic/orch/internal/events"
	"github.com/alekpopovic/orch/pkg/types"
)

type bookClient struct {
	service *controlplane.MemoryService
	reports []api.AgentTaskStatusRequest
}

func (c *bookClient) Register(context.Context, api.AgentRegisterRequest) (api.AgentResponse, error) {
	return api.AgentResponse{}, fmt.Errorf("not used")
}
func (c *bookClient) Heartbeat(context.Context, api.AgentHeartbeatRequest) (api.AgentResponse, error) {
	return api.AgentResponse{}, fmt.Errorf("not used")
}
func (c *bookClient) ListAssignedTasks(ctx context.Context, n types.NodeID) ([]api.AgentTask, error) {
	return c.service.ListAssignedTasks(ctx, n)
}
func (c *bookClient) ReportTaskStatus(ctx context.Context, id types.TaskID, r api.AgentTaskStatusRequest) (types.Task, error) {
	c.reports = append(c.reports, r)
	return c.service.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: id, NodeID: r.NodeID, Status: r.Status, ContainerID: r.ContainerID, FailureReason: r.FailureReason, ExitCode: r.ExitCode})
}
func bookWrite(t *testing.T, key string, data any) {
	t.Helper()
	p := os.Getenv("ORCH_BOOK_LAB03_OUTPUT") + "-" + key + ".json"
	b, e := json.MarshalIndent(data, "", "  ")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(p, append(b, '\n'), 0600); e != nil {
		t.Fatal(e)
	}
}

func TestBookDriftWithLifecycle(t *testing.T) {
	ctx := context.Background()
	results := []map[string]any{}
	cases := []struct {
		name, mode      string
		running, reject bool
		creates         int
		removeOld       bool
	}{
		{"missing-assigned", "missing", false, false, 1, false},
		{"missing-running", "missing", true, true, 0, false},
		{"stopped-owned", "stopped", true, false, 0, false},
		{"image-mismatch-running", "image", true, true, 0, true},
		{"version-mismatch-assigned", "version", false, false, 1, true},
		{"service-label-mismatch-running", "service", true, true, 0, true},
		{"foreign-node-reference", "foreign", true, true, 0, false},
		{"unexpected-owned", "unexpected", false, false, 0, true},
		{"unmanaged-name-similarity", "unmanaged", true, true, 0, false},
		{"soft-delete-owned", "delete", true, false, 0, true},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			cp := controlplane.NewMemoryService()
			nc, e := cp.RegisterNode(ctx, controlplane.NodeRegistration{Name: "atlas-lab-node", AdvertiseAddress: "127.0.0.1:19001", Capacity: types.Resources{CPU: 4000, Memory: 4 << 30}})
			if e != nil {
				t.Fatal(e)
			}
			svc, e := cp.CreateService(ctx, types.ServiceSpec{Name: "atlas-api", Image: "nginx:1.27", Replicas: 1, RestartPolicy: types.RestartPolicy{Condition: types.RestartNever}})
			if e != nil {
				t.Fatal(e)
			}
			tasks, e := cp.ListTasksByService(ctx, svc.ID)
			if e != nil || len(tasks) != 1 {
				t.Fatalf("tasks %v %v", tasks, e)
			}
			task := tasks[0]
			if tc.running {
				task, e = cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: nc.Node.ID, Status: types.TaskRunning, ContainerID: "owned-before"})
				if e != nil {
					t.Fatal(e)
				}
			}
			rt := orchdocker.NewFakeRuntime(orchdocker.WithFakeContainerIDs("replacement"))
			// Both protected sentinels exist in EVERY case, including deletion and mismatch cleanup.
			rt.AddContainer(orchdocker.ContainerStatus{ID: "unmanaged-sentinel", Name: "orch-atlas-api-similar", Running: true, Labels: map[string]string{orchdocker.TaskIDLabel: "not-owned"}})
			rt.AddContainer(managedTaskContainer("other-node-sentinel", "other-node", "other-task", svc.ID, "nginx:1.27", 1, true))
			old := managedTaskContainer("owned-before", nc.Node.ID, task.ID, svc.ID, "nginx:1.27", task.Version, true)
			switch tc.mode {
			case "stopped":
				old.Running = false
				old.State = "exited"
				old.Status = "exited"
				rt.AddContainer(old)
			case "image":
				old.Image = "nginx:1.26"
				rt.AddContainer(old)
			case "version":
				old.Labels[orchdocker.VersionLabel] = "999"
				rt.AddContainer(old)
			case "service":
				old.Labels[orchdocker.ServiceIDLabel] = "different-service"
				rt.AddContainer(old)
			case "foreign":
				old.Labels[orchdocker.NodeIDLabel] = "other-node"
				rt.AddContainer(old)
			case "unmanaged":
				delete(old.Labels, orchdocker.ManagedLabel)
				rt.AddContainer(old)
			case "delete":
				rt.AddContainer(old)
				if e = cp.DeleteService(ctx, svc.ID); e != nil {
					t.Fatal(e)
				}
			case "unexpected": // Keep the real task assigned elsewhere; unexpected orphan is not in the assignment set.
				if e = cp.DeleteService(ctx, svc.ID); e != nil {
					t.Fatal(e)
				}
				_, e = cp.ReportTaskStatus(ctx, controlplane.TaskStatusReport{TaskID: task.ID, NodeID: nc.Node.ID, Status: types.TaskRemoved})
				if e != nil {
					t.Fatal(e)
				}
				old.Labels[orchdocker.TaskIDLabel] = "orphan-task"
				rt.AddContainer(old)
			}
			initialTask, _ := cp.GetTask(ctx, task.ID)
			initialService, _ := cp.GetService(ctx, svc.ID)
			initialContainers, _ := rt.ListManagedContainers(ctx, nil)
			before, _ := cp.ListEvents(ctx, events.Filter{})
			cl := &bookClient{service: cp}
			drift := &fakeDriftRecorder{}
			runner := NewRunner(config.AgentConfig{}, cl, slog.New(slog.NewTextHandler(io.Discard, nil))).WithRuntime(rt).WithDriftRecorder(drift)
			e = runner.reconcileAssignedTasks(ctx, nc.Node.ID)
			errText := ""
			if e != nil {
				errText = e.Error()
			}
			if tc.reject {
				if !strings.Contains(errText, "cannot accept agent status \"pulling\"") {
					t.Fatalf("expected lifecycle rejection, got %v", e)
				}
			} else if e != nil {
				t.Fatal(e)
			}
			if len(rt.CreatedSpecs()) != tc.creates {
				t.Fatalf("creates want %d got %d", tc.creates, len(rt.CreatedSpecs()))
			}
			for _, id := range []orchdocker.ContainerID{"unmanaged-sentinel", "other-node-sentinel"} {
				if _, e := rt.InspectContainer(ctx, id); e != nil {
					t.Fatalf("protected %s removed: %v", id, e)
				}
			}
			_, oldErr := rt.InspectContainer(ctx, "owned-before")
			if tc.removeOld && oldErr == nil {
				t.Fatal("owned mismatch/orphan/deleted container survived")
			}
			if (tc.mode == "foreign" || tc.mode == "unmanaged") && oldErr != nil {
				t.Fatal("foreign or unmanaged referenced container removed")
			}
			finalTask, _ := cp.GetTask(ctx, task.ID)
			finalService, _ := cp.GetService(ctx, svc.ID)
			if tc.reject && finalTask.ActualStatus != types.TaskRunning {
				t.Fatalf("rejected report changed task %v", finalTask)
			}
			if tc.mode == "delete" && (initialService.Status != types.ServiceDeleting || finalService.Status != types.ServiceDeleted || finalTask.ActualStatus != types.TaskRemoved) {
				t.Fatalf("deletion did not wait for removed report: %v %v %v", initialService.Status, finalService.Status, finalTask.ActualStatus)
			}
			after, _ := cp.ListEvents(ctx, events.Filter{})
			eventCount := len(after)
			reports := len(cl.reports)
			second := runner.reconcileAssignedTasks(ctx, nc.Node.ID)
			if tc.reject && (second == nil || !strings.Contains(second.Error(), "cannot accept agent status")) {
				t.Fatalf("second rejection %v", second)
			}
			if !tc.reject && second != nil {
				t.Fatal(second)
			}
			for _, id := range []orchdocker.ContainerID{"unmanaged-sentinel", "other-node-sentinel"} {
				if _, e := rt.InspectContainer(ctx, id); e != nil {
					t.Fatalf("second pass removed protected %s: %v", id, e)
				}
			}
			twice, _ := cp.ListEvents(ctx, events.Filter{})
			if len(twice) != eventCount {
				t.Fatalf("unchanged pass added transition events: %d -> %d", eventCount, len(twice))
			}
			results = append(results, map[string]any{"id": tc.name, "initial_service": initialService, "initial_task": initialTask, "initial_managed_containers": initialContainers, "protected_unmanaged_container_id": "unmanaged-sentinel", "protected_foreign_container_id": "other-node-sentinel", "expected_directive": map[string]any{"reject_pulling": tc.reject, "create_count": tc.creates, "remove_owned_before": tc.removeOld}, "observed_operations": rt.OperationStrings(), "status_reports_first_pass": cl.reports[:reports], "exact_error": errText, "final_task": finalTask, "final_service": finalService, "event_count_initial": len(before), "event_count_first_pass": eventCount, "event_count_second_pass": len(twice), "drift": drift.events, "ownership_conclusion": "Both protected sentinels survived; only matching node/task managed containers eligible for cleanup", "created_count": len(rt.CreatedSpecs()), "passed": true})
		})
	}
	if !t.Failed() {
		bookWrite(t, "agent", results)
	}
}
