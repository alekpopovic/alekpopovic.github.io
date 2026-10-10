"""Convert completed Nginx JSON access logs into the lab's integer-time NDJSON."""
import argparse
import datetime
import json
import sys

from logbranik.central import validate_event
from logbranik.protocol import encode


def normalize(line):
    value = json.loads(line)
    observed = datetime.datetime.fromisoformat(value["event_time"].replace("Z", "+00:00"))
    if observed.utcoffset() is None:
        raise ValueError("event timestamp requires UTC offset")
    value["event_time"] = int(observed.timestamp())
    value["status"] = int(value["status"])
    value["bytes_sent"] = int(value["bytes_sent"])
    value["request_time_ms"] = float(value.pop("request_time_seconds")) * 1000
    return validate_event(value, ["site-demo"])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("file"); args=parser.parse_args()
    with open(args.file) as source:
        for number,line in enumerate(source,1):
            try: sys.stdout.buffer.write(encode(normalize(line))+b"\n")
            except (ValueError,KeyError) as exc:
                raise SystemExit(f"invalid input at line {number}: {exc}")
