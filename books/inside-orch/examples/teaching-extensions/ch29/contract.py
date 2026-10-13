"""Book-only decision contract with supplied verdicts; performs no verification/network IO."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Request:
    namespace: str
    digest: str
    policy_revision: str

@dataclass(frozen=True)
class Verdict:
    namespace: str
    digest: str
    policy_revision: str
    signature_trusted: bool
    signature_expires: datetime
    scan_state: str
    scan_expires: datetime
    critical_findings: int


def decide(request: Request, verdict: Verdict, now: datetime, *, allow_scan_pending=False):
    if (request.namespace, request.digest, request.policy_revision) != (verdict.namespace, verdict.digest, verdict.policy_revision):
        return "deny", "subject_mismatch"
    if not verdict.signature_trusted:
        return "deny", "signature_untrusted"
    if now >= verdict.signature_expires:
        return "deny", "signature_expired"
    if verdict.scan_state != "complete":
        if allow_scan_pending and verdict.scan_state == "pending":
            return "allow_with_audit", "explicit_pending_scan_exception"
        return "deny", "scan_unavailable"
    if now >= verdict.scan_expires:
        return "deny", "scan_expired"
    if verdict.critical_findings > 0:
        return "deny", "critical_findings"
    return "allow", "fresh_supplied_verdict"
