"""Signed, bounded teaching protocol; no network or database dependency."""
import base64
import hashlib
import ipaddress
import json
import math
import os
import re
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

DOMAIN = b"nginx-guard/snapshot/v1\x00"
MAX_BODY = 1_048_576
MAX_DECISIONS = 5_000
MAX_REVISION = 2**63 - 1


class Rejected(ValueError):
    """Untrusted input failed the teaching protocol."""


def require(condition, message):
    if not condition:
        raise Rejected(message)


def exact_keys(value, keys):
    require(isinstance(value, dict) and set(value) == set(keys), "object keys")


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def decode(data):
    require(isinstance(data, bytes) and len(data) <= MAX_BODY, "body size")
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite JSON")))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Rejected("invalid JSON") from exc


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def integer(value, minimum=0, maximum=MAX_REVISION):
    require(type(value) is int and minimum <= value <= maximum, "integer bounds")
    return value


def text(value, maximum=128):
    require(isinstance(value, str) and 0 < len(value) <= maximum, "string bounds")
    require(not any(ord(c) < 32 for c in value), "control characters")
    return value


def timestamp(value):
    # Lab uses integer UTC Unix seconds, deliberately different from production RFC3339.
    return integer(value)


def ip(value):
    require(isinstance(value, str) and "%" not in value, "IP string")
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise Rejected("invalid IP") from exc
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        address = address.ipv4_mapped
    return str(address)


def sign(payload, private_key, key_id="lab-key"):
    raw = encode(payload)
    return encode({"key_id": key_id, "payload_b64": base64.b64encode(raw).decode(),
                   "signature_b64": base64.b64encode(private_key.sign(DOMAIN + raw)).decode()})


def verify(envelope, public_keys):
    outer = decode(envelope)
    exact_keys(outer, ["key_id", "payload_b64", "signature_b64"])
    text(outer["key_id"])
    require(outer["key_id"] in public_keys, "unknown signing key")
    try:
        raw = base64.b64decode(outer["payload_b64"], validate=True)
        signature = base64.b64decode(outer["signature_b64"], validate=True)
        public_keys[outer["key_id"]].verify(signature, DOMAIN + raw)
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise Rejected("signature or encoding") from exc
    return decode(raw), hashlib.sha256(raw).hexdigest()


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".state-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@dataclass(frozen=True)
class View:
    revision: int
    digest: str
    sites: object
    allowlist: frozenset
    bans: object


class Agent:
    def __init__(self, agent_id, epoch, sites, keys, state_file,
                 clock=time.time, monotonic=time.monotonic, emergency=()):
        self.agent_id, self.epoch = agent_id, epoch
        self.sites, self.keys = frozenset(sites), dict(keys)
        self.state_file = Path(state_file)
        self.clock, self.monotonic = clock, monotonic
        self.emergency = frozenset(ip(x) for x in emergency)
        self.bypass = False
        self.view = None
        self.update_lock = threading.Lock()
        self.anchor = (clock(), monotonic())
        if self.state_file.exists():
            self._apply(self.state_file.read_bytes(), restore=True)

    def healthy_clock(self):
        wall, mono = self.anchor
        return abs((self.clock() - wall) - (self.monotonic() - mono)) <= 30

    def apply(self, envelope):
        with self.update_lock:
            return self._apply(envelope, restore=False)

    def _apply(self, envelope, restore):
        payload, digest = verify(envelope, self.keys)
        exact_keys(payload, ["schema_version", "agent_id", "epoch", "revision",
                             "issued_at", "valid_until", "sites", "allowlist", "decisions"])
        require(type(payload["schema_version"]) is int and payload["schema_version"] == 1, "version")
        require(payload["agent_id"] == self.agent_id and payload["epoch"] == self.epoch, "target or epoch")
        revision = integer(payload["revision"], 1)
        issued, valid = timestamp(payload["issued_at"]), timestamp(payload["valid_until"])
        require(0 < valid - issued <= 120, "delivery interval")
        current = self.view
        if current and not restore:
            require(revision >= current.revision, "stale revision")
            if revision == current.revision:
                require(digest == current.digest, "revision conflict")
                return self.ack(current)
        now, mono = self.clock(), self.monotonic()
        require(self.healthy_clock() and issued <= now + 30, "clock health")
        if not restore:
            require(now < valid, "delivery expired")
        exact_keys(payload["sites"], self.sites)
        require(all(v in ("monitor", "enforce") for v in payload["sites"].values()), "site mode")
        require(isinstance(payload["allowlist"], list) and len(payload["allowlist"]) <= MAX_DECISIONS,
                "allowlist count")
        allow = set()
        for item in payload["allowlist"]:
            exact_keys(item, ["site_id", "ip"])
            text(item["site_id"])
            require(item["site_id"] in self.sites, "allowlist scope")
            pair = (item["site_id"], ip(item["ip"]))
            require(pair not in allow, "duplicate allowlist")
            allow.add(pair)
        decisions = payload["decisions"]
        require(isinstance(decisions, list) and len(decisions) <= MAX_DECISIONS, "decision count")
        bans, ids = {}, set()
        for decision in decisions:
            exact_keys(decision, ["decision_id", "site_id", "ip", "issued_at", "expires_at", "reason_code"])
            did = text(decision["decision_id"])
            require(did not in ids, "duplicate decision id")
            ids.add(did)
            site = decision["site_id"]
            text(site)
            require(site in self.sites, "decision scope")
            address = ip(decision["ip"])
            start, end = timestamp(decision["issued_at"]), timestamp(decision["expires_at"])
            require(0 < end - start <= 86400 and start <= issued, "ban TTL")
            text(decision["reason_code"], 64)
            key = (site, address)
            require(key not in bans, "duplicate IP decision")
            deadline = mono + max(0, end - now)
            if current and key in current.bans and current.bans[key][0] == did:
                deadline = min(deadline, current.bans[key][2])
            bans[key] = (did, end, deadline)
        view = View(revision, digest, MappingProxyType(dict(payload["sites"])),
                    frozenset(allow), MappingProxyType(bans))
        if not restore:
            atomic_write(self.state_file, envelope)
        self.view = view
        return self.ack(view)

    def ack(self, view):
        return {"agent_id": self.agent_id, "epoch": self.epoch,
                "revision": view.revision, "payload_sha256": view.digest}

    def check(self, site, address):
        require(site in self.sites, "unknown site")
        address = ip(address)
        view = self.view
        if self.bypass or address in self.emergency:
            return 204, "bypass"
        if view is None or not self.healthy_clock():
            return 503, "unavailable"
        if (site, address) in view.allowlist:
            return 204, "allow"
        ban = view.bans.get((site, address))
        if ban and self.clock() < ban[1] and self.monotonic() < ban[2]:
            if view.sites[site] == "monitor":
                return 204, "would_block"
            return 403, "block"
        return 204, "allow"
