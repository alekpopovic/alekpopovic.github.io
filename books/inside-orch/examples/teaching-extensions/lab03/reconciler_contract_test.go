// Original teaching extension using unchanged upstream reconciler and its test store.
package reconciler

import (
	"context"
	"encoding/json"
	"github.com/alekpopovic/orch/pkg/types"
	"os"
	"reflect"
	"testing"
)

func TestBookReplicaIntent(t *testing.T) {
	results := []map[string]any{}
	cases := []struct {
		name     string
		replicas int
		policy   types.RestartCondition
		status   types.ServiceStatus
		tasks    []types.Task
		created  int
		stopped  []types.TaskID
	}{
		{name: "below-target", replicas: 3, status: types.ServiceActive, tasks: []types.Task{taskFixture("running", "svc", 1, types.TaskRunning, types.TaskRunning)}, created: 2},
		{name: "failed-always", replicas: 1, policy: types.RestartAlways, status: types.ServiceActive, tasks: []types.Task{taskFixture("failed", "svc", 1, types.TaskRunning, types.TaskFailed)}, created: 1},
		{name: "failed-never", replicas: 1, policy: types.RestartNever, status: types.ServiceActive, tasks: []types.Task{taskFixture("failed", "svc", 1, types.TaskRunning, types.TaskFailed)}},
		{name: "scale-order", replicas: 1, status: types.ServiceActive, tasks: []types.Task{taskFixture("running", "svc", 1, types.TaskRunning, types.TaskRunning), taskFixture("pending-a", "svc", 1, types.TaskRunning, types.TaskPending), taskFixture("pending-z", "svc", 1, types.TaskRunning, types.TaskPending), taskFixture("assigned", "svc", 1, types.TaskRunning, types.TaskAssigned)}, stopped: []types.TaskID{"pending-z", "pending-a", "assigned"}},
		{name: "soft-delete", replicas: 1, status: types.ServiceDeleting, tasks: []types.Task{taskFixture("running", "svc", 1, types.TaskRunning, types.TaskRunning)}, stopped: []types.TaskID{"running"}},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			svc := serviceFixtureWithStatus("svc", c.replicas, 1, types.RestartPolicy{Condition: c.policy}, c.status)
			s := newFakeStore([]types.Service{svc}, c.tasks)
			r := New(s)
			if e := r.ReconcileOnce(context.Background()); e != nil {
				t.Fatal(e)
			}
			first := len(s.events)
			if len(s.created) != c.created || !reflect.DeepEqual(s.stopped, c.stopped) {
				t.Fatalf("directives got created=%d stopped=%v want=%d %v", len(s.created), s.stopped, c.created, c.stopped)
			}
			if e := r.ReconcileOnce(context.Background()); e != nil {
				t.Fatal(e)
			}
			if len(s.events) != first || len(s.created) != c.created || len(s.stopped) != len(c.stopped) {
				t.Fatal("second unchanged pass duplicated intent/events")
			}
			if c.name == "failed-never" {
				if s.tasks["failed"].ActualStatus != types.TaskFailed || len(s.tasks) != 1 {
					t.Fatal("failed never task not preserved")
				}
			}
			beforeAck := s.services["svc"].Status
			if c.status == types.ServiceDeleting {
				if beforeAck != types.ServiceDeleting {
					t.Fatal("premature terminal deletion")
				}
				for id, x := range s.tasks {
					x.ActualStatus = types.TaskRemoved
					s.tasks[id] = x
				}
				if e := r.ReconcileOnce(context.Background()); e != nil {
					t.Fatal(e)
				}
				if s.services["svc"].Status != types.ServiceDeleted {
					t.Fatal("removed acknowledgements did not finish deletion")
				}
			}
			results = append(results, map[string]any{"id": c.name, "initial_service": svc, "initial_tasks": c.tasks, "expected_created": c.created, "expected_stop_order": c.stopped, "observed_created": s.created, "observed_stop_order": s.stopped, "event_count_first_pass": first, "event_count_second_pass": first, "service_before_removed_ack": beforeAck, "final_service_status": s.services["svc"].Status, "ownership_conclusion": "Store intent only; no runtime calls", "passed": true})
		})
	}
	if !t.Failed() {
		b, e := json.MarshalIndent(results, "", "  ")
		if e != nil {
			t.Fatal(e)
		}
		if e = os.WriteFile(os.Getenv("ORCH_BOOK_LAB03_OUTPUT")+"-reconciler.json", append(b, '\n'), 0600); e != nil {
			t.Fatal(e)
		}
	}
}
