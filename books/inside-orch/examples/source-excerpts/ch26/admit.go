func (controller *Controller) Admit(ctx context.Context, request Request) error {
	violations := Evaluate(request.Spec, request.Policy)
	if len(violations) == 0 {
		return nil
	}
	if controller != nil && controller.sink != nil {
		controller.sink.RecordAdmissionRejection(ctx, Rejection{
			Actor: request.Actor, Operation: request.Operation, Namespace: request.Namespace,
			Service: request.Spec.Name, Violations: violations,
		})
	}
	return &Error{Operation: request.Operation, Namespace: request.Namespace, Violations: violations}
}
