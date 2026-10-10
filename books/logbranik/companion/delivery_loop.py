"""Lab-only periodic signed push. Production uses a durable outbox dispatcher."""
import argparse
import json
import random
import time
import urllib.error
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from logbranik.central import Central
from logbranik.protocol import Rejected
from logbranik.servers import push


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--directory",default="lab-state")
    parser.add_argument("--url",default="https://localhost:9443/v1/snapshots")
    parser.add_argument("--interval",type=float,default=1.0)
    args=parser.parse_args()
    if not 0.1 <= args.interval <= 60: parser.error("interval must be 0.1..60 seconds")
    root=Path(args.directory)
    config=json.loads((root/"config.json").read_text())
    key=Ed25519PrivateKey.from_private_bytes((root/"signing.key").read_bytes())
    central=Central(root/"central.sqlite3")
    delay=args.interval
    try:
        while True:
            envelope=central.snapshot(config["agent_id"],config["epoch"],key)
            try:
                ack=push(args.url,envelope,root/"tls")
                print(json.dumps({"applied_revision":ack["revision"]}),flush=True)
                delay=args.interval
            except urllib.error.HTTPError as exc:
                if 400 <= exc.code < 500 and exc.code != 429:
                    raise SystemExit(f"control rejected ({exc.code}); inspect epoch, clock and permissions")
                print("transient HTTP delivery failure",flush=True)
                delay=min(30,max(args.interval,delay*2))
            except (urllib.error.URLError,OSError):
                print("control unavailable",flush=True)
                delay=min(30,max(args.interval,delay*2))
            except Rejected as exc:
                raise SystemExit(f"invalid acknowledgement: {exc}")
            time.sleep(delay+random.uniform(0,delay*0.1))
    finally: central.close()


if __name__ == "__main__": main()
