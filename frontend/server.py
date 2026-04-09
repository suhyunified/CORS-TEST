#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

HOST = "0.0.0.0"
PORT = 3000
ROOT = os.path.dirname(__file__)


if __name__ == "__main__":
    os.chdir(ROOT)
    print(f"[frontend] serving {ROOT} at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    server.serve_forever()
