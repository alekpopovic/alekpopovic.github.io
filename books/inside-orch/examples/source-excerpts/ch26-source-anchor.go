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
