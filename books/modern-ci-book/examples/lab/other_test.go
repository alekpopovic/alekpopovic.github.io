package lab

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"strings"
	"testing"
	"time"
)

func signature(secret, body []byte) string {
	m := hmac.New(sha256.New, secret)
	m.Write(body)
	return "sha256=" + hex.EncodeToString(m.Sum(nil))
}
func TestWebhookExactBytes(t *testing.T) {
	secret := []byte("local-test-secret")
	body := []byte(`{"x":1}`)
	s := signature(secret, body)
	if !VerifySignature(secret, body, s) {
		t.Fatal("valid rejected")
	}
	if VerifySignature(secret, []byte(`{"x": 1}`), s) {
		t.Fatal("changed bytes accepted")
	}
}
func TestWebhookInvalid(t *testing.T) {
	for _, s := range []string{"", "sha1=abc", "sha256=xyz", "sha256=" + strings.Repeat("g", 64), "sha256=" + strings.Repeat("0", 64)} {
		if VerifySignature([]byte("s"), []byte("b"), s) {
			t.Fatal(s)
		}
	}
	if VerifySignature(nil, []byte("b"), signature(nil, []byte("b"))) {
		t.Fatal("empty secret")
	}
}
func TestLogRetryAndConflict(t *testing.T) {
	s, _ := NewLogStore(16, 32)
	d, e := s.Put(0, []byte("one"))
	if d || e != nil {
		t.Fatal(d, e)
	}
	d, e = s.Put(0, []byte("one"))
	if !d || e != nil {
		t.Fatal(d, e)
	}
	if _, e = s.Put(0, []byte("two")); e == nil {
		t.Fatal("conflict accepted")
	}
	if s.Next() != 1 {
		t.Fatal("duplicate stored")
	}
}
func TestLogLimitsAndGap(t *testing.T) {
	s, _ := NewLogStore(4, 8)
	for _, seq := range []int{-1, 2} {
		if _, e := s.Put(seq, []byte("x")); e == nil {
			t.Fatal("sequence")
		}
	}
	if _, e := s.Put(0, []byte("12345")); e == nil {
		t.Fatal("size")
	}
	_, _ = s.Put(0, []byte("1234"))
	_, _ = s.Put(1, []byte("1234"))
	if _, e := s.Put(2, []byte("x")); e == nil {
		t.Fatal("quota")
	}
	if _, e := NewLogStore(0, 4); e == nil {
		t.Fatal("limits")
	}
}
func TestLogCopiesInput(t *testing.T) {
	s, _ := NewLogStore(4, 8)
	b := []byte("abc")
	_, _ = s.Put(0, b)
	b[0] = 'z'
	if string(s.segments[0].data) != "abc" {
		t.Fatal("borrowed caller memory")
	}
}
func TestApprovalIdentity(t *testing.T) {
	subject := Subject{"p", "production", "sha256:" + strings.Repeat("a", 64), "sha256:" + strings.Repeat("b", 64), "policy-1"}
	a := Approval{Subject: subject, Approver: "operator", ExpiresAt: t0.Add(time.Minute)}
	if !a.Allows(subject, t0) {
		t.Fatal("valid rejected")
	}
	changed := subject
	changed.ArtifactDigest = "sha256:" + strings.Repeat("c", 64)
	if a.Allows(changed, t0) {
		t.Fatal("different artifact")
	}
	changed = subject
	changed.PolicyRevision = "policy-2"
	if a.Allows(changed, t0) {
		t.Fatal("different policy")
	}
	if a.Allows(subject, t0.Add(time.Minute)) {
		t.Fatal("expired")
	}
	a.Revoked = true
	if a.Allows(subject, t0) {
		t.Fatal("revoked")
	}
}
func TestApprovalMissingIdentity(t *testing.T) {
	a := Approval{ExpiresAt: t0.Add(time.Minute)}
	if a.Allows(Subject{}, t0) {
		t.Fatal("empty approval")
	}
}
