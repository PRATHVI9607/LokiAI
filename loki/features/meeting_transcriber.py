"""
MeetingTranscriber — transcribe meeting audio files and generate structured minutes.
Uses Whisper (already loaded by Loki's STT module) or a standalone load.
"""

import logging
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".mp4", ".mkv", ".webm", ".mov"}


class MeetingTranscriber:
    def __init__(self, brain: Optional["LokiBrain"] = None, whisper_model=None):
        self._brain = brain
        self._model = whisper_model  # Shared Whisper instance from STT module

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _ensure_model(self):
        if self._model:
            return True
        try:
            import whisper
            self._model = whisper.load_model("base")
            return True
        except ImportError:
            return False

    def transcribe(self, audio_path: str, language: str = "en") -> dict:
        """Transcribe an audio file and return the full transcript."""
        fp = Path(audio_path).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"File not found: {audio_path}"}
        if fp.suffix.lower() not in AUDIO_EXTS:
            return {"success": False, "message": f"Unsupported audio format: {fp.suffix}"}

        if not self._ensure_model():
            return {
                "success": False,
                "message": "Whisper not installed. Run: pip install openai-whisper",
            }

        try:
            options = {"language": language, "task": "transcribe", "verbose": False}
            result = self._model.transcribe(str(fp), **options)
            transcript = result.get("text", "").strip()
            if not transcript:
                return {"success": False, "message": "No speech detected in audio."}

            return {
                "success": True,
                "message": f"Transcribed {fp.name} ({len(transcript)} chars).",
                "data": {"transcript": transcript, "file": str(fp), "language": language},
            }
        except Exception as e:
            return {"success": False, "message": f"Transcription failed: {e}"}

    def generate_minutes(self, audio_path: str, language: str = "en") -> dict:
        """Transcribe audio and generate structured meeting minutes."""
        tr = self.transcribe(audio_path, language)
        if not tr["success"]:
            return tr

        transcript = tr["data"]["transcript"]

        if not self._brain:
            return {
                "success": True,
                "message": "Transcription complete (LLM unavailable for minutes generation).",
                "data": {"transcript": transcript, "minutes": None},
            }

        prompt = (
            f"Generate structured meeting minutes from this transcript.\n\n"
            f"Include:\n"
            f"1. Meeting Summary (2-3 sentences)\n"
            f"2. Key Discussion Points (bullet list)\n"
            f"3. Decisions Made (bullet list)\n"
            f"4. Action Items (person → task, if names mentioned)\n"
            f"5. Next Steps\n\n"
            f"TRANSCRIPT:\n{transcript[:4000]}"
        )
        minutes = self._llm(prompt)

        return {
            "success": True,
            "message": minutes or "Minutes generated.",
            "data": {"transcript": transcript, "minutes": minutes, "file": tr["data"]["file"]},
        }

    def extract_action_items(self, text_or_path: str) -> dict:
        """Extract action items from transcript text or a file."""
        # Determine if it's a file or raw text
        fp = Path(text_or_path)
        if fp.exists() and fp.suffix.lower() in AUDIO_EXTS:
            tr = self.transcribe(text_or_path)
            if not tr["success"]:
                return tr
            text = tr["data"]["transcript"]
        elif fp.exists() and fp.suffix.lower() in {".txt", ".md"}:
            text = fp.read_text(encoding="utf-8", errors="replace")
        else:
            text = text_or_path

        if not self._brain:
            return {"success": False, "message": "LLM required for action item extraction."}

        prompt = (
            f"Extract all action items from this meeting transcript or notes.\n"
            f"Format each as: • [Person responsible (if known)] → [Task] [Deadline if mentioned]\n\n"
            f"TEXT:\n{text[:3000]}\n\nAction items:"
        )
        items = self._llm(prompt)
        return {
            "success": True,
            "message": items or "No action items found.",
            "data": {"action_items": items},
        }

    def summarize_transcript(self, transcript: str, max_words: int = 150) -> dict:
        """Summarize a raw transcript string."""
        if not transcript.strip():
            return {"success": False, "message": "Empty transcript."}
        if not self._brain:
            return {"success": False, "message": "LLM required for summarization."}

        prompt = (
            f"Summarize this meeting transcript in {max_words} words or fewer. "
            f"Highlight key decisions and outcomes.\n\nTRANSCRIPT:\n{transcript[:4000]}"
        )
        summary = self._llm(prompt)
        return {"success": True, "message": summary or "Summary unavailable.", "data": {"summary": summary}}
