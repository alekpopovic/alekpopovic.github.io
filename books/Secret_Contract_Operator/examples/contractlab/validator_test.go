package contractlab

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"reflect"
	"testing"
)

func boolPtr(v bool) *bool { return &v }
func intPtr(v int) *int    { return &v }

func TestValidator(t *testing.T) {
	p := pem.EncodeToMemory(&pem.Block{Type: "TEST DATA", Bytes: []byte{1, 2, 3}})
	tests := []struct {
		name      string
		rule      Rule
		data      map[string][]byte
		valid     bool
		specValid bool
		reason    string
	}{
		{"valid", Rule{Name: "KEY"}, map[string][]byte{"KEY": []byte("demo")}, true, true, ""},
		{"missing", Rule{Name: "KEY"}, nil, false, true, "MissingRequiredKey"},
		{"optional absent", Rule{Name: "KEY", Required: boolPtr(false)}, nil, true, true, ""},
		{"optional present invalid", Rule{Name: "KEY", Required: boolPtr(false)}, map[string][]byte{"KEY": {}}, false, true, "EmptyValue"},
		{"empty", Rule{Name: "KEY"}, map[string][]byte{"KEY": {}}, false, true, "EmptyValue"},
		{"empty allowed", Rule{Name: "KEY", NonEmpty: boolPtr(false)}, map[string][]byte{"KEY": {}}, true, true, ""},
		{"byte boundary", Rule{Name: "KEY", MinLength: intPtr(4), MaxLength: intPtr(4)}, map[string][]byte{"KEY": []byte("žž")}, true, true, ""},
		{"short", Rule{Name: "KEY", MinLength: intPtr(8)}, map[string][]byte{"KEY": []byte("demo")}, false, true, "TooShort"},
		{"long", Rule{Name: "KEY", MaxLength: intPtr(3)}, map[string][]byte{"KEY": []byte("demo")}, false, true, "TooLong"},
		{"pattern match", Rule{Name: "KEY", Pattern: "^demo$"}, map[string][]byte{"KEY": []byte("demo")}, true, true, ""},
		{"pattern mismatch", Rule{Name: "KEY", Pattern: "^other$"}, map[string][]byte{"KEY": []byte("demo")}, false, true, "PatternMismatch"},
		{"pattern invalid", Rule{Name: "KEY", Pattern: "["}, nil, false, false, "InvalidPattern"},
		{"json object", Rule{Name: "KEY", Format: "JSON"}, map[string][]byte{"KEY": []byte(`{"demo":true}`)}, true, true, ""},
		{"json scalar", Rule{Name: "KEY", Format: "JSON"}, map[string][]byte{"KEY": []byte(`42`)}, true, true, ""},
		{"json bad", Rule{Name: "KEY", Format: "JSON"}, map[string][]byte{"KEY": []byte(`{"bad"`)}, false, true, "InvalidJSON"},
		{"uri", Rule{Name: "KEY", Format: "URI"}, map[string][]byte{"KEY": []byte("https://example.invalid/path")}, true, true, ""},
		{"opaque uri", Rule{Name: "KEY", Format: "URI"}, map[string][]byte{"KEY": []byte("urn:example:test")}, true, true, ""},
		{"relative uri", Rule{Name: "KEY", Format: "URI"}, map[string][]byte{"KEY": []byte("/relative")}, false, true, "InvalidURI"},
		{"pem", Rule{Name: "KEY", Format: "PEM"}, map[string][]byte{"KEY": p}, true, true, ""},
		{"pem bundle", Rule{Name: "KEY", Format: "PEM"}, map[string][]byte{"KEY": append(append([]byte{}, p...), p...)}, true, true, ""},
		{"pem trailing junk", Rule{Name: "KEY", Format: "PEM"}, map[string][]byte{"KEY": append(append([]byte{}, p...), []byte("junk")...)}, false, true, "InvalidPEM"},
		{"pem leading junk", Rule{Name: "KEY", Format: "PEM"}, map[string][]byte{"KEY": append([]byte("junk"), p...)}, false, true, "InvalidPEM"},
		{"invalid range", Rule{Name: "KEY", MinLength: intPtr(5), MaxLength: intPtr(2)}, nil, false, false, "InvalidLengthRange"},
		{"negative range", Rule{Name: "KEY", MinLength: intPtr(-1)}, nil, false, false, "InvalidLengthRange"},
		{"invalid format", Rule{Name: "KEY", Format: "Other"}, nil, false, false, "InvalidFormat"},
		{"value budget", Rule{Name: "KEY"}, map[string][]byte{"KEY": make([]byte, MaxValueBytes+1)}, false, true, "ValueTooLarge"},
		{"data budget", Rule{Name: "KEY"}, map[string][]byte{"KEY": make([]byte, MaxDataBytes+1)}, false, true, "EvaluationBudgetExceeded"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := Validate([]Rule{tt.rule}, tt.data)
			if got.Valid != tt.valid || got.SpecValid != tt.specValid {
				t.Fatal("unexpected validation outcome")
			}
			if tt.reason != "" {
				found := false
				for _, v := range got.Violations {
					if v.Reason == tt.reason {
						found = true
					}
				}
				if !found {
					t.Fatal("expected controlled reason was not returned")
				}
			}
		})
	}
}

func TestMalformedFirstPEMBlock(t *testing.T) {
	valid := pem.EncodeToMemory(&pem.Block{Type: "TEST DATA", Bytes: []byte{1, 2, 3}})
	input := append([]byte("-----BEGIN TEST DATA-----\nnot-base64!\n"), valid...)
	result := Validate([]Rule{{Name: "KEY", Format: "PEM"}}, map[string][]byte{"KEY": input})
	if result.Valid {
		t.Fatal("malformed preceding PEM block accepted")
	}
}

func TestInvalidSpecifications(t *testing.T) {
	for _, rules := range [][]Rule{
		nil,
		{{Name: "KEY"}, {Name: "KEY"}},
		{{Name: "invalid key"}},
		{{Name: "KEY", Pattern: string(make([]byte, MaxPatternBytes+1))}},
		make([]Rule, MaxRules+1),
	} {
		if Validate(rules, nil).SpecValid {
			t.Fatal("malformed specification accepted")
		}
	}
}

func TestNoSensitiveOutput(t *testing.T) {
	sentinel := []byte("SENSITIVE_TEST_VALUE_DO_NOT_LEAK_7dA9")
	hash := sha256.Sum256(sentinel)
	forbidden := [][]byte{
		sentinel,
		[]byte(base64.StdEncoding.EncodeToString(sentinel)),
		[]byte(hex.EncodeToString(sentinel)),
		[]byte(hex.EncodeToString(hash[:])),
	}
	for _, format := range []string{"JSON", "URI", "PEM"} {
		result := Validate([]Rule{{Name: "KEY", Format: format}}, map[string][]byte{"KEY": sentinel})
		encoded, err := json.Marshal(result)
		if err != nil {
			t.Fatal("could not serialize controlled result")
		}
		for _, f := range forbidden {
			if bytes.Contains(encoded, f) {
				t.Fatal("sensitive representation leaked")
			}
		}
	}
}

func TestDeterminism(t *testing.T) {
	rules := []Rule{{Name: "B"}, {Name: "A"}}
	a := Validate(rules, nil)
	b := Validate(rules, nil)
	if !reflect.DeepEqual(a, b) {
		t.Fatal("non-deterministic output")
	}
	if len(a.Missing) != 2 || a.Missing[0] != "A" {
		t.Fatal("missing keys not sorted")
	}
}

func FuzzValidator(f *testing.F) {
	f.Add([]byte("demo"))
	f.Add([]byte(`{"ok":true}`))
	f.Fuzz(func(t *testing.T, input []byte) {
		// Test fixtures only: never seed this corpus with real secrets.
		for _, format := range []string{"None", "JSON", "URI", "PEM"} {
			rules := []Rule{{Name: "KEY", Format: format}}
			a := Validate(rules, map[string][]byte{"KEY": input})
			b := Validate(rules, map[string][]byte{"KEY": input})
			if !reflect.DeepEqual(a, b) {
				t.Fatal("non-deterministic output")
			}
			if _, err := json.Marshal(a); err != nil {
				t.Fatal("unsafe result shape")
			}
		}
	})
}
