// SPDX-License-Identifier: MIT
package lab

import (
	"regexp"
	"time"
)

var digestPattern = regexp.MustCompile(`^sha256:[0-9a-f]{64}$`)

type Subject struct{ Project, Environment, ArtifactDigest, ConfigDigest, PolicyRevision string }
type Approval struct {
	Subject   Subject
	Approver  string
	ExpiresAt time.Time
	Revoked   bool
}

func (s Subject) valid() bool {
	return s.Project != "" && s.Environment != "" && s.PolicyRevision != "" && digestPattern.MatchString(s.ArtifactDigest) && digestPattern.MatchString(s.ConfigDigest)
}

// Allows compares immutable identity. Current membership/policy is checked by caller.
func (a Approval) Allows(wanted Subject, now time.Time) bool {
	return a.Subject.valid() && wanted.valid() && a.Approver != "" && !a.Revoked && now.Before(a.ExpiresAt) && a.Subject == wanted
}
