// Teaching fixture: calls locked packages; creates no Docker or SQL resources.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"time"

	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/internal/scheduler"
	"github.com/alekpopovic/orch/pkg/types"
)

const sourceSHA = "cbfc94ade5b57e449d6b73bf1485b1c5b1647022"
const Mi int64 = 1024 * 1024

type fixture struct {
	SourceSHA string              `json:"source_sha"`
	Input     scheduler.PlanInput `json:"input"`
}

func check(ok bool, message string) {
	if !ok {
		panic(message)
	}
}

func service(id string, cpu, memory int64, port int, zone string) types.Service {
	return types.Service{ID: types.ServiceID(id), Spec: types.ServiceSpec{
		Name: id, Image: "nginx:1.27-alpine", Replicas: 1,
		ResourceRequirements: types.ResourceRequirements{
			Requests: types.Resources{CPU: cpu, Memory: memory * Mi},
			Limits:   types.Resources{CPU: cpu * 2, Memory: memory * 2 * Mi},
		},
		Ports:                []types.Port{{Protocol: types.PortTCP, ContainerPort: 80, PublishedPort: port}},
		PlacementConstraints: []types.PlacementConstraint{{Key: "zone", Operator: types.ConstraintEquals, Value: zone}},
	}}
}

func initial() fixture {
	specs := []types.Service{service("fixed", 400, 128, 31080, "blue"), service("dynamic", 400, 128, 0, "blue"), service("label-miss", 100, 64, 0, "green"), service("too-large", 2000, 1024, 0, "blue"), service("existing", 100, 64, 31080, "blue")}
	services := map[types.ServiceID]types.Service{}
	for _, s := range specs {
		services[s.ID] = s
	}
	nodes := []types.Node{
		{ID: "a", Status: types.NodeOffline, Labels: map[string]string{"zone": "green"}, Capacity: types.Resources{CPU: 8000, Memory: 8192 * Mi}, Allocatable: types.Resources{CPU: 4000, Memory: 4096 * Mi}},
		{ID: "b", Status: types.NodeReady, Labels: map[string]string{"zone": "blue"}, Capacity: types.Resources{CPU: 2000, Memory: 1024 * Mi}, Allocatable: types.Resources{CPU: 1000, Memory: 512 * Mi}},
		{ID: "c", Status: types.NodeReady, Labels: map[string]string{"zone": "blue"}, Capacity: types.Resources{CPU: 2000, Memory: 1024 * Mi}, Allocatable: types.Resources{CPU: 1000, Memory: 512 * Mi}},
	}
	stamp := time.Date(2026, 10, 13, 0, 0, 0, 0, time.UTC)
	ids := []types.ServiceID{"fixed", "dynamic", "dynamic", "label-miss", "too-large", "fixed"}
	var tasks []types.Task
	for i, id := range ids {
		tasks = append(tasks, types.Task{ID: types.TaskID(fmt.Sprintf("atlas-%02d", i+1)), ServiceID: id, DesiredStatus: types.TaskRunning, ActualStatus: types.TaskPending, UpdatedAt: stamp})
	}
	existing := types.Task{ID: "occupied-b", ServiceID: "existing", NodeID: "b", DesiredStatus: types.TaskRunning, ActualStatus: types.TaskStopping, Ports: specs[4].Spec.Ports, UpdatedAt: stamp}
	return fixture{sourceSHA, scheduler.PlanInput{Nodes: nodes, PendingTasks: tasks, RunningTasks: []types.Task{existing}, Services: services}}
}

func permutations(n int) [][]int {
	var result [][]int
	var visit func([]int, []bool)
	visit = func(order []int, used []bool) {
		if len(order) == n {
			result = append(result, append([]int(nil), order...))
			return
		}
		for i := 0; i < n; i++ {
			if !used[i] {
				used[i] = true
				visit(append(order, i), used)
				used[i] = false
			}
		}
	}
	visit(nil, make([]bool, n))
	return result
}

func main() {
	if len(os.Args) == 2 && os.Args[1] == "--emit-fixture" {
		json.NewEncoder(os.Stdout).Encode(initial())
		return
	}
	check(len(os.Args) == 2, "Pass the canonical fixture JSON path")
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	var f fixture
	if err = json.Unmarshal(data, &f); err != nil {
		panic(err)
	}
	check(f.SourceSHA == sourceSHA, "Wrong source edition")
	check(len(f.Input.Nodes) == 3 && len(f.Input.PendingTasks) == 6, "Expected three nodes and six candidates")
	baseline := scheduler.Plan(f.Input)
	want := []struct {
		task, node string
		port       int
	}{{"atlas-01", "c", 31080}, {"atlas-02", "b", 30000}, {"atlas-03", "c", 30000}}
	check(len(baseline) == len(want), "Unexpected placement count")
	for i, w := range want {
		a := baseline[i]
		check(string(a.TaskID) == w.task && string(a.NodeID) == w.node && len(a.Ports) == 1 && a.Ports[0].PublishedPort == w.port, "Unexpected placement")
	}
	// Distinct order pairs: all six node orders and four task orders, including reverse.
	taskOrders := permutations(6)
	selected := [][]int{taskOrders[0], taskOrders[117], taskOrders[358], taskOrders[719]}
	var orders []map[string]any
	for _, no := range permutations(3) {
		for _, to := range selected {
			input := f.Input
			input.Nodes = nil
			input.PendingTasks = nil
			for _, i := range no {
				input.Nodes = append(input.Nodes, f.Input.Nodes[i])
			}
			for _, i := range to {
				input.PendingTasks = append(input.PendingTasks, f.Input.PendingTasks[i])
			}
			check(reflect.DeepEqual(baseline, scheduler.Plan(input)), "Input order changed output")
			orders = append(orders, map[string]any{"nodes": no, "tasks": to})
		}
	}
	used := map[types.NodeID]types.Resources{"b": {CPU: 100, Memory: 64 * Mi}}
	ports := map[string]bool{"b/tcp/31080": true}
	taskByID := map[types.TaskID]types.Task{}
	for _, t := range f.Input.PendingTasks {
		taskByID[t.ID] = t
		check(t.ActualStatus == types.TaskPending, "Plan mutated candidate status")
	}
	for _, a := range baseline {
		t := taskByID[a.TaskID]
		r := f.Input.Services[t.ServiceID].Spec.ResourceRequirements.Requests
		u := used[a.NodeID]
		u.CPU += r.CPU
		u.Memory += r.Memory
		used[a.NodeID] = u
		check(a.NodeID != "a", "Offline assignment")
		for _, p := range a.Ports {
			key := fmt.Sprintf("%s/%s/%d", a.NodeID, p.Protocol, p.PublishedPort)
			check(!ports[key], "Duplicate node port")
			ports[key] = true
		}
	}
	for _, n := range f.Input.Nodes {
		u := used[n.ID]
		check(u.CPU <= n.Allocatable.CPU && u.Memory <= n.Allocatable.Memory, "Accounted capacity exceeded")
	}
	tie := f.Input
	tie.RunningTasks = nil
	tie.PendingTasks = []types.Task{f.Input.PendingTasks[1]}
	tieResult := scheduler.Plan(tie)
	check(len(tieResult) == 1 && tieResult[0].NodeID == "b", "Lexical tie break")
	stopping := f.Input.RunningTasks[0]
	check(types.IsActiveTask(stopping), "Actual stopping with desired running must count")
	stopping.DesiredStatus = types.TaskStopped
	check(!types.IsActiveTask(stopping), "Desired stopped is excluded before physical acknowledgement")
	// The default memory composition bypasses this planner for immediate service creation.
	ctx := context.Background()
	cp := controlplane.NewMemoryService()
	node, err := cp.RegisterNode(ctx, controlplane.NodeRegistration{Name: "lab02-owned-model", AdvertiseAddress: "http://127.0.0.1:1", Labels: map[string]string{"zone": "red"}, Capacity: types.Resources{CPU: 100, Memory: 64 * Mi}, Allocatable: types.Resources{CPU: 100, Memory: 64 * Mi}})
	if err != nil {
		panic(err)
	}
	_, err = cp.HeartbeatNode(ctx, controlplane.NodeHeartbeat{NodeID: node.Node.ID, Labels: map[string]string{"zone": "red"}, Capacity: node.Node.Capacity, Allocatable: node.Node.Allocatable})
	if err != nil {
		panic(err)
	}
	spec := service("atlas-bypass", 600, 256, 0, "blue").Spec
	svc, err := cp.CreateService(ctx, spec)
	if err != nil {
		panic(err)
	}
	assigned, err := cp.ListAssignedTasks(ctx, node.Node.ID)
	if err != nil {
		panic(err)
	}
	check(len(assigned) == 1 && assigned[0].Task.ActualStatus == types.TaskAssigned, "Expected ordinary memory assignment")
	check(assigned[0].Task.ResourceRequirements == nil, "Ordinary service task unexpectedly transports requirements")
	output := map[string]any{"status": "passed", "source_sha": sourceSHA, "fixture": os.Args[1], "assignments": baseline, "distinct_input_permutations": orders, "permutations_checked": len(orders), "pending_no_fit": []string{"atlas-04", "atlas-05", "atlas-06"}, "accounted_resources": used, "lexical_tie_node": tieResult[0].NodeID, "actual_stopping_desired_running_counted": true, "desired_stopped_before_actual_ack_excluded": true, "memory_path": map[string]any{"declared_requests": svc.Spec.ResourceRequirements.Requests, "advertised_allocatable": node.Node.Allocatable, "node_labels": node.Node.Labels, "required_zone": "blue", "actual_task_status": assigned[0].Task.ActualStatus, "ordinary_task_resource_requirements_absent": assigned[0].Task.ResourceRequirements == nil}, "scope": "Deterministic planner and actual in-process MemoryService methods; no Docker, SQL, network listeners or physical resource pressure"}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err = enc.Encode(output); err != nil {
		panic(err)
	}
}
