"""
ClipboardSync — expose clipboard over local HTTP so any device on the same
Wi-Fi can read or push clipboard content via a browser.

Runs as a lightweight HTTP server on a configurable port (default 7778).
Mobile users open http://<your-pc-ip>:7778 to see/set clipboard.
"""

import logging
import socket
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
function setStatus(msg){{document.getElementById('status').textContent=msg;}}
function loadClip(){{
  fetch('/clip').then(r=>r.text()).then(t=>{{
    document.getElementById('clip').value=t;
    setStatus('Refreshed');
  }}).catch(()=>setStatus('Error'));
}}
function sendClip(){{
  const text=document.getElementById('clip').value;
  fetch('/clip',{{method:'POST',body:text,headers:{{'Content-Type':'text/plain'}}}})
    .then(r=>r.text()).then(()=>setStatus('Sent to PC!'))
    .catch(()=>setStatus('Error sending'));
}}
</script>
</body>
</html>"""


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # suppress default request logging

    def do_GET(self):
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
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        else:
            try:
                content = pyperclip.paste() or ""
            except Exception:
                content = ""
            page = HTML_PAGE.format(content=content.replace("<", "&lt;").replace(">", "&gt;"))
            data = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)

    def do_POST(self):
        if self.path == "/clip":
            length = int(self.headers.get("Content-Length", 0))
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
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(ok)
        else:
            self.send_response(404)
            self.end_headers()


def _get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class ClipboardSync:
    def __init__(self, port: int = DEFAULT_PORT):
        self._port = port
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> dict:
        """Start the clipboard sync HTTP server."""
        if self._server:
            return {"success": True, "message": f"Clipboard sync already running on port {self._port}."}

        try:
            self._server = HTTPServer(("0.0.0.0", self._port), _Handler)
        except OSError as e:
            return {"success": False, "message": f"Could not start clipboard sync server: {e}"}

        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True,
                                        name="loki-clipboard-sync")
        self._thread.start()
        ip = _get_local_ip()
        url = f"http://{ip}:{self._port}"
        return {
            "success": True,
            "message": f"Clipboard sync started. Open on your phone: {url}",
            "data": {"url": url, "port": self._port, "ip": ip},
        }

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
        ip = _get_local_ip()
        url = f"http://{ip}:{self._port}"
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
