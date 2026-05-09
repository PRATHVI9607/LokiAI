"""
Web summarizer — fetch URL content and summarize via LLM.
"""

import logging
import re
from typing import Dict, Any, Optional, TYPE_CHECKING

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

        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
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

        # Fallback: first paragraph extraction
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
        summary = "\n".join(paragraphs[:3])
        return {"success": True, "message": f"Summary (no LLM):\n{summary}", "data": {"url": url}}
