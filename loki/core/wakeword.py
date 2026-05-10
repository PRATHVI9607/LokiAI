"""
Wakeword detector — Whisper-based "Hey Loki" detection.
Porcupine is optional if access key is configured.
Callback-based; no Qt dependency.
"""

import logging
import threading
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


class WakewordDetector:
    """Detects 'Hey Loki' wakeword using Whisper or Porcupine."""

    SAMPLE_RATE = 16000
    CHUNK_SECONDS = 2.0

    WAKEWORD_VARIANTS = {
        "hey loki", "hay loki", "hello loki", "ok loki", "okay loki",
        "loki", "hey lolly", "hey lucky",
    }

    def __init__(self, config: dict):
        self._config = config.get("wakeword", {})
        self._method = self._config.get("method", "whisper")
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._model = None

        self.on_wakeword: Optional[Callable] = None
        self.on_transcript: Optional[Callable[[str], None]] = None

        if self._method == "whisper" and WHISPER_AVAILABLE:
            try:
                self._model = whisper.load_model("tiny.en")
                logger.info("Wakeword Whisper model loaded (tiny.en)")
            except Exception as e:
                logger.error(f"Wakeword Whisper load failed: {e}")

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._detect_loop, daemon=True)
        self._thread.start()
        logger.info("Wakeword detector started — say 'Hey Loki'")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        logger.info("Wakeword detector stopped")

    def _detect_loop(self) -> None:
        if not SD_AVAILABLE:
            logger.error("sounddevice not available — wakeword disabled")
            return

        chunk_samples = int(self.SAMPLE_RATE * self.CHUNK_SECONDS)

        while self._running:
            try:
                audio = sd.rec(chunk_samples, samplerate=self.SAMPLE_RATE,
                               channels=1, dtype="float32")
                sd.wait()

                if not self._running:
                    break

                audio_np = audio[:, 0]
                if self._is_wakeword(audio_np):
                    logger.info("Wakeword detected!")
                    if self.on_wakeword:
                        self.on_wakeword()

            except Exception as e:
                logger.error(f"Wakeword loop error: {e}")
                import time
                time.sleep(0.5)

    def _is_wakeword(self, audio_np: np.ndarray) -> bool:
        if self._model is None:
            return False

        rms = float(np.sqrt(np.mean(audio_np ** 2)))
        if rms < 0.01:
            return False

        try:
            result = self._model.transcribe(audio_np, language="en", fp16=False)
            text = result.get("text", "").strip().lower()

            if text and self.on_transcript:
                self.on_transcript(text)

            for variant in self.WAKEWORD_VARIANTS:
                if variant in text:
                    return True
        except Exception as e:
            logger.debug(f"Wakeword transcription error: {e}")

        return False
