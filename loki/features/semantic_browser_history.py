"""
SemanticBrowserHistory — read Chrome/Edge SQLite history and perform
keyword or LLM-assisted semantic search over visited pages.
"""

import logging
import shutil
import sqlite3
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

# Chrome/Edge store timestamps as microseconds since 1601-01-01
CHROMIUM_EPOCH_DELTA = 11644473600  # seconds between 1601-01-01 and 1970-01-01


def _chrome_ts_to_dt(ts: int) -> datetime:
    try:
        return datetime.utcfromtimestamp(ts / 1_000_000 - CHROMIUM_EPOCH_DELTA)
    except Exception:
        return datetime.min


BROWSER_PROFILES = {
    "chrome": [
        Path.home() / "AppData/Local/Google/Chrome/User Data/Default/History",
        Path.home() / "AppData/Local/Google/Chrome/User Data/Profile 1/History",
    ],
    "edge": [
        Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default/History",
        Path.home() / "AppData/Local/Microsoft/Edge/User Data/Profile 1/History",
    ],
    "brave": [
        Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History",
    ],
}


class SemanticBrowserHistory:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _find_history_db(self, browser: str = "auto") -> Optional[Path]:
        candidates: list[Path] = []
        if browser == "auto":
            for paths in BROWSER_PROFILES.values():
                candidates.extend(paths)
        else:
            candidates = BROWSER_PROFILES.get(browser.lower(), [])

        for p in candidates:
            if p.exists():
                return p
        return None

    def _read_history(self, db_path: Path, limit: int = 500) -> list[dict]:
        """Copy DB (Chrome locks it) and query visits."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            shutil.copy2(db_path, tmp_path)
            conn = sqlite3.connect(str(tmp_path))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                """
                SELECT u.url, u.title, v.visit_time
                FROM visits v JOIN urls u ON v.url = u.id
                ORDER BY v.visit_time DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = [
                {
                    "url": r["url"],
                    "title": r["title"] or "",
                    "visited_at": _chrome_ts_to_dt(r["visit_time"]).strftime("%Y-%m-%d %H:%M"),
                }
                for r in cur.fetchall()
            ]
            conn.close()
            return rows
        except Exception as e:
            logger.debug("History read error: %s", e)
            return []
        finally:
            try:
                tmp_path.unlink()
            except Exception:
                pass

    def search(self, query: str, browser: str = "auto", days: int = 30, limit: int = 20) -> dict:
        """Keyword search over recent browser history."""
        db = self._find_history_db(browser)
        if not db:
            return {"success": False, "message": "No browser history database found (Chrome/Edge/Brave)."}

        history = self._read_history(db, limit=1000)
        if not history:
            return {"success": False, "message": "Could not read browser history (browser may be open — close it and retry)."}

        # Filter by date
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = [h for h in history if datetime.strptime(h["visited_at"], "%Y-%m-%d %H:%M") >= cutoff]

        # Keyword match
        q = query.lower()
        matches = [h for h in recent if q in h["url"].lower() or q in h["title"].lower()][:limit]

        if not matches:
            return {"success": True, "message": f"No history matching '{query}' in the last {days} days.", "data": {"results": []}}

        lines = [f"  [{h['visited_at']}] {h['title'][:50] or h['url'][:60]}" for h in matches]
        return {
            "success": True,
            "message": f"Found {len(matches)} matches for '{query}':\n" + "\n".join(lines),
            "data": {"results": matches},
        }

    def semantic_search(self, query: str, browser: str = "auto", days: int = 30) -> dict:
        """LLM-assisted semantic search — finds conceptually related pages."""
        if not self._brain:
            return self.search(query, browser, days)

        db = self._find_history_db(browser)
        if not db:
            return {"success": False, "message": "No browser history database found."}

        history = self._read_history(db, limit=500)
        if not history:
            return {"success": False, "message": "Could not read browser history."}

        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = [h for h in history if datetime.strptime(h["visited_at"], "%Y-%m-%d %H:%M") >= cutoff][:200]

        # Build compact listing for LLM
        listing = "\n".join(
            f"{h['visited_at']} | {h['title'][:60] or h['url'][:60]}"
            for h in recent
        )
        prompt = (
            f"Given this browser history, find the 10 entries most relevant to the query.\n"
            f"Query: {query}\n\n"
            f"HISTORY (date | title/url):\n{listing}\n\n"
            f"Reply with the matching lines only, most relevant first. No extra explanation."
        )
        result = self._llm(prompt)
        return {
            "success": True,
            "message": result or "No relevant results found.",
            "data": {"query": query, "results_raw": result},
        }

    def recent(self, browser: str = "auto", days: int = 1, limit: int = 20) -> dict:
        """Show most recently visited pages."""
        db = self._find_history_db(browser)
        if not db:
            return {"success": False, "message": "No browser history database found."}

        history = self._read_history(db, limit=200)
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = [
            h for h in history
            if datetime.strptime(h["visited_at"], "%Y-%m-%d %H:%M") >= cutoff
        ][:limit]

        if not recent:
            return {"success": True, "message": f"No browsing activity in the last {days} day(s).", "data": {"results": []}}

        lines = [f"  [{h['visited_at']}] {h['title'][:55] or h['url'][:60]}" for h in recent]
        return {
            "success": True,
            "message": f"Last {len(recent)} pages visited:\n" + "\n".join(lines),
            "data": {"results": recent},
        }

    def get_stats(self, browser: str = "auto") -> dict:
        """Return browsing stats for the last 30 days."""
        db = self._find_history_db(browser)
        if not db:
            return {"success": False, "message": "No browser history database found."}

        history = self._read_history(db, limit=2000)
        cutoff = datetime.utcnow() - timedelta(days=30)
        recent = [h for h in history if datetime.strptime(h["visited_at"], "%Y-%m-%d %H:%M") >= cutoff]

        from urllib.parse import urlparse
        domains: dict[str, int] = {}
        for h in recent:
            try:
                d = urlparse(h["url"]).netloc
                domains[d] = domains.get(d, 0) + 1
            except Exception:
                pass

        top = sorted(domains.items(), key=lambda x: -x[1])[:10]
        msg = f"Last 30 days: {len(recent)} page visits, {len(domains)} unique domains.\nTop sites:\n"
        msg += "\n".join(f"  {d}: {c} visits" for d, c in top)
        return {"success": True, "message": msg, "data": {"total_visits": len(recent), "top_domains": top}}
