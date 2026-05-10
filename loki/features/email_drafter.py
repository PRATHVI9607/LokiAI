"""
EmailDrafter — compose and reply to emails using LLM in the user's voice.
Does not send anything; returns draft text only.
"""

import logging
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class EmailDrafter:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def draft(self, context: str, tone: str = "professional", recipient: str = "") -> dict:
        """Draft a new email from a description of what to say."""
        if not context.strip():
            return {"success": False, "message": "Describe what the email should say."}

        tone_map = {
            "professional": "formal and professional",
            "friendly": "warm and friendly",
            "assertive": "confident and direct",
            "apologetic": "sincere and apologetic",
            "concise": "brief and to the point",
        }
        tone_desc = tone_map.get(tone.lower(), "professional and clear")
        recipient_line = f" to {recipient}" if recipient else ""

        prompt = (
            f"Write a complete email{recipient_line} with the following context:\n{context}\n\n"
            f"Tone: {tone_desc}\n"
            f"Include a subject line prefixed with 'Subject:', then a blank line, then the email body.\n"
            f"Sign off appropriately. Return only the email, no explanation."
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not draft email."}

        # Split subject from body
        lines = result.strip().split("\n")
        subject = ""
        body_start = 0
        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line[8:].strip()
                body_start = i + 1
                break
        body = "\n".join(lines[body_start:]).strip()

        msg = f"Subject: {subject}\n\n{body}" if subject else result.strip()
        return {
            "success": True,
            "message": msg,
            "data": {"subject": subject, "body": body, "full_draft": msg},
        }

    def reply(self, original: str, instruction: str, tone: str = "professional") -> dict:
        """Draft a reply to an existing email thread."""
        if not original.strip():
            return {"success": False, "message": "Provide the original email to reply to."}
        if not instruction.strip():
            return {"success": False, "message": "Describe how you want to reply."}

        prompt = (
            f"Write a reply to the following email.\n\n"
            f"--- Original Email ---\n{original}\n--- End ---\n\n"
            f"Instructions for the reply: {instruction}\n"
            f"Tone: {tone}\n"
            f"Return only the reply body (no subject line needed), starting with an appropriate greeting."
        )
        result = self._ask(prompt)
        if not result.strip():
            return {"success": False, "message": "Could not draft reply."}
        return {"success": True, "message": result.strip(), "data": result.strip()}
