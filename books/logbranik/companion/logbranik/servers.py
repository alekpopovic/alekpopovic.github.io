"""Unix authorization and bounded role-pinned mTLS teaching endpoints."""
import hashlib
import http.server
import socket
import socketserver
import ssl
import sqlite3
import threading
import urllib.request
from pathlib import Path

from .protocol import MAX_BODY, Rejected, decode, encode, require


class BoundedThreads(socketserver.ThreadingMixIn):
    daemon_threads = True
    def __init__(self, *args, **kwargs):
        self.slots = threading.BoundedSemaphore(32)
        super().__init__(*args, **kwargs)

    def process_request(self, request, address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.slots.release()


class UnixServer(BoundedThreads, socketserver.UnixStreamServer):
    pass


class TLSHTTPServer(BoundedThreads, http.server.HTTPServer):
    pass


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def setup(self):
        self.request.settimeout(5)
        super().setup()

    def log_message(self, *args):
        pass  # Do not dump request input or certificates into teaching logs.

    def reply(self, status, body=b"", headers=None):
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        if body:
            self.send_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            self.send_header(key, str(value))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def read_body(self):
        require(not self.headers.get("Transfer-Encoding"), "chunked not supported in lab")
        lengths = self.headers.get_all("Content-Length", [])
        require(len(lengths) == 1 and lengths[0].isdigit(), "content length")
        size = int(lengths[0])
        require(0 < size <= MAX_BODY, "body size")
        body = self.rfile.read(size)
        require(len(body) == size, "truncated body")
        return body


def auth_handler(agent):
    class Auth(Handler):
        def do_GET(self):
            if self.path != "/v1/check":
                return self.reply(404)
            try:
                for header in ("X-Guard-IP", "X-Guard-Site"):
                    require(len(self.headers.get_all(header, [])) == 1, "check header")
                status, outcome = agent.check(self.headers["X-Guard-Site"], self.headers["X-Guard-IP"])
                self.reply(status, headers={"X-Guard-Outcome": outcome,
                                           "X-Guard-Revision": agent.view.revision if agent.view else 0})
            except Rejected:
                self.reply(400)
        def do_POST(self):
            self.reply(405)
    return Auth


def auth_tcp_server(address, agent):
    require(address[0] == "127.0.0.1", "lab auth TCP must be loopback")
    return TLSHTTPServer(address, auth_handler(agent))


def auth_server(path, agent):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.exists(), "socket already exists; inspect before removing")
    server = UnixServer(str(path), auth_handler(agent))
    path.chmod(0o660)
    return server


def server_context(directory, name):
    directory = Path(directory)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(directory / f"{name}.crt", directory / f"{name}.key")
    context.load_verify_locations(directory / "ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def client_context(directory, name):
    directory = Path(directory)
    context = ssl.create_default_context(cafile=str(directory / "ca.crt"))
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(directory / f"{name}.crt", directory / f"{name}.key")
    return context


def tls_server(address, directory, role, agent=None, central=None, allowed=None):
    allowed = dict(allowed or {})
    class TLSHandler(Handler):
        def do_POST(self):
            fingerprint = hashlib.sha256(self.connection.getpeercert(binary_form=True)).hexdigest()
            identity = allowed.get(fingerprint)
            if identity is None:
                return self.reply(403)
            try:
                if role == "agent" and self.path == "/v1/snapshots":
                    require(identity["role"] == "publisher", "wrong role")
                    require(self.headers.get("Content-Type", "").split(";")[0] == "application/json", "content type")
                    self.reply(200, encode(agent.apply(self.read_body())))
                elif role == "central" and self.path == "/v1/events:batch":
                    require(identity["role"] == "collector", "wrong role")
                    require(self.headers.get("Content-Type", "").split(";")[0] == "application/x-ndjson", "content type")
                    counts = central.ingest(identity["node"], self.read_body(), identity["sites"])
                    self.reply(200, encode(counts))
                else:
                    self.reply(404)
            except Rejected as exc:
                self.reply(422, encode({"error": str(exc)}))
            except (OSError, sqlite3.Error):
                self.reply(503)
    server = TLSHTTPServer(address, TLSHandler)
    server.socket = server_context(directory, role).wrap_socket(server.socket, server_side=True)
    return server


def push(url, envelope, directory):
    require(url.startswith("https://"), "HTTPS only")
    request = urllib.request.Request(url, data=envelope, method="POST",
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, context=client_context(directory, "publisher"), timeout=5) as response:
        ack = decode(response.read(MAX_BODY + 1))
    import base64
    raw = base64.b64decode(decode(envelope)["payload_b64"], validate=True)
    payload = decode(raw)
    for field in ("agent_id", "epoch", "revision"):
        require(ack.get(field) == payload[field], "ack identity")
    require(ack.get("payload_sha256") == hashlib.sha256(raw).hexdigest(), "ack digest")
    return ack
