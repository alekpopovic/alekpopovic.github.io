# ch07-source-anchor

Follow validation and authorization at the HTTP boundary. The listing is a contiguous source window; surrounding implementation is explained separately.

Unchanged, contiguous source excerpt: [internal/apperrors/errors.go, lines 35–54](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/apperrors/errors.go#L35-L54).

```go
func New(code Code, message string) *Error {
	return &Error{Code: normalizeCode(code), Message: strings.TrimSpace(message)}
}

func Wrap(code Code, message string, err error) *Error {
	return &Error{Code: normalizeCode(code), Message: strings.TrimSpace(message), Err: err}
}

func (e *Error) Error() string {
	if e == nil {
		return ""
	}
	if e.Message != "" {
		return e.Message
	}
	if e.Err != nil {
		return e.Err.Error()
	}
	return string(normalizeCode(e.Code))
}
```

SHA-256: `0e06a7b1943ebd533e500a698e428387591e0e8d1d35c3c3f67c4447374b990e`. This excerpt is not an independently compilable program.
