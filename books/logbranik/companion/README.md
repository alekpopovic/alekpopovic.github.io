# LogBranik teaching lab

Run from this directory with Python 3.12+ and `requirements.txt` installed. Preparation used Cryptography 50.0.1. Follow lesson 4 and Appendix A for commands.

```bash
python3 -m unittest discover -s tests -v
python3 -m logbranik demo
```

For persistent live endpoints run `python3 -m logbranik init`, then `python3 -m logbranik certificates`. Start `agent`, `central-server`, and `delivery_loop.py` in separate terminals. The authorization handler uses a Unix socket by default; `agent --tcp-auth` enables a loopback-only teaching fallback.

The lab has one site, integer UTC timestamps, a narrow distinct-404 detector, exact IP bans, and a SQLite store. It supports signed full policies, strict parsing, ordered revisions, atomic agent persistence, local TTL enforcement, monitor/enforce/revoke, mTLS role authorization, and validated applied acknowledgements.

The lab is not wire-compatible with the richer production protocol. `production-design/` preserves original design documents and configuration candidates from the Claude pack. That stack uses Vector, FastAPI, PostgreSQL, and Go and requires separate implementation and actual-host tests. The bundled ZIP contains the original sixty-task pack; it is not a completed production application.

The periodic lab dispatcher creates revisions repeatedly and does not implement production outbox pruning or pull reconciliation. Stop it after exercises. Never publish populated `lab-state` directories or generated keys. TLS fixtures are disposable loopback credentials, expire in seven days, and are unsuitable for a two-machine deployment.

`render_nginx_config.py` only generates an isolated configuration; it does not start or install Nginx. Confirm the module, socket permissions and route acceptance on your Linux host.


## Author and open licenses

Aleksandar Popovic — https://github.com/alekpopovic. Original code, tests and
configuration are MIT; prose and prompts are CC BY 4.0. These grants include
the bundled Claude Code archive and production-design extracts. License
notices are at the package root and inside the archive.
