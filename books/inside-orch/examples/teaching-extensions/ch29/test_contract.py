"""Supplied fake verdict tests; no signature, SBOM or scanner is executed."""
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from contract import Request, Verdict, decide

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 13, tzinfo=timezone.utc)
        self.request = Request("atlas-dev", "synthetic-non-executing-digest", "policy-1")
        self.verdict = Verdict(self.request.namespace, self.request.digest, "policy-1", True, self.now + timedelta(hours=1), "complete", self.now + timedelta(hours=1), 0)
    def test_fresh_supplied_verdict(self):
        self.assertEqual(decide(self.request, self.verdict, self.now), ("allow", "fresh_supplied_verdict"))
    def test_namespace_digest_policy_are_bound(self):
        for changed in [replace(self.request, namespace="another"), replace(self.request, digest="other"), replace(self.request, policy_revision="policy-2")]:
            with self.subTest(changed=changed):
                self.assertEqual(decide(changed, self.verdict, self.now)[1], "subject_mismatch")
    def test_untrusted_or_expired_signature_denied(self):
        self.assertEqual(decide(self.request, replace(self.verdict, signature_trusted=False), self.now)[1], "signature_untrusted")
        self.assertEqual(decide(self.request, replace(self.verdict, signature_expires=self.now), self.now)[1], "signature_expired")
    def test_stale_scan_and_critical_findings_denied(self):
        self.assertEqual(decide(self.request, replace(self.verdict, scan_expires=self.now), self.now)[1], "scan_expired")
        self.assertEqual(decide(self.request, replace(self.verdict, critical_findings=1), self.now)[1], "critical_findings")
    def test_pending_exception_is_explicit_and_narrow(self):
        pending = replace(self.verdict, scan_state="pending")
        self.assertEqual(decide(self.request, pending, self.now)[0], "deny")
        self.assertEqual(decide(self.request, pending, self.now, allow_scan_pending=True), ("allow_with_audit", "explicit_pending_scan_exception"))
        unavailable = replace(self.verdict, scan_state="unavailable")
        self.assertEqual(decide(self.request, unavailable, self.now, allow_scan_pending=True)[0], "deny")
        self.assertEqual(decide(self.request, replace(pending, signature_trusted=False), self.now, allow_scan_pending=True)[0], "deny")

if __name__ == "__main__":
    unittest.main(verbosity=2)
