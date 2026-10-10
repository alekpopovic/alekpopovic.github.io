# 7. The Pure Go Validator

## 7.1 The Boundary Around the Most Sensitive Code

The validator is the only component that needs to understand the contents of declared Secret keys. It accepts rules and `map[string][]byte`, and returns a structured result without the sensitive input. It has no logger, event recorder, Kubernetes client, HTTP client, or clock.

This organization enables fast table-driven tests and fuzz testing. It also simplifies review: every output from the function can be inspected as a potential leakage channel.

## 7.2 Two Levels of Error

An **invalid specification** means that a rule makes no sense: a key is listed twice, a regexp cannot compile, or the minimum exceeds the maximum. **Invalid data** means that a well-defined rule is not satisfied.

Keep these cases distinct. `InvalidPattern` is a contract configuration error, whereas `PatternMismatch` is a data finding. Both must be safe to display, but responsibility for fixing them differs.

## 7.3 Types Without Value Fields

```go
// Reference snippet: no Kubernetes dependencies.
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
```

User-defined message text is not part of a rule. This prevents someone from putting a secret into `messageTemplate` and having the operator blindly copy it into status later. Public message text is generated from known codes in a separate layer.

## 7.4 Evaluation Order

Check budgets and rule validity first. Then determine whether each key exists. If it is absent and optional, finish checking that key. If it is absent and required, add `MissingRequiredKey` without running parsers on empty input.

For a present value, check its size budget, then emptiness, length, pattern, and format. Sort results by key and rule type. Multiple findings for one key are allowed, but bound the total number of findings and avoid unhelpful repetition.

Do not truncate a value before validation to fit a budget. Truncation would change the meaning of the check. Return `ValueTooLarge` or `EvaluationBudgetExceeded` instead, and document that reason clearly.

## 7.5 Regular Expressions

Go's regexp implementation guarantees execution time linear in input size for the expressions it supports. This is a good reason to avoid introducing another engine merely for additional syntax. Still bound the number of rules, input size, and pattern length, because total work grows with their product. [S11](https://pkg.go.dev/regexp)

Do not return a raw `regexp.Compile` error in status. A pattern belongs to the contract, but may contain sensitive or inappropriate text. `InvalidPattern` and a path to the rule are sufficient. Explain anchors in the documentation and test the difference between substring and full-string expectations.

## 7.6 JSON, URI, and PEM

`json.Valid` is sufficient for JSON syntax. A semantic contract over JSON fields would require a new, explicit feature with a controlled schema and additional complexity limits. The MVP does not promise JSON Schema validation.

The URI parser must confirm that a scheme exists, but must not require a host for every valid URI form: `urn:` and other absolute URIs need not have a network authority. Do not open the address or perform a DNS lookup. This keeps validation deterministic and prevents it from becoming an SSRF surface.

PEM checking allows one or more blocks with nonempty decoded content, with whitespace between blocks. Check for the expected beginning before each `pem.Decode` call, because the decoder can skip some non-PEM text. Do not display block contents on failure. This is not X.509 verification.

## 7.7 The Standalone Lab

The accompanying `examples/contractlab` directory contains an implementation of this narrowly scoped evaluator and its tests. It is not the entire operator. The code uses the standard library and can be checked independently of the Kubernetes scaffold.

```bash
cd examples/contractlab
go test ./...
go test -race ./...
go vet ./...
```

Tests cover required and optional keys, empty values, byte length, invalid regexps, JSON, absolute URIs, PEM, duplicate rules, budgets, and sentinel leakage. Synthetic sensitive values deliberately appear in test fixtures; the prohibition concerns their public outputs, not the ability to test secrets.

## 7.8 Moving into the Real Operator

The adapter between CRD types and the pure evaluator explicitly normalizes defaults. It does not assume the API server has applied them, because unit tests may construct Go objects directly. The same rule applies to old or incomplete objects.

Before moving into a production controller, add fuzz tests for arbitrary bytes and combinations of rules. Fuzzing looks for panics, nondeterminism, and unexpected output; it does not prove the absence of every vulnerability. Go provides a built-in workflow for coverage-guided fuzz tests. [S12](https://go.dev/doc/security/fuzz/)

**Checkpoint.** The validator must be testable without Kubernetes, and its result must be safe to serialize as JSON even when the input is deliberately hostile.
