# ch26-source-anchor

Distinguish supported security context fields from host isolation. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/admission/admission.go, lines 48–67](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/admission/admission.go#L48-L67).

```go
func (e *Error) Error() string {
	if e == nil || len(e.Violations) == 0 {
		return "admission rejected"
	}
	return fmt.Sprintf("admission rejected: %s", e.Violations[0].Message)
}

type Rejection struct {
	Actor      Actor
	Operation  Operation
	Namespace  string
	Service    string
	Violations []Violation
}

type AuditSink interface {
	RecordAdmissionRejection(context.Context, Rejection)
}

type Controller struct {
```

SHA-256: `e8b00b7d5b863f1b14d7aced7aaef279be18032629c6adb30204e223a27fcbc8`. This excerpt is not an independently compilable program.
