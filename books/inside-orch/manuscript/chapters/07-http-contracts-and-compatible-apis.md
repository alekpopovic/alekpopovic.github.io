# Chapter 7 - HTTP Contracts and Compatible APIs

An Atlas deployment script should distinguish a malformed service request from a missing service, insufficient authorization, and a temporarily unavailable server. Parsing whatever human message happened to arrive is fragile. The public API supplies structured errors, versioned routes, request identifiers, and a hand-written Go client; this chapter tests how those pieces agree and where the documentation remains incomplete.

We will keep two boundaries separate. Public user requests express workload intent. Internal agent requests register workers and report execution. Sharing an HTTP listener does not give those contracts the same credentials, audience, or documentation policy. The public OpenAPI document deliberately excludes agent paths.

You will be able to follow authentication and validation, interpret structured errors, and compare the public client and OpenAPI against actual routes without merging public and agent contracts.

## Request Boundaries and Middleware Order

The handler assembly is unusually compact:

```go
func (s *Server) middleware(next http.Handler) http.Handler {
	return requestIDMiddleware(apiVersionMiddleware(s.accessLogMiddleware(s.recoveryMiddleware(s.timeoutMiddleware(s.userAuthMiddleware(next))))))
}
```

Exact source: [internal/api/api.go:1255–1257](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L1255-L1257).

Read the nested calls from the outside inward: request ID, API version, access log, panic recovery, timeout, user authentication, then route dispatch. Consequently rejected authentication can still receive a request ID and version header. The recovery layer is inside access logging, allowing recovered failures to be reflected in the outer request observation. Timeout behavior remains separate from proof that a domain mutation was rolled back.

Namespace selection occurs in user-auth middleware before role evaluation. `X-Orch-Namespace` takes precedence over the query parameter, with normalization to default when omitted. The namespace is validated and placed into context, then the required role is looked up for the route. When no user JWT secret is configured, the middleware bypasses user token enforcement. A bearerAuth entry in OpenAPI therefore documents the configured public contract; it does not prove the development server currently requires tokens.

With JWT configured, the middleware parses a bearer token, validates it, applies static-user overrides when configured, selects the namespace role, and checks whether that role satisfies the route's required role. Static overrides clear token namespace-role assignments. These checks decide whether the handler is reached. They do not validate a Docker operation or reserve resources on a worker.

A create request then reaches [createService with a spec envelope](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L880-L902). The decoder rejects unknown JSON fields and requires the body to decode successfully. The handler validates the specification and delegates mutation to the control plane. The preceding chapter traced admission, normalization, references, quota, and map mutation. A successful response is HTTP 201 with a top-level `service` object, not the bare specification.

The distinction between unknown request and response fields is intentional. The server rejects an unknown request field to catch mistakes at the command boundary. The public Go client's ordinary JSON decoder ignores unknown response fields so an older client can survive additive server information. Applying strictness in both directions would make harmless response additions break existing callers.

## Domain Errors as Public JSON Contracts

The API maps domain conditions into stable error codes and HTTP statuses. [CodeOf recognizes](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/apperrors/errors.go#L78-L100) missing objects, duplicate/conflicting objects, invalid state, and cancellation/deadline failures. Admission and quota receive additional translation with structured details. Unexpected internal errors expose a generic message rather than the raw internal failure string.

| Condition | HTTP status | Public code |
| --- | --- | --- |
| Invalid UUID or invalid specification | 400 | invalid_argument |
| Missing object | 404 | not_found |
| Duplicate service name | 409 | conflict |
| Quota exceeded | 409 | quota_exceeded |
| Missing configured user credential | 401 | unauthorized |
| Insufficient configured role | 403 | forbidden |

The actual response envelope contains `error`, whose fields include `code`, `message`, optional `request_id`, and optional `details`. These are defined in [the API DTO and response writer](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L293-L302). The following is an illustrative shape, not copied terminal output:

```json
{"error":{"code":"invalid_argument","message":"service id must be a UUID","request_id":"example-only"}}
```

Clients should branch on the stable code and status while preserving the request identifier for investigation. The message explains the issue to a human and can change wording. A request ID is correlation metadata, not a secret, authentication proof, or transaction commit identifier. The middleware accepts a supplied identifier or generates one; it does not prove an end-to-end distributed trace exists.

The public client decodes non-2xx responses into `client.APIError`, carrying status, code, message, request ID, and details. [decodeAPIError also falls back](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/client/client.go#L461-L475) to an error containing status when the body is not the expected JSON. This distinction matters behind a proxy: an HTML gateway failure should remain an HTTP failure, not be misreported as an absent service.

Redaction belongs at multiple boundaries. App-error details recursively redact sensitive keys and URL user information according to the implemented policy. That mechanism does not authorize logging an entire request body, token, or resolved secret environment. Our smoke tests use synthetic values and discard server log output. They assert the presence of correlation metadata without printing credentials.

## The v1 Compatibility Surface

Public workload routes are registered under `/v1`, while operational probes remain unversioned. The [version middleware sets](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/versioning.go#L14-L21) `API-Version: v1` on v1 responses. `/v1/version` exposes API, server, agent-range, and schema metadata. This is useful compatibility information, but an advertised schema range does not establish durable store integration.

The repository documents additive response fields and optional request fields as compatible changes. Renaming a field, changing its meaning, requiring previously optional input, or changing stable error codes requires a new contract version. Adding an enum value also requires clients that tolerate unknown values; code that exhaustively panics on a new task status can still break even when the JSON structure remains valid.

The deprecation wrapper can set Deprecation, Sunset, and a migration Link header. Its implementation is available for routes that need it; the presence of the helper does not mean every current endpoint is deprecated. No v2 route is registered. Our actual test checks that `/v2/services` returns 404 rather than assuming a future version exists because the guide describes how one should be introduced.

Compatibility is easiest to demonstrate with a small controlled response. The teaching smoke test presents the current client with an added `future_hint` top-level field. The existing service name still decodes. Another fixture renames the nested spec name to `service_name`; decoding itself succeeds, but the client's expected `Name` value becomes empty. That silent loss is precisely why a renamed field is breaking even when no JSON syntax error occurs.

These fixtures are deliberately synthetic server responses. They demonstrate the pinned client's decoding behavior, not that the real API already emits future_hint or service_name. The real-handler part of the same test remains separate and creates Atlas through the actual API.

## OpenAPI and the Client Agree—or Differ

The public client is hand-written. Its methods construct paths, wrap request bodies, decode response envelopes, and attach bearer and namespace headers. [CreateService builds](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/pkg/client/client.go#L211-L237) its request explicitly; there is no evidence here of a generator transforming OpenAPI into this implementation. Original development prompt 61 requested generated clients, but the current artifact and workflow govern what we can claim.

There is a concrete client-versus-raw-HTTP distinction at resource defaulting. Public CreateService normalizes a zero-valued specification before serialization. Directly json.Marshal-ing that same raw Go specification emits numeric CPU 0 and memory 0, which the resource decoder rejects. Omitted fields or empty request/limit objects permit defaulting. Our expanded smoke test observed raw-zero HTTP 400 followed by successful public-client creation using the same original Go value. DOC-016 records the mismatch; validation/labs/ch07/public-contract-raw-zero.json preserves the actual run. This is a boundary of the current DTO/conversion path, not a baseline repair.

The upstream OpenAPI test parses YAML, checks nonempty top-level sections, requires a selected list of paths, and rejects internal agent paths. It does not perform full OpenAPI semantic validation, verify every response schema, or compare all handler methods automatically. Passing that test is useful evidence of its stated checks, not full contract conformance.

We therefore add a narrow, reproducible static comparison in `examples/teaching-extensions/ch07/compare_routes.py`. It extracts registered HTTP method/path pairs from the pinned router, normalizes path-parameter names, and compares them with parsed OpenAPI operations. Agent routes are classified as intentionally internal; metrics is treated as operational. This is still not schema validation or live response checking.

The actual comparison passed its expected-gap assertions and found three public GET operations missing from OpenAPI: `/v1/discovery/services`, `/v1/discovery/services/{name}`, and `/v1/integrations/traefik/config`. Their registrations are [visible together in the router](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/internal/api/api.go#L199-L201). DOC-015 records the omission, with `validation/labs/ch07/openapi-routes.json` retaining the command and output. We leave the immutable upstream document unchanged.

An omission has concrete consequences. A consumer building documentation or a client from only the schema would miss those discovery/integration operations. That is different from a wrong existing response schema, which can cause a generated consumer to misread data. Keep method coverage, schema correctness, authentication description, and actual behavior as separate review dimensions.

## Atlas Contract Lab

The canonical extension is `examples/teaching-extensions/ch07/contract_test.go`. Copy it unchanged into `.book-labs/ch07/contract_test.go` in the disposable source tree so Go's internal-package rules permit the real handler imports. Use the locked Go toolchain and its matching GOROOT/module cache. The actual application working directory must be the disposable copy, never the website root or immutable evidence directory.

```bash
go test -count=1 -v ./.book-labs/ch07
```

The observed command record is `validation/labs/ch07/public-contract-loopback.json`. It passed with ephemeral loopback test servers. The first attempt, retained separately, failed because the sandbox denied listening on a local socket; that was an environment limitation, not evidence that the API contract failed. The authorized retry allowed only the local test execution and required no Docker, database, or external service.

The real-handler test creates Atlas, checks its returned identity/name, requests a non-UUID service ID, and verifies a 400 invalid_argument APIError with a request ID. It submits an unknown top-level request field and expects 400 with the v1 header. It also verifies absent credentials produce 401 when JWT enforcement is configured, and v2 remains 404. The additive/renamed fixtures test a different, explicitly controlled decoding boundary.

A useful failure window remains after the server mutates state but before a response reaches the client. A transport error is not proof that creation failed. The caller should inspect identity and name under the intended namespace before deciding whether another create is appropriate. Duplicate-name conflict can help identify an already accepted request, but it is not a universal idempotency key. The current API contract does not provide a durable exactly-once create guarantee.

The harness starts only ephemeral servers and closes each with defer. It modifies no baseline source and creates no containers or tables. Retain the extension's byte hash alongside its copied version, and preserve failed and passed records separately. Reproducing a test means running that copy against the specified source, not replaying a previous transcript.

History includes [structured errors](https://github.com/alekpopovic/orch/commit/b5d4573f8fa5d56a5dcfde609e3794e93644a39d), [OpenAPI and client additions](https://github.com/alekpopovic/orch/commit/f94414db486b96e7088fccc8c4c502a1fa616d38), and [policy/namespace integration](https://github.com/alekpopovic/orch/commit/9e78fed31df03d7a985a9f4ceae4770739b05014). Inspecting those patches shows separate contract evolution. It does not make the schema a complete executable substitute for current handlers, or transform a hand-written client into generated output.

For Atlas consumers, the operational checklist is therefore concrete: retain stable response envelopes, tolerate additive response fields, validate required values after decoding, classify structured errors, and keep the selected namespace visible in automation configuration. When an error body is absent, preserve transport or HTTP failure rather than inventing a domain cause. When schema and router differ, record the exact method and revision so a future edition can review a real correction. This workflow makes compatibility review a set of observable checks instead of a claim inferred from a version label.

## Exercises

1. Explain why a rejected JWT can still have an API-Version header and request ID. Trace the actual middleware nesting.
2. What should an operator script branch on when a service ID is malformed? Explain the roles of code, status, message, and request ID.
3. Reproduce the additive-response fixture and explain why the renamed-field fixture is breaking despite successful JSON decoding.
4. A reviewer calls every agent route missing from public OpenAPI a defect. Correct the assumption, then name the three genuine public method omissions found by this lab.

See the [worked answers](../solutions/ch07.md).
