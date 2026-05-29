"""
ClipboardSync — expose clipboard over localhost HTTP for local browser access.

Binds to 127.0.0.1 (loopback only). A random 8-char session token is required
on every request — open the URL shown by `get_url()` which embeds the token.
Token + loopback-only = two layers of access control.
"""

import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import parse_qs, urlparse

import pyperclip

logger = logging.getLogger(__name__)

DEFAULT_PORT = 7778

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Loki Clipboard Sync</title>
<style>
  body{{font-family:sans-serif;background:#0d0d1a;color:#cdd6f4;padding:20px;max-width:600px;margin:auto}}
  h1{{color:#c4a45a}}
  textarea{{width:100%;height:180px;background:#1a1a3a;color:#cdd6f4;border:1px solid #2a2a5a;padding:10px;border-radius:6px;font-size:14px}}
  button{{background:#c4a45a;color:#0d0d1a;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;font-weight:bold;margin:5px}}
  #status{{color:#50fa7b;margin-top:10px;min-height:20px}}
</style>
</head>
<body>
<h1>Loki Clipboard Sync</h1>
<p>PC clipboard content:</p>
<textarea id="clip">{content}</textarea>
<br>
<button onclick="sendClip()">Push to PC</button>
<button onclick="loadClip()">Refresh from PC</button>
<div id="status"></div>
<script>
const TOKEN='{token}';
function setStatus(msg){{document.getElementById('status').textContent=msg;}}
function loadClip(){{
  fetch('/clip?t='+TOKEN).then(r=>r.text()).then(t=>{{
    document.getElementById('clip').value=t;
    setStatus('Refreshed');
  }}).catch(()=>setStatus('Error'));
}}
function sendClip(){{
  const text=document.getElementById('clip').value;
  fetch('/clip?t='+TOKEN,{{method:'POST',body:text,headers:{{'Content-Type':'text/plain'}}}})
    .then(r=>r.text()).then(()=>setStatus('Sent to PC!'))
    .catch(()=>setStatus('Error sending'));
}}
</script>
</body>
</html>"""


def _make_token() -> str:
    return os.urandom(6).hex()  # 12 hex chars


class _Handler(BaseHTTPRequestHandler):
    """Require ?t=<token> on every request."""

    token: str = ""  # set on server start

    def log_message(self, *args):
        pass

    def _check_token(self) -> bool:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        return params.get("t", [""])[0] == self.__class__.token

    def _deny(self):
        body = b"Forbidden: invalid or missing token."
        self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self._check_token():
            self._deny()
            return

        parsed = urlparse(self.path)
        if parsed.path == "/clip":
            try:
                content = pyperclip.paste() or ""
            except Exception:
                content = ""
            data = content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            try:
                content = pyperclip.paste() or ""
            except Exception:
                content = ""
            page = HTML_PAGE.format(
                content=content.replace("<", "&lt;").replace(">", "&gt;"),
                token=self.__class__.token,
            )
            data = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)

    def do_POST(self):
        if not self._check_token():
            self._deny()
            return

        if urlparse(self.path).path == "/clip":
            length = min(int(self.headers.get("Content-Length", 0)), 1 << 20)  # cap at 1 MB
            body = self.rfile.read(length).decode("utf-8", errors="replace")
            try:
                pyperclip.copy(body)
                logger.info("ClipboardSync: received %d chars from remote", len(body))
                ok = b"OK"
            except Exception as e:
                logger.warning("ClipboardSync: copy failed: %s", e)
                ok = f"ERROR: {e}".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", len(ok))
            self.end_headers()
            self.wfile.write(ok)
        else:
            self.send_response(404)
            self.end_headers()


class ClipboardSync:
    def __init__(self, port: int = DEFAULT_PORT):
        self._port = port
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self._token: str = ""

    def start(self) -> dict:
        """Start the clipboard sync HTTP server."""
        if self._server:
            return {"success": True, "message": f"Clipboard sync already running on port {self._port}."}

        self._token = _make_token()
        _Handler.token = self._token

        try:
            self._server = HTTPServer(("127.0.0.1", self._port), _Handler)
        except OSError as e:
            return {"success": False, "message": f"Could not start clipboard sync server: {e}"}

        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True,
                                        name="loki-clipboard-sync")
        self._thread.start()
        url = self._build_url()
        logger.info("ClipboardSync started: %s", url)
        return {
            "success": True,
            "message": f"Clipboard sync active. Open this URL in a local browser:\n{url}",
            "data": {"url": url, "port": self._port},
        }

    def _build_url(self) -> str:
        return f"http://127.0.0.1:{self._port}/?t={self._token}"

    def stop(self) -> dict:
        """Stop the clipboard sync server."""
        if not self._server:
            return {"success": False, "message": "Clipboard sync is not running."}
        self._server.shutdown()
        self._server = None
        return {"success": True, "message": "Clipboard sync stopped.", "data": {}}

    def get_url(self) -> dict:
        """Return the sync URL if running."""
        if not self._server:
            return {"success": False, "message": "Clipboard sync is not running. Start it first."}
        url = self._build_url()
        return {"success": True, "message": f"Clipboard sync URL: {url}", "data": {"url": url}}

    def is_running(self) -> bool:
        return self._server is not None

    def get_clipboard(self) -> dict:
        """Get current clipboard content."""
        try:
            content = pyperclip.paste() or ""
            return {
                "success": True,
                "message": f"Clipboard ({len(content)} chars):\n{content[:500]}",
                "data": {"content": content},
            }
        except Exception as e:
            return {"success": False, "message": f"Could not read clipboard: {e}"}

    def set_clipboard(self, text: str) -> dict:
        """Set clipboard content."""
        try:
            pyperclip.copy(text)
            return {"success": True, "message": f"Clipboard set ({len(text)} chars).", "data": {}}
        except Exception as e:
            return {"success": False, "message": f"Could not set clipboard: {e}"}
