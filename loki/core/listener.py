"""
Speech listener — microphone + VAD + Whisper STT.

Key fixes over the original:
- VAD aggressiveness 1 (was 2) — catches softer speech without missing words
- Minimum audio guard — skips < 0.5s clips that produce garbage transcriptions
- Buffer accumulation fallback — if speech detected but silence never triggers,
  flush after max_record_sec to avoid infinite accumulation
- Whisper params tuned: temperature=0, condition_on_previous_text=False,
  no_speech_threshold=0.5, logprob_threshold=-1.0 — far more reliable
- PCM frame size validation before passing to webrtcvad
"""

import logging
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
    logger.warning("sounddevice not available — pip install sounddevice")

try:
    import webrtcvad
    VAD_AVAILABLE = True
except ImportError:
    VAD_AVAILABLE = False
    logger.warning("webrtcvad not available — pip install webrtcvad-wheels")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("openai-whisper not available — pip install openai-whisper")


# Minimum valid audio before sending to Whisper (0.5 seconds at 16kHz)
MIN_AUDIO_SAMPLES = 8_000
# Maximum seconds to record before force-flushing (prevents infinite accumulation)
MAX_RECORD_SEC = 30


class SpeechListener:
    """Listens to microphone, detects speech via VAD, transcribes with Whisper."""

    SAMPLE_RATE = 16_000
    FRAME_MS = 30
    FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_MS / 1000)  # 480 samples per frame
    FRAME_BYTES = FRAME_SAMPLES * 2                      # int16 = 2 bytes per sample

    def __init__(self, config: dict):
        audio_cfg = config.get("audio", {})
        whisper_cfg = config.get("whisper", {})

        # Use aggressiveness 1 — level 2 filters too aggressively and misses soft speech
        self._vad_level = audio_cfg.get("vad_aggressiveness", 1)
        self._silence_sec = audio_cfg.get("silence_duration", 2.0)
        self._listening = False
        self._thread: Optional[threading.Thread] = None
        self._model = None

        self.on_transcript: Optional[Callable[[str], None]] = None
        self.on_listening_started: Optional[Callable] = None
        self.on_listening_stopped: Optional[Callable] = None

        if WHISPER_AVAILABLE:
            model_name = whisper_cfg.get("model", "base.en")
            logger.info(f"Loading Whisper model: {model_name}")
            try:
                self._model = whisper.load_model(model_name)
                logger.info("Whisper model loaded successfully")
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
            logger.error("Required audio libraries not available — cannot start listener")
            return

        vad = webrtcvad.Vad(self._vad_level)
        frames: list[bytes] = []
        silence_frames = 0
        max_silence = int(self._silence_sec * 1000 / self.FRAME_MS)
        max_record_frames = int(MAX_RECORD_SEC * 1000 / self.FRAME_MS)
        triggered = False

        # PCM remainder buffer for handling partial frames from sounddevice
        pcm_buffer = b""

        def callback(indata, frame_count, time_info, status):
            nonlocal frames, silence_frames, triggered, pcm_buffer

            if not self._listening:
                raise sd.CallbackStop()

            if status:
                logger.debug(f"Audio status: {status}")

            # Convert float32 → int16 PCM bytes
            pcm_chunk = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            pcm_buffer += pcm_chunk

            # Process complete 30ms frames from the buffer
            while len(pcm_buffer) >= self.FRAME_BYTES:
                frame = pcm_buffer[:self.FRAME_BYTES]
                pcm_buffer = pcm_buffer[self.FRAME_BYTES:]

                is_speech = False
                try:
                    is_speech = vad.is_speech(frame, self.SAMPLE_RATE)
                except Exception as e:
                    logger.debug(f"VAD frame error: {e}")
                    continue

                if is_speech:
                    triggered = True
                    frames.append(frame)
                    silence_frames = 0
                elif triggered:
                    frames.append(frame)
                    silence_frames += 1

                    # Silence threshold reached → flush to Whisper
                    if silence_frames >= max_silence:
                        self._transcribe(frames[:])
                        frames.clear()
                        silence_frames = 0
                        triggered = False

                # Safety: flush if recording has gone on too long
                if len(frames) >= max_record_frames:
                    logger.warning("Max record duration hit — force flushing audio")
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
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Audio stream error: {e}")

    def _transcribe(self, frames: list[bytes]) -> None:
        if not frames or not self._model:
            return

        try:
            audio_bytes = b"".join(frames)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            # Skip clips shorter than 0.5 seconds — Whisper hallucinates on micro-clips
            if len(audio_np) < MIN_AUDIO_SAMPLES:
                logger.debug(f"Audio too short ({len(audio_np)} samples) — skipped")
                return

            result = self._model.transcribe(
                audio_np,
                language="en",
                fp16=False,
                # temperature=0 → deterministic, no creative hallucination
                temperature=0,
                # Don't condition on previous transcript — prevents runaway repetition
                condition_on_previous_text=False,
                # Threshold below which segment is treated as silence (lower = more permissive)
                no_speech_threshold=0.5,
                # Allow lower confidence transcriptions through
                logprob_threshold=-1.0,
            )

            text = result.get("text", "").strip()

            # Reject single-word garbage and common Whisper hallucinations
            if text and len(text) > 2 and text.lower() not in {
                "you", ".", "thank you.", "thanks.", "bye.", "okay.",
                "hmm.", "uh.", "um.", "ah.", "oh.", "huh.",
            }:
                logger.info(f"Transcribed: {text}")
                if self.on_transcript:
                    self.on_transcript(text)
            else:
                logger.debug(f"Transcript filtered out: {text!r}")

        except Exception as e:
            logger.error(f"Transcription error: {e}")
