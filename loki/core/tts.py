"""
Loki TTS — edge-tts primary (Microsoft Neural), pyttsx3 fallback.
"""

import asyncio
import logging
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal

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


class LokiTTS(QObject):
    """Text-to-speech engine with edge-tts primary, pyttsx3 fallback."""

    speaking_started = pyqtSignal()
    speaking_stopped = pyqtSignal()

    def __init__(self, config: dict):
        super().__init__()
        self._config = config
        self._engine_name = config.get("engine", "edge")
        self._voice = config.get("voice", "en-GB-RyanNeural")
        self._rate = config.get("rate", "+0%")
        self._volume_str = config.get("volume", "+0%")
        self._pyttsx3_engine: Optional[Any] = None
        self._speaking = False
        self._lock = threading.Lock()

        if self._engine_name == "pyttsx3" or not EDGE_TTS_AVAILABLE:
            self._init_pyttsx3()

        logger.info(f"TTS initialized: {self._engine_name}")

    def _init_pyttsx3(self) -> None:
        if not PYTTSX3_AVAILABLE:
            return
        try:
            self._pyttsx3_engine = pyttsx3.init()
            # Set a deeper, more authoritative voice
            voices = self._pyttsx3_engine.getProperty("voices")
            for voice in voices:
                if "male" in voice.name.lower() or "david" in voice.name.lower():
                    self._pyttsx3_engine.setProperty("voice", voice.id)
                    break
            self._pyttsx3_engine.setProperty("rate", 175)
            self._pyttsx3_engine.setProperty("volume", 0.9)
        except Exception as e:
            logger.error(f"pyttsx3 init failed: {e}")

    def speak(self, text: str, streaming: bool = False) -> None:
        if not text or not text.strip():
            return
        with self._lock:
            if self._speaking:
                return
            self._speaking = True

        self.speaking_started.emit()
        thread = threading.Thread(target=self._speak_thread, args=(text,), daemon=True)
        thread.start()

    def _speak_thread(self, text: str) -> None:
        try:
            if EDGE_TTS_AVAILABLE and self._engine_name == "edge":
                self._speak_edge(text)
            elif self._pyttsx3_engine:
                self._speak_pyttsx3(text)
            else:
                logger.warning(f"TTS: no engine available. Text: {text[:50]}")
        except Exception as e:
            logger.error(f"TTS error: {e}", exc_info=True)
        finally:
            with self._lock:
                self._speaking = False
            self.speaking_stopped.emit()

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
                # WMPlayer.OCX.7 supports MP3 natively; 8s ceiling covers any TTS clip
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
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        with self._lock:
            self._speaking = False

    @property
    def is_speaking(self) -> bool:
        return self._speaking


def create_tts_engine(config: dict) -> LokiTTS:
    tts_config = config.get("tts", {})
    return LokiTTS(tts_config)
