// SPDX-License-Identifier: MIT
package core

import (
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestSessionLifecycle(t *testing.T) {
	s := NewSession()
	for _, next := range []State{Provisioning, Ready, Terminating, Terminated} {
		_, v := s.Snapshot()
		if err := s.Transition(v, next); err != nil {
			t.Fatal(err)
		}
	}
	_, v := s.Snapshot()
	if !errors.Is(s.Transition(v, Ready), ErrTransition) {
		t.Fatal("resurrection")
	}
	if err := s.Transition(v, Terminated); err != nil {
		t.Fatal("duplicate terminal", err)
	}
}
func TestStaleTransition(t *testing.T) {
	s := NewSession()
	_ = s.Transition(1, Provisioning)
	if !errors.Is(s.Transition(1, Ready), ErrStale) {
		t.Fatal("stale accepted")
	}
}
func TestInvalidTransitions(t *testing.T) {
	s := NewSession()
	for _, state := range []State{Ready, Terminated, "invented"} {
		if !errors.Is(s.Transition(1, state), ErrTransition) {
			t.Fatal(state)
		}
	}
}
func TestConcurrentTransition(t *testing.T) {
	s := NewSession()
	var accepted atomic.Int32
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if s.Transition(1, Provisioning) == nil {
				accepted.Add(1)
			}
		}()
	}
	wg.Wait()
	if accepted.Load() != 1 {
		t.Fatal(accepted.Load())
	}
}
func binding() Binding { return Binding{"a", "p", "actor", "s", "server", "tool", "hash", "v1", "op"} }
func TestApprovalBindingAndReplay(t *testing.T) {
	now := time.Unix(100, 0)
	s := NewApprovalStore()
	b := binding()
	if err := s.Grant("id", b, now.Add(time.Minute), now); err != nil {
		t.Fatal(err)
	}
	variants := []Binding{b, b, b, b, b, b, b, b, b}
	variants[0].Organization = "other"
	variants[1].Project = "other"
	variants[2].Actor = "other"
	variants[3].Session = "other"
	variants[4].Server = "other"
	variants[5].Tool = "other"
	variants[6].InputDigest = "other"
	variants[7].PolicyVersion = "v2"
	variants[8].Operation = "other"
	for _, v := range variants {
		if !errors.Is(s.Consume("id", v, now), ErrDenied) {
			t.Fatal(v)
		}
	}
	if err := s.Consume("id", b, now); err != nil {
		t.Fatal(err)
	}
	if !errors.Is(s.Consume("id", b, now), ErrDenied) {
		t.Fatal("replay")
	}
}
func TestApprovalExpiryAndOverwrite(t *testing.T) {
	now := time.Unix(100, 0)
	s := NewApprovalStore()
	b := binding()
	_ = s.Grant("id", b, now.Add(time.Minute), now)
	if !errors.Is(s.Grant("id", b, now.Add(time.Hour), now), ErrDenied) {
		t.Fatal("overwrite")
	}
	if !errors.Is(s.Consume("id", b, now.Add(time.Minute)), ErrDenied) {
		t.Fatal("expiry")
	}
	if !errors.Is(s.Grant("", b, now, now), ErrInvalid) {
		t.Fatal("invalid grant")
	}
}
func TestConcurrentApproval(t *testing.T) {
	now := time.Unix(100, 0)
	s := NewApprovalStore()
	b := binding()
	_ = s.Grant("id", b, now.Add(time.Minute), now)
	var n atomic.Int32
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if s.Consume("id", b, now) == nil {
				n.Add(1)
			}
		}()
	}
	wg.Wait()
	if n.Load() != 1 {
		t.Fatal(n.Load())
	}
}
func TestQuotaConcurrentReservations(t *testing.T) {
	l, _ := NewLedger(7)
	scope := Scope{"a", "p"}
	var n atomic.Int32
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			if l.Reserve(scope, fmt.Sprint(i)) == nil {
				n.Add(1)
			}
		}(i)
	}
	wg.Wait()
	if n.Load() != 7 || l.Used(scope) != 7 {
		t.Fatal(n.Load(), l.Used(scope))
	}
}
func TestQuotaIdentityAndRelease(t *testing.T) {
	l, _ := NewLedger(1)
	a := Scope{"a", "p"}
	b := Scope{"b", "p"}
	if l.Reserve(a, "same") != nil || l.Reserve(a, "same") != nil || l.Reserve(b, "same") != nil {
		t.Fatal("identity")
	}
	if l.Used(a) != 1 || l.Used(b) != 1 {
		t.Fatal("scope")
	}
	l.Release(a, "same")
	l.Release(a, "same")
	if l.Used(a) != 0 {
		t.Fatal("negative")
	}
	if !errors.Is(l.Reserve(a, "same"), ErrStale) {
		t.Fatal("released retry")
	}
}
func TestInvalidQuota(t *testing.T) {
	if _, err := NewLedger(-1); err == nil {
		t.Fatal("negative limit")
	}
	l, _ := NewLedger(0)
	if !errors.Is(l.Reserve(Scope{"a", "p"}, "op"), ErrLimit) {
		t.Fatal("zero limit")
	}
	if !errors.Is(l.Reserve(Scope{}, "op"), ErrInvalid) {
		t.Fatal("scope")
	}
}
