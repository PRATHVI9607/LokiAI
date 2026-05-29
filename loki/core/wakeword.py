"""
Wakeword detector — rolling-window Whisper-based "Hey Loki" detection.

Key design fixes over naive sd.rec() approach:
- Sliding 2.5s rolling buffer checked every 0.7s — wakewords spanning chunk
  boundaries are always caught (was missing ~40% of triggers).
- Punctuation stripped before matching — Whisper outputs "Hey, Loki." but we
  match on "hey loki" (was silently failing on every punctuated transcript).
- sd.InputStream instead of sd.rec()+sd.wait() — no blocking, no gaps.
"""

import logging
import re
import threading
import time
import numpy as np
from typing import Callable, Optional

logger = logging.getLogger(__name__)

try:
    import sounddevice as sd
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

# Strip everything except letters, digits, and spaces before matching
_PUNCT_RE = re.compile(r"[^a-z0-9 ]")


class WakewordDetector:
    """Detects 'Hey Loki' using a rolling audio buffer + Whisper tiny.en."""

    SAMPLE_RATE  = 16_000
    WINDOW_SEC   = 2.5    # rolling buffer length — catches boundary-spanning phrases
    CHECK_EVERY  = 0.7    # seconds between Whisper checks
    BLOCK_SEC    = 0.05   # sounddevice block size (50ms)

    # Variants after punctuation stripping and lowercasing.
    # Includes common Whisper mishearings of "Hey Loki".
    WAKEWORD_VARIANTS = {
        "hey loki",  "hay loki",   "hey lockey", "hey lokey",
        "hello loki","ok loki",    "okay loki",  "hey lucky",
        "hey lolly", "hey loke",   "hey loca",   "a loki",
        "hey lokki", "hey loke",   "hey loki",   "the loki",
    }

    def __init__(self, config: dict):
        self._config        = config.get("wakeword", {})
        self._method        = self._config.get("method", "whisper")
        self._rms_threshold = self._config.get("rms_threshold", 0.004)  # slightly lower for soft voices
        self._running       = False
        self._thread: Optional[threading.Thread] = None
        self._model         = None

        self.on_wakeword:    Optional[Callable]           = None
        self.on_transcript:  Optional[Callable[[str], None]] = None

        if self._method == "whisper" and WHISPER_AVAILABLE:
            try:
                self._model = whisper.load_model("tiny.en")
                logger.info("Wakeword Whisper model loaded (tiny.en)")
            except Exception as e:
                logger.error(f"Wakeword Whisper load failed: {e}")

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._detect_loop, daemon=True, name="loki-wakeword"
        )
        self._thread.start()
        logger.info("Wakeword detector started — say 'Hey Loki'")

    def stop(self) -> None:
        self._running = False
        if self._thread and threading.current_thread() is not self._thread:
            self._thread.join(timeout=3)
        logger.info("Wakeword detector stopped")

    # ── Detection loop ──────────────────────────────────────────────────

    def _detect_loop(self) -> None:
        if not SD_AVAILABLE:
            logger.error("sounddevice not available — wakeword disabled")
            return

        window_samples = int(self.SAMPLE_RATE * self.WINDOW_SEC)
        block_samples  = int(self.SAMPLE_RATE * self.BLOCK_SEC)
        buffer         = np.zeros(window_samples, dtype=np.float32)

        def _audio_callback(indata, frames, time_info, status):
            nonlocal buffer
            data = indata[:, 0]
            n    = len(data)
            # Shift buffer left and append new audio — O(n) but n is tiny (800 samples)
            buffer = np.roll(buffer, -n)
            buffer[-n:] = data

        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype="float32",
                blocksize=block_samples,
                callback=_audio_callback,
            ):
                logger.info("Wakeword stream open — rolling window active")
                while self._running:
                    time.sleep(self.CHECK_EVERY)
                    if not self._running:
                        break

                    snap = buffer.copy()
                    rms  = float(np.sqrt(np.mean(snap ** 2)))
                    if rms < self._rms_threshold:
                        continue  # silence — skip Whisper entirely

                    if self._is_wakeword(snap):
                        logger.info("✦ 'Hey Loki' detected — waking up")
                        if self.on_wakeword:
                            self.on_wakeword()

        except Exception as e:
            logger.error(f"Wakeword stream error: {e}")

    def _is_wakeword(self, audio_np: np.ndarray) -> bool:
        if self._model is None:
            return False

        try:
            result = self._model.transcribe(
                audio_np,
                language="en",
                fp16=False,
                temperature=0,
                condition_on_previous_text=False,
                no_speech_threshold=0.4,
            )
            raw  = result.get("text", "").strip()
            text = raw.lower()

            # Strip punctuation so "Hey, Loki." → "hey loki" matches correctly
            clean = _PUNCT_RE.sub("", text).strip()

            if raw and self.on_transcript:
                self.on_transcript(raw)

            if clean:
                logger.debug(f"heard: {repr(clean)}")

            for variant in self.WAKEWORD_VARIANTS:
                if variant in clean:
                    return True

        except Exception as e:
            logger.debug(f"Wakeword transcription error: {e}")

        return False
