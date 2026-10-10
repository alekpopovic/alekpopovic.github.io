# Appendix C. Glossary and sources

## Glossary

**Access event:** A terminal observation of one completed Nginx request. It is not a pre-request inspection.

**Agent:** A local service that validates remote policies and answers authorization checks.

**Applied state:** The complete policy view an agent has persisted and published.

**Backpressure:** A condition in which downstream capacity restricts upstream progress. Its effect depends on the whole collection topology.

**Decision:** A bounded data record describing an address, scope, reason, and expiry.

**Delivery interval:** The period during which a new envelope can be applied. It is separate from each contained decision's lifetime.

**Desired state:** The central configuration and decisions the fleet is intended to apply.

**Epoch:** A provisioned identifier for one agent policy stream. Changing it requires a controlled recovery action.

**Event time:** The time the observed request completed.

**Idempotency:** Repeating the same operation identity does not create additional effects.

**Monitor mode:** A mode that reports would-block while permitting requests.

**mTLS:** TLS with authenticated client and server credentials. Application authorization still determines permitted roles and scopes.

**NDJSON:** Newline-delimited JSON objects, distinct from a JSON array.

**Outbox:** Durable delivery intent or bytes stored with the state transition that requires them.

**Policy snapshot:** A complete replacement of an agent's remote policy state.

**Processing time:** The time an observation is handled by the analyzer.

**Revision:** A monotonically increasing integer within one provisioned policy stream.

**TTL:** A decision's mandatory time to live, bounded independently by the agent.

## Primary technical references

The book's architecture is an original project design developed from the companion implementation pack. The following official documentation supports the external mechanisms used. Consult the documentation for your installed versions before adapting examples. References were checked in October 2026.

1. Nginx authorization-subrequest module: [nginx.org/en/docs/http/ngx_http_auth_request_module.html](https://nginx.org/en/docs/http/ngx_http_auth_request_module.html). Module availability, authorization statuses, and directive semantics.
2. Nginx real-IP module: [nginx.org/en/docs/http/ngx_http_realip_module.html](https://nginx.org/en/docs/http/ngx_http_realip_module.html). Trusted peer configuration and resolved client addresses.
3. Nginx HTTP log module: [nginx.org/en/docs/http/ngx_http_log_module.html](https://nginx.org/en/docs/http/ngx_http_log_module.html). JSON escaping, log contexts, and buffering.
4. Vector HTTP sink: [vector.dev/docs/reference/configuration/sinks/http/](https://vector.dev/docs/reference/configuration/sinks/http/). Transport configuration and sink behavior.
5. Vector end-to-end acknowledgements: [vector.dev/docs/architecture/end-to-end-acknowledgements/](https://vector.dev/docs/architecture/end-to-end-acknowledgements/). Topology-dependent acknowledgement guarantees.
6. PostgreSQL SELECT and locking: [postgresql.org/docs/current/sql-select.html](https://www.postgresql.org/docs/current/sql-select.html). Queue-like uses of row locking and `SKIP LOCKED`.
7. Cryptography Ed25519 interface: [cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/). Library signing and verification interfaces.

## Publishing references

8. Leanpub Git/GitHub writing mode: [help.leanpub.com/en/articles/2916385](https://help.leanpub.com/en/articles/2916385-getting-started-using-leanpub-s-git-and-github-writing-mode-to-write-and-publish-a-book). Manuscript workflow and preview.
9. Leanpub manuscript ordering: [help.leanpub.com/en/articles/15408698](https://help.leanpub.com/en/articles/15408698-how-can-i-comment-out-lines-in-my-book-txt-file). `Book.txt` ordering.
10. Leanpub AI quality policy: [help.leanpub.com/en/articles/11853585](https://help.leanpub.com/en/articles/11853585-ai-slop-is-not-permitted-on-leanpub). Human curation and content quality.
11. Leanpub AI-use settings: [help.leanpub.com/en/articles/9363893](https://help.leanpub.com/en/articles/9363893-ai-usage-disclosure-details-for-leanpub-authors). Platform disclosure controls; retain the book's own transparency statement.
12. Leanpub terms: [leanpub.com/terms](https://leanpub.com/terms). Current account and content terms.

## How to use these sources

The references are mechanisms, not endorsements of LogBranik. The book does not copy a vendor manual or claim that a third-party feature proves this complete system works. Its policy ordering, role map, data contract, and operational boundaries are project decisions, supported by the tests recorded with this edition and by the deployment gates readers must execute.

If a reference changes, check whether the change affects the installed mechanism before revising the book. A new Nginx release does not automatically change an existing host. A different collector acknowledgement capability can change the end-to-end guarantee even when the ingestion code remains identical.
