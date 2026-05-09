"""
Browser control — open URLs and search queries safely.
"""

import re
import logging
import webbrowser
from typing import Dict, Any
from urllib.parse import quote_plus, urlparse

logger = logging.getLogger(__name__)

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

        try:
            webbrowser.open(url)
            logger.info(f"Opened URL: {url[:80]}")
            return {"success": True, "message": f"Opening {url[:50]}..."}
        except Exception as e:
            return {"success": False, "message": f"Failed to open URL: {e}"}

    def search(self, query: str, engine: str = "google") -> Dict[str, Any]:
        if not query or not query.strip():
            return {"success": False, "message": "No search query specified."}

        base_url = SEARCH_ENGINES.get(engine.lower(), SEARCH_ENGINES["google"])
        encoded = quote_plus(query.strip())
        url = base_url + encoded

        try:
            webbrowser.open(url)
            return {"success": True, "message": f"Searching {engine} for '{query[:40]}'."}
        except Exception as e:
            return {"success": False, "message": f"Search failed: {e}"}
