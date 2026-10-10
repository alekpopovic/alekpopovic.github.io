# Nginx Open Source integration

Check `nginx -V` for http_auth_request_module and, when behind proxies, http_realip_module.
Use vendor-supported packages or document a compatible build. No Nginx Plus dependency.
Initial include installation requires `nginx -t` and a graceful reload. Per-IP changes are
agent state updates only; the agent has no permission to write Nginx config or signal Nginx.

## Routing coverage

Apply the check to every protected content location. Audit exact matches, regex matches,
static files, proxy locations, named locations, internal redirects, and existing authentication.
Never test protection using a public `return 200`: rewrite-phase returns can finish before
the access-phase check. Use a real static file or echo upstream for successful test traffic.
Do not claim a redirect-only server is authenticated merely because it has auth_request.
Explicit health/ACME exclusions are documented, narrow and contain no application content.

Nginx supports one auth_request target per context. If the site already uses external auth,
design and test a composition endpoint rather than silently replacing it. `satisfy any` can
bypass the security check when another access module allows; audit existing use. Leave
proxy caching of auth responses off initially so new bans and revocations are immediate.

## Trusted identity

For a direct edge, use the socket peer IP and do not consume visitor-supplied X-Forwarded-For.
For ALB/CDN/proxy ingress, trust only the actual ingress peers and restrict network access
to those peers. Configure the corresponding header/proxy protocol from documented topology.
Never use set_real_ip_from 0.0.0.0/0 or ::/0. Private networks are not automatically all trusted.
Test direct access, forged headers, multiple hops, IPv6 and IPv4-mapped IPv6.

Assign a stable site ID by deployment configuration, not raw Host. A site with aliases shares
an explicit registered ID; a catch-all host does not inherit a real tenant's identity.
The agent accepts X-Guard-IP/X-Guard-Site only from its protected local listener, and Nginx
overwrites the fields. Strip visitor cookies, authorization and forwarding headers from checks.

## Reference files

`examples/nginx/http.conf.example` belongs in http context. `site.conf.example` belongs
under http as a server. Adapt include paths and socket ownership. The sample auth location
is internal and recursive auth is disabled. A local timeout is bounded; choose the actual
budget from measured load, not from the example alone.

The sample uses fail-closed. For explicit fail-open, add the lines from
`fail-open-auth-only.conf.example` inside the internal auth location and add its named
fallback at server level. This is conditional source guidance until runtime integration tests
prove the behavior on the selected build. Do not map errors on the public content location.
Existing application authentication remains active regardless of the Guard availability mode.

The logged path uses a pre-rewrite query-free capture from request_uri so a named or URI
internal redirect does not erase the original path. Query parameters, full request lines,
bodies, cookies, Authorization, referer and user-agent are omitted by default. Optional
user-agent collection must be bounded and explicitly justified; it is not a core signal.

Access logs observe completed requests; long requests and WebSockets delay log evidence.
Already admitted requests/streams continue after a ban. Local rate limits and connection
limits can supplement this system, while network DDoS protection remains a separate layer.
