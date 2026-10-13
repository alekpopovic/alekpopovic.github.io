// Teaching harness: no published ports, local cached image only, exact owned-ID cleanup.
package main

import (
	"bytes"
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/alekpopovic/orch/internal/agent"
	"github.com/alekpopovic/orch/internal/api"
	"github.com/alekpopovic/orch/internal/cli"
	"github.com/alekpopovic/orch/internal/config"
	"github.com/alekpopovic/orch/internal/controlplane"
	d "github.com/alekpopovic/orch/internal/docker"
	"github.com/alekpopovic/orch/internal/events"
	"github.com/alekpopovic/orch/pkg/types"
	"github.com/docker/docker/client"
	"io"
	"log/slog"
	"net/http/httptest"
	"os"
	"os/exec"
	"strings"
	"sync"
	"time"
)

type ownedRuntime struct {
	d.Runtime
	cli   *client.Client
	mu    sync.Mutex
	ids   map[d.ContainerID]bool
	specs []d.ContainerSpec
	node  string
}

func (r *ownedRuntime) PullImage(ctx context.Context, image string, auth *d.RegistryAuth) error {
	_, err := r.cli.ImageInspect(ctx, image)
	return err
}
func (r *ownedRuntime) CreateContainer(ctx context.Context, s d.ContainerSpec) (d.ContainerID, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if s.NodeID != r.node || r.node == "" {
		return "", fmt.Errorf("not owned node")
	}
	id, err := r.Runtime.CreateContainer(ctx, s)
	if err == nil {
		r.ids[id] = true
		r.specs = append(r.specs, s)
	}
	return id, err
}
func (r *ownedRuntime) ListManagedContainers(ctx context.Context, labels map[string]string) ([]d.ContainerStatus, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	node := labels[d.NodeIDLabel]
	if node == "" {
		owned := false
		for _, s := range r.specs {
			if s.TaskID == labels[d.TaskIDLabel] {
				owned = true
			}
		}
		if !owned {
			return nil, fmt.Errorf("unowned task filter")
		}
		labels[d.NodeIDLabel] = r.node
		node = r.node
	}
	if r.node == "" {
		r.node = node
	}
	if node != r.node {
		return nil, fmt.Errorf("wrong node")
	}
	return r.Runtime.ListManagedContainers(ctx, labels)
}
func (r *ownedRuntime) RemoveContainer(ctx context.Context, id d.ContainerID, force bool) error {
	r.mu.Lock()
	ok := r.ids[id]
	r.mu.Unlock()
	if !ok {
		return fmt.Errorf("remove unowned ID refused")
	}
	return r.Runtime.RemoveContainer(ctx, id, force)
}
func (r *ownedRuntime) StopContainer(ctx context.Context, id d.ContainerID, timeout time.Duration) error {
	r.mu.Lock()
	ok := r.ids[id]
	r.mu.Unlock()
	if !ok {
		return fmt.Errorf("stop unowned ID refused")
	}
	return r.Runtime.StopContainer(ctx, id, timeout)
}
func must(e error) {
	if e != nil {
		panic(e)
	}
}
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 40*time.Second)
	defer cancel()
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	cp := controlplane.NewMemoryService()
	server := httptest.NewServer(api.NewHandler(logger, cp, api.WithBootstrapToken("book-only-registration")))
	defer server.Close()
	dockercli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	must(err)
	defer dockercli.Close()
	rt := &ownedRuntime{Runtime: d.NewEngineRuntime(dockercli), cli: dockercli, ids: map[d.ContainerID]bool{}}
	defer func() {
		for id := range rt.ids {
			_ = rt.Runtime.RemoveContainer(context.Background(), id, true)
		}
	}()
	logServer := httptest.NewServer(agent.NewLogHandler(rt, "book-only-registration", logger))
	defer logServer.Close()
	ac, err := agent.NewHTTPClient(server.URL, "book-only-registration")
	must(err)
	runner := agent.NewRunner(config.AgentConfig{NodeName: "inside-orch-book-" + rand.Text(), AdvertiseAddress: logServer.URL, AgentAddr: "127.0.0.1:0", ServerURL: server.URL, BootstrapToken: "book-only-registration", DockerSocketPath: "/var/run/docker.sock", HeartbeatInterval: 50 * time.Millisecond, GracefulShutdownTTL: time.Second}, ac, logger).WithRuntime(rt)
	agentCtx, stop := context.WithCancel(ctx)
	errCh := make(chan error, 1)
	go func() { errCh <- runner.Run(agentCtx) }()
	defer func() {
		stop()
		select {
		case e := <-errCh:
			if e != nil && !errors.Is(e, context.Canceled) {
				panic(e)
			}
		case <-time.After(3 * time.Second):
			panic("agent cleanup timeout")
		}
	}()
	apiClient, err := cli.NewAPIClient(server.URL)
	must(err)
	deadline := time.Now().Add(15 * time.Second)
	var node types.Node
	for {
		nodes, e := apiClient.ListNodes(ctx)
		must(e)
		if len(nodes) == 1 && nodes[0].Status == types.NodeReady {
			node = nodes[0]
			break
		}
		if time.Now().After(deadline) {
			panic("register deadline")
		}
		time.Sleep(25 * time.Millisecond)
	}
	svc, err := apiClient.CreateService(ctx, types.ServiceSpec{Name: "book-http", Image: "nginx:1.27-alpine", Replicas: 1, ResourceRequirements: types.ResourceRequirements{Requests: types.Resources{CPU: 100, Memory: 67108864}, Limits: types.Resources{CPU: 250, Memory: 134217728}}, RestartPolicy: types.RestartPolicy{Condition: types.RestartNever}})
	must(err)
	var task types.Task
	for {
		tasks, e := cp.ListTasks(ctx, controlplane.TaskFilter{})
		must(e)
		if len(tasks) == 1 && tasks[0].ContainerID != "" && types.IsAvailableTaskStatus(tasks[0].ActualStatus) {
			task = tasks[0]
			break
		}
		if time.Now().After(deadline) {
			panic("running deadline")
		}
		time.Sleep(25 * time.Millisecond)
	}
	actual, err := dockercli.ContainerInspect(ctx, task.ContainerID)
	must(err)
	if actual.HostConfig.Memory != 0 || actual.HostConfig.NanoCPUs != 0 {
		panic("observed propagation changed")
	}
	// Compare direct adapter support with the ordinary agent path.
	directID, err := rt.CreateContainer(ctx, d.ContainerSpec{Name: "inside-orch-book-limits-" + rand.Text(), Image: "nginx:1.27-alpine", ServiceID: string(svc.ID), TaskID: "book-direct-" + rand.Text(), NodeID: string(node.ID), Version: 1, Resources: d.ResourceLimits{CPUMilli: 250, Memory: 134217728}})
	must(err)
	direct, err := dockercli.ContainerInspect(ctx, string(directID))
	must(err)
	if direct.HostConfig.Memory != 134217728 || direct.HostConfig.NanoCPUs != 250000000 {
		panic("direct adapter limits")
	}
	// Exercise the actual runtime flow; HTTP stays inside the owned container.
	httpBody, err := exec.CommandContext(ctx, "docker", "exec", task.ContainerID, "wget", "-qO-", "http://127.0.0.1/").Output()
	must(err)
	if !bytes.Contains(httpBody, []byte("Welcome to nginx!")) {
		panic("HTTP body mismatch")
	}
	var logs bytes.Buffer
	must(apiClient.StreamLogs(ctx, string(svc.ID), "", false, "20", &logs))
	if !strings.Contains(logs.String(), "nginx") {
		panic("real nginx logs absent")
	}
	eventRows, err := apiClient.ListEvents(ctx, events.Filter{ServiceID: svc.ID, Type: events.TypeServiceCreated})
	must(err)
	if len(eventRows) != 1 {
		panic("service creation event count")
	}
	timeline := []map[string]any{}
	waitCounts := func(stage string, wantActive, wantRemoved int) {
		until := time.Now().Add(10 * time.Second)
		for {
			tasks, err := cp.ListTasks(ctx, controlplane.TaskFilter{})
			must(err)
			active, removed := 0, 0
			for _, x := range tasks {
				if x.ServiceID != svc.ID {
					continue
				}
				if x.DesiredStatus == types.TaskRunning && types.IsAvailableTaskStatus(x.ActualStatus) {
					active++
				}
				if x.ActualStatus == types.TaskRemoved {
					removed++
				}
			}
			if active == wantActive && removed == wantRemoved {
				timeline = append(timeline, map[string]any{"stage": stage, "at_utc": time.Now().UTC(), "active": active, "removed": removed, "tasks": tasks})
				return
			}
			if time.Now().After(until) {
				panic("flow deadline " + stage)
			}
			time.Sleep(25 * time.Millisecond)
		}
	}
	waitCounts("deployed", 1, 0)
	_, err = apiClient.ScaleService(ctx, string(svc.ID), 2)
	must(err)
	waitCounts("scaled-up", 2, 0)
	_, err = apiClient.ScaleService(ctx, string(svc.ID), 1)
	must(err)
	waitCounts("scaled-down", 1, 1)
	must(apiClient.DeleteService(ctx, string(svc.ID)))
	waitCounts("deleted", 0, 2)
	deleted, err := apiClient.GetService(ctx, string(svc.ID))
	must(err)
	if deleted.Status != types.ServiceDeleted {
		panic("delete terminal service")
	}
	logDigest := sha256.Sum256(logs.Bytes())
	httpDigest := sha256.Sum256(httpBody)
	result := map[string]any{"status": "passed", "source_sha": "cbfc94ade5b57e449d6b73bf1485b1c5b1647022", "observed_at_utc": time.Now().UTC(), "scope": "actual server handler plus agent Runner plus Docker adapter; teaching wrapper requires cached images and guards owned IDs; no published workload ports", "captured_ids": map[string]any{"node": node.ID, "service": svc.ID, "task": task.ID, "ordinary_container": task.ContainerID, "direct_container": directID}, "ordinary_host_config": map[string]int64{"memory": actual.HostConfig.Memory, "nano_cpus": actual.HostConfig.NanoCPUs}, "direct_host_config": map[string]int64{"memory": direct.HostConfig.Memory, "nano_cpus": direct.HostConfig.NanoCPUs}, "image_id": actual.Image, "ordinary_running": actual.State.Running, "published_ports": len(actual.HostConfig.PortBindings), "flow": timeline, "http_probe": map[string]any{"method": "docker exec wget loopback inside captured container", "welcome_matched": true, "bytes": len(httpBody), "sha256": hex.EncodeToString(httpDigest[:])}, "logs": map[string]any{"nginx_matched": true, "bytes": logs.Len(), "sha256": hex.EncodeToString(logDigest[:])}, "creation_events": len(eventRows), "cleanup": "agent canceled before exact captured container IDs removed; deferred cleanup runs after JSON emission"}
	data, err := json.MarshalIndent(result, "", "  ")
	must(err)
	fmt.Println(string(data))
	_ = os.Stdout.Sync()
}
