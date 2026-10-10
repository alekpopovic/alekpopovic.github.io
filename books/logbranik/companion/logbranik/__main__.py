import argparse
import json
import secrets
import tempfile
import threading
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .central import Central
from .protocol import Agent, atomic_write, encode, require, sign
from . import certificates, servers


def fixture_event(number, now, address="198.51.100.23", enforcement="allow"):
    return {"schema_version": 1, "request_id": f"{number:032x}", "event_time": int(now),
            "site_id": "site-demo", "client_ip": address, "method": "GET", "path": f"/missing-{number}",
            "status": 404, "request_time_ms": 2, "bytes_sent": 64, "enforcement": enforcement}


def demo():
    with tempfile.TemporaryDirectory(prefix="logbranik-") as root:
        private = Ed25519PrivateKey.generate()
        central = Central(Path(root) / "central.sqlite3")
        agent = Agent("edge-a", "demo-epoch", ["site-demo"], {"lab-key": private.public_key()},
                      Path(root) / "agent.json")
        try:
            initial = central.snapshot("edge-a", "demo-epoch", private)
            agent.apply(initial)
            print("before", agent.check("site-demo", "198.51.100.23"))
            body = b"\n".join(encode(fixture_event(i, time.time())) for i in range(1, 6))
            print("ingest", central.ingest("node-a", body))
            agent.apply(central.snapshot("edge-a", "demo-epoch", private))
            print("monitor", agent.check("site-demo", "198.51.100.23"))
            central.mode("site-demo", "enforce")
            ack = agent.apply(central.snapshot("edge-a", "demo-epoch", private))
            print("enforce", agent.check("site-demo", "198.51.100.23"))
            print("revision", ack["revision"])
            central.revoke(central.decisions()[0]["id"])
            agent.apply(central.snapshot("edge-a", "demo-epoch", private))
            print("revoked", agent.check("site-demo", "198.51.100.23"))
        finally:
            central.close()


def main():
    parser = argparse.ArgumentParser(description="LogBranik teaching lab")
    parser.add_argument("--directory", default="lab-state")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("certificates")
    sub.add_parser("demo")
    p = sub.add_parser("agent"); p.add_argument("--tcp-auth",action="store_true")
    sub.add_parser("central-server")
    sub.add_parser("snapshot")
    sub.add_parser("decisions")
    p = sub.add_parser("ingest"); p.add_argument("file"); p.add_argument("--node", default="node-a")
    p = sub.add_parser("mode"); p.add_argument("mode", choices=["monitor", "enforce"])
    p = sub.add_parser("revoke"); p.add_argument("id")
    p = sub.add_parser("push"); p.add_argument("url", nargs="?", default="https://localhost:9443/v1/snapshots")
    args = parser.parse_args()
    root = Path(args.directory)
    if args.command == "demo":
        return demo()
    if args.command == "init":
        require(not root.exists(), "state directory already exists")
        root.mkdir(parents=True, mode=0o700)
        private = Ed25519PrivateKey.generate()
        atomic_write(root / "signing.key", private.private_bytes_raw())
        atomic_write(root / "signing.pub", private.public_key().public_bytes_raw())
        atomic_write(root / "config.json", encode({"agent_id": "edge-a", "epoch": secrets.token_hex(16)}))
        with_context = Central(root / "central.sqlite3"); with_context.close()
        print("initialized", root)
        return
    if args.command == "certificates":
        require(root.exists(), "run init first")
        certificates.create(root / "tls")
        print("created disposable loopback certificates")
        return
    config = json.loads((root / "config.json").read_text())
    if args.command == "agent":
        agent = Agent(config["agent_id"], config["epoch"], ["site-demo"],
                      {"lab-key": Ed25519PublicKey.from_public_bytes((root / "signing.pub").read_bytes())},
                      root / "agent.json")
        fingerprints = json.loads((root / "tls/fingerprints.json").read_text())
        auth = (servers.auth_tcp_server(("127.0.0.1",9101),agent) if args.tcp_auth else
                servers.auth_server(root / "auth.sock", agent))
        control = servers.tls_server(("127.0.0.1", 9443), root / "tls", "agent", agent=agent,
                                    allowed={fingerprints["publisher"]: {"role": "publisher"}})
        thread = threading.Thread(target=auth.serve_forever, daemon=True); thread.start()
        print("local auth and loopback mTLS control ready; first snapshot required", flush=True)
        try:
            control.serve_forever()
        finally:
            auth.shutdown(); auth.server_close(); control.server_close()
            (root / "auth.sock").unlink(missing_ok=True)
        return
    if args.command == "push":
        print(servers.push(args.url, (root / "snapshot.json").read_bytes(), root / "tls"))
        return
    central = Central(root / "central.sqlite3")
    try:
        if args.command == "central-server":
            fingerprints = json.loads((root / "tls/fingerprints.json").read_text())
            api = servers.tls_server(("127.0.0.1", 9444), root / "tls", "central", central=central,
                      allowed={fingerprints["collector"]: {"role": "collector", "node": "node-a", "sites": ["site-demo"]}})
            print("loopback mTLS ingestion ready", flush=True)
            try: api.serve_forever()
            finally: api.server_close()
        elif args.command == "snapshot":
            private = Ed25519PrivateKey.from_private_bytes((root / "signing.key").read_bytes())
            atomic_write(root / "snapshot.json", central.snapshot(config["agent_id"], config["epoch"], private))
            print("snapshot saved")
        elif args.command == "ingest":
            print(central.ingest(args.node, Path(args.file).read_bytes()))
        elif args.command == "mode":
            central.mode("site-demo", args.mode)
        elif args.command == "revoke":
            central.revoke(args.id)
        elif args.command == "decisions":
            print(json.dumps(central.decisions(), indent=2))
    finally:
        central.close()


if __name__ == "__main__":
    main()
