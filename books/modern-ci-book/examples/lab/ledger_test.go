package lab

import (
	"errors"
	"sync"
	"testing"
	"time"
)

var t0 = time.Date(2026, 10, 10, 0, 0, 0, 0, time.UTC)

func started(t *testing.T) (*Ledger, Claim) {
	t.Helper()
	l := NewLedger()
	if e := l.Add("j"); e != nil {
		t.Fatal(e)
	}
	c, e := l.Claim("j", "r", t0, time.Minute)
	if e != nil {
		t.Fatal(e)
	}
	if e = l.Start(c, t0); e != nil {
		t.Fatal(e)
	}
	return l, c
}
func TestSingleConcurrentClaim(t *testing.T) {
	l := NewLedger()
	_ = l.Add("j")
	var wg sync.WaitGroup
	results := make(chan error, 30)
	for i := 0; i < 30; i++ {
		wg.Add(1)
		go func() { defer wg.Done(); _, e := l.Claim("j", "r", t0, time.Minute); results <- e }()
	}
	wg.Wait()
	close(results)
	n := 0
	for e := range results {
		if e == nil {
			n++
		}
	}
	if n != 1 {
		t.Fatalf("claims=%d", n)
	}
}
func TestExpiryDoesNotRequeue(t *testing.T) {
	l, _ := started(t)
	if n := l.Expire(t0.Add(time.Minute)); n != 1 {
		t.Fatal(n)
	}
	if l.State("j") != "uncertain" || l.Retry("j") == nil {
		t.Fatal("unsafe retry")
	}
}
func TestStaleCompletion(t *testing.T) {
	l, c := started(t)
	l.Expire(t0.Add(time.Minute))
	_ = l.ReconcileStopped(c, "failed")
	_ = l.Retry("j")
	n, e := l.Claim("j", "other", t0.Add(time.Minute), time.Minute)
	if e != nil {
		t.Fatal(e)
	}
	_ = l.Start(n, t0.Add(time.Minute))
	if e = l.Complete(c, "succeeded", t0.Add(time.Minute)); !errors.Is(e, ErrStale) {
		t.Fatal(e)
	}
	if n.Fence <= c.Fence {
		t.Fatal("non-monotonic fence")
	}
	old, _ := l.Snapshot(c.Attempt)
	if old.Outcome != "failed" {
		t.Fatal("history overwritten")
	}
}
func TestDuplicateCompletion(t *testing.T) {
	l, c := started(t)
	if e := l.Complete(c, "succeeded", t0); e != nil {
		t.Fatal(e)
	}
	if e := l.Complete(c, "succeeded", t0.Add(time.Hour)); e != nil {
		t.Fatal(e)
	}
	if e := l.Complete(c, "failed", t0); !errors.Is(e, ErrConflict) {
		t.Fatal(e)
	}
}
func TestExpiredCompletion(t *testing.T) {
	l, c := started(t)
	if e := l.Complete(c, "succeeded", t0.Add(time.Minute)); !errors.Is(e, ErrExpired) {
		t.Fatal(e)
	}
}
func TestRunnerIdentity(t *testing.T) {
	l, c := started(t)
	c.Runner = "imposter"
	if e := l.Complete(c, "succeeded", t0); !errors.Is(e, ErrStale) {
		t.Fatal(e)
	}
}
func TestFenceIdentity(t *testing.T) {
	l, c := started(t)
	c.Fence++
	if e := l.Heartbeat(c, t0, time.Minute); !errors.Is(e, ErrStale) {
		t.Fatal(e)
	}
}
func TestCancellationIsRequest(t *testing.T) {
	l, c := started(t)
	if e := l.RequestCancel("j"); e != nil {
		t.Fatal(e)
	}
	if l.State("j") != "cancel_requested" {
		t.Fatal("premature terminal status")
	}
	if e := l.Complete(c, "cancelled", t0); e != nil {
		t.Fatal(e)
	}
}
func TestCancelCanRaceSuccess(t *testing.T) {
	l, c := started(t)
	_ = l.RequestCancel("j")
	if e := l.Complete(c, "succeeded", t0); e != nil {
		t.Fatal(e)
	}
}
func TestExpiredHeartbeatCannotResurrect(t *testing.T) {
	l, c := started(t)
	if e := l.Heartbeat(c, t0.Add(time.Minute), time.Minute); !errors.Is(e, ErrExpired) {
		t.Fatal(e)
	}
}
func TestHeartbeatExtends(t *testing.T) {
	l, c := started(t)
	if e := l.Heartbeat(c, t0.Add(30*time.Second), time.Minute); e != nil {
		t.Fatal(e)
	}
	if l.Expire(t0.Add(time.Minute)) != 0 {
		t.Fatal("extension lost")
	}
}
func TestClaimValidation(t *testing.T) {
	l := NewLedger()
	if l.Add("") == nil {
		t.Fatal("empty job")
	}
	_ = l.Add("j")
	if l.Add("j") == nil {
		t.Fatal("duplicate job")
	}
	if _, e := l.Claim("j", "", t0, time.Minute); e == nil {
		t.Fatal("empty runner")
	}
	if _, e := l.Claim("j", "r", t0, 0); e == nil {
		t.Fatal("zero ttl")
	}
}
func TestCannotCompleteBeforeStart(t *testing.T) {
	l := NewLedger()
	_ = l.Add("j")
	c, _ := l.Claim("j", "r", t0, time.Minute)
	if l.Complete(c, "succeeded", t0) == nil {
		t.Fatal("no start observation")
	}
}
func TestRetryCannotAcceptPreviousResult(t *testing.T) {
	l, c := started(t)
	_ = l.Complete(c, "failed", t0)
	_ = l.Retry("j")
	if !errors.Is(l.Complete(c, "failed", t0), ErrStale) {
		t.Fatal("queued state changed by old result")
	}
}
