"""
CitationGenerator — produce APA, MLA, Chicago, IEEE citations from URLs or raw info.
"""

import logging
import re
import requests
from typing import Optional, TYPE_CHECKING
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class CitationGenerator:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _fetch_metadata(self, url: str) -> dict:
        """Extract title, author, date, site from a URL's meta tags."""
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            soup = BeautifulSoup(resp.text, "html.parser")
            meta = {}
            # Title
            og_title = soup.find("meta", property="og:title")
            meta["title"] = (og_title["content"] if og_title else None) or (soup.title.string if soup.title else "Unknown Title")
            # Author
            author_tag = soup.find("meta", {"name": "author"}) or soup.find("meta", property="article:author")
            meta["author"] = author_tag["content"] if author_tag else "Unknown Author"
            # Date
            date_tag = (
                soup.find("meta", property="article:published_time")
                or soup.find("meta", {"name": "date"})
                or soup.find("meta", {"name": "pubdate"})
            )
            if date_tag:
                raw = date_tag.get("content", "")
                meta["date"] = raw[:10] if raw else "n.d."
            else:
                meta["date"] = "n.d."
            # Site name
            site_tag = soup.find("meta", property="og:site_name")
            meta["site"] = site_tag["content"] if site_tag else re.sub(r"https?://(www\.)?", "", url).split("/")[0]
            meta["url"] = url
            return meta
        except Exception as e:
            logger.warning(f"Metadata fetch failed for {url}: {e}")
            return {"title": "Unknown Title", "author": "Unknown Author", "date": "n.d.", "site": url, "url": url}

    def from_url(self, url: str, style: str = "APA") -> dict:
        """Generate a citation from a URL."""
        if not url.strip():
            return {"success": False, "message": "No URL provided."}
        meta = self._fetch_metadata(url)
        return self._format(meta, style)

    def from_info(self, title: str, author: str = "", year: str = "", publisher: str = "",
                  url: str = "", style: str = "APA") -> dict:
        """Generate a citation from manually supplied info."""
        meta = {
            "title": title or "Unknown Title",
            "author": author or "Unknown Author",
            "date": year or "n.d.",
            "site": publisher or "",
            "url": url,
        }
        return self._format(meta, style)

    def _format(self, meta: dict, style: str) -> dict:
        style = style.upper()
        title = meta.get("title", "Unknown Title")
        author = meta.get("author", "Unknown Author")
        date = meta.get("date", "n.d.")
        site = meta.get("site", "")
        url = meta.get("url", "")

        year = date[:4] if date and date != "n.d." else "n.d."

        if style == "APA":
            citation = f"{author}. ({year}). {title}. {site}. {url}"
        elif style == "MLA":
            citation = f'"{title}." {site}, {date}, {url}. Accessed {__import__("datetime").date.today()}.'
        elif style == "CHICAGO":
            citation = f'{author}. "{title}." {site}, {date}. {url}.'
        elif style == "IEEE":
            citation = f'{author}, "{title}," {site}, {date}. [Online]. Available: {url}'
        else:
            # Use LLM for unknown styles
            prompt = (
                f"Generate a {style} format citation for:\n"
                f"Title: {title}\nAuthor: {author}\nDate: {date}\nPublisher: {site}\nURL: {url}\n"
                f"Return only the citation."
            )
            citation = self._ask(prompt).strip() or f"{author}. ({year}). {title}. {site}. {url}"

        return {
            "success": True,
            "message": citation,
            "data": {"citation": citation, "style": style, "metadata": meta},
        }
