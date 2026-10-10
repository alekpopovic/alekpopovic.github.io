# Appendix A. Laboratory runbook

## Files and responsibilities

| File | Purpose |
| --- | --- |
| `logbranik/protocol.py` | Strict parsing, signatures, policy validation, agent state |
| `logbranik/central.py` | SQLite events, deduplication, small detector, revisions |
| `logbranik/servers.py` | Local checks, mTLS endpoints, role authorization, push |
| `logbranik/certificates.py` | Disposable loopback TLS fixtures |
| `logbranik/__main__.py` | Laboratory CLI and function demo |
| `delivery_loop.py` | Periodic signed push for the teaching exercise |
| `normalize_logs.py` | Finite Nginx-log conversion into lab NDJSON |
| `render_nginx_config.py` | Isolated Nginx lab configuration generation |
| `echo.py` | Local application used for real access-phase testing |
| `tests/test_guard.py` | Behavioral and live transport tests |

Run commands from the `companion` directory unless a command says otherwise. No command in this runbook installs configuration into `/etc/nginx`. The generated Nginx configuration listens only on loopback and uses a directory you control.

## Quick function demonstration

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m logbranik demo
```

For a repeatable dependency baseline, the preparation run used Cryptography 50.0.1. The requirements range permits compatible releases; upgrading within it still requires rerunning the tests.

## Process laboratory

```bash
python3 -m logbranik init
python3 -m logbranik certificates
```

Run agent, central server, delivery loop, and echo application in separate terminals:

```bash
python3 -m logbranik agent
python3 -m logbranik central-server
python3 delivery_loop.py
python3 echo.py
```

These lines are four separate long-running processes, not a sequence to paste into one blocked terminal. Use the same initialized directory for this single-host lab. Disposable credentials expire after seven days. Regenerate fixtures in a new isolated directory when needed; do not disable TLS verification to work around expiration.

## Nginx host acceptance

On a Linux host with the required Nginx module, generate the isolated configuration:

```bash
python3 render_nginx_config.py
nginx -t -c "$PWD/lab-state/nginx.conf" -p "$PWD/lab-state/"
nginx -c "$PWD/lab-state/nginx.conf" -p "$PWD/lab-state/"
```

The echo application must already be running. The agent must have a valid applied policy before public requests can be allowed. The delivery process supplies the initial signed empty policy.

If you chose the loopback TCP teaching option for the agent, generate the matching profile with `python3 render_nginx_config.py --tcp-auth`. Do not mix a TCP agent with a Unix proxy target. Both variants remain lab-only until deployment acceptance is recorded.

Create five actual local requests:

```bash
for i in 1 2 3 4 5; do
  curl -s -o /dev/null http://127.0.0.1:8080/missing-$i
done
python3 normalize_logs.py lab-state/guard-access.json > events.ndjson
```

Submit the finite capture with the collector credential:

```bash
curl --cacert lab-state/tls/ca.crt \
  --cert lab-state/tls/collector.crt \
  --key lab-state/tls/collector.key \
  -H 'Content-Type: application/x-ndjson' \
  --data-binary @events.ndjson \
  https://localhost:9444/v1/events:batch
python3 -m logbranik decisions
python3 -m logbranik mode enforce
```

Wait for a newly acknowledged delivery revision, then request another path. The local requests originate from `127.0.0.1`, so that is the address the lab rule will match. The fixture address from lesson 4 is a separate demonstration and does not match a real loopback curl request.

This finite-capture exercise closes the full path once. Continuous real-time tailing, rotation, and replay use the production collector design and require their own acceptance test. Do not claim that manually normalizing a file is a streaming collector.

## Stop and preserve evidence

Stop the isolated Nginx instance using its generated configuration:

```bash
nginx -s quit -c "$PWD/lab-state/nginx.conf" -p "$PWD/lab-state/"
```

Interrupt the lab processes. Save the command output and relevant request IDs. The agent cleans its socket during orderly shutdown; a hard-killed process can leave a stale socket path. Verify that the process is absent and that the path is the lab socket before removing only that socket. The program refuses to overwrite an existing socket automatically.

Never archive a populated `lab-state` directory into a public code package. It contains private keys and may contain access observations. The distributed package contains generation code and empty configuration examples only.

## Deployment evidence still required

Record the actual Nginx version and configure options, route coverage, body preservation, blocked-upstream exclusion, unavailable-agent profile, proxy trust behavior, Unix ownership, collector rotation, and end-to-end latency. The delivered preparation evidence does not substitute for this run on your server.
