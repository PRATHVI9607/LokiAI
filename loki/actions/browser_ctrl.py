"""
Browser control — open URLs and search queries safely.
"""

import re
import logging
import threading
import webbrowser
from typing import Dict, Any
from urllib.parse import quote_plus, urlparse

from loki.core.log_utils import redact

logger = logging.getLogger(__name__)


def _open_with_timeout(url: str, timeout: float = 4.0) -> bool:
    """Open a URL but don't hang forever if the default browser misbehaves.
    Returns True if the open call returned in time."""
    done = {"ok": False}

    def _run():
        try:
            webbrowser.open(url)
            done["ok"] = True
        except Exception as e:
            logger.error(f"webbrowser.open failed: {e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout)
    return done["ok"]

SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q=",
    "ddg": "https://duckduckgo.com/?q=",
    "youtube": "https://www.youtube.com/results?search_query=",
    "github": "https://github.com/search?q=",
}

BLOCKED_SCHEMES = {"javascript", "data", "vbscript", "file"}


class BrowserCtrl:
    """Open URLs and perform web searches safely."""

    def open_url(self, url: str) -> Dict[str, Any]:
        if not url or not url.strip():
            return {"success": False, "message": "No URL specified."}

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Validate URL scheme
        parsed = urlparse(url)
        if parsed.scheme in BLOCKED_SCHEMES:
            logger.warning(f"Blocked URL scheme: {parsed.scheme}")
            return {"success": False, "message": "That URL scheme is not permitted."}

        if _open_with_timeout(url):
            logger.info(f"Opened URL: {redact(url)[:80]}")
            return {"success": True, "message": f"Opening {url[:50]}..."}
        return {"success": False, "message": "The browser didn't respond in time."}

    def search(self, query: str, engine: str = "google") -> Dict[str, Any]:
        if not query or not query.strip():
            return {"success": False, "message": "No search query specified."}

        base_url = SEARCH_ENGINES.get(engine.lower(), SEARCH_ENGINES["google"])
        encoded = quote_plus(query.strip())
        url = base_url + encoded

        if _open_with_timeout(url):
            return {"success": True, "message": f"Searching {engine} for '{query[:40]}'."}
        return {"success": False, "message": "The browser didn't respond in time."}
