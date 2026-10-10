## Chapter 8 - Authorization with RBAC, ABAC, and Resource Policies

Authentication answers who a principal is. Authorization answers whether that principal may perform a specific action on a specific resource under the current conditions. In a tracking platform, the answer may depend on organization role, team membership, subject relationship, session status, time window, data precision, and purpose.

### A permission catalog

Start with stable action names instead of role-specific checks spread through handlers:

```text
subjects.read
subjects.manage
devices.read
devices.manage
locations.live.read
locations.history.read
locations.export
geofences.manage
alerts.manage
tasks.dispatch
public_links.create
privacy.manage
audit.read
```

Roles group permissions. Built-in roles can include owner, administrator, dispatcher, manager, viewer, driver, courier, and athlete. Organizations may define custom roles using the same catalog.

Handlers ask for an action, not a role:

```go
if err := authorizer.Require(ctx, principal, authorization.Request{
    Action:   "locations.history.read",
    Resource: subject,
}); err != nil {
    return writeAuthorizationError(w, err)
}
```

This prevents code such as `if user.Role == "admin"` from becoming an undocumented privilege system.

### Resource attributes

Role-based access control is necessary but insufficient. A dispatcher may view only assigned teams. A courier may view their own current task but not another courier's history. A public link may show only rounded positions from the last hour.

Attribute-based rules can evaluate:

- principal organization and team memberships;
- subject ownership and team assignment;
- relationship type, such as guardian or operator;
- requested time range;
- tracking session and shift boundaries;
- location precision classification;
- public-link scope and expiry;
- step-up authentication age;
- emergency-access policy.

Keep the policy engine explicit. A policy decision should return a result and optional constraints:

```go
type Decision struct {
    Allowed            bool
    ReasonCode         string
    MaxPrecisionMeters *float64
    EarliestTime       *time.Time
    LatestTime         *time.Time
    AllowedFields      []string
}
```

A public share may be allowed with reduced precision. Authorization is not always a Boolean gate; it can shape the safe response.

### Deny by default

The engine should deny when:

- an action is unknown;
- the principal type is unsupported;
- tenant context is missing;
- a resource belongs to another organization;
- required attributes cannot be loaded;
- a policy evaluation fails;
- a public capability is expired or revoked.

An internal error must not become an allow decision. Log the policy failure without sensitive route data and return a generic error.

### Centralize resource loading

Avoid authorization checks on partial objects supplied by the client. Load the canonical resource in tenant scope, then evaluate. For list endpoints, incorporate policy predicates into the query rather than loading all rows and filtering in memory.

For example, a team-scoped viewer query may include:

```sql
SELECT s.*
FROM tracking_subjects s
JOIN team_subjects ts
  ON ts.organization_id = s.organization_id
 AND ts.subject_id = s.id
JOIN team_memberships tm
  ON tm.organization_id = ts.organization_id
 AND tm.team_id = ts.team_id
WHERE s.organization_id = $1
  AND tm.user_id = $2
  AND s.status = 'active';
```

RLS still applies. The query expresses the narrower business policy.

### Emergency access

Some products require a break-glass path for safety incidents. Emergency access must be exceptional, time-limited, and noisy:

- require a dedicated permission and recent step-up authentication;
- require a reason and incident reference;
- limit duration and subject scope;
- notify privacy or security owners;
- record every viewed object;
- expose the access in the subject's history when appropriate;
- review usage after the event.

Do not implement break-glass as a hidden administrator bypass.

### Prevent indirect privilege escalation

Authorization must cover references as well as top-level resources. Creating a task with a foreign team, assigning a device to a subject, or attaching a webhook to an organization can cross boundaries even if the create endpoint itself is protected.

For every command, validate:

1. the caller may perform the action;
2. every referenced resource is visible in the same tenant;
3. the caller may establish the requested relationship;
4. resulting scopes do not exceed the caller's own grant.

A user who can create roles must not grant permissions they do not possess unless the product deliberately allows delegated administration.

### Policy tests

Use table-driven tests to cover principal type, action, resource, and context:

```go
func TestLocationHistoryPolicy(t *testing.T) {
    tests := []struct {
        name      string
        principal Principal
        subject   Subject
        context   RequestContext
        allowed   bool
    }{
        {"dispatcher in assigned team", dispatcherA, subjectA, onShift, true},
        {"viewer in another team", viewerA, subjectB, onShift, false},
        {"courier reads own active session", courierA, courierSubjectA, onShift, true},
        {"courier reads own off-shift history", courierA, courierSubjectA, offShift, false},
    }
    // Execute each case and assert reason codes as well as Allow/Deny.
}
```

Add integration tests that verify list queries and WebSocket subscriptions apply the same policy. Policy drift between REST and realtime paths is a common security defect.

### Chapter checklist

A robust authorization layer has:

- stable permission names and role composition;
- resource-aware policy evaluation;
- response constraints such as precision and time range;
- deny-by-default behavior;
- query-level filtering for lists;
- controlled break-glass access;
- reference validation against privilege escalation;
- shared policy tests across REST, WebSocket, exports, and workers.
