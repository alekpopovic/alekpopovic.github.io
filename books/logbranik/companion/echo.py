"""Loopback-only upstream with deterministic 404s and a body-preserving echo."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json


class Echo(BaseHTTPRequestHandler):
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()
    def respond(self):
        body=self.rfile.read(min(int(self.headers.get("Content-Length",0)),65536))
        value=json.dumps({"method":self.command,"path":self.path,"body":body.decode(errors="replace")}).encode()
        self.send_response(404 if self.path.startswith("/missing-") else 200)
        self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(value)))
        self.end_headers(); self.wfile.write(value)
    def log_message(self,*args): pass


if __name__ == "__main__": ThreadingHTTPServer(("127.0.0.1",8081),Echo).serve_forever()
