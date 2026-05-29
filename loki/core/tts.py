"""
Loki TTS — edge-tts primary (Microsoft Neural), pyttsx3 fallback.
Callback-based; no Qt dependency.
"""

import asyncio
import logging
import queue as _queue_module
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    logger.warning("edge-tts not available")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logger.warning("pyttsx3 not available")

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


class LokiTTS:
    """Text-to-speech engine with edge-tts primary, pyttsx3 fallback.

    Uses a queue so messages are never dropped — on_speaking_stopped fires
    only when the queue fully drains, so the mic isn't returned prematurely.
    """

    def __init__(self, config: dict):
        self._config = config
        self._engine_name = config.get("engine", "edge")
        self._voice = config.get("voice", "en-GB-RyanNeural")
        self._rate = config.get("rate", "+0%")
        self._volume_str = config.get("volume", "+0%")
        self._pyttsx3_engine: Optional[Any] = None
        self._pyttsx3_ready = False  # True once initialized inside the worker thread
        self._speaking = False
        self._lock = threading.Lock()
        self._stopped = False  # set True on stop() to skip remaining items

        self._queue: _queue_module.Queue = _queue_module.Queue()

        self.on_speaking_started: Optional[Callable] = None
        self.on_speaking_stopped: Optional[Callable] = None

        # Start the single-threaded queue worker — pyttsx3 is initialized there
        # so COM is created in the same thread that calls runAndWait() (Windows req.)
        threading.Thread(target=self._queue_worker, daemon=True, name="loki-tts").start()

        logger.info(f"TTS initialized: {self._engine_name}")

    def _init_pyttsx3(self) -> None:
        if not PYTTSX3_AVAILABLE:
            return
        try:
            self._pyttsx3_engine = pyttsx3.init()
            voices = self._pyttsx3_engine.getProperty("voices")
            for voice in voices:
                if "male" in voice.name.lower() or "david" in voice.name.lower():
                    self._pyttsx3_engine.setProperty("voice", voice.id)
                    break
            self._pyttsx3_engine.setProperty("rate", 175)
            self._pyttsx3_engine.setProperty("volume", 0.9)
        except Exception as e:
            logger.error(f"pyttsx3 init failed: {e}")

    def speak(self, text: str) -> None:
        """Enqueue text for speaking. Never drops messages."""
        if not text or not text.strip():
            return
        self._queue.put(text)

    def _queue_worker(self) -> None:
        """Single background thread — serializes all speech, signals when queue drains.
        pyttsx3 is initialized here (same-thread requirement for COM on Windows)."""
        if PYTTSX3_AVAILABLE and not self._pyttsx3_ready:
            self._init_pyttsx3()
            self._pyttsx3_ready = True

        while True:
            text = self._queue.get()
            skip = False
            with self._lock:
                if self._stopped:
                    skip = True
                else:
                    self._speaking = True
            if not skip:
                if self.on_speaking_started:
                    self.on_speaking_started()
                try:
                    if EDGE_TTS_AVAILABLE and self._engine_name == "edge":
                        self._speak_edge(text)
                    elif self._pyttsx3_engine:
                        self._speak_pyttsx3(text)
                    else:
                        logger.warning(f"TTS: no engine available. Text: {text[:50]}")
                except Exception as e:
                    logger.error(f"TTS error: {e}", exc_info=True)
            self._queue.task_done()
            if self._queue.empty():
                with self._lock:
                    self._speaking = False
                    self._stopped = False  # ready for next use
                if not skip and self.on_speaking_stopped:
                    self.on_speaking_stopped()

    def _speak_edge(self, text: str) -> None:
        async def _run():
            communicate = edge_tts.Communicate(
                text=text,
                voice=self._voice,
                rate=self._rate,
                volume=self._volume_str,
            )
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp_path = f.name
            await communicate.save(tmp_path)
            return tmp_path

        try:
            loop = asyncio.new_event_loop()
            tmp_path = loop.run_until_complete(_run())
            loop.close()
            self._play_audio(tmp_path)
        except Exception as e:
            logger.error(f"edge-tts failed: {e}, falling back to pyttsx3")
            if self._pyttsx3_engine:
                self._speak_pyttsx3(text)

    def _speak_pyttsx3(self, text: str) -> None:
        if self._pyttsx3_engine:
            self._pyttsx3_engine.say(text)
            self._pyttsx3_engine.runAndWait()

    def _play_audio(self, path: str) -> None:
        played = False
        try:
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
                played = True
        except Exception as e:
            logger.error(f"pygame playback error: {e}")

        if not played:
            try:
                import subprocess
                safe = path.replace("'", "''")
                ps = (
                    f"$w=New-Object -ComObject WMPlayer.OCX.7;"
                    f"$w.URL='{safe}';"
                    f"$w.controls.play();"
                    f"$end=[DateTime]::Now.AddSeconds(8);"
                    f"while($w.playState-eq 3 -and [DateTime]::Now-lt$end){{Start-Sleep -ms 100}};"
                    f"$w.controls.stop();$w.close()"
                )
                subprocess.run(
                    ["powershell", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", ps],
                    capture_output=True, timeout=12,
                )
            except Exception as e:
                logger.warning(f"Audio playback fallback failed: {e}")

        try:
            Path(path).unlink(missing_ok=True)
        except Exception:
            pass

    def stop(self) -> None:
        """Stop current playback and drain all queued speech."""
        with self._lock:
            self._stopped = True
            self._speaking = False

        # Drain queued items so they are not spoken after stop()
        try:
            while True:
                self._queue.get_nowait()
                self._queue.task_done()
        except _queue_module.Empty:
            pass

        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

        # Best-effort stop of pyttsx3 runAndWait loop
        if self._pyttsx3_engine:
            try:
                self._pyttsx3_engine.stop()
            except Exception:
                pass

    @property
    def is_speaking(self) -> bool:
        return self._speaking

    @property
    def is_idle(self) -> bool:
        """True when neither speaking nor queued."""
        return not self._speaking and self._queue.empty()


def create_tts_engine(config: dict) -> LokiTTS:
    tts_config = config.get("tts", {})
    return LokiTTS(tts_config)
