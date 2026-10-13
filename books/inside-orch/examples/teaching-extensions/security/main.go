// Synthetic local-only security observations against the unchanged source.
package main

import (
	"bytes"
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/alekpopovic/orch/internal/api"
	"github.com/alekpopovic/orch/internal/auth"
	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/internal/health"
	"github.com/alekpopovic/orch/internal/namespace"
	"github.com/alekpopovic/orch/internal/secrets"
	"github.com/alekpopovic/orch/pkg/types"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"sync/atomic"
	"time"
)

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
func digest(v []byte) string { h := sha256.Sum256(v); return hex.EncodeToString(h[:]) }
func main() {
	require(len(os.Args) == 2, "provide owned evidence directory")
	ctx := context.Background()
	canary := "inside-orch-one-use-" + rand.Text()
	key := rand.Text()
	jwtKey := rand.Text()
	bootstrap := rand.Text()
	envelope, e := secrets.NewLocalEnvelope(key)
	must(e)
	ciphertext, e := envelope.Encrypt(ctx, []byte(canary))
	must(e)
	plain, e := envelope.Decrypt(ctx, ciphertext)
	must(e)
	require(string(plain) == canary, "decrypt comparison")
	wrong, e := secrets.NewLocalEnvelope(rand.Text())
	must(e)
	_, wrongErr := wrong.Decrypt(ctx, ciphertext)
	require(wrongErr != nil, "wrong key rejected")
	var logs bytes.Buffer
	logger := slog.New(slog.NewJSONHandler(&logs, nil))
	cp := controlplane.NewMemoryService(controlplane.WithSecretEnvelope(envelope))
	for _, n := range []string{"team-a", "team-b"} {
		_, e = cp.CreateNamespace(ctx, n)
		must(e)
	}
	h := api.NewHandler(logger, cp, api.WithUserJWT(jwtKey), api.WithBootstrapToken(bootstrap))
	cases := []map[string]any{}
	forbidden := map[string][]byte{}
	add := func(id, actor, ns string, want, actual int, visibility string) {
		require(want == actual, id+" HTTP mismatch: "+fmt.Sprint(actual))
		cases = append(cases, map[string]any{"id": id, "actor": actor, "namespace": ns, "expected_http": want, "actual_http": actual, "secret_visibility": visibility, "destination": "in-process httptest request; no network dial"})
	}
	request := func(id, actor, ns, method, path string, body any, token string, want int, permitted bool) *httptest.ResponseRecorder {
		data, e := json.Marshal(body)
		must(e)
		if body == nil {
			data = nil
		}
		r := httptest.NewRequest(method, path, bytes.NewReader(data))
		r.Header.Set("Content-Type", "application/json")
		if token != "" {
			r.Header.Set("Authorization", "Bearer "+token)
		}
		if ns != "" {
			r.Header.Set("X-Orch-Namespace", ns)
		}
		rec := httptest.NewRecorder()
		h.ServeHTTP(rec, r)
		if rec.Code != want {
			require(!bytes.Contains(rec.Body.Bytes(), []byte(canary)), "unexpected response contains canary")
			panic(id + ": " + rec.Body.String())
		}
		visibility := "forbidden; scanned before persistence"
		if permitted {
			visibility = "permitted assigned-agent/token delivery; raw response discarded"
		} else {
			require(!bytes.Contains(rec.Body.Bytes(), []byte(canary)), id+" leaked canary")
			forbidden[id] = append([]byte(nil), rec.Body.Bytes()...)
		}
		add(id, actor, ns, want, rec.Code, visibility)
		return rec
	}
	token := func(role auth.Role, scoped map[string]auth.Role) string {
		t, e := auth.SignJWT(auth.Claims{Subject: "book-actor-" + string(role), Role: role, NamespaceRoles: scoped, ExpiresAt: time.Now().Add(time.Hour).Unix()}, jwtKey)
		must(e)
		return t
	}
	viewer := token(auth.RoleViewer, nil)
	admin := token(auth.RoleAdmin, nil)
	operator := token("", map[string]auth.Role{"team-a": auth.RoleOperator})
	request("missing-user-token", "anonymous", "team-a", "GET", "/v1/services", nil, "", 401, false)
	request("viewer-read", "viewer", "team-a", "GET", "/v1/services", nil, viewer, 200, false)
	spec := map[string]any{"spec": map[string]any{"name": "book-api", "image": "nginx:1.27-alpine", "replicas": 0, "resource_requirements": map[string]any{"requests": map[string]any{}, "limits": map[string]any{}}}}
	request("viewer-mutation-denied", "viewer", "team-a", "POST", "/v1/services", spec, viewer, 403, false)
	request("scoped-operator-create", "operator", "team-a", "POST", "/v1/services", spec, operator, 201, false)
	request("scoped-operator-other-namespace", "operator", "team-b", "GET", "/v1/services", nil, operator, 403, false)
	request("scoped-operator-cluster-admin-denied", "operator", "team-a", "GET", "/v1/audit", nil, operator, 403, false)
	request("admin-audit", "admin", "team-a", "GET", "/v1/audit", nil, admin, 200, false)
	secretBody := api.CreateSecretRequest{Name: "book-canary", Value: canary}
	request("secret-create-metadata", "admin", "team-a", "POST", "/v1/secrets", secretBody, admin, 201, false)
	request("secret-get-metadata", "viewer", "team-a", "GET", "/v1/secrets/book-canary", nil, viewer, 200, false)
	request("secret-list-metadata", "viewer", "team-a", "GET", "/v1/secrets", nil, viewer, 200, false)
	request("secret-namespace-hidden", "admin", "team-b", "GET", "/v1/secrets/book-canary", nil, admin, 404, false)
	request("secret-events-redacted", "viewer", "team-a", "GET", "/v1/events", nil, viewer, 200, false)
	request("secret-audit-redacted", "admin", "team-a", "GET", "/v1/audit", nil, admin, 200, false)
	request("missing-secret-error", "admin", "team-b", "POST", "/v1/services", map[string]any{"spec": map[string]any{"name": "cross-namespace", "image": "nginx:1.27-alpine", "replicas": 1, "secret_refs": []types.SecretRef{{Name: "book-canary", Env: "BOOK_CANARY"}}, "resource_requirements": map[string]any{"requests": map[string]any{}, "limits": map[string]any{}}}}, admin, 400, false)
	registration := map[string]any{"node_name": "book-security-a", "advertise_address": "http://127.0.0.1:1", "capacity": types.Resources{CPU: 1000, Memory: 1 << 30}, "allocatable": types.Resources{CPU: 1000, Memory: 1 << 30}}
	request("bootstrap-missing", "agent", "", "POST", "/v1/agent/register", registration, "", 401, false)
	rec := request("bootstrap-issued", "agent", "", "POST", "/v1/agent/register", registration, bootstrap, 201, true)
	var a api.AgentResponse
	must(json.Unmarshal(rec.Body.Bytes(), &a))
	require(a.Credential != nil, "issued credential")
	assignedSpec := types.ServiceSpec{Name: "book-secret-work", Image: "nginx:1.27-alpine", Replicas: 1, SecretRefs: []types.SecretRef{{Name: "book-canary", Env: "BOOK_CANARY"}}}
	_, e = cp.CreateService(namespace.WithContext(ctx, "team-a"), assignedSpec)
	must(e)
	rec = request("assigned-agent-plaintext", "assigned-agent", "", "GET", "/v1/agent/tasks?node_id="+string(a.Node.ID), nil, a.Credential.Token, 200, true)
	var tasks api.AgentTasksResponse
	must(json.Unmarshal(rec.Body.Bytes(), &tasks))
	require(len(tasks.Tasks) == 1, "one assigned task")
	require(tasks.Tasks[0].Env["BOOK_CANARY"] == canary, "authorized plaintext delivered")
	task := tasks.Tasks[0].Task
	registration["node_name"] = "book-security-b"
	rec = request("second-agent-issued", "agent", "", "POST", "/v1/agent/register", registration, bootstrap, 201, true)
	var b api.AgentResponse
	must(json.Unmarshal(rec.Body.Bytes(), &b))
	require(b.Credential != nil, "second credential")
	request("wrong-node-credential", "agent-b", "", "POST", "/v1/agent/tasks/"+string(task.ID)+"/status", api.AgentTaskStatusRequest{NodeID: a.Node.ID, Status: types.TaskRunning}, b.Credential.Token, 401, false)
	unchanged, e := cp.ListTasks(ctx, controlplane.TaskFilter{ServiceID: task.ServiceID})
	must(e)
	require(len(unchanged) == 1 && unchanged[0].ActualStatus == task.ActualStatus, "denial must not mutate")
	heartbeat := map[string]any{"node_id": a.Node.ID, "capacity": types.Resources{CPU: 1000, Memory: 1 << 30}, "allocatable": types.Resources{CPU: 1000, Memory: 1 << 30}}
	rec = request("heartbeat-rotates", "agent-a", "", "POST", "/v1/agent/heartbeat", heartbeat, a.Credential.Token, 200, true)
	var rotated api.AgentResponse
	must(json.Unmarshal(rec.Body.Bytes(), &rotated))
	require(rotated.Credential.Token != a.Credential.Token, "new credential")
	request("rotated-old-token-denied", "agent-a", "", "POST", "/v1/agent/heartbeat", heartbeat, a.Credential.Token, 401, false)
	issuer := auth.NewTokenAgentCredentialIssuer(time.Minute)
	issued, record, e := issuer.Issue(ctx, auth.AgentIdentity{NodeID: "book-fixture"})
	must(e)
	require(issuer.Validate(ctx, issued.Token, record, record.ExpiresAt) != nil, "expiry boundary rejected")
	cases = append(cases, map[string]any{"id": "credential-expiry-boundary", "actor": "issuer fixture", "expected": "invalid exactly at expiry", "actual": "invalid", "destination": "none"})
	record.Revoked = true
	require(issuer.Validate(ctx, issued.Token, record, time.Now()) != nil, "revoked rejected")
	disabled := api.NewHandler(logger, controlplane.NewMemoryService())
	rr := httptest.NewRecorder()
	disabled.ServeHTTP(rr, httptest.NewRequest("GET", "/v1/services", nil))
	add("empty-user-jwt-auth-disabled", "anonymous", "default", 200, rr.Code, "empty service metadata")
	// Network probes are separate actual loopback listeners. Never resolve outside hosts.
	var crossHits atomic.Int32
	cross := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) { crossHits.Add(1); w.WriteHeader(200) }))
	defer cross.Close()
	origin := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/same":
			http.Redirect(w, r, "/ok", 302)
		case "/cross":
			http.Redirect(w, r, cross.URL+"/blocked", 302)
		case "/slow":
			time.Sleep(100 * time.Millisecond)
			w.WriteHeader(200)
		case "/large":
			_, _ = w.Write([]byte(strings.Repeat("x", int(health.MaxHTTPResponseBodyBytes)+100)))
		default:
			w.WriteHeader(200)
		}
	}))
	defer origin.Close()
	checker := health.NewChecker()
	for _, p := range []struct {
		id, path string
		ok       bool
		timeout  time.Duration
	}{{"same-origin-redirect", "/same", true, time.Second}, {"cross-origin-blocked", "/cross", false, time.Second}, {"bounded-large-response", "/large", true, time.Second}, {"timeout-unhealthy", "/slow", false, 10 * time.Millisecond}} {
		res, e := checker.Check(ctx, health.Check{Type: health.HTTPProbe, Target: origin.URL + p.path, Timeout: p.timeout})
		must(e)
		require(res.Healthy == p.ok, p.id)
		forbidden[p.id] = []byte(res.Message)
		cases = append(cases, map[string]any{"id": p.id, "expected_healthy": p.ok, "actual_healthy": res.Healthy, "destination": origin.URL + p.path, "redirect_target": cross.URL, "response_body_cap_bytes": health.MaxHTTPResponseBodyBytes})
	}
	require(crossHits.Load() == 0, "cross-origin destination was contacted")
	for _, path := range []string{"/ready", "https://example.invalid/", "//127.0.0.1/"} {
		hc := types.Healthcheck{Type: types.HealthcheckHTTP, Path: path, Port: 8080}
		e := hc.Validate()
		want := path == "/ready"
		require((e == nil) == want, "health path validation")
		cases = append(cases, map[string]any{"id": "health-path-" + path, "expected_valid": want, "actual_valid": e == nil, "destination": "none: input validation only"})
	}
	forbidden["captured-logs"] = logs.Bytes()
	forbidden["wrong-envelope-error"] = []byte(wrongErr.Error())
	scanned := []map[string]any{}
	dir := os.Args[1]
	must(os.MkdirAll(dir, 0755))
	for id, data := range forbidden {
		require(!bytes.Contains(data, []byte(canary)), "forbidden canary in "+id)
		name := id + ".txt"
		must(os.WriteFile(filepath.Join(dir, name), data, 0644))
		scanned = append(scanned, map[string]any{"file": name, "sha256": digest(data), "bytes": len(data), "canary_found": false})
	}
	result := map[string]any{"status": "passed", "source_sha": "cbfc94ade5b57e449d6b73bf1485b1c5b1647022", "at_utc": time.Now().UTC(), "scope": "local envelope, actual API handler/issuer, local health checker; no Docker or public network; plaintext and credentials exist only in process memory", "cases": cases, "canary_sha256": digest([]byte(canary)), "ciphertext_sha256": digest(ciphertext.Data), "ciphertext_contains_plaintext": bytes.Contains(ciphertext.Data, []byte(canary)), "same_key_roundtrip": true, "wrong_key_rejected": true, "assigned_agent_plaintext_permitted": true, "wrong_node_unchanged_task": true, "cross_origin_destination_requests": crossHits.Load(), "scanned_forbidden_channels": scanned, "cleanup": "all local listeners deferred closed; canary/key/token raw values never written"}
	require(!bytes.Contains(ciphertext.Data, []byte(canary)), "ciphertext accidentally contains canary")
	encoded, e := json.MarshalIndent(result, "", "  ")
	must(e)
	require(!bytes.Contains(encoded, []byte(canary)), "result leak")
	fmt.Println(string(encoded))
}
