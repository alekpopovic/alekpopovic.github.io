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
