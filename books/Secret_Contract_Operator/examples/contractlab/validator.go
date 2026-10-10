// Package contractlab is a standalone educational validator.
// It is not the Kubernetes operator implementation.
package contractlab

import (
	"bytes"
	"encoding/json"
	"encoding/pem"
	"net/url"
	"regexp"
	"sort"
)

const (
	MaxRules        = 256
	MaxPatternBytes = 1024
	MaxValueBytes   = 128 << 10
	MaxDataBytes    = 1 << 20
)

type Rule struct {
	Name      string
	Required  *bool
	NonEmpty  *bool
	MinLength *int
	MaxLength *int
	Pattern   string
	Format    string
}

type Violation struct {
	Key    string `json:"key,omitempty"`
	Rule   string `json:"rule"`
	Reason string `json:"reason"`
}

type Result struct {
	SpecValid  bool        `json:"specValid"`
	Valid      bool        `json:"valid"`
	Missing    []string    `json:"missing"`
	Violations []Violation `json:"violations"`
}

var keyName = regexp.MustCompile(`^[A-Za-z0-9._-]+$`)

func defaultTrue(v *bool) bool { return v == nil || *v }

// Validate returns only key identifiers and controlled reason codes.
// Never add raw input or parser errors to this result.
func Validate(rules []Rule, data map[string][]byte) Result {
	out := Result{SpecValid: true, Missing: []string{}, Violations: []Violation{}}
	add := func(key, rule, reason string) {
		out.Violations = append(out.Violations, Violation{key, rule, reason})
	}
	if len(rules) == 0 || len(rules) > MaxRules {
		out.SpecValid = false
		add("", "spec", "InvalidRuleCount")
		return finish(out)
	}
	compiled := make([]*regexp.Regexp, len(rules))
	seen := map[string]bool{}
	for i, r := range rules {
		validName := len(r.Name) > 0 && len(r.Name) <= 253 && keyName.MatchString(r.Name)
		if !validName {
			out.SpecValid = false
			add("", "spec", "InvalidKeyName")
			continue
		}
		if seen[r.Name] {
			out.SpecValid = false
			add(r.Name, "spec", "DuplicateKey")
		}
		seen[r.Name] = true
		if (r.MinLength != nil && *r.MinLength < 0) ||
			(r.MaxLength != nil && *r.MaxLength < 0) ||
			(r.MinLength != nil && r.MaxLength != nil && *r.MinLength > *r.MaxLength) {
			out.SpecValid = false
			add(r.Name, "spec", "InvalidLengthRange")
		}
		switch r.Format {
		case "", "None", "JSON", "URI", "PEM":
		default:
			out.SpecValid = false
			add(r.Name, "spec", "InvalidFormat")
		}
		if len(r.Pattern) > MaxPatternBytes {
			out.SpecValid = false
			add(r.Name, "spec", "PatternTooLarge")
		} else if r.Pattern != "" {
			rx, err := regexp.Compile(r.Pattern)
			if err != nil {
				out.SpecValid = false
				add(r.Name, "spec", "InvalidPattern")
			} else {
				compiled[i] = rx
			}
		}
	}
	if !out.SpecValid {
		return finish(out)
	}
	total := 0
	for _, v := range data {
		if len(v) > MaxDataBytes-total {
			add("", "budget", "EvaluationBudgetExceeded")
			return finish(out)
		}
		total += len(v)
	}
	for i, r := range rules {
		v, exists := data[r.Name]
		if !exists {
			if defaultTrue(r.Required) {
				out.Missing = append(out.Missing, r.Name)
				add(r.Name, "required", "MissingRequiredKey")
			}
			continue
		}
		if len(v) > MaxValueBytes {
			add(r.Name, "budget", "ValueTooLarge")
			continue
		}
		if defaultTrue(r.NonEmpty) && len(v) == 0 {
			add(r.Name, "nonEmpty", "EmptyValue")
		}
		if r.MinLength != nil && len(v) < *r.MinLength {
			add(r.Name, "minLength", "TooShort")
		}
		if r.MaxLength != nil && len(v) > *r.MaxLength {
			add(r.Name, "maxLength", "TooLong")
		}
		if compiled[i] != nil && !compiled[i].Match(v) {
			add(r.Name, "pattern", "PatternMismatch")
		}
		switch r.Format {
		case "JSON":
			if !json.Valid(v) {
				add(r.Name, "format", "InvalidJSON")
			}
		case "URI":
			u, err := url.Parse(string(v))
			if err != nil || u.Scheme == "" {
				add(r.Name, "format", "InvalidURI")
			}
		case "PEM":
			if !validPEM(v) {
				add(r.Name, "format", "InvalidPEM")
			}
		}
	}
	return finish(out)
}

func validPEM(input []byte) bool {
	remaining := bytes.TrimSpace(input)
	blocks := 0
	for len(remaining) > 0 {
		if !bytes.HasPrefix(remaining, []byte("-----BEGIN ")) {
			return false
		}
		lineEnd := bytes.IndexByte(remaining, '\n')
		if lineEnd < 0 {
			return false
		}
		header := bytes.TrimSuffix(remaining[:lineEnd], []byte("\r"))
		if !bytes.HasSuffix(header, []byte("-----")) || len(header) <= 16 {
			return false
		}
		typ := header[len("-----BEGIN ") : len(header)-len("-----")]
		endMarker := append(append([]byte("\n-----END "), typ...), []byte("-----")...)
		endIndex := bytes.Index(remaining, endMarker)
		if endIndex < 0 {
			return false
		}
		end := endIndex + len(endMarker)
		segment := remaining[:end]
		// pem.Decode may otherwise skip a malformed block and accept a later one.
		if bytes.Contains(segment[lineEnd+1:], []byte("-----BEGIN ")) {
			return false
		}
		block, rest := pem.Decode(segment)
		if block == nil || len(block.Bytes) == 0 || len(bytes.TrimSpace(rest)) != 0 || block.Type != string(typ) {
			return false
		}
		blocks++
		remaining = bytes.TrimSpace(remaining[end:])
	}
	return blocks > 0
}

func finish(out Result) Result {
	sort.Strings(out.Missing)
	sort.Slice(out.Violations, func(i, j int) bool {
		a, b := out.Violations[i], out.Violations[j]
		if a.Key != b.Key {
			return a.Key < b.Key
		}
		if a.Rule != b.Rule {
			return a.Rule < b.Rule
		}
		return a.Reason < b.Reason
	})
	out.Valid = out.SpecValid && len(out.Violations) == 0
	return out
}
