"""Single-process SQLite laboratory, not the production PostgreSQL worker."""
import hashlib
import math
import re
import sqlite3
import threading
import time
import uuid

from .protocol import (Rejected, decode, encode, exact_keys, integer, ip,
                       require, sign, text, timestamp)

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
 node TEXT NOT NULL, request_id TEXT NOT NULL, hash TEXT NOT NULL,
 site TEXT NOT NULL, ip TEXT NOT NULL, event_time INTEGER NOT NULL,
 status INTEGER NOT NULL, path TEXT NOT NULL, enforcement TEXT NOT NULL,
 eligible INTEGER NOT NULL, PRIMARY KEY(node,request_id));
CREATE INDEX IF NOT EXISTS evidence ON events(site,ip,event_time);
CREATE TABLE IF NOT EXISTS decisions (
 id TEXT PRIMARY KEY, site TEXT NOT NULL, ip TEXT NOT NULL,
 issued INTEGER NOT NULL, expires INTEGER NOT NULL, reason TEXT NOT NULL,
 revoked INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS quarantine (created INTEGER NOT NULL, reason TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS modes (site TEXT PRIMARY KEY, mode TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS revisions (agent TEXT PRIMARY KEY, value INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS outbox (
 agent TEXT NOT NULL, revision INTEGER NOT NULL, envelope BLOB NOT NULL,
 created INTEGER NOT NULL, PRIMARY KEY(agent,revision));
"""


def validate_event(value, sites):
    exact_keys(value, ["schema_version", "request_id", "event_time", "site_id", "client_ip",
                       "method", "path", "status", "request_time_ms", "bytes_sent", "enforcement"])
    require(type(value["schema_version"]) is int and value["schema_version"] == 1, "event version")
    require(isinstance(value["request_id"], str) and
            re.fullmatch(r"[0-9a-f]{32}", value["request_id"]) is not None, "request id")
    text(value["site_id"])
    require(value["site_id"] in sites, "event site")
    timestamp(value["event_time"])
    address = ip(value["client_ip"])
    text(value["method"], 16)
    path = text(value["path"], 2048)
    require(path.startswith("/") and "?" not in path and "#" not in path, "query-free path")
    integer(value["status"], 100, 599)
    integer(value["bytes_sent"], 0)
    duration = value["request_time_ms"]
    require(type(duration) in (int, float) and math.isfinite(duration) and 0 <= duration <= 86400000,
            "duration")
    require(value["enforcement"] in ("allow", "block", "would_block", "bypass", "unavailable", "unknown"),
            "enforcement")
    return dict(value, client_ip=address)


class Central:
    def __init__(self, path, sites=("site-demo",), clock=time.time, threshold=5, ttl=900):
        require(1 <= threshold <= 10000 and 0 < ttl <= 86400, "detector settings")
        self.clock, self.sites, self.threshold, self.ttl = clock, frozenset(sites), threshold, ttl
        self.lock = threading.Lock()
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.executescript(SCHEMA)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        with self.db:
            for site in sites:
                self.db.execute("INSERT OR IGNORE INTO modes VALUES (?, 'monitor')", (site,))

    def close(self):
        self.db.close()

    def ingest(self, node, body, authorized_sites=None):
        text(node)
        require(isinstance(body, bytes) and 0 < len(body) <= 1048576, "batch size")
        lines = body.splitlines()
        require(0 < len(lines) <= 500, "batch count")
        allowed = self.sites if authorized_sites is None else self.sites & frozenset(authorized_sites)
        counts = {"accepted": 0, "duplicates": 0, "quarantined": 0}
        now = int(self.clock())
        with self.lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            for line in lines:
                try:
                    require(0 < len(line) <= 16384, "line size")
                    event = validate_event(decode(line), allowed)
                    # Hash original validated representation before normalization.
                    digest = hashlib.sha256(encode(decode(line))).hexdigest()
                    existing = self.db.execute("SELECT hash FROM events WHERE node=? AND request_id=?",
                                               (node, event["request_id"])).fetchone()
                    if existing:
                        require(existing[0] == digest, "conflicting duplicate")
                        counts["duplicates"] += 1
                        continue
                    eligible = int(now - 120 <= event["event_time"] <= now + 30 and
                                   event["enforcement"] == "allow")
                    self.db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)",
                                    (node, event["request_id"], digest, event["site_id"], event["client_ip"],
                                     event["event_time"], event["status"], event["path"], event["enforcement"], eligible))
                    counts["accepted"] += 1
                    if eligible and event["status"] == 404:
                        self._detect(event["site_id"], event["client_ip"], now)
                except Rejected as exc:
                    self.db.execute("INSERT INTO quarantine VALUES (?,?)", (now, str(exc)[:128]))
                    counts["quarantined"] += 1
        return counts

    def _detect(self, site, address, now):
        # A deliberately small teaching rule: 404s on distinct paths, last 60s.
        count = self.db.execute("""SELECT count(DISTINCT path) FROM events
          WHERE site=? AND ip=? AND eligible=1 AND status=404
          AND event_time BETWEEN ? AND ?""", (site, address, now - 60, now)).fetchone()[0]
        active = self.db.execute("""SELECT 1 FROM decisions
          WHERE site=? AND ip=? AND expires>? AND revoked=0""", (site, address, now)).fetchone()
        # Persisted cooldown prevents immediate renewal from old window evidence.
        recent = self.db.execute("""SELECT 1 FROM decisions
          WHERE site=? AND ip=? AND issued>?""", (site, address, now - max(self.ttl, 120))).fetchone()
        if count >= self.threshold and not active and not recent:
            self.db.execute("INSERT INTO decisions(id,site,ip,issued,expires,reason) VALUES(?,?,?,?,?,?)",
                            (uuid.uuid4().hex, site, address, now, now + self.ttl, "distinct-404-paths/v1"))

    def mode(self, site, mode):
        require(site in self.sites and mode in ("monitor", "enforce"), "mode")
        with self.lock, self.db:
            self.db.execute("UPDATE modes SET mode=? WHERE site=?", (mode, site))

    def revoke(self, decision_id):
        with self.lock, self.db:
            result = self.db.execute("UPDATE decisions SET revoked=1 WHERE id=?", (decision_id,))
            require(result.rowcount == 1, "unknown decision")

    def snapshot(self, agent_id, epoch, private_key, allowlist=()):
        now = int(self.clock())
        with self.lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            row = self.db.execute("SELECT value FROM revisions WHERE agent=?", (agent_id,)).fetchone()
            revision = integer((row[0] if row else 0) + 1, 1)
            self.db.execute("INSERT OR REPLACE INTO revisions VALUES (?,?)", (agent_id, revision))
            sites = dict(self.db.execute("SELECT site, mode FROM modes"))
            rows = self.db.execute("""SELECT id,site,ip,issued,expires,reason FROM decisions
              WHERE revoked=0 AND expires>? ORDER BY site,ip""", (now,)).fetchall()
            payload = {"schema_version": 1, "agent_id": agent_id, "epoch": epoch, "revision": revision,
                       "issued_at": now, "valid_until": now + 120, "sites": sites,
                       "allowlist": list(allowlist), "decisions": [dict(zip(
                           ["decision_id", "site_id", "ip", "issued_at", "expires_at", "reason_code"], row))
                           for row in rows]}
            envelope = sign(payload, private_key)
            self.db.execute("INSERT INTO outbox VALUES (?,?,?,?)", (agent_id, revision, envelope, now))
        return envelope

    def decisions(self):
        with self.lock:
            return [dict(zip(["id", "site", "ip", "issued", "expires", "reason", "revoked"], row))
                    for row in self.db.execute("SELECT * FROM decisions ORDER BY issued,id")]
