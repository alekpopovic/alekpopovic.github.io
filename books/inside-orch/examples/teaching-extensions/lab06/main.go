// Book-only in-process HTTP/state lab. No listener, Docker or database.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/alekpopovic/orch/internal/api"
	"github.com/alekpopovic/orch/internal/auth"
	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/internal/namespace"
	"github.com/alekpopovic/orch/internal/quota"
	"github.com/alekpopovic/orch/internal/store"
	"github.com/alekpopovic/orch/pkg/types"
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

type observation struct {
	ID           string `json:"id"`
	Tenant       string `json:"tenant"`
	Actor        string `json:"actor"`
	Route        string `json:"source_route"`
	InitialQuota any    `json:"initial_quota"`
	Delta        any    `json:"requested_delta"`
	Expected     any    `json:"expected_response"`
	Observed     any    `json:"observed_response"`
	Usage        any    `json:"final_usage"`
	Passed       bool   `json:"passed"`
}

var cases []observation
var baseSpec types.ServiceSpec
var limits = types.ResourceQuota{MaxServices: 2, MaxReplicas: 3, MaxCPUMillicores: 300, MaxMemoryBytes: 192 << 20, MaxPublicPorts: 2, MaxSecrets: 1, MaxRegistryCredentials: 1}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func check(id, tenant, actor, route string, expected, observed, delta any, usage any, pass bool) {
	cases = append(cases, observation{id, tenant, actor, route, limits, delta, expected, observed, usage, pass})
	if !pass {
		panic(fmt.Sprintf("case %s: expected%v observed%v", id, expected, observed))
	}
}
func token(role auth.Role, roles map[string]auth.Role) string {
	t, err := auth.SignJWT(auth.Claims{Subject: "book-actor", Role: role, NamespaceRoles: roles, ExpiresAt: time.Now().Add(time.Hour).Unix()}, "book-only-not-a-live-secret")
	must(err)
	return t
}
func request(h http.Handler, method, path, ns, bearer string, body any) (int, map[string]any) {
	var raw []byte
	var err error
	if body != nil {
		raw, err = json.Marshal(body)
		must(err)
	}
	r := httptest.NewRequest(method, path, bytes.NewReader(raw))
	r.Header.Set("Content-Type", "application/json")
	if ns != "" {
		r.Header.Set("X-Orch-Namespace", ns)
	}
	if bearer != "" {
		r.Header.Set("Authorization", "Bearer "+bearer)
	}
	w := httptest.NewRecorder()
	h.ServeHTTP(w, r)
	var out map[string]any
	if w.Body.Len() > 0 {
		must(json.Unmarshal(w.Body.Bytes(), &out))
	}
	return w.Code, out
}
func usage(s *controlplane.MemoryService, ns string) types.ResourceUsage {
	_, u, err := s.GetResourceQuota(namespace.WithContext(context.Background(), ns))
	must(err)
	return u
}
func spec(name, team string) types.ServiceSpec {
	raw, err := json.Marshal(baseSpec)
	must(err)
	var s types.ServiceSpec
	must(json.Unmarshal(raw, &s))
	s.Name = name
	s.Env["LAB_TEAM"] = team
	return s
}
func create(h http.Handler, ns, bearer string, s types.ServiceSpec) types.Service {
	code, out := request(h, "POST", "/v1/services", ns, bearer, map[string]any{"spec": s})
	if code != 201 {
		panic(fmt.Sprintf("create status%d body%v", code, out))
	}
	raw, _ := json.Marshal(out["service"])
	var result types.Service
	must(json.Unmarshal(raw, &result))
	return result
}
func main() {
	if len(os.Args) != 2 {
		panic("pass canonical fixtures directory")
	}
	for file, target := range map[string]any{"quota.json": &limits, "api-base.json": &baseSpec} {
		raw, err := os.ReadFile(filepath.Join(os.Args[1], file))
		must(err)
		must(json.Unmarshal(raw, target))
	}
	ctx := context.Background()
	s := controlplane.NewMemoryService()
	admin := token(auth.RoleAdmin, nil)
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	h := api.NewHandler(logger, s, api.WithUserJWT("book-only-not-a-live-secret"))
	for _, ns := range []string{"book-payments", "book-observability"} {
		code, out := request(h, "POST", "/v1/namespaces", "", admin, map[string]string{"name": ns})
		check("namespace-create-"+ns, ns, "cluster-admin", "POST /v1/namespaces", 201, code, out, nil, code == 201)
	}
	a := create(h, "book-payments", admin, spec("api", "payments"))
	b := create(h, "book-observability", admin, spec("api", "observability"))
	check("duplicate-local-name", "both", "cluster-admin", "POST /v1/services", "distinct IDs", map[string]any{"payments": a.ID, "observability": b.ID}, nil, usage(s, "book-payments"), a.ID != b.ID && a.Namespace != b.Namespace)
	code, out := request(h, "GET", "/v1/services/"+string(b.ID), "book-payments", admin, nil)
	check("cross-id-hidden", "book-payments", "cluster-admin", "GET /v1/services/{other-ID}", 404, code, nil, usage(s, "book-payments"), code == 404)
	code, out = request(h, "GET", "/v1/services?namespace=book-observability", "book-payments", admin, nil)
	raw, _ := json.Marshal(out)
	check("header-precedes-query", "book-payments", "cluster-admin", "GET /v1/services?namespace=book-observability", "payments only", out, nil, usage(s, "book-payments"), code == 200 && bytes.Contains(raw, []byte(`"LAB_TEAM":"payments"`)) && !bytes.Contains(raw, []byte(`"LAB_TEAM":"observability"`)))
	code, out = request(h, "GET", "/v1/services?namespace=book-observability", "", admin, nil)
	raw, _ = json.Marshal(out)
	check("query-fallback", "book-observability", "cluster-admin", "GET /v1/services?namespace=book-observability", "observability", out, nil, usage(s, "book-observability"), code == 200 && bytes.Contains(raw, []byte(`"LAB_TEAM":"observability"`)))
	def := spec("api", "default")
	def.Replicas = 0
	create(h, "", admin, def)
	code, out = request(h, "GET", "/v1/services", "", admin, nil)
	raw, _ = json.Marshal(out)
	check("default-compatible", "default", "cluster-admin", "GET /v1/services", "default only", out, nil, usage(s, "default"), code == 200 && bytes.Contains(raw, []byte(`"LAB_TEAM":"default"`)) && !bytes.Contains(raw, []byte(`"LAB_TEAM":"payments"`)))
	viewer := token("", map[string]auth.Role{"book-payments": auth.RoleViewer})
	code, _ = request(h, "GET", "/v1/services", "book-payments", viewer, nil)
	check("viewer-own-scope", "book-payments", "namespace-viewer", "GET /v1/services", 200, code, nil, nil, code == 200)
	code, _ = request(h, "GET", "/v1/services", "book-observability", viewer, nil)
	check("viewer-other-scope", "book-observability", "namespace-viewer", "GET /v1/services", 403, code, nil, nil, code == 403)
	nsAdmin := token("", map[string]auth.Role{"book-payments": auth.RoleAdmin})
	code, _ = request(h, "GET", "/v1/namespaces", "book-payments", nsAdmin, nil)
	check("namespace-admin-not-cluster", "book-payments", "namespace-admin", "GET /v1/namespaces", 403, code, nil, nil, code == 403)
	code, _ = request(h, "GET", "/v1/namespaces", "", admin, nil)
	check("cluster-admin-list", "all", "cluster-admin", "GET /v1/namespaces", 200, code, nil, nil, code == 200)
	for _, ns := range []string{"book-payments", "book-observability"} {
		_, err := s.CreateSecret(namespace.WithContext(ctx, ns), "shared", "non-sensitive-"+ns)
		must(err)
		m, err := s.GetSecret(namespace.WithContext(ctx, ns), "shared")
		must(err)
		check("secret-local-"+ns, ns, "cluster-admin", "CreateSecret/GetSecret", "same local name in own namespace", m, nil, nil, m.Namespace == ns)
	}
	_, err := s.CreateSecret(namespace.WithContext(ctx, "book-payments"), "payments-only", "non-sensitive-fixture")
	must(err)
	cross := spec("cross", "observability")
	cross.SecretRefs = []types.SecretRef{{Name: "payments-only", Env: "EXAMPLE"}}
	_, err = s.CreateService(namespace.WithContext(ctx, "book-observability"), cross)
	check("secret-reference-isolation", "book-observability", "cluster-admin", "CreateService", "invalid missing local reference", fmt.Sprint(err), nil, nil, errors.Is(err, store.ErrInvalidState))
	must(s.DeleteSecret(namespace.WithContext(ctx, "book-payments"), "payments-only"))
	for _, ns := range []string{"book-payments", "book-observability"} {
		q := limits
		code, out = request(h, "PUT", "/v1/quota", ns, admin, q)
		check("quota-config-"+ns, ns, "cluster-admin", "PUT /v1/quota", 200, code, q, usage(s, ns), code == 200)
	}
	u := usage(s, "book-payments")
	check("arithmetic-one", "book-payments", "cluster-admin", "GetResourceQuota", map[string]int64{"cpu": 100, "memory": 64 << 20, "replicas": 1, "ports": 1}, u, nil, u, u.CPUMillicores == 100 && u.MemoryBytes == 64<<20 && u.Replicas == 1 && u.PublicPorts == 1)
	code, out = request(h, "POST", "/v1/services/"+string(a.ID)+"/scale", "book-payments", admin, map[string]int{"replicas": 4})
	raw, _ = json.Marshal(out)
	after, err := s.GetService(namespace.WithContext(ctx, "book-payments"), a.ID)
	must(err)
	check("denied-scale-atomic", "book-payments", "cluster-admin", "POST /v1/services/{ID}/scale", "409 quota_exceeded replicas", out, map[string]int{"replicas_delta": 3}, usage(s, "book-payments"), code == 409 && bytes.Contains(raw, []byte(`"code":"quota_exceeded"`)) && bytes.Contains(raw, []byte(`"resource":"replicas"`)) && after.Spec.Replicas == 1)
	second := spec("worker", "payments")
	second.Ports = nil
	c := create(h, "book-payments", admin, second)
	start := make(chan struct{})
	results := make(chan error, 2)
	var wg sync.WaitGroup
	for _, id := range []types.ServiceID{a.ID, c.ID} {
		wg.Add(1)
		go func(id types.ServiceID) {
			defer wg.Done()
			<-start
			_, err := s.ScaleService(namespace.WithContext(ctx, "book-payments"), id, 2)
			results <- err
		}(id)
	}
	close(start)
	wg.Wait()
	close(results)
	wins, denials := 0, 0
	for e := range results {
		if e == nil {
			wins++
		} else {
			var qerr *quota.Error
			if errors.As(e, &qerr) {
				denials++
			} else {
				panic(e)
			}
		}
	}
	u = usage(s, "book-payments")
	check("concurrent-final-slot", "book-payments", "two-cluster-admin-calls", "ScaleService concurrent", map[string]int{"wins": 1, "denials": 1}, map[string]int{"wins": wins, "denials": denials}, map[string]int{"each_replica_delta": 1}, u, wins == 1 && denials == 1 && u.Replicas == 3 && u.CPUMillicores == 300 && u.MemoryBytes == 192<<20 && u.Services == 2 && u.PublicPorts == 1)
	code, out = request(h, "POST", "/v1/secrets", "book-payments", admin, map[string]string{"name": "second", "value": "non-sensitive-fixture"})
	raw, _ = json.Marshal(out)
	check("secret-quota", "book-payments", "cluster-admin", "POST /v1/secrets", "409 secrets", out, 1, usage(s, "book-payments"), code == 409 && bytes.Contains(raw, []byte(`"resource":"secrets"`)) && !bytes.Contains(raw, []byte("non-sensitive-fixture")))
	for i, id := range []string{"robot-one", "robot-two"} {
		code, out = request(h, "POST", "/v1/registry-credentials", "book-payments", admin, map[string]string{"id": id, "registry": "registry.example.test", "username": "fixture-robot", "password": "non-sensitive-password"})
		expected := 201
		if i == 1 {
			expected = 409
		}
		raw, _ = json.Marshal(out)
		check("registry-quota-"+id, "book-payments", "cluster-admin", "POST /v1/registry-credentials", expected, out, 1, usage(s, "book-payments"), code == expected && !bytes.Contains(raw, []byte("non-sensitive-password")))
	}
	zero := controlplane.NewMemoryService()
	zctx := namespace.WithContext(ctx, "default")
	_, _, err = zero.SetResourceQuota(zctx, types.ResourceQuota{})
	must(err)
	zspec := spec("unlimited", "zero")
	zspec.Replicas = 1000
	_, err = zero.CreateService(zctx, zspec)
	must(err)
	zu := usage(zero, "default")
	check("zero-is-unlimited", "default", "direct-library", "CreateService under all0limits", "1000replicas accepted", zu, 1000, zu, zu.Replicas == 1000)
	must(s.DeleteService(namespace.WithContext(ctx, "book-payments"), c.ID))
	u = usage(s, "book-payments")
	left, err := s.GetService(namespace.WithContext(ctx, "book-payments"), a.ID)
	must(err)
	check("deleted-release", "book-payments", "cluster-admin", "DeleteService", "deleted service excluded", u, nil, u, u.Services == 1 && u.Replicas == left.Spec.Replicas)
	code, out = request(h, "DELETE", "/v1/namespaces/default", "", admin, nil)
	check("default-undeletable", "default", "cluster-admin", "DELETE /v1/namespaces/default", 400, code, nil, nil, code == 400)
	must(s.DeleteService(namespace.WithContext(ctx, "book-observability"), b.ID))
	must(s.DeleteSecret(namespace.WithContext(ctx, "book-observability"), "shared"))
	code, out = request(h, "DELETE", "/v1/namespaces/book-observability", "", admin, nil)
	check("history-blocks-namespace-delete", "book-observability", "cluster-admin", "DELETE /v1/namespaces/book-observability", 409, out, nil, usage(s, "book-observability"), code == 409)
	code, out = request(h, "GET", "/v1/usage?namespace=book-observability", "book-payments", admin, nil)
	check("usage-query-conflict", "book-payments", "cluster-admin", "GET /v1/usage?namespace=book-observability with payments header", 404, out, nil, nil, code == 404)
	independent := controlplane.NewMemoryService()
	h2 := api.NewHandler(logger, independent, api.WithUserJWT("book-only-not-a-live-secret"))
	code, out = request(h2, "GET", "/v1/services/"+string(a.ID), "book-payments", admin, nil)
	other, err := independent.ListNamespaces(ctx)
	must(err)
	check("independent-servers-no-shared-state", "book-payments", "same-cluster-admin-config", "second independently constructed handler GET /v1/services/{A-ID}", 404, out, nil, map[string]any{"server_b_namespaces": other}, code == 404 && len(other) == 1)
	if len(cases) < 10 {
		panic("too few cases")
	}
	data := map[string]any{"source_sha": "cbfc94ade5b57e449d6b73bf1485b1c5b1647022", "classification": "teaching extension", "scope": "real in-process HTTP handlers and MemoryService; no connected network host, daemon or database", "cases": cases, "case_count": len(cases), "postgresql_quota_test": "not executed; separate transaction-advisory-lock prerequisite", "schema_note": "ServiceSpec has no arbitrary labels field; tenant markers use supported Env and fixture labels", "discrepancies": []string{"API query fallback exists despite documentation wording header/default", "conflicting usage query and selected header returns not-found", "quota Used/Requested are projected totals, not old total/delta"}, "cleanup": "process-local state discarded; namespace deletion blocked by retained service/history, no unsafe map/database deletion"}
	encoded, err := json.MarshalIndent(data, "", "  ")
	must(err)
	if strings.Contains(string(encoded), "Bearer ") {
		panic("token output")
	}
	fmt.Fprintln(os.Stdout, string(encoded))
}
