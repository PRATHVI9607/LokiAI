"""
Speech listener — microphone + VAD + Whisper STT.
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
    logger.warning("sounddevice not available")

try:
    import webrtcvad
    VAD_AVAILABLE = True
except ImportError:
    VAD_AVAILABLE = False
    logger.warning("webrtcvad not available")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("openai-whisper not available")


class SpeechListener:
    """Listens to microphone, detects speech, transcribes with Whisper."""

    SAMPLE_RATE = 16000
    FRAME_MS = 30
    FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_MS / 1000)

    def __init__(self, config: dict):
        self._config = config.get("audio", {})
        self._whisper_config = config.get("whisper", {})
        self._vad_level = self._config.get("vad_aggressiveness", 2)
        self._silence_sec = self._config.get("silence_duration", 1.5)
        self._listening = False
        self._thread: Optional[threading.Thread] = None
        self._model = None

        self.on_transcript: Optional[Callable[[str], None]] = None
        self.on_listening_started: Optional[Callable] = None
        self.on_listening_stopped: Optional[Callable] = None

        if WHISPER_AVAILABLE:
            model_name = self._whisper_config.get("model", "base.en")
            logger.info(f"Loading Whisper model: {model_name}")
            try:
                self._model = whisper.load_model(model_name)
                logger.info("Whisper model loaded")
            except Exception as e:
                logger.error(f"Whisper load failed: {e}")

    def start_listening(self) -> None:
        if self._listening:
            return
        self._listening = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        if self.on_listening_started:
            self.on_listening_started()
        logger.info("Listening started")

    def stop_listening(self) -> None:
        self._listening = False
        if self._thread:
            self._thread.join(timeout=3)
        if self.on_listening_stopped:
            self.on_listening_stopped()
        logger.info("Listening stopped")

    def _listen_loop(self) -> None:
        if not SD_AVAILABLE or not VAD_AVAILABLE or not self._model:
            logger.error("Required audio libraries not available")
            return

        vad = webrtcvad.Vad(self._vad_level)
        frames = []
        silence_frames = 0
        max_silence = int(self._silence_sec * 1000 / self.FRAME_MS)
        triggered = False

        def callback(indata, frame_count, time_info, status):
            nonlocal frames, silence_frames, triggered
            if not self._listening:
                raise sd.CallbackStop()

            pcm = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            is_speech = False
            try:
                is_speech = vad.is_speech(pcm, self.SAMPLE_RATE)
            except Exception:
                pass

            if is_speech:
                triggered = True
                frames.append(pcm)
                silence_frames = 0
            elif triggered:
                frames.append(pcm)
                silence_frames += 1
                if silence_frames >= max_silence:
                    self._transcribe(frames[:])
                    frames.clear()
                    silence_frames = 0
                    triggered = False

        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype="float32",
                blocksize=self.FRAME_SAMPLES,
                callback=callback,
            ):
                while self._listening:
                    import time
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Audio stream error: {e}")

    def _transcribe(self, frames: list) -> None:
        if not frames or not self._model:
            return
        try:
            audio_bytes = b"".join(frames)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            result = self._model.transcribe(
                audio_np,
                language=self._whisper_config.get("language", "en"),
                fp16=False,
            )
            text = result.get("text", "").strip()
            if text:
                logger.info(f"Transcribed: {text}")
                if self.on_transcript:
                    self.on_transcript(text)
        except Exception as e:
            logger.error(f"Transcription error: {e}")
