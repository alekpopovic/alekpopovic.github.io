// Book teaching extension: exercises locked packages without modifying application files.
package main

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/alekpopovic/orch/internal/leadership"
	"github.com/alekpopovic/orch/internal/migrations"
	"github.com/alekpopovic/orch/internal/secrets"
	"github.com/alekpopovic/orch/internal/store"
	"github.com/alekpopovic/orch/pkg/types"
	"github.com/jackc/pgx/v5/pgxpool"
	"os"
	"strings"
	"time"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func check(ok bool, name string) {
	if !ok {
		panic(name)
	}
}
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	url := os.Getenv("INSIDE_ORCH_LAB_DATABASE_URL")
	check(strings.Contains(url, "/inside_orch_lab_") && strings.Contains(url, "127.0.0.1:"), "explicit lab URL required; external ownership guard also mandatory")
	r, err := migrations.Open(ctx, url, "migrations")
	must(err)
	defer r.Close()
	mode := "prepare"
	if len(os.Args) > 1 {
		mode = os.Args[1]
	}
	result := map[string]any{"mode": mode, "started_at_utc": time.Now().UTC(), "scope": "teaching extension against full-schema PostgreSQL package, not default server persistence"}
	if mode == "prepare" {
		before, err := r.Status(ctx)
		must(err)
		check(len(before.Pending) == 16, "fresh database must have 16 pending migrations")
		must(r.Up(ctx))
		after, err := r.Status(ctx)
		must(err)
		check(after.Current == "000016" && len(after.Pending) == 0, "all16 up")
		must(r.Up(ctx))
		twice, err := r.Status(ctx)
		must(err)
		check(twice.Current == after.Current && len(twice.Pending) == 0, "up idempotence")
		err = r.Down(ctx, false)
		check(err != nil && strings.Contains(err.Error(), "--allow-down"), "down refused")
		pool, err := store.ConnectPostgres(ctx, url)
		must(err)
		defer pool.Close()
		s := store.NewPostgresStore(pool)
		n, err := s.CreateNode(ctx, types.NodeSpec{Hostname: "book-claim-node", AdvertiseAddress: "127.0.0.1", Capacity: types.Resources{CPU: 4000, Memory: 1073741824}, Allocatable: types.Resources{CPU: 4000, Memory: 1073741824}})
		must(err)
		svc, err := s.CreateService(ctx, types.ServiceSpec{Name: "book-recovery", Image: "nginx:1.27-alpine", Replicas: 1})
		must(err)
		task, err := s.CreateTask(ctx, types.Task{ServiceID: svc.ID, DesiredStatus: types.TaskRunning, ActualStatus: types.TaskPending, Image: svc.Spec.Image, Version: svc.DeploymentVersion})
		must(err)
		outcomes := make(chan error, 2)
		start := make(chan struct{})
		for i := 0; i < 2; i++ {
			go func() { <-start; _, err := s.AssignTask(ctx, task.ID, n.ID, nil, task.UpdatedAt); outcomes <- err }()
		}
		close(start)
		winners, conflicts := 0, 0
		for i := 0; i < 2; i++ {
			err := <-outcomes
			if err == nil {
				winners++
			} else if errors.Is(err, store.ErrConflict) {
				conflicts++
			} else {
				must(err)
			}
		}
		check(winners == 1 && conflicts == 1, "exactly one per-task claim")
		env, err := secrets.NewLocalEnvelope("book-only-recovery-key")
		must(err)
		canary := make([]byte, 32)
		_, err = rand.Read(canary)
		must(err)
		cipher, err := env.Encrypt(ctx, canary)
		must(err)
		_, err = s.CreateSecret(ctx, types.Secret{Name: "book-canary", KeyID: cipher.KeyID, EncryptedValue: cipher.Data})
		must(err)
		digest := sha256.Sum256(canary)
		result["canary_sha256"] = hex.EncodeToString(digest[:])
		result["schema_before"] = before
		result["schema_after"] = after
		result["schema_after_second_up"] = twice
		result["down_without_allow_rejected"] = true
		result["claims"] = map[string]int{"winners": winners, "conflicts": conflicts}
		result["captured_ids"] = map[string]any{"node": n.ID, "service": svc.ID, "task": task.ID}
		// Actual cancellation semantics with two independent pools, avoiding pool reuse as evidence.
		p1, err := pgxpool.New(ctx, url)
		must(err)
		p2, err := pgxpool.New(ctx, url)
		must(err)
		defer p2.Close()
		leaseCtx, leaseCancel := context.WithCancel(ctx)
		l, err := leadership.NewPostgresElector(p1).Acquire(leaseCtx, "inside-orch-book-cancel")
		must(err)
		_, heldErr := leadership.NewPostgresElector(p2).Acquire(ctx, "inside-orch-book-cancel")
		check(errors.Is(heldErr, leadership.ErrLockHeld), "second pool initially held")
		leaseCancel()
		select {
		case <-l.Done():
		case <-time.After(2 * time.Second):
			panic("lease cancellation timeout")
		}
		must(l.Release(ctx))
		_, afterCancel := leadership.NewPostgresElector(p2).Acquire(ctx, "inside-orch-book-cancel")
		retained := errors.Is(afterCancel, leadership.ErrLockHeld)
		check(retained, "expected inspected retained session lock; revisit if behavior changes")
		p1.Close()
		l2, err := leadership.NewPostgresElector(p2).Acquire(ctx, "inside-orch-book-cancel")
		must(err)
		must(l2.Release(ctx))
		result["leadership"] = map[string]any{"other_pool_initially_blocked": true, "done_closed_after_cancel": true, "lock_retained_after_cancel_and_release": retained, "other_pool_acquires_after_original_pool_close": true, "scope": "package cancellation path with healthy pooled session, not running server HA"}
	} else if mode == "verify" {
		status, err := r.Status(ctx)
		must(err)
		check(status.Current == "000016" && len(status.Pending) == 0, "restored schema16")
		pool, err := store.ConnectPostgres(ctx, url)
		must(err)
		defer pool.Close()
		s := store.NewPostgresStore(pool)
		services, err := s.ListServices(ctx)
		must(err)
		nodes, err := s.ListNodesByStatus(ctx, types.NodeUnknown)
		must(err)
		check(len(services) == 1 && len(nodes) == 1, "restored rows")
		secret, err := s.GetSecret(ctx, "book-canary")
		must(err)
		env, err := secrets.NewLocalEnvelope("book-only-recovery-key")
		must(err)
		plain, err := env.Decrypt(ctx, secrets.Ciphertext{KeyID: secret.KeyID, Data: secret.EncryptedValue})
		must(err)
		digest := sha256.Sum256(plain)
		wrong, err := secrets.NewLocalEnvelope("book-only-wrong-key")
		must(err)
		_, err = wrong.Decrypt(ctx, secrets.Ciphertext{KeyID: secret.KeyID, Data: secret.EncryptedValue})
		check(err != nil, "wrong key must reject")
		result["canary_sha256"] = hex.EncodeToString(digest[:])
		result["schema"] = status
		result["row_counts"] = map[string]int{"services": len(services), "nodes": len(nodes)}
		result["wrong_key_rejected"] = true
	} else {
		panic("unknown mode")
	}
	result["status"] = "passed"
	result["finished_at_utc"] = time.Now().UTC()
	data, err := json.MarshalIndent(result, "", "  ")
	must(err)
	fmt.Println(string(data))
}
