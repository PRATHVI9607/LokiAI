"""
FactChecker — verify claims by cross-referencing web sources and LLM reasoning.
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


class FactChecker:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _search_web(self, query: str) -> list[str]:
        """Fetch snippets from DuckDuckGo HTML search."""
        snippets = []
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            resp = requests.get(url, headers=HEADERS, timeout=8)
            soup = BeautifulSoup(resp.text, "html.parser")
            for result in soup.select(".result__snippet")[:5]:
                text = result.get_text(strip=True)
                if text:
                    snippets.append(text)
        except Exception as e:
            logger.warning(f"FactChecker web search failed: {e}")
        return snippets

    def check(self, claim: str) -> dict:
        """Verify a claim against web evidence and LLM reasoning."""
        if not claim.strip():
            return {"success": False, "message": "No claim provided to fact-check."}

        snippets = self._search_web(claim)
        evidence_block = "\n".join(f"- {s}" for s in snippets) if snippets else "No web results found."

        prompt = (
            f"You are a fact-checking assistant. Evaluate the following claim based on the "
            f"web evidence provided and your knowledge.\n\n"
            f"Claim: {claim}\n\n"
            f"Web evidence:\n{evidence_block}\n\n"
            f"Respond with:\n"
            f"Verdict: [TRUE / FALSE / PARTIALLY TRUE / UNVERIFIED]\n"
            f"Explanation: (2-3 sentences explaining the verdict)\n"
            f"Confidence: [HIGH / MEDIUM / LOW]"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not evaluate the claim."}

        verdict_match = re.search(r"Verdict:\s*(.+)", result, re.IGNORECASE)
        verdict = verdict_match.group(1).strip() if verdict_match else "UNVERIFIED"
        return {
            "success": True,
            "message": result.strip(),
            "data": {"claim": claim, "verdict": verdict, "analysis": result.strip(), "sources_checked": len(snippets)},
        }
