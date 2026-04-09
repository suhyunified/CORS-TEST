#!/usr/bin/env python3
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 4000
ALLOW_ORIGIN = os.environ.get("ALLOW_ORIGIN", "")
ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS", "false").lower() == "true"


def set_cors_headers(handler: BaseHTTPRequestHandler) -> None:
    if ALLOW_ORIGIN:
        handler.send_header("Access-Control-Allow-Origin", ALLOW_ORIGIN)
        handler.send_header("Vary", "Origin")

    if ALLOW_CREDENTIALS:
        handler.send_header("Access-Control-Allow-Credentials", "true")

    handler.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Demo-Header")


class Handler(BaseHTTPRequestHandler):
    def _write_json(self, status: int, payload: dict) -> None:
        self.send_response(status)
        set_cors_headers(self)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        set_cors_headers(self)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/api/hello":
            self._write_json(404, {"ok": False, "message": "not found"})
            return

        self._write_json(
            200,
            {
                "ok": True,
                "message": "Hello from backend",
                "allow_origin": ALLOW_ORIGIN or "(not configured)",
            },
        )


if __name__ == "__main__":
    print(f"[backend] running on http://{HOST}:{PORT}")
    print(f"[backend] ALLOW_ORIGIN={ALLOW_ORIGIN or '(empty: CORS off)'}")
    print(f"[backend] ALLOW_CREDENTIALS={ALLOW_CREDENTIALS}")
    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()
