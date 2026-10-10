# 8. Connect ordinary Nginx to the guard

## Verify the module before editing configuration

Nginx Open Source can authorize a request using an HTTP subrequest when the `auth_request` module is present. It treats successful 2xx authorization responses as allows and 401/403 as denials. Other authorization statuses are errors. The module is not enabled in every possible build, so inspect the build you actually run:

```bash
nginx -V
```

Check the configure arguments or distribution documentation for `--with-http_auth_request_module`. Do not infer support from a different host or from an Nginx Plus example. The system in this book needs no Plus management API and does not change the Nginx configuration for each ban.

## Protect a real content location

The internal authorization location proxies to the local agent. The public application location invokes that subrequest and then proxies allowed traffic to the application. The core structure is:

```nginx
location / {
    auth_request /_guard_auth;
    auth_request_set $guard_outcome
        $upstream_http_x_guard_outcome;
    proxy_pass http://127.0.0.1:8081;
}

location = /_guard_auth {
    internal;
    auth_request off;
    access_log off;
    proxy_pass http://unix:/run/logbranik/auth.sock:/v1/check;
    proxy_method GET;
    proxy_pass_request_body off;
    proxy_pass_request_headers off;
    proxy_set_header Content-Length "";
    proxy_set_header Host localhost;
    proxy_set_header X-Guard-IP $remote_addr;
    proxy_set_header X-Guard-Site "site-demo";
    proxy_next_upstream off;
    proxy_cache off;
}
```

This is a structural excerpt. The delivered configuration files add logging and timeout settings. Socket paths and permissions must match your deployment. Use the generated lab configuration described in the runbook instead of pasting this excerpt as a whole server.

Do not use `return 200` in the public location as your proof that authorization works. Nginx processing phases matter, and a rewrite-phase return can finish a request before the access phase you intend to test. The companion echo application supplies an actual content upstream so the test exercises the relevant path.

## Keep bodies and identity separate

The authorization subrequest needs an address and site, not the visitor's upload. Clearing its body prevents a guard call from waiting on content it does not inspect. This does not remove the body from the main application request. Verify that a permitted POST still reaches the upstream with its method and body intact.

Overwriting guard headers is essential. A visitor may send `X-Guard-IP` claiming to be an allowlisted address. That input must never become the address the agent evaluates. The site ID similarly comes from deployment configuration rather than the visitor's Host header or a body parameter.

## Audit every route

Location selection can route static files, error pages, API paths, and named locations differently. An existing authentication integration may already use `auth_request`; simply replacing it would remove application authentication. Compose the checks deliberately or preserve the existing mechanism through a supported integration design.

Also inspect `satisfy` settings and IP access rules. A combination that allows one access module to satisfy authorization may bypass the guard when another module permits the request. The acceptance matrix should include every route class and every preexisting authentication rule.

## Reload once, then update policy

Installing the integration requires configuration validation and a controlled Nginx reload. After installation, bans and revocations change agent state rather than Nginx files. The claim "no reload for a ban" applies to policy changes, not to the initial integration or future routing edits.

## Exercise

On a disposable Linux host, test a permitted GET, a denied GET, a POST body, an attempted direct request to `/_guard_auth`, and a spoofed guard header. Record the public response and whether the upstream received each request.

## Answer

Allowed requests reach the upstream. A guard denial returns 403 without contacting it. A permitted POST preserves method and body. The internal location is not publicly callable as an ordinary route. A spoofed header does not alter the resolved identity. These observations require actual Nginx execution; the preparation environment did not run this deployment gate.
