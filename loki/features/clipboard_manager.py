"""
Clipboard manager — maintain clipboard history.
"""

import logging
import threading
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class ClipboardManager:
    """Track and manage clipboard history."""

    MAX_HISTORY = 20

    def __init__(self):
        self._history: List[str] = []
        self._last_seen = ""
        self._monitoring = False
        self._thread = None

    def start_monitoring(self) -> None:
        if not PYPERCLIP_AVAILABLE or self._monitoring:
            return
        self._monitoring = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("Clipboard monitoring started")

    def stop_monitoring(self) -> None:
        self._monitoring = False

    def _monitor_loop(self) -> None:
        while self._monitoring:
            try:
                content = pyperclip.paste()
                if content and content != self._last_seen:
                    self._last_seen = content
                    self._add(content)
            except Exception:
                pass
            time.sleep(1.0)

    def _add(self, text: str) -> None:
        if text in self._history:
            self._history.remove(text)
        self._history.insert(0, text)
        if len(self._history) > self.MAX_HISTORY:
            self._history.pop()

    def get_history(self) -> Dict[str, Any]:
        if not PYPERCLIP_AVAILABLE:
            return {"success": False, "message": "pyperclip not installed."}
        if not self._history:
            return {"success": True, "message": "Clipboard history is empty."}

        lines = [f"Clipboard history ({len(self._history)} items):"]
        for i, item in enumerate(self._history[:10], 1):
            preview = item[:60].replace("\n", " ")
            lines.append(f"  {i}. {preview}{'...' if len(item) > 60 else ''}")

        return {"success": True, "message": "\n".join(lines), "data": self._history}

    def get_item(self, index: int) -> Dict[str, Any]:
        if 0 <= index < len(self._history):
            item = self._history[index]
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(item)
            return {"success": True, "message": f"Copied item {index + 1} to clipboard.", "data": item}
        return {"success": False, "message": f"No item at index {index + 1}."}

    def clear(self) -> Dict[str, Any]:
        self._history.clear()
        if PYPERCLIP_AVAILABLE:
            try:
                pyperclip.copy("")
            except Exception:
                pass
        return {"success": True, "message": "Clipboard history cleared."}
