// SPDX-License-Identifier: MIT
package lab

import (
	"errors"
	"fmt"
	"sync"
	"time"
)

var (
	ErrState    = errors.New("invalid state")
	ErrStale    = errors.New("stale claim")
	ErrExpired  = errors.New("lease expired")
	ErrConflict = errors.New("conflicting completion")
)

type Claim struct {
	Job, Attempt, Runner string
	Fence                uint64
}
type Attempt struct {
	Claim          Claim
	State, Outcome string
	LeaseUntil     time.Time
}
type jobRecord struct {
	state, current string
	generation     uint64
}

// Ledger is a process-local model. Its mutex does not coordinate other processes.
// The model requires trusted caller-supplied time and authorization outside the API.
type Ledger struct {
	mu       sync.Mutex
	jobs     map[string]*jobRecord
	attempts map[string]*Attempt
}

func NewLedger() *Ledger {
	return &Ledger{jobs: map[string]*jobRecord{}, attempts: map[string]*Attempt{}}
}
func (l *Ledger) Add(job string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if job == "" || l.jobs[job] != nil {
		return ErrState
	}
	l.jobs[job] = &jobRecord{state: "queued"}
	return nil
}
func (l *Ledger) Claim(job, runner string, now time.Time, ttl time.Duration) (Claim, error) {
	l.mu.Lock()
	defer l.mu.Unlock()
	j := l.jobs[job]
	if j == nil || j.state != "queued" || runner == "" || ttl <= 0 {
		return Claim{}, ErrState
	}
	j.generation++
	c := Claim{Job: job, Attempt: fmt.Sprintf("%s/%d", job, j.generation), Runner: runner, Fence: j.generation}
	l.attempts[c.Attempt] = &Attempt{Claim: c, State: "leased", LeaseUntil: now.Add(ttl)}
	j.current = c.Attempt
	j.state = "leased"
	return c, nil
}
func active(state string) bool {
	return state == "leased" || state == "running" || state == "cancel_requested"
}
func terminal(state string) bool {
	return state == "succeeded" || state == "failed" || state == "cancelled"
}
func (l *Ledger) current(c Claim) (*jobRecord, *Attempt, error) {
	j := l.jobs[c.Job]
	a := l.attempts[c.Attempt]
	if j == nil || a == nil || j.current != c.Attempt || a.Claim != c {
		return nil, nil, ErrStale
	}
	return j, a, nil
}
func (l *Ledger) Start(c Claim, now time.Time) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j, a, e := l.current(c)
	if e != nil {
		return e
	}
	if j.state != "leased" || a.State != "leased" {
		return ErrState
	}
	if !now.Before(a.LeaseUntil) {
		return ErrExpired
	}
	j.state = "running"
	a.State = "running"
	return nil
}
func (l *Ledger) Heartbeat(c Claim, now time.Time, ttl time.Duration) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j, a, e := l.current(c)
	if e != nil {
		return e
	}
	if !active(j.state) || !active(a.State) || ttl <= 0 {
		return ErrState
	}
	if !now.Before(a.LeaseUntil) {
		return ErrExpired
	}
	proposed := now.Add(ttl)
	if proposed.After(a.LeaseUntil) {
		a.LeaseUntil = proposed
	}
	return nil
}
func (l *Ledger) Complete(c Claim, outcome string, now time.Time) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j, a, e := l.current(c)
	if e != nil {
		return e
	}
	if !terminal(outcome) {
		return ErrState
	}
	if terminal(a.State) {
		if j.state != a.State {
			return ErrStale
		}
		if a.Outcome == outcome {
			return nil
		}
		return ErrConflict
	}
	if (a.State != "running" && a.State != "cancel_requested") || j.state != a.State {
		return ErrState
	}
	if !now.Before(a.LeaseUntil) {
		return ErrExpired
	}
	a.State = outcome
	a.Outcome = outcome
	j.state = outcome
	return nil
}
func (l *Ledger) RequestCancel(job string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j := l.jobs[job]
	if j == nil {
		return ErrState
	}
	if j.state == "queued" {
		j.state = "cancelled"
		return nil
	}
	if j.state == "cancel_requested" {
		return nil
	}
	if j.state != "leased" && j.state != "running" {
		return ErrState
	}
	j.state = "cancel_requested"
	l.attempts[j.current].State = "cancel_requested"
	return nil
}
func (l *Ledger) Expire(now time.Time) int {
	l.mu.Lock()
	defer l.mu.Unlock()
	n := 0
	for _, j := range l.jobs {
		a := l.attempts[j.current]
		if a != nil && active(j.state) && !now.Before(a.LeaseUntil) {
			j.state = "uncertain"
			a.State = "uncertain"
			n++
		}
	}
	return n
}

// ReconcileStopped represents a separately authorized operator observation.
// A real implementation must persist who observed what and verify the target.
func (l *Ledger) ReconcileStopped(c Claim, outcome string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j, a, e := l.current(c)
	if e != nil {
		return e
	}
	if j.state != "uncertain" || a.State != "uncertain" || !terminal(outcome) {
		return ErrState
	}
	a.State = outcome
	a.Outcome = outcome
	j.state = outcome
	return nil
}
func (l *Ledger) Retry(job string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	j := l.jobs[job]
	if j == nil || (j.state != "failed" && j.state != "cancelled") {
		return ErrState
	}
	j.state = "queued"
	return nil
}
func (l *Ledger) State(job string) string {
	l.mu.Lock()
	defer l.mu.Unlock()
	if j := l.jobs[job]; j != nil {
		return j.state
	}
	return "missing"
}
func (l *Ledger) Snapshot(id string) (Attempt, bool) {
	l.mu.Lock()
	defer l.mu.Unlock()
	a, ok := l.attempts[id]
	if !ok {
		return Attempt{}, false
	}
	return *a, true
}
