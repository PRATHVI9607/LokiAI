"""
Speech listener — microphone + VAD + Whisper STT.

Key design:
- Audio callback is NON-BLOCKING: it only buffers raw PCM frames into a Queue.
- A dedicated worker thread drains the queue and runs Whisper transcription.
  This prevents Whisper (100-600ms) from stalling the sounddevice callback
  which must return in < one audio block or the driver drops frames.
- VAD aggressiveness 1 — catches softer speech without missing words.
- Minimum audio guard — skips < 0.35s clips that produce garbage transcriptions.
- Buffer flush — if speech starts but silence never triggers, flush after max_record_sec.
- Whisper params: temperature=0, condition_on_previous_text=False — more reliable.
"""

import logging
import queue
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


def _whisper_device(pref: str) -> str:
    """Resolve the Whisper device. 'auto' → cuda if available, else cpu."""
    if pref == "cuda":
        return "cuda"
    if pref == "cpu":
        return "cpu"
    # auto
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


class SpeechListener:
    """Listens to microphone, detects speech via VAD, transcribes with Whisper."""

    SAMPLE_RATE = 16_000
    FRAME_MS = 30
    FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_MS / 1000)  # 480 samples per frame
    FRAME_BYTES = FRAME_SAMPLES * 2                      # int16 = 2 bytes per sample

    def __init__(self, config: dict):
        audio_cfg = config.get("audio", {})
        whisper_cfg = config.get("whisper", {})

        self._vad_level = audio_cfg.get("vad_aggressiveness", 1)
        self._silence_sec = audio_cfg.get("silence_duration", 1.0)
        self._min_audio_samples = int(audio_cfg.get("min_audio_seconds", 0.35) * self.SAMPLE_RATE)
        self._max_record_sec = audio_cfg.get("max_record_seconds", 15)
        self._no_speech_threshold = audio_cfg.get("no_speech_threshold", 0.35)
        self._listening = False
        self._thread: Optional[threading.Thread] = None
        self._model = None

        # Worker queue: callback puts completed frame-lists here; worker runs Whisper
        self._work_queue: queue.Queue = queue.Queue(maxsize=8)
        self._worker: threading.Thread = threading.Thread(
            target=self._transcribe_worker, daemon=True, name="loki-stt-worker"
        )
        self._worker.start()

        self.on_transcript: Optional[Callable[[str], None]] = None
        self.on_listening_started: Optional[Callable] = None
        self.on_listening_stopped: Optional[Callable] = None

        if WHISPER_AVAILABLE:
            model_name = whisper_cfg.get("model", "base.en")
            device = _whisper_device(whisper_cfg.get("device", "auto"))
            logger.info(f"Loading Whisper model: {model_name} on {device.upper()}")
            try:
                self._model = whisper.load_model(model_name, device=device)
                logger.info(f"Whisper model loaded successfully ({device})")
            except Exception as e:
                logger.error(f"Whisper load failed: {e}")

    # ── Public interface ────────────────────────────────────────────────

    @property
    def is_listening(self) -> bool:
        return self._listening

    def start_listening(self) -> None:
        if self._listening:
            return
        self._listening = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        if self.on_listening_started:
            self.on_listening_started()
        logger.info("🎤 mic open — listening for your command")

    def stop_listening(self) -> None:
        was_listening = self._listening
        self._listening = False
        if self._thread and threading.current_thread() is not self._thread:
            self._thread.join(timeout=3)
        if self.on_listening_stopped:
            self.on_listening_stopped()
        if was_listening:
            logger.info("🎤 mic closed")

    # ── Audio capture loop (runs on its own thread) ─────────────────────

    def _listen_loop(self) -> None:
        if not SD_AVAILABLE or not VAD_AVAILABLE or not self._model:
            logger.error("Required audio libraries not available — cannot start listener")
            return

        vad = webrtcvad.Vad(self._vad_level)
        frames: list[bytes] = []
        silence_frames = 0
        max_silence = int(self._silence_sec * 1000 / self.FRAME_MS)
        max_record_frames = int(self._max_record_sec * 1000 / self.FRAME_MS)
        triggered = False
        pcm_buffer = b""

        def callback(indata, frame_count, time_info, status):
            nonlocal frames, silence_frames, triggered, pcm_buffer

            if not self._listening:
                raise sd.CallbackStop()

            if status:
                logger.debug(f"Audio status: {status}")

            pcm_chunk = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            pcm_buffer += pcm_chunk

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

                    if silence_frames >= max_silence:
                        # Enqueue for worker; never block the callback
                        try:
                            self._work_queue.put_nowait(frames[:])
                        except queue.Full:
                            logger.warning("STT work queue full — dropping audio clip")
                        frames.clear()
                        silence_frames = 0
                        triggered = False

                if len(frames) >= max_record_frames:
                    logger.warning("Max record duration hit — force flushing audio")
                    try:
                        self._work_queue.put_nowait(frames[:])
                    except queue.Full:
                        logger.warning("STT work queue full — dropping long clip")
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

    # ── Transcription worker (runs on its own daemon thread) ────────────

    def _transcribe_worker(self) -> None:
        """Drain the work queue and run Whisper on each frame list.
        Completely separate from the audio capture thread — no callback blocking.
        Stale frames queued before stop_listening() are silently dropped."""
        while True:
            try:
                frames = self._work_queue.get(timeout=1.0)
            except queue.Empty:
                continue
            try:
                # Drop if we stopped listening before this frame was picked up —
                # prevents stale audio firing on_transcript after conversation ends
                if self._listening:
                    self._transcribe(frames)
                else:
                    logger.debug("Dropped stale audio frame (not listening)")
            except Exception as e:
                logger.error(f"Transcription worker error: {e}", exc_info=True)
            finally:
                self._work_queue.task_done()

    def _transcribe(self, frames: list[bytes]) -> None:
        if not frames or not self._model:
            return

        try:
            audio_bytes = b"".join(frames)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            if len(audio_np) < self._min_audio_samples:
                logger.debug(f"Audio too short ({len(audio_np)} samples) — skipped")
                return

            result = self._model.transcribe(
                audio_np,
                language="en",
                fp16=False,
                temperature=0,
                condition_on_previous_text=False,
                no_speech_threshold=self._no_speech_threshold,
                logprob_threshold=-1.0,
            )

            text = result.get("text", "").strip()

            if text and len(text) > 2 and text.lower() not in {
                "you", ".", "thank you.", "thanks.", "bye.", "okay.",
                "hmm.", "uh.", "um.", "ah.", "oh.", "huh.",
            }:
                # Double-check: only fire if still listening at point of callback
                # (stop_listening may have been called while Whisper was running)
                if self._listening and self.on_transcript:
                    logger.info(f"📝 you said: \"{text}\"")
                    self.on_transcript(text)
                elif not self._listening:
                    logger.debug(f"discarded (mic closed): {text!r}")
            else:
                logger.debug(f"Transcript filtered out: {text!r}")

        except Exception as e:
            logger.error(f"Transcription error: {e}")
