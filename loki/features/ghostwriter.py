"""
GhostWriter — expand notes, continue text, convert bullets to prose.
"""

import logging
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class GhostWriter:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def expand(self, notes: str, style: str = "professional") -> dict:
        """Expand rough notes or bullet points into full polished prose."""
        if not notes.strip():
            return {"success": False, "message": "No notes provided to expand."}

        style_map = {
            "professional": "formal, professional business writing",
            "casual": "friendly, conversational tone",
            "academic": "formal academic writing with precise language",
            "creative": "engaging, vivid creative writing",
            "technical": "clear, concise technical documentation",
        }
        tone = style_map.get(style.lower(), style_map["professional"])

        prompt = (
            f"Expand the following rough notes into well-written, coherent prose "
            f"in a {tone} style. Preserve all key points. Do not add fabricated facts.\n\n"
            f"Notes:\n{notes}\n\nExpanded text:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not expand notes."}
        return {"success": True, "message": result.strip(), "data": result.strip()}

    def continue_text(self, text: str, sentences: int = 3) -> dict:
        """Continue a piece of writing, matching its style and tone."""
        if not text.strip():
            return {"success": False, "message": "No text provided to continue."}
        prompt = (
            f"Continue the following text naturally, matching its style and tone. "
            f"Write approximately {sentences} additional sentences. "
            f"Do not repeat what was already written.\n\n"
            f"Text:\n{text}\n\nContinuation:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not continue text."}
        return {"success": True, "message": result.strip(), "data": result.strip()}

    def bullets_to_prose(self, bullets: str, style: str = "professional") -> dict:
        """Convert a bullet-point list into flowing paragraphs."""
        if not bullets.strip():
            return {"success": False, "message": "No bullet points provided."}
        prompt = (
            f"Convert the following bullet points into flowing, well-structured paragraphs "
            f"in a {style} tone. Keep all information intact.\n\n"
            f"Bullets:\n{bullets}\n\nProse:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not convert bullets to prose."}
        return {"success": True, "message": result.strip(), "data": result.strip()}
