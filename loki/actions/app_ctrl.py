"""
App control — open and close ANY application on the system.

Resolution order when opening:
  1. Known alias map (chrome → chrome, etc.)
  2. Direct os.startfile (works for PATH exes, registered apps, protocols)
  3. `where.exe` lookup on PATH
  4. Start-Menu .lnk shortcut search (finds anything the user has installed:
     games, Spotify, Discord, custom apps…) — fuzzy name match
"""

import os
import glob
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)

# Quick aliases for common apps (spoken name → launch target)
APP_MAP = {
    "chrome": "chrome", "google chrome": "chrome",
    "firefox": "firefox", "edge": "msedge", "microsoft edge": "msedge",
    "brave": "brave", "opera": "opera",
    "notepad": "notepad", "notepad++": "notepad++",
    "vscode": "code", "vs code": "code", "visual studio code": "code", "code": "code",
    "explorer": "explorer", "file explorer": "explorer", "files": "explorer",
    "calculator": "calc", "calc": "calc",
    "terminal": "wt", "windows terminal": "wt",
    "cmd": "cmd", "command prompt": "cmd", "powershell": "powershell",
    "task manager": "taskmgr", "taskmgr": "taskmgr",
    "word": "winword", "excel": "excel", "powerpoint": "powerpnt", "outlook": "outlook",
    "teams": "teams", "slack": "slack", "discord": "discord",
    "spotify": "spotify", "vlc": "vlc", "paint": "mspaint", "snipping tool": "snippingtool",
    "obs": "obs64", "steam": "steam", "epic games": "EpicGamesLauncher",
    "settings": "ms-settings:", "control panel": "control",
    "camera": "microsoft.windows.camera:", "photos": "ms-photos:",
}

# Start-Menu locations to scan for .lnk shortcuts
_START_MENU_DIRS = [
    os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
    os.path.join(os.environ.get("PROGRAMDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
]


class AppCtrl:
    """Open and close any application by name."""

    def __init__(self):
        self._shortcut_cache: Optional[dict] = None

    # ── opening ─────────────────────────────────────────────────────────

    def open_app(self, name: str) -> Dict[str, Any]:
        if not name or not name.strip():
            return {"success": False, "message": "Specify an application name."}
        name = name.strip()
        key = name.lower()

        # 1. alias map
        target = APP_MAP.get(key, name)

        # 2. direct launch (PATH exe / registered app / protocol like ms-settings:)
        if self._try_startfile(target):
            return {"success": True, "message": f"Opening {name}."}

        # 3. where.exe on PATH (handles things on PATH without .exe)
        resolved = self._which(target)
        if resolved and self._try_startfile(resolved):
            return {"success": True, "message": f"Opening {name}."}

        # 4. Start-Menu shortcut fuzzy search (finds installed games/apps)
        lnk = self._find_shortcut(name)
        if lnk and self._try_startfile(lnk):
            return {"success": True, "message": f"Opening {name}."}

        return {"success": False, "message": f"Couldn't find '{name}'. Is it installed? Try the exact name."}

    def _try_startfile(self, target: str) -> bool:
        try:
            os.startfile(target)  # type: ignore[attr-defined]
            logger.info(f"Launched: {target}")
            return True
        except Exception:
            return False

    @staticmethod
    def _which(name: str) -> Optional[str]:
        # strip .exe for shutil.which, it adds it back
        found = shutil.which(name) or shutil.which(name + ".exe")
        return found

    def _find_shortcut(self, name: str) -> Optional[str]:
        """Fuzzy-match a Start-Menu .lnk by name (case-insensitive substring)."""
        if self._shortcut_cache is None:
            self._shortcut_cache = {}
            for d in _START_MENU_DIRS:
                if not d or not os.path.isdir(d):
                    continue
                for lnk in glob.glob(os.path.join(d, "**", "*.lnk"), recursive=True):
                    stem = Path(lnk).stem.lower()
                    self._shortcut_cache.setdefault(stem, lnk)
        q = name.lower()
        # exact stem first, then substring
        if q in self._shortcut_cache:
            return self._shortcut_cache[q]
        for stem, lnk in self._shortcut_cache.items():
            if q in stem or stem in q:
                return lnk
        return None

    # ── closing ─────────────────────────────────────────────────────────

    def close_app(self, name: str) -> Dict[str, Any]:
        if not name or not name.strip():
            return {"success": False, "message": "Specify an application name."}
        if not PSUTIL_AVAILABLE:
            return {"success": False, "message": "psutil not available."}

        exe = APP_MAP.get(name.lower().strip(), name.strip())
        exe_lower = exe.lower().replace(".exe", "")
        query = name.lower().strip()
        killed = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                proc_name = proc.info["name"].lower().replace(".exe", "")
                if proc_name == exe_lower or query in proc_name:
                    proc.terminate()
                    killed.append(proc.info["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed:
            return {"success": True, "message": f"Closed: {', '.join(sorted(set(killed)))}."}
        return {"success": False, "message": f"'{name}' is not running."}
