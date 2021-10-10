#!/usr/bin/env python3

"""python3 -m http.server PORT for a CORS world."""
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    """CORS class request."""

    def end_headers(self):
        """CORS call for end_headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        return super().end_headers()

    def do_OPTIONS(self):  # CORS specific function name pylint: disable=C0103
        """CORS call for do_OPTIONS."""
        self.send_response(200, "ok")
        self.end_headers()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 2 else "127.0.0.1"
    port = int(sys.argv[len(sys.argv) - 1]) if len(sys.argv) > 1 else 9000
    httpd = HTTPServer((host, port), CORSRequestHandler)
    httpd.serve_forever()

# Run: ./simple_cors_server.py
# Then, open your file server in http://127.0.0.1:9000
