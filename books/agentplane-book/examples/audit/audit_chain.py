# SPDX-License-Identifier: MIT
"""A deterministic teaching chain, not a signature or immutable audit service."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac
import json
from typing import Any

ZERO = "0" * 64
DOMAIN = b"agentplane-book-audit-v1\x00"

def canonical(value: Any) -> bytes:
    """Use a deliberately restricted JSON domain; no float canonicalization."""
    def valid(v: Any) -> bool:
        if v is None or isinstance(v, (str, bool, int)):
            return True
        if isinstance(v, list):
            return all(valid(x) for x in v)
        if isinstance(v, dict):
            return all(isinstance(k, str) and valid(x) for k, x in v.items())
        return False
    if not valid(value):
        raise ValueError("only null, string, boolean, integer, list and string-key map")
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")

@dataclass(frozen=True)
class Checkpoint:
    count: int
    head: str


def build(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Checkpoint]:
    rows: list[dict[str, Any]] = []
    previous = ZERO
    for seq, event in enumerate(events, 1):
        # Detach caller data so later mutation cannot change a stored event.
        detached = json.loads(canonical(event))
        body = {"sequence": seq, "previous": previous, "event": detached}
        digest = hashlib.sha256(DOMAIN + canonical(body)).hexdigest()
        rows.append({**body, "hash": digest})
        previous = digest
    return rows, Checkpoint(len(rows), previous)


def verify(rows: list[dict[str, Any]], trusted: Checkpoint) -> bool:
    if len(rows) != trusted.count:
        return False
    previous = ZERO
    try:
        for seq, row in enumerate(rows, 1):
            if set(row) != {"sequence", "previous", "event", "hash"}:
                return False
            if type(row["sequence"]) is not int or row["sequence"] != seq:
                return False
            if row["previous"] != previous or not isinstance(row["hash"], str):
                return False
            body = {"sequence": seq, "previous": previous, "event": row["event"]}
            digest = hashlib.sha256(DOMAIN + canonical(body)).hexdigest()
            if not hmac.compare_digest(digest, row["hash"]):
                return False
            previous = digest
        return hmac.compare_digest(previous, trusted.head)
    except (ValueError, TypeError, KeyError, UnicodeError):
        return False

if __name__ == "__main__":
    events = [
        {"scope": "org-example", "action": "session.requested", "resource": "s1"},
        {"scope": "org-example", "action": "session.terminated", "resource": "s1"},
    ]
    records, checkpoint = build(events)
    print(json.dumps({"count": checkpoint.count, "head": checkpoint.head,
                      "verified": verify(records, checkpoint)}, indent=2))
