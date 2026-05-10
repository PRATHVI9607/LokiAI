"""
PhishingDetector — heuristic + LLM analysis of URLs and email text for phishing signals.
No external API required for heuristics; LLM used for deeper content analysis.
"""

import logging
import re
import socket
from typing import Optional, TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

# Common legitimate domains that are often spoofed
COMMON_LEGIT = {
    "google.com", "microsoft.com", "apple.com", "amazon.com", "paypal.com",
    "facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com",
    "github.com", "netflix.com", "spotify.com", "dropbox.com", "outlook.com",
    "office.com", "icloud.com", "chase.com", "bankofamerica.com", "wellsfargo.com",
}

PHISH_KEYWORDS = [
    "verify your account", "confirm your identity", "click here to secure",
    "your account has been suspended", "unusual activity detected",
    "update your payment", "you have won", "claim your prize",
    "limited time offer", "act now", "urgent action required",
    "your password will expire", "validate your information",
    "login attempt", "we noticed", "temporary suspension",
]

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


class PhishingDetector:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _heuristic_url(self, url: str) -> dict:
        """Score a URL on phishing heuristics."""
        signals: list[str] = []
        risk = 0

        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
        except Exception:
            return {"risk": 10, "signals": ["Could not parse URL"]}

        # IP address instead of domain
        try:
            socket.inet_aton(domain.split(":")[0])
            signals.append("IP address as hostname instead of domain name")
            risk += 4
        except OSError:
            pass

        # Homograph / lookalike checks
        for legit in COMMON_LEGIT:
            base = legit.split(".")[0]
            if base in domain and not domain.endswith(legit):
                signals.append(f"Domain resembles '{legit}' but is different: {domain}")
                risk += 5

        # Excessive subdomains
        parts = domain.split(".")
        if len(parts) > 4:
            signals.append(f"Excessive subdomains ({len(parts)} levels): {domain}")
            risk += 2

        # Suspicious TLDs
        suspicious_tlds = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club", ".work"}
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                signals.append(f"Suspicious TLD: {tld}")
                risk += 2

        # Long URL
        if len(url) > 100:
            signals.append(f"Unusually long URL ({len(url)} chars)")
            risk += 1

        # @ symbol in URL (redirects)
        if "@" in url:
            signals.append("URL contains '@' — browser ignores everything before it")
            risk += 3

        # URL encoding tricks
        if "%" in path and re.search(r"%[0-9a-fA-F]{2}", path):
            signals.append("URL contains percent-encoded characters in path")
            risk += 1

        # Keyword in path
        for kw in ["login", "signin", "account", "password", "verify", "secure", "update", "confirm"]:
            if kw in path:
                signals.append(f"Sensitive keyword in URL path: '{kw}'")
                risk += 1
                break

        return {"risk": min(risk, 10), "signals": signals}

    def analyze_url(self, url: str) -> dict:
        """Analyze a URL for phishing indicators."""
        url = url.strip()
        h = self._heuristic_url(url)
        risk = h["risk"]
        signals = h["signals"]

        if risk >= 6 or (risk >= 3 and self._brain):
            prompt = (
                f"Is this URL a phishing or scam link? Analyze briefly.\nURL: {url}\n"
                f"Heuristic signals found: {signals or 'none'}\n"
                f"Respond: verdict (Safe / Suspicious / Likely Phishing), then one sentence why."
            )
            llm_verdict = self._llm(prompt)
        else:
            llm_verdict = ""

        level = "Low" if risk < 3 else "Medium" if risk < 6 else "High"
        msg = f"Phishing risk: {level} ({risk}/10)"
        if signals:
            msg += "\n" + "\n".join(f"  ⚠ {s}" for s in signals)
        if llm_verdict:
            msg += f"\n\nAI verdict: {llm_verdict}"

        return {
            "success": True,
            "message": msg,
            "data": {"url": url, "risk_score": risk, "level": level, "signals": signals, "llm_verdict": llm_verdict},
        }

    def analyze_email(self, email_text: str) -> dict:
        """Analyze email content for phishing patterns."""
        text_lower = email_text.lower()
        signals: list[str] = []
        risk = 0

        # Keyword matches
        matched_kw = [kw for kw in PHISH_KEYWORDS if kw in text_lower]
        if matched_kw:
            signals.append(f"Phishing language: {', '.join(matched_kw[:4])}")
            risk += min(len(matched_kw) * 2, 5)

        # Urgency indicators
        urgency = ["immediately", "within 24 hours", "right now", "as soon as possible", "before it expires"]
        if any(u in text_lower for u in urgency):
            signals.append("Urgency language detected")
            risk += 2

        # URLs in email
        urls = URL_PATTERN.findall(email_text)
        url_results = []
        for url in urls[:5]:
            h = self._heuristic_url(url)
            if h["risk"] >= 3:
                signals.append(f"Suspicious URL: {url[:80]}")
                risk += 2
            url_results.append({"url": url, "risk": h["risk"]})

        # Mismatched display vs actual links (heuristic from text patterns)
        if re.search(r'\[.*?\]\(https?://', email_text):
            signals.append("Markdown-style links with potentially hidden destinations")
            risk += 1

        # Request for credentials
        cred_words = ["password", "social security", "credit card", "bank account", "pin number", "cvv", "ssn"]
        if any(c in text_lower for c in cred_words):
            signals.append("Requests sensitive credentials")
            risk += 3

        risk = min(risk, 10)

        if risk >= 4 and self._brain:
            snippet = email_text[:600].replace("\n", " ")
            prompt = (
                f"Analyze this email excerpt for phishing. Give a verdict: Safe / Suspicious / Likely Phishing.\n\n"
                f"EMAIL:\n{snippet}\n\nSignals found: {signals}\n\nOne-sentence verdict:"
            )
            llm_verdict = self._llm(prompt)
        else:
            llm_verdict = ""

        level = "Low" if risk < 3 else "Medium" if risk < 6 else "High"
        msg = f"Email phishing risk: {level} ({risk}/10)"
        if signals:
            msg += "\n" + "\n".join(f"  ⚠ {s}" for s in signals)
        if llm_verdict:
            msg += f"\n\nAI verdict: {llm_verdict}"

        return {
            "success": True,
            "message": msg,
            "data": {"risk_score": risk, "level": level, "signals": signals, "urls": url_results, "llm_verdict": llm_verdict},
        }
