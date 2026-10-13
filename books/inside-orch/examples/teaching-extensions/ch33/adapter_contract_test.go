// Teaching extension: adapter seam and proposed handshake contract, not an RPC plugin loader.
package adaptercontract

import (
	"context"
	"errors"
	"fmt"
	d "github.com/alekpopovic/orch/internal/docker"
	"github.com/alekpopovic/orch/internal/secrets"
	"testing"
	"time"
)

type Handshake struct {
	ProtocolMajor int
	Kind          string
	Capabilities  []string
}

// ValidateHandshake is a deliberately small design exercise. It neither loads nor executes plugins.
func ValidateHandshake(h Handshake, kind string, required ...string) error {
	if h.ProtocolMajor != 1 {
		return fmt.Errorf("unsupported protocol major %d", h.ProtocolMajor)
	}
	if h.Kind != kind {
		return fmt.Errorf("wrong plugin kind")
	}
	for _, needed := range required {
		found := false
		for _, c := range h.Capabilities {
			if c == needed {
				found = true
			}
		}
		if !found {
			return fmt.Errorf("missing capability %s", needed)
		}
	}
	return nil
}
func TestHandshakeRejectsBeforeEffects(t *testing.T) {
	for _, tc := range []struct {
		name   string
		h      Handshake
		reject bool
	}{
		{"compatible", Handshake{1, "runtime", []string{"task-idempotency", "cancel"}}, false},
		{"new-major", Handshake{2, "runtime", []string{"task-idempotency", "cancel"}}, true},
		{"wrong-kind", Handshake{1, "secrets", []string{"task-idempotency", "cancel"}}, true},
		{"missing-capability", Handshake{1, "runtime", []string{"cancel"}}, true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			err := ValidateHandshake(tc.h, "runtime", "task-idempotency", "cancel")
			if (err != nil) != tc.reject {
				t.Fatalf("rejection=%v error=%v", tc.reject, err)
			}
		})
	}
}
func TestRuntimeContractReplayCancellationAndCleanup(t *testing.T) {
	var r d.Runtime = d.NewFakeRuntime()
	ctx := context.Background()
	spec := d.ContainerSpec{Name: "atlas-contract", Image: "fixture-image", ServiceID: "atlas", TaskID: "same-operation", NodeID: "node-fixture", Version: 1}
	first, err := r.CreateContainer(ctx, spec)
	if err != nil {
		t.Fatal(err)
	}
	second, err := r.CreateContainer(ctx, spec)
	if err != nil || first != second {
		t.Fatalf("replay changed identity %q %q %v", first, second, err)
	}
	canceled, cancel := context.WithCancel(ctx)
	cancel()
	if _, err := r.CreateContainer(canceled, d.ContainerSpec{Name: "late", Image: "fixture-image", TaskID: "late"}); !errors.Is(err, context.Canceled) {
		t.Fatalf("cancellation not honored %v", err)
	}
	if err := r.StartContainer(ctx, first); err != nil {
		t.Fatal(err)
	}
	if err := r.StopContainer(ctx, first, time.Second); err != nil {
		t.Fatal(err)
	}
	if err := r.RemoveContainer(ctx, first, false); err != nil {
		t.Fatal(err)
	}
	all, err := r.ListManagedContainers(ctx, nil)
	if err != nil || len(all) != 0 {
		t.Fatalf("residual fake containers=%d error=%v", len(all), err)
	}
}
func TestEnvelopeWrongKeyAndCanceledRequest(t *testing.T) {
	a, err := secrets.NewLocalEnvelope("atlas-fixture-a")
	if err != nil {
		t.Fatal(err)
	}
	b, err := secrets.NewLocalEnvelope("atlas-fixture-b")
	if err != nil {
		t.Fatal(err)
	}
	ciphertext, err := a.Encrypt(context.Background(), []byte("synthetic-only"))
	if err != nil {
		t.Fatal(err)
	}
	if _, err := b.Decrypt(context.Background(), ciphertext); err == nil {
		t.Fatal("wrong key accepted")
	}
	canceled, cancel := context.WithCancel(context.Background())
	cancel()
	if _, err := a.Decrypt(canceled, ciphertext); !errors.Is(err, context.Canceled) {
		t.Fatalf("cancellation=%v", err)
	}
}
