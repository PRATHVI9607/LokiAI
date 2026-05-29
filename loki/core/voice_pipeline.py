"""
VoicePipeline — owns the microphone.

Only one component can hold the mic at a time:
  WAKEWORD mode → WakewordDetector listens for "Hey Loki"
  LISTENING mode → SpeechListener captures a command utterance

State transitions fire callbacks rather than reaching into other modules.
"""

import logging
import threading
import time
from typing import Callable, Optional

from loki.core.wakeword import WakewordDetector
from loki.core.listener import SpeechListener

logger = logging.getLogger(__name__)

# Delay between TTS finishing and mic resuming — prevents the listener from
# picking up soundcard echo/reverb of Loki's own voice as a new command.
_MIC_RESUME_DELAY = 0.45  # seconds


class VoicePipeline:
    """Exclusive-mic manager: wakeword ↔ listener handoff."""

    def __init__(self, wakeword: WakewordDetector, listener: SpeechListener):
        self._wakeword = wakeword
        self._listener = listener
        self._lock = threading.Lock()
        self._active = False
        self._muted = False

        # Outbound callbacks
        self.on_wakeword: Optional[Callable] = None
        self.on_transcript: Optional[Callable[[str], None]] = None
        self.on_transcript_partial: Optional[Callable[[str], None]] = None

        # Wire wakeword → self
        self._wakeword.on_wakeword = self._handle_wakeword
        self._wakeword.on_transcript = self._handle_partial

        # Wire listener → self
        self._listener.on_transcript = self._handle_transcript

    # ── Public interface ────────────────────────────────────────────────

    def activate(self) -> None:
        """Start wakeword detection. Call once on app start."""
        with self._lock:
            if self._active:
                return
            self._active = True
        if not self._muted:
            self._wakeword.start()
            logger.info("VoicePipeline activated — wakeword listening")

    def deactivate(self) -> None:
        """Shut down both components."""
        with self._lock:
            self._active = False
        self._wakeword.stop()
        self._listener.stop_listening()
        logger.info("VoicePipeline deactivated")

    def resume_listening(self) -> None:
        """After TTS finishes mid-conversation: start listener for next utterance.
        Applies a short delay so soundcard echo of Loki's voice drains before
        the mic opens — prevents Loki hearing its own responses as new commands."""
        if self._muted or not self._active:
            return
        # Use a timer so the calling thread (TTS worker) is not blocked
        threading.Timer(_MIC_RESUME_DELAY, self._start_listener_safe).start()

    def _start_listener_safe(self) -> None:
        """Timer callback — only starts listener if still active and not already running."""
        if self._active and not self._muted and not self._listener.is_listening:
            self._listener.start_listening()

    def return_to_wakeword(self) -> None:
        """Conversation ended: hand mic back to wakeword detector."""
        self._listener.stop_listening()
        if not self._muted and self._active and not self._wakeword.is_running:
            self._wakeword.start()
            logger.info("VoicePipeline returned to wakeword mode")

    def set_muted(self, muted: bool) -> None:
        self._muted = muted
        if muted:
            self._wakeword.stop()
            self._listener.stop_listening()
        elif self._active and not self._wakeword.is_running:
            self._wakeword.start()

    @property
    def is_muted(self) -> bool:
        return self._muted

    # ── Internal handlers ───────────────────────────────────────────────

    def _handle_wakeword(self) -> None:
        """Wakeword detected: release wakeword mic, hand to listener."""
        self._wakeword.stop()
        # Brief delay so wakeword audio drains before listener opens
        time.sleep(0.15)
        self._listener.start_listening()
        if self.on_wakeword:
            self.on_wakeword()

    def _handle_partial(self, text: str) -> None:
        if self.on_transcript_partial:
            self.on_transcript_partial(text)

    def _handle_transcript(self, text: str) -> None:
        """Full STT transcript ready: release listener mic, fire callback."""
        self._listener.stop_listening()
        if self.on_transcript:
            self.on_transcript(text)
