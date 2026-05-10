"""
GrammarPolisher — rewrite text for clarity, fix grammar, adjust tone, translate.
"""

import logging
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class GrammarPolisher:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def polish(self, text: str, tone: str = "professional") -> dict:
        """Fix grammar, spelling, punctuation and improve clarity."""
        if not text.strip():
            return {"success": False, "message": "No text provided."}

        tone_map = {
            "professional": "formal and professional",
            "casual": "friendly and conversational",
            "academic": "precise and academic",
            "concise": "brief and to the point",
            "assertive": "confident and assertive",
        }
        target_tone = tone_map.get(tone.lower(), "professional")

        prompt = (
            f"Rewrite the following text to fix all grammar, spelling, and punctuation errors. "
            f"Make it clear, natural, and {target_tone}. "
            f"Do not change the meaning or add new information. "
            f"Return only the corrected text without explanation.\n\n"
            f"Original:\n{text}\n\nCorrected:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not polish text."}
        return {"success": True, "message": result.strip(), "data": {"original": text, "polished": result.strip()}}

    def change_tone(self, text: str, target_tone: str) -> dict:
        """Rewrite text in a different tone while preserving meaning."""
        if not text.strip():
            return {"success": False, "message": "No text provided."}
        prompt = (
            f"Rewrite the following text in a {target_tone} tone. "
            f"Keep all the same information but adjust the language and style. "
            f"Return only the rewritten text.\n\n"
            f"Original:\n{text}\n\nRewritten:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not change tone."}
        return {"success": True, "message": result.strip(), "data": result.strip()}

    def translate(self, text: str, target_language: str) -> dict:
        """Translate text to the target language."""
        if not text.strip():
            return {"success": False, "message": "No text to translate."}
        if not target_language.strip():
            return {"success": False, "message": "No target language specified."}
        prompt = (
            f"Translate the following text to {target_language}. "
            f"Return only the translation, no explanation.\n\n"
            f"Text:\n{text}\n\nTranslation:"
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": f"Could not translate to {target_language}."}
        return {
            "success": True,
            "message": result.strip(),
            "data": {"original": text, "translated": result.strip(), "language": target_language},
        }
