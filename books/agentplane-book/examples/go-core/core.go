// SPDX-License-Identifier: MIT
// Package core contains in-memory teaching examples, not distributed services.
package core

import (
	"errors"
	"sync"
	"time"
)

var (
	ErrStale      = errors.New("stale intent version")
	ErrTransition = errors.New("invalid state transition")
	ErrDenied     = errors.New("approval denied")
	ErrLimit      = errors.New("quota exhausted")
	ErrInvalid    = errors.New("invalid input")
)

type State string

const (
	Requested    State = "requested"
	Provisioning State = "provisioning"
	Ready        State = "ready"
	Terminating  State = "terminating"
	Terminated   State = "terminated"
	Failed       State = "failed"
)

// Session protects a small local state machine. Version is an intent revision,
// not a substitute for recipient-side fencing in a real distributed system.
type Session struct {
	mu      sync.Mutex
	state   State
	version uint64
}

func NewSession() *Session { return &Session{state: Requested, version: 1} }
func (s *Session) Snapshot() (State, uint64) {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.state, s.version
}
func (s *Session) Transition(expected uint64, next State) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if expected != s.version {
		return ErrStale
	}
	if next == s.state {
		return nil
	}
	allowed := map[State]map[State]bool{
		Requested:    {Provisioning: true, Terminating: true, Failed: true},
		Provisioning: {Ready: true, Terminating: true, Failed: true},
		Ready:        {Terminating: true, Failed: true},
		Terminating:  {Terminated: true, Failed: true},
		Failed:       {Terminating: true},
	}
	if !allowed[s.state][next] {
		return ErrTransition
	}
	s.state = next
	s.version++
	return nil
}

// Binding values must be derived from authenticated, validated request context.
// InputDigest requires a canonicalization contract at the real API boundary.
type Binding struct {
	Organization, Project, Actor, Session, Server, Tool string
	InputDigest, PolicyVersion, Operation               string
}

func (b Binding) valid() bool {
	return b.Organization != "" && b.Project != "" && b.Actor != "" &&
		b.Session != "" && b.Server != "" && b.Tool != "" && b.InputDigest != "" &&
		b.PolicyVersion != "" && b.Operation != ""
}

type approval struct {
	binding  Binding
	expires  time.Time
	consumed bool
}
type ApprovalStore struct {
	mu      sync.Mutex
	entries map[string]approval
}

func NewApprovalStore() *ApprovalStore {
	return &ApprovalStore{entries: make(map[string]approval)}
}

// Grant is an internal operation: a real service must authorize the approver.
func (s *ApprovalStore) Grant(id string, b Binding, expires, now time.Time) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if id == "" || !b.valid() || !expires.After(now) {
		return ErrInvalid
	}
	if _, exists := s.entries[id]; exists {
		return ErrDenied
	}
	s.entries[id] = approval{binding: b, expires: expires}
	return nil
}

// Consume is single-use. It does not execute a tool or prove exactly-once effects.
func (s *ApprovalStore) Consume(id string, b Binding, now time.Time) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	a, ok := s.entries[id]
	if !ok || a.consumed || !now.Before(a.expires) || a.binding != b {
		return ErrDenied
	}
	a.consumed = true
	s.entries[id] = a
	return nil
}

type Scope struct{ Organization, Project string }
type reservation struct {
	Scope     Scope
	Operation string
}
type Ledger struct {
	mu     sync.Mutex
	limit  int
	used   map[Scope]int
	active map[reservation]bool
	// Retain completed identities so a delayed retry cannot reserve again.
	released map[reservation]bool
}

func NewLedger(limit int) (*Ledger, error) {
	if limit < 0 {
		return nil, ErrInvalid
	}
	return &Ledger{limit: limit, used: make(map[Scope]int),
		active: make(map[reservation]bool), released: make(map[reservation]bool)}, nil
}
func (l *Ledger) Reserve(scope Scope, op string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if scope.Organization == "" || scope.Project == "" || op == "" {
		return ErrInvalid
	}
	k := reservation{scope, op}
	if l.released[k] {
		return ErrStale
	}
	if l.active[k] {
		return nil
	}
	if l.used[scope] >= l.limit {
		return ErrLimit
	}
	l.active[k] = true
	l.used[scope]++
	return nil
}
func (l *Ledger) Release(scope Scope, op string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	k := reservation{scope, op}
	if l.active[k] {
		delete(l.active, k)
		l.released[k] = true
		l.used[scope]--
	}
}
func (l *Ledger) Used(scope Scope) int {
	l.mu.Lock()
	defer l.mu.Unlock()
	return l.used[scope]
}
