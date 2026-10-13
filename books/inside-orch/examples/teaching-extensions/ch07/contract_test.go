package contract_test

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/alekpopovic/orch/internal/api"
	"github.com/alekpopovic/orch/internal/controlplane"
	"github.com/alekpopovic/orch/pkg/client"
	"github.com/alekpopovic/orch/pkg/types"
)

// Teaching smoke test; real pinned handler/client, memory only, no Docker/database.
func TestAtlasPublicContract(t *testing.T) {
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	server := httptest.NewServer(api.NewHandler(logger, controlplane.NewMemoryService()))
	defer server.Close()
	c, err := client.New(server.URL)
	if err != nil {
		t.Fatal(err)
	}
	ctx := context.Background()
	service, err := c.CreateService(ctx, types.ServiceSpec{Name: "atlas-api", Image: "nginx:1.27", Replicas: 1})
	if err != nil {
		t.Fatal(err)
	}
	if service.ID == "" || service.Spec.Name != "atlas-api" {
		t.Fatalf("bad service: %#v", service)
	}
	_, err = c.GetService(ctx, "not-a-uuid")
	var rejected *client.APIError
	if !errors.As(err, &rejected) || rejected.StatusCode != 400 || rejected.Code != "invalid_argument" || rejected.RequestID == "" {
		t.Fatalf("bad rejection: %#v", err)
	}
	t.Logf("public client rejection: status=%d code=%s request_id_present=%t", rejected.StatusCode, rejected.Code, rejected.RequestID != "")
	request, _ := http.NewRequest(http.MethodPost, server.URL+"/v1/services", bytes.NewBufferString(`{"spec":{"name":"bad","image":"nginx:1.27","replicas":1},"surprise":true}`))
	response, err := http.DefaultClient.Do(request)
	if err != nil {
		t.Fatal(err)
	}
	if response.StatusCode != 400 || response.Header.Get("API-Version") != "v1" {
		t.Fatalf("bad strict request: %d", response.StatusCode)
	}
	response.Body.Close()
	response, err = http.Get(server.URL + "/v2/services")
	if err != nil {
		t.Fatal(err)
	}
	if response.StatusCode != 404 {
		t.Fatal("v2 unexpectedly exists")
	}
	response.Body.Close()
	protected := httptest.NewServer(api.NewHandler(logger, controlplane.NewMemoryService(), api.WithUserJWT("book-synthetic-only")))
	defer protected.Close()
	pc, _ := client.New(protected.URL)
	_, err = pc.ListServices(ctx)
	if !errors.As(err, &rejected) || rejected.StatusCode != 401 || rejected.Code != "unauthorized" {
		t.Fatalf("auth bypass: %#v", err)
	}
}

func TestAtlasAdditiveResponseCompatibility(t *testing.T) {
	// Controlled response fixtures demonstrate client decoding, not new server behavior.
	for _, tc := range []struct {
		name, body string
		wantName   string
	}{
		{"additive", `{"service":{"id":"example","spec":{"name":"atlas-api","image":"nginx:1.27","replicas":1}},"future_hint":{"safe":true}}`, "atlas-api"},
		{"renamed", `{"service":{"id":"example","spec":{"service_name":"atlas-api","image":"nginx:1.27","replicas":1}}}`, ""},
	} {
		t.Run(tc.name, func(t *testing.T) {
			fixture := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.Header().Set("Content-Type", "application/json")
				io.WriteString(w, tc.body)
			}))
			defer fixture.Close()
			c, _ := client.New(fixture.URL)
			got, err := c.GetService(context.Background(), "example")
			if err != nil {
				t.Fatal(err)
			}
			if got.Spec.Name != tc.wantName {
				t.Fatalf("name=%q wanted%q", got.Spec.Name, tc.wantName)
			}
			b, _ := json.Marshal(map[string]any{"fixture": tc.name, "decoded_name": got.Spec.Name})
			t.Log(string(b))
		})
	}
}

func TestAtlasRawZeroResourceHTTP(t *testing.T) {
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	server := httptest.NewServer(api.NewHandler(logger, controlplane.NewMemoryService()))
	defer server.Close()
	raw := types.ServiceSpec{Name: "atlas-raw-zero", Image: "nginx:1.27", Replicas: 1}
	payload, err := json.Marshal(map[string]any{"spec": raw})
	if err != nil {
		t.Fatal(err)
	}
	response, err := http.Post(server.URL+"/v1/services", "application/json", bytes.NewReader(payload))
	if err != nil {
		t.Fatal(err)
	}
	defer response.Body.Close()
	var rejected client.ErrorResponse
	if err = json.NewDecoder(response.Body).Decode(&rejected); err != nil {
		t.Fatal(err)
	}
	if response.StatusCode != 400 || rejected.Error.Code != "invalid_argument" {
		t.Fatalf("zero resources unexpectedly accepted: status%d code%s", response.StatusCode, rejected.Error.Code)
	}
	t.Logf("raw-zero serialization rejected: status=%d code=%s", response.StatusCode, rejected.Error.Code)
	// The actual public client normalizes these same zero values before serialization.
	c, _ := client.New(server.URL)
	service, err := c.CreateService(context.Background(), raw)
	if err != nil {
		t.Fatal(err)
	}
	if service.Spec.ResourceRequirements.Requests.CPU != 100 {
		t.Fatal("client failed to normalize defaults")
	}
}
