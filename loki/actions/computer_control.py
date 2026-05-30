"""
ComputerControl — direct desktop control: move, click, type, scroll, hotkeys,
and screen reading. Lets Loki operate the machine like a person sitting at it.

Backed by pyautogui (mouse/keyboard) + the existing screenshot OCR for "read
the screen" and "click the button that says X".

Safety:
  - pyautogui FAILSAFE is ON — slam the mouse to a screen corner to abort.
  - Typing/among-app control is powerful; destructive intents are gated by the
    router's confirmation layer where applicable.
"""

import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
    PYAUTOGUI = True
except Exception:
    PYAUTOGUI = False
    logger.warning("pyautogui not available — computer control disabled (pip install pyautogui)")


class ComputerControl:
    """Mouse, keyboard, and screen-reading control of the desktop."""

    def __init__(self, screenshot_search=None):
        # screenshot_search provides OCR for 'click the text that says X'
        self._ocr = screenshot_search

    def _na(self) -> Dict[str, Any]:
        return {"success": False, "message": "Computer control unavailable — run: pip install pyautogui"}

    # ── pointer ─────────────────────────────────────────────────────────

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              button: str = "left", double: bool = False) -> Dict[str, Any]:
        if not PYAUTOGUI:
            return self._na()
        try:
            btn = "right" if button == "right" else "left"
            if x is not None and y is not None:
                pyautogui.moveTo(int(x), int(y), duration=0.15)
            if double:
                pyautogui.doubleClick(button=btn)
            else:
                pyautogui.click(button=btn)
            where = f"({x},{y})" if x is not None else "current position"
            return {"success": True, "message": f"{'Double-' if double else ''}{btn}-clicked at {where}."}
        except Exception as e:
            return {"success": False, "message": f"Click failed: {e}"}

    def move(self, x: int, y: int) -> Dict[str, Any]:
        if not PYAUTOGUI:
            return self._na()
        try:
            pyautogui.moveTo(int(x), int(y), duration=0.2)
            return {"success": True, "message": f"Moved cursor to ({x},{y})."}
        except Exception as e:
            return {"success": False, "message": f"Move failed: {e}"}

    def scroll(self, amount: int = -500) -> Dict[str, Any]:
        if not PYAUTOGUI:
            return self._na()
        try:
            pyautogui.scroll(int(amount))
            return {"success": True, "message": f"Scrolled {'down' if amount < 0 else 'up'}."}
        except Exception as e:
            return {"success": False, "message": f"Scroll failed: {e}"}

    # ── keyboard ────────────────────────────────────────────────────────

    def type_text(self, text: str) -> Dict[str, Any]:
        if not PYAUTOGUI:
            return self._na()
        if not text:
            return {"success": False, "message": "Nothing to type."}
        try:
            pyautogui.typewrite(text, interval=0.01)
            return {"success": True, "message": f"Typed {len(text)} characters."}
        except Exception as e:
            return {"success": False, "message": f"Type failed: {e}"}

    def press(self, key: str) -> Dict[str, Any]:
        """Press a single key or a hotkey combo like 'ctrl+s', 'alt+tab', 'win+d'."""
        if not PYAUTOGUI:
            return self._na()
        if not key:
            return {"success": False, "message": "No key specified."}
        try:
            if "+" in key:
                keys = [k.strip().lower() for k in key.split("+")]
                pyautogui.hotkey(*keys)
                return {"success": True, "message": f"Pressed {key}."}
            pyautogui.press(key.strip().lower())
            return {"success": True, "message": f"Pressed {key}."}
        except Exception as e:
            return {"success": False, "message": f"Key press failed: {e}"}

    # ── screen reading + click-by-text ──────────────────────────────────

    def read_screen(self) -> Dict[str, Any]:
        """OCR the current screen and return the visible text."""
        if not self._ocr:
            return {"success": False, "message": "Screen reading not wired up."}
        try:
            return self._ocr.capture_and_read()
        except Exception as e:
            return {"success": False, "message": f"Screen read failed: {e}"}

    def click_text(self, target: str) -> Dict[str, Any]:
        """Find on-screen text and click its location (OCR with bounding boxes)."""
        if not PYAUTOGUI:
            return self._na()
        if not self._ocr or not hasattr(self._ocr, "locate_text"):
            return {"success": False, "message": "Click-by-text needs OCR with bounding boxes (pytesseract)."}
        try:
            loc = self._ocr.locate_text(target)
            if not loc or not loc.get("success"):
                return {"success": False, "message": f"Couldn't find '{target}' on screen."}
            x, y = loc["data"]["x"], loc["data"]["y"]
            pyautogui.moveTo(x, y, duration=0.15)
            pyautogui.click()
            return {"success": True, "message": f"Clicked '{target}'."}
        except Exception as e:
            return {"success": False, "message": f"Click-by-text failed: {e}"}

    # ── window / desktop shortcuts ──────────────────────────────────────

    def hotkey_action(self, action: str) -> Dict[str, Any]:
        """Common desktop actions by name."""
        if not PYAUTOGUI:
            return self._na()
        mapping = {
            "minimize": ("win", "down"), "maximize": ("win", "up"),
            "show desktop": ("win", "d"), "switch window": ("alt", "tab"),
            "close window": ("alt", "f4"), "lock": ("win", "l"),
            "copy": ("ctrl", "c"), "paste": ("ctrl", "v"), "cut": ("ctrl", "x"),
            "save": ("ctrl", "s"), "undo": ("ctrl", "z"), "select all": ("ctrl", "a"),
            "new tab": ("ctrl", "t"), "close tab": ("ctrl", "w"),
            "screenshot": ("win", "shift", "s"),
        }
        combo = mapping.get(action.lower().strip())
        if not combo:
            return {"success": False, "message": f"Unknown action '{action}'."}
        try:
            pyautogui.hotkey(*combo)
            return {"success": True, "message": f"Did: {action}."}
        except Exception as e:
            return {"success": False, "message": f"Action failed: {e}"}
