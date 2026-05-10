"""
DynamicUI — change Windows wallpaper and push theme tokens based on time of day,
user mood, or explicit command. Theme changes are pushed to the Next.js frontend
via a shared state file that the FastAPI server reads on the next poll.
"""

import ctypes
import json
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDCHANGE = 0x0002

# Time-based theme periods
TIME_THEMES = {
    "dawn":      (5,  8,  {"period": "dawn",      "bg": "#1a1a2e", "accent": "#f4a261", "text": "#ffd6a5", "label": "Dawn"}),
    "morning":   (8,  12, {"period": "morning",   "bg": "#0d0d1a", "accent": "#c4a45a", "text": "#cdd6f4", "label": "Morning"}),
    "afternoon": (12, 17, {"period": "afternoon", "bg": "#0d0d1a", "accent": "#8be9fd", "text": "#cdd6f4", "label": "Afternoon"}),
    "evening":   (17, 21, {"period": "evening",   "bg": "#0a0a14", "accent": "#bd93f9", "text": "#cdd6f4", "label": "Evening"}),
    "night":     (21, 29, {"period": "night",     "bg": "#06060f", "accent": "#50fa7b", "text": "#a0a8c0", "label": "Night"}),
}

MOOD_THEMES = {
    "focus":       {"bg": "#0a0a14", "accent": "#50fa7b", "text": "#cdd6f4", "label": "Focus"},
    "creative":    {"bg": "#1a0a2e", "accent": "#ff79c6", "text": "#f8f8f2", "label": "Creative"},
    "energetic":   {"bg": "#0d1a0d", "accent": "#f1fa8c", "text": "#cdd6f4", "label": "Energetic"},
    "calm":        {"bg": "#0d1420", "accent": "#8be9fd", "text": "#cdd6f4", "label": "Calm"},
    "professional":{"bg": "#0d0d1a", "accent": "#c4a45a", "text": "#cdd6f4", "label": "Professional"},
    "dark":        {"bg": "#000000", "accent": "#ff5555", "text": "#ff5555", "label": "Dark"},
}

# Bundled wallpaper colors (solid color BMP via Pillow if available)
PERIOD_COLORS = {
    "dawn":      (26, 20, 40),
    "morning":   (13, 13, 26),
    "afternoon": (10, 15, 30),
    "evening":   (10, 8, 20),
    "night":     (5, 5, 15),
}


def _set_wallpaper_path(path: str) -> bool:
    try:
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        return True
    except Exception as e:
        logger.debug("Wallpaper set failed: %s", e)
        return False


def _create_solid_bmp(color: tuple[int, int, int], width: int = 1920, height: int = 1080) -> Optional[Path]:
    """Create a solid-color BMP as a wallpaper using Pillow."""
    try:
        from PIL import Image
        img = Image.new("RGB", (width, height), color)
        out = Path.home() / "AppData/Local/Temp" / f"loki_wallpaper_{color[0]}_{color[1]}_{color[2]}.bmp"
        img.save(str(out), format="BMP")
        return out
    except Exception as e:
        logger.debug("BMP creation failed: %s", e)
        return None


class DynamicUI:
    def __init__(self, state_path: Optional[str] = None):
        self._state_path = Path(state_path) if state_path else Path.home() / ".loki_ui_theme.json"
        self._auto_thread: Optional[threading.Thread] = None
        self._auto_running = False

    def _write_state(self, theme: dict) -> None:
        try:
            self._state_path.write_text(json.dumps(theme, indent=2), encoding="utf-8")
        except Exception as e:
            logger.debug("Theme state write failed: %s", e)

    def _get_period_theme(self) -> dict:
        hour = datetime.now().hour
        for name, (start, end, theme) in TIME_THEMES.items():
            if start <= hour < end:
                return theme
        return TIME_THEMES["night"][2]

    def get_current_theme(self) -> dict:
        """Read the current active theme state."""
        if self._state_path.exists():
            try:
                data = json.loads(self._state_path.read_text(encoding="utf-8"))
                return {"success": True, "message": f"Current theme: {data.get('label', '?')}", "data": data}
            except Exception:
                pass
        theme = self._get_period_theme()
        return {"success": True, "message": f"Current theme: {theme['label']}", "data": theme}

    def apply_time_theme(self) -> dict:
        """Apply the theme appropriate for the current time of day."""
        theme = self._get_period_theme()
        self._write_state(theme)

        # Try to set wallpaper to matching solid color
        color = PERIOD_COLORS.get(theme["period"])
        wallpaper_set = False
        if color:
            bmp = _create_solid_bmp(color)
            if bmp:
                wallpaper_set = _set_wallpaper_path(str(bmp))

        msg = f"Theme set to '{theme['label']}' (time-based)"
        if wallpaper_set:
            msg += " + wallpaper updated."
        return {"success": True, "message": msg, "data": theme}

    def apply_mood_theme(self, mood: str) -> dict:
        """Apply a mood-based theme."""
        mood_key = mood.lower().strip()
        theme = MOOD_THEMES.get(mood_key)
        if not theme:
            available = ", ".join(MOOD_THEMES.keys())
            return {"success": False, "message": f"Unknown mood '{mood}'. Available: {available}"}

        self._write_state(theme)
        return {"success": True, "message": f"Theme set to '{theme['label']}' mode.", "data": theme}

    def set_wallpaper(self, image_path: str) -> dict:
        """Set a custom wallpaper from a file path."""
        fp = Path(image_path).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"Image not found: {fp}"}
        if fp.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".gif"}:
            return {"success": False, "message": f"Unsupported image format: {fp.suffix}"}

        # Windows requires BMP or JPG; convert PNG if needed
        path_to_set = str(fp)
        if fp.suffix.lower() == ".png":
            try:
                from PIL import Image
                bmp = fp.with_suffix(".bmp")
                Image.open(fp).convert("RGB").save(str(bmp), format="BMP")
                path_to_set = str(bmp)
            except Exception:
                pass

        ok = _set_wallpaper_path(path_to_set)
        if ok:
            return {"success": True, "message": f"Wallpaper set to {fp.name}.", "data": {"path": path_to_set}}
        return {"success": False, "message": "Could not set wallpaper (Windows API failed)."}

    def start_auto_theme(self) -> dict:
        """Start a background thread that auto-applies time-based theme every 30 minutes."""
        if self._auto_running:
            return {"success": True, "message": "Auto-theme is already running."}

        self._auto_running = True

        def _loop():
            import time
            while self._auto_running:
                self.apply_time_theme()
                time.sleep(1800)  # 30 minutes

        self._auto_thread = threading.Thread(target=_loop, daemon=True, name="loki-auto-theme")
        self._auto_thread.start()
        return {"success": True, "message": "Auto-theme started — updates every 30 minutes.", "data": {}}

    def stop_auto_theme(self) -> dict:
        """Stop the auto-theme background thread."""
        self._auto_running = False
        return {"success": True, "message": "Auto-theme stopped.", "data": {}}

    def list_themes(self) -> dict:
        """List all available themes."""
        time_list = [{"id": k, "label": v[2]["label"], "hours": f"{v[0]}:00–{v[1]}:00"} for k, v in TIME_THEMES.items()]
        mood_list = [{"id": k, "label": v["label"]} for k, v in MOOD_THEMES.items()]
        msg = "Time-based themes: " + ", ".join(t["label"] for t in time_list)
        msg += "\nMood themes: " + ", ".join(m["label"] for m in mood_list)
        return {"success": True, "message": msg, "data": {"time_themes": time_list, "mood_themes": mood_list}}
