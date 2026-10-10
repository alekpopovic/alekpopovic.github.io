import base64
import concurrent.futures
import http.client
import json
import socket
import ssl
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from logbranik import certificates, servers
from logbranik.__main__ import fixture_event
from logbranik.central import Central
from logbranik.protocol import Agent, Rejected, decode, encode, sign


class Clock:
    def __init__(self): self.wall, self.mono = 2_000_000_000, 1000
    def advance(self, seconds): self.wall += seconds; self.mono += seconds
    def time(self): return self.wall
    def monotonic(self): return self.mono


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.key = Ed25519PrivateKey.generate()
        self.clock = Clock()
        self.central = Central(self.root / "central.sqlite", clock=self.clock.time)
        self.agent = self.new_agent()
    def tearDown(self): self.central.close(); self.temp.cleanup()
    def new_agent(self):
        return Agent("edge-a", "epoch-a", ["site-demo"], {"lab-key": self.key.public_key()},
                     self.root / "state.json", clock=self.clock.time, monotonic=self.clock.monotonic)
    def envelope(self): return self.central.snapshot("edge-a", "epoch-a", self.key)
    def ingest(self, events): return self.central.ingest("node-a", b"\n".join(encode(e) for e in events))
    def trigger(self): self.ingest([fixture_event(i, self.clock.wall) for i in range(1, 6)])
    def payload(self, revision=1):
        return {"schema_version": 1, "agent_id": "edge-a", "epoch": "epoch-a", "revision": revision,
                "issued_at": self.clock.wall, "valid_until": self.clock.wall+120,
                "sites": {"site-demo": "enforce"}, "allowlist": [], "decisions": []}
    def test_first_boot_not_ready(self):
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (503, "unavailable"))
    def test_signed_empty_snapshot_readies(self):
        self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "allow"))
    def test_monitor_then_enforce_then_revoke(self):
        self.trigger(); self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "would_block"))
        self.central.mode("site-demo", "enforce"); self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (403, "block"))
        self.central.revoke(self.central.decisions()[0]["id"]); self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "allow"))
    def test_duplicates_do_not_trigger(self):
        event = fixture_event(1, self.clock.wall)
        self.assertEqual(self.ingest([event]*5), {"accepted": 1, "duplicates": 4, "quarantined": 0})
        self.assertEqual(self.central.decisions(), [])
    def test_conflicting_duplicate_quarantined(self):
        event = fixture_event(1, self.clock.wall); self.ingest([event])
        changed = dict(event, status=500)
        self.assertEqual(self.ingest([changed])["quarantined"], 1)
        self.assertEqual(self.central.db.execute("SELECT status FROM events").fetchone()[0], 404)
    def test_stale_events_never_trigger(self):
        self.ingest([fixture_event(i, self.clock.wall-121) for i in range(5)])
        self.assertEqual(self.central.decisions(), [])
    def test_future_events_never_trigger(self):
        self.ingest([fixture_event(i, self.clock.wall+31) for i in range(5)])
        self.assertEqual(self.central.decisions(), [])
    def test_guard_responses_never_trigger(self):
        self.ingest([fixture_event(i, self.clock.wall, enforcement="block") for i in range(5)])
        self.assertEqual(self.central.decisions(), [])
    def test_single_path_does_not_trigger(self):
        self.ingest([dict(fixture_event(i, self.clock.wall), path="/same") for i in range(5)])
        self.assertEqual(self.central.decisions(), [])
    def test_ipv4_mapped_ipv6_matches(self):
        self.trigger(); self.central.mode("site-demo", "enforce"); self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "::ffff:198.51.100.23"), (403, "block"))
    def test_ipv6_exact_address(self):
        self.ingest([fixture_event(i, self.clock.wall, address="2001:db8::123") for i in range(5)])
        self.central.mode("site-demo", "enforce"); self.agent.apply(self.envelope())
        self.assertEqual(self.agent.check("site-demo", "2001:db8:0:0::123"), (403, "block"))
    def test_scope_rejected(self):
        with self.assertRaises(Rejected): self.agent.check("other", "198.51.100.23")
        e = dict(fixture_event(1, self.clock.wall), site_id="other")
        self.assertEqual(self.ingest([e])["quarantined"], 1)
    def test_bad_record_does_not_poison_neighbors(self):
        body = encode(fixture_event(1, self.clock.wall))+b'\n{"broken":true}\n'+encode(fixture_event(2,self.clock.wall))
        self.assertEqual(self.central.ingest("node-a", body), {"accepted": 2,"duplicates": 0,"quarantined": 1})
    def test_allowlist_wins(self):
        self.trigger(); self.central.mode("site-demo", "enforce")
        self.agent.apply(self.central.snapshot("edge-a", "epoch-a", self.key,
                        [{"site_id": "site-demo", "ip": "198.51.100.23"}]))
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "allow"))
    def test_local_emergency_bypass(self):
        self.agent.bypass = True
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "bypass"))
    def test_expiry_without_central(self):
        self.trigger(); self.central.mode("site-demo", "enforce"); self.agent.apply(self.envelope())
        self.clock.advance(900)
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "allow"))
    def test_refresh_does_not_extend_ttl(self):
        self.trigger(); self.central.mode("site-demo", "enforce"); self.agent.apply(self.envelope())
        self.clock.advance(800); self.agent.apply(self.envelope()); self.clock.advance(100)
        self.assertEqual(self.agent.check("site-demo", "198.51.100.23"), (204, "allow"))
    def test_old_snapshot_cannot_resurrect_revoke(self):
        self.trigger(); old=self.envelope(); self.agent.apply(old)
        self.central.revoke(self.central.decisions()[0]["id"]); self.agent.apply(self.envelope())
        with self.assertRaises(Rejected): self.agent.apply(old)
    def test_exact_duplicate_after_delivery_expiry(self):
        envelope = self.envelope(); ack=self.agent.apply(envelope); self.clock.advance(121)
        self.assertEqual(self.agent.apply(envelope), ack)
    def test_new_expired_envelope_rejected(self):
        envelope=self.envelope(); self.clock.advance(121)
        with self.assertRaises(Rejected): self.agent.apply(envelope)
    def test_same_revision_different_bytes_rejected(self):
        self.agent.apply(sign(self.payload(), self.key))
        p=self.payload(); p["sites"]["site-demo"]="monitor"
        with self.assertRaises(Rejected): self.agent.apply(sign(p,self.key))
    def test_tampered_signature_rejected(self):
        outer=decode(self.envelope()); outer["payload_b64"]=base64.b64encode(b'{}').decode()
        with self.assertRaises(Rejected): self.agent.apply(encode(outer))
    def test_wrong_key_and_epoch_rejected(self):
        with self.assertRaises(Rejected): self.agent.apply(sign(self.payload(),Ed25519PrivateKey.generate()))
        p=self.payload(); p["epoch"]="other"
        with self.assertRaises(Rejected): self.agent.apply(sign(p,self.key))
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(Rejected): decode(b'{"revision":1,"revision":2}')
    def test_boolean_revision_rejected(self):
        p=self.payload(); p["revision"]=True
        with self.assertRaises(Rejected): self.agent.apply(sign(p,self.key))
    def test_bad_ttl_and_zone_id_rejected(self):
        p=self.payload(); p["decisions"]=[{"decision_id":"d","site_id":"site-demo","ip":"198.51.100.23",
            "issued_at":self.clock.wall,"expires_at":self.clock.wall+86401,"reason_code":"test"}]
        with self.assertRaises(Rejected): self.agent.apply(sign(p,self.key))
        with self.assertRaises(Rejected): self.agent.check("site-demo", "fe80::1%eth0")
    def test_atomic_persistence_failure_keeps_old_view(self):
        self.agent.apply(self.envelope()); old=self.agent.view
        with patch("logbranik.protocol.atomic_write", side_effect=OSError("disk full")):
            with self.assertRaises(OSError): self.agent.apply(self.envelope())
        self.assertIs(self.agent.view,old)
        self.assertEqual(self.new_agent().view.revision,old.revision)
    def test_restart_accepts_saved_envelope_after_delivery_expiry(self):
        self.trigger(); self.central.mode("site-demo","enforce"); self.agent.apply(self.envelope())
        self.clock.advance(121)
        self.assertEqual(self.new_agent().check("site-demo","198.51.100.23"),(403,"block"))
    def test_backward_clock_unavailable(self):
        self.agent.apply(self.envelope()); self.clock.wall -= 60
        self.assertEqual(self.agent.check("site-demo","198.51.100.23"),(503,"unavailable"))
    def test_concurrent_checks_during_update(self):
        self.trigger(); self.agent.apply(self.envelope()); self.central.mode("site-demo","enforce")
        new=self.envelope()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            checks=[pool.submit(self.agent.check,"site-demo","198.51.100.23") for _ in range(100)]
            pool.submit(self.agent.apply,new).result()
            outcomes=[f.result() for f in checks]
        self.assertTrue(all(x in [(204,"would_block"),(403,"block")] for x in outcomes))
    def test_unknown_field_and_oversize_rejected(self):
        p=self.payload(); p["execute"]="anything"
        with self.assertRaises(Rejected): self.agent.apply(sign(p,self.key))
        with self.assertRaises(Rejected): decode(b'x'*1048577)
    def test_batch_rejection_is_atomic(self):
        with self.assertRaises(Rejected): self.central.ingest("node-a", b'x'*1048577)
        self.assertEqual(self.central.db.execute("SELECT count(*) FROM events").fetchone()[0],0)
    def test_malformed_nested_types_quarantined(self):
        self.assertEqual(self.ingest([dict(fixture_event(1,self.clock.wall),site_id=[])])["quarantined"],1)
    def test_central_restart_preserves_revision(self):
        first=self.agent.apply(self.envelope())["revision"]
        self.central.close(); self.central=Central(self.root/"central.sqlite",clock=self.clock.time)
        self.assertGreater(self.agent.apply(self.envelope())["revision"],first)


class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(); cls.root=Path(cls.temp.name)
        cls.fingerprints=certificates.create(cls.root/"tls")
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()
    def setUp(self):
        self.key=Ed25519PrivateKey.generate(); self.servers=[]
        self.work=tempfile.TemporaryDirectory(dir=self.root); self.path=Path(self.work.name)
        self.central=Central(self.path/"central.sqlite")
        self.agent=Agent("edge-a","epoch-a",["site-demo"],{"lab-key":self.key.public_key()},self.path/"state.json")
    def tearDown(self):
        for server in self.servers: server.shutdown(); server.server_close()
        self.central.close(); self.work.cleanup()
    def start(self,server):
        self.servers.append(server); threading.Thread(target=server.serve_forever,daemon=True).start()
        return server
    def control(self):
        return self.start(servers.tls_server(("127.0.0.1",0),self.root/"tls","agent",agent=self.agent,
            allowed={self.fingerprints["publisher"]:{"role":"publisher"}}))
    def test_unix_auth_has_no_control_route(self):
        self.agent.apply(self.central.snapshot("edge-a","epoch-a",self.key))
        try:
            self.start(servers.auth_server(self.path/"auth.sock",self.agent))
        except PermissionError:
            self.skipTest("execution host disallows AF_UNIX; run this gate on Linux deployment host")
        connection=http.client.HTTPConnection("localhost")
        def connect():
            connection.sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
            connection.sock.connect(str(self.path/"auth.sock"))
        connection.connect=connect
        connection.request("GET","/v1/check",headers={"X-Guard-IP":"198.51.100.23","X-Guard-Site":"site-demo"})
        self.assertEqual(connection.getresponse().status,204); connection.close()
        connection.request("POST","/v1/snapshots",body=b'{}')
        self.assertEqual(connection.getresponse().status,405); connection.close()
    def test_loopback_auth_has_no_control_route(self):
        self.agent.apply(self.central.snapshot("edge-a","epoch-a",self.key))
        server=self.start(servers.auth_tcp_server(("127.0.0.1",0),self.agent))
        connection=http.client.HTTPConnection("127.0.0.1",server.server_port)
        connection.request("GET","/v1/check",headers={"X-Guard-IP":"198.51.100.23","X-Guard-Site":"site-demo"})
        self.assertEqual(connection.getresponse().status,204); connection.close()
        connection.request("POST","/v1/snapshots",body=b'{}')
        self.assertEqual(connection.getresponse().status,405); connection.close()
    def test_mtls_push_and_ack(self):
        server=self.control(); envelope=self.central.snapshot("edge-a","epoch-a",self.key)
        ack=servers.push(f"https://localhost:{server.server_port}/v1/snapshots",envelope,self.root/"tls")
        self.assertEqual(ack["revision"],1)
        self.assertEqual(self.agent.check("site-demo","198.51.100.23"),(204,"allow"))
    def test_ca_valid_wrong_role_denied(self):
        server=self.control()
        request=urllib.request.Request(f"https://localhost:{server.server_port}/v1/snapshots",data=b'{}',method="POST")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request,context=servers.client_context(self.root/"tls","wrong-role"),timeout=3)
        self.assertEqual(caught.exception.code,403)
    def test_missing_client_certificate_fails(self):
        server=self.control(); context=ssl.create_default_context(cafile=str(self.root/"tls/ca.crt"))
        with self.assertRaises((urllib.error.URLError,ssl.SSLError,ConnectionError,http.client.RemoteDisconnected)):
            urllib.request.urlopen(f"https://localhost:{server.server_port}/v1/snapshots",context=context,timeout=3)
    def test_ingest_identity_from_certificate(self):
        server=self.start(servers.tls_server(("127.0.0.1",0),self.root/"tls","central",central=self.central,
            allowed={self.fingerprints["collector"]:{"role":"collector","node":"cert-node","sites":["site-demo"]}}))
        import time
        request=urllib.request.Request(f"https://localhost:{server.server_port}/v1/events:batch",
            data=encode(fixture_event(1,time.time())),method="POST",headers={"Content-Type":"application/x-ndjson"})
        with urllib.request.urlopen(request,context=servers.client_context(self.root/"tls","collector"),timeout=3) as response:
            self.assertEqual(decode(response.read())["accepted"],1)
        self.assertEqual(self.central.db.execute("SELECT node FROM events").fetchone()[0],"cert-node")


if __name__ == "__main__": unittest.main()
