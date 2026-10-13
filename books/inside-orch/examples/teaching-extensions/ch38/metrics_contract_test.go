// Teaching fixture: actual instrumented FakeRuntime and collector exposition; no Prometheus evaluator.
package metricscontract

import (
	"context"
	"errors"
	d "github.com/alekpopovic/orch/internal/docker"
	"github.com/alekpopovic/orch/internal/metrics"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestFailedPullExposesCountedOperation(t *testing.T) {
	m := metrics.NewAgent()
	fault := errors.New("synthetic pull failure")
	runtime := d.WithMetrics(d.NewFakeRuntime(d.WithFakePullFailure(fault)), m)
	if err := runtime.PullImage(context.Background(), "fixture-only", nil); !errors.Is(err, fault) {
		t.Fatalf("wrong error %v", err)
	}
	rec := httptest.NewRecorder()
	m.Handler().ServeHTTP(rec, httptest.NewRequest("GET", "/metrics", nil))
	if rec.Code != 200 {
		t.Fatal(rec.Code)
	}
	for _, want := range []string{`docker_operations_total{operation="pull_image"} 1`, `docker_operation_errors_total{operation="pull_image"} 1`} {
		if !strings.Contains(rec.Body.String(), want) {
			t.Fatalf("missing %s", want)
		}
		t.Log(want)
	}
}
