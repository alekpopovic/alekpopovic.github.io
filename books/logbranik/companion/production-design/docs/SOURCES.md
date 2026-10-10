# Official references

Reviewed 2026-10-09. Recheck against the installed/pinned versions during prompt 001.
Design choices such as thresholds, limits, schema, TTLs and rollout stages are project proposals.

- Nginx auth_request: https://nginx.org/en/docs/http/ngx_http_auth_request_module.html
  — module availability, allowed/denied/error outcomes.
- Nginx logging: https://nginx.org/en/docs/http/ngx_http_log_module.html
  — JSON escaping, flush controls and log-time variables.
- Nginx real IP: https://nginx.org/en/docs/http/ngx_http_realip_module.html
  — trusted peers and client address reconstruction.
- Nginx core: https://nginx.org/en/docs/http/ngx_http_core_module.html#error_page
  — internal error handling and named locations.
- Nginx proxy: https://nginx.org/en/docs/http/ngx_http_proxy_module.html
  — local subrequest proxying and response interception.
- Nginx rewrite: https://nginx.org/en/docs/http/ngx_http_rewrite_module.html
  — rewrite/return processing and routing hazards.
- Vector HTTP sink: https://vector.dev/docs/reference/configuration/sinks/http/
  — framing, buffers, TLS, retryable response codes.
- Vector file source: https://vector.dev/docs/reference/configuration/sources/file/
  — checkpoints, fingerprints and rotation.

Additional implementation references to consult when their prompts execute:
https://fastapi.tiangolo.com/ ; https://docs.sqlalchemy.org/ ;
https://alembic.sqlalchemy.org/ ; https://www.postgresql.org/docs/current/ ;
https://pkg.go.dev/crypto/ed25519 ; https://pkg.go.dev/net/netip ;
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/ .

Claude Code edition references, checked 2026-10-10 (Europe/Belgrade):
https://code.claude.com/docs/en/memory ; https://code.claude.com/docs/en/model-config ;
https://code.claude.com/docs/en/cli-reference . See CLAUDE_CODE_GUIDE.md for usage.
