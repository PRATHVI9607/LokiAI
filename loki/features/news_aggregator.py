"""
NewsAggregator — pull headlines from RSS feeds, personalised by topic.
No API key required.
"""

import logging
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

FEEDS: dict[str, list[str]] = {
    "technology": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.wired.com/feed/rss",
        "https://hnrss.org/frontpage",
    ],
    "science": [
        "https://www.sciencedaily.com/rss/top/technology.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    ],
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    ],
    "business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    ],
    "ai": [
        "https://hnrss.org/frontpage?q=AI+LLM+machine+learning",
        "https://www.marktechpost.com/feed/",
    ],
}


class NewsAggregator:
    def _fetch_feed(self, url: str, max_items: int = 5) -> list[str]:
        headlines = []
        try:
            resp = requests.get(url, headers=HEADERS, timeout=6)
            root = ET.fromstring(resp.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            # RSS 2.0
            for item in root.iter("item"):
                title = item.findtext("title", "").strip()
                if title:
                    headlines.append(title)
                if len(headlines) >= max_items:
                    break
            # Atom
            if not headlines:
                for entry in root.findall(".//atom:entry", ns):
                    title_el = entry.find("atom:title", ns)
                    if title_el is not None and title_el.text:
                        headlines.append(title_el.text.strip())
                    if len(headlines) >= max_items:
                        break
        except Exception as e:
            logger.warning(f"Feed fetch failed {url}: {e}")
        return headlines

    def get_headlines(self, category: str = "technology", count: int = 5) -> dict:
        """Fetch top headlines for a category from RSS feeds."""
        cat = category.lower()
        feed_urls = FEEDS.get(cat, FEEDS["technology"])
        headlines = []
        for url in feed_urls:
            fetched = self._fetch_feed(url, count)
            headlines.extend(fetched)
            if len(headlines) >= count:
                break
        headlines = list(dict.fromkeys(headlines))[:count]  # deduplicate
        if not headlines:
            return {"success": False, "message": f"Could not fetch {category} headlines right now."}
        summary = f"Top {category} headlines:\n" + "\n".join(f"• {h}" for h in headlines)
        return {"success": True, "message": summary, "data": {"category": category, "headlines": headlines}}

    def get_briefing(self, topics: Optional[list] = None) -> dict:
        """Fetch headlines across multiple topics for a morning briefing."""
        topics = topics or ["technology", "world"]
        all_headlines = []
        for topic in topics:
            result = self.get_headlines(topic, count=3)
            if result["success"]:
                all_headlines.append(f"\n[{topic.upper()}]")
                all_headlines.extend(f"• {h}" for h in result["data"]["headlines"])
        if not all_headlines:
            return {"success": False, "message": "No news headlines available right now."}
        brief = "News briefing:\n" + "\n".join(all_headlines)
        return {"success": True, "message": brief, "data": {"topics": topics, "headlines": all_headlines}}
