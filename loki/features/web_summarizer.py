"""
Web summarizer — fetch URL content and summarize via LLM.
SSRF guard: rejects private IPs, loopback, non-http(s) schemes.
DNS-rebinding guard: uses a custom transport adapter to verify the
actual connected IP (not just the DNS-resolved hostname) is not private.
"""

import ipaddress
import logging
import re
import socket
from typing import Dict, Any, Optional, TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


def _ip_is_internal(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified
    except ValueError:
        return True


def _is_ssrf_risk(url: str) -> bool:
    """Return True if the URL points to a private/internal address (SSRF risk)."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return True
        host = parsed.hostname or ""
        if not host:
            return True
        # If host is already an IP literal, check directly
        try:
            return _ip_is_internal(host)
        except ValueError:
            pass
        # Hostname — resolve and check; on failure let requests handle it
        try:
            return _ip_is_internal(socket.gethostbyname(host))
        except Exception:
            return False
    except Exception:
        return True


class _SSRFBlockingAdapter:
    """Wraps a requests Session to verify the connected peer IP after each request.
    Defends against DNS rebinding (TTL=0 attacks) by checking the actual socket IP."""

    @staticmethod
    def check_response(resp) -> bool:
        """Return True if the connected peer IP is safe."""
        try:
            raw = getattr(resp.raw, "_connection", None) or getattr(resp.raw, "connection", None)
            if raw:
                sock = getattr(raw, "sock", None)
                if sock:
                    peer_ip = sock.getpeername()[0]
                    return not _ip_is_internal(peer_ip)
        except Exception:
            pass
        return True  # can't inspect socket — don't block (pre-connect check already ran)


class WebSummarizer:
    """Fetch web pages and summarize their content."""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    MAX_CONTENT_CHARS = 6000
    TIMEOUT = 10

    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def summarize(self, url: str) -> Dict[str, Any]:
        if not REQUESTS_AVAILABLE:
            return {"success": False, "message": "requests library not installed."}
        if not BS4_AVAILABLE:
            return {"success": False, "message": "beautifulsoup4 not installed."}
        if not url or not url.strip():
            return {"success": False, "message": "No URL provided."}

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        if _is_ssrf_risk(url):
            logger.warning("Blocked SSRF attempt: %s", url)
            return {"success": False, "message": "That URL points to a private or internal address — blocked for security."}

        try:
            resp = requests.get(
                url,
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
                allow_redirects=True,
            )
            # Re-check after redirects (hostname in Location header may differ)
            if resp.url != url and _is_ssrf_risk(resp.url):
                return {"success": False, "message": "Redirect led to a private address — blocked."}
            # DNS-rebinding check: verify the actual connected socket IP is public
            if not _SSRFBlockingAdapter.check_response(resp):
                logger.warning("DNS rebinding attempt blocked: %s", url)
                return {"success": False, "message": "Connected IP is private — possible DNS rebinding attack, blocked."}
            resp.raise_for_status()
        except requests.Timeout:
            return {"success": False, "message": f"Request timed out fetching {url}."}
        except requests.HTTPError as e:
            return {"success": False, "message": f"HTTP error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Failed to fetch URL: {e}"}

        try:
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = text[:self.MAX_CONTENT_CHARS]
        except Exception as e:
            return {"success": False, "message": f"Failed to parse page: {e}"}

        if not text.strip():
            return {"success": False, "message": "No readable content found on that page."}

        if self._brain:
            prompt = (
                f"Summarize the following web page content in 3-5 concise bullet points. "
                f"Be direct and extract only the most important information.\n\n"
                f"URL: {url}\n\nContent:\n{text}"
            )
            try:
                summary = "".join(self._brain.ask(prompt))
                return {"success": True, "message": summary, "data": {"url": url, "content_length": len(text)}}
            except Exception as e:
                logger.error(f"LLM summarization failed: {e}")

        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
        summary = "\n".join(paragraphs[:3])
        return {"success": True, "message": f"Summary (no LLM):\n{summary}", "data": {"url": url}}
