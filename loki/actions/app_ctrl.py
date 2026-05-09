"""
App control — open and close applications.
"""

import subprocess
import logging
import psutil
from typing import Dict, Any

logger = logging.getLogger(__name__)

APP_MAP = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "notepad": "notepad",
    "notepad++": "notepad++",
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "explorer": "explorer",
    "file explorer": "explorer",
    "calculator": "calc",
    "calc": "calc",
    "terminal": "wt",
    "windows terminal": "wt",
    "cmd": "cmd",
    "powershell": "powershell",
    "task manager": "taskmgr",
    "taskmgr": "taskmgr",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "outlook": "outlook",
    "teams": "teams",
    "slack": "slack",
    "discord": "discord",
    "spotify": "spotify",
    "vlc": "vlc",
    "paint": "mspaint",
    "obs": "obs64",
    "steam": "steam",
    "settings": "ms-settings:",
}


class AppCtrl:
    """Open and close applications by name."""

    def open_app(self, name: str) -> Dict[str, Any]:
        if not name:
            return {"success": False, "message": "Specify an application name."}

        exe = APP_MAP.get(name.lower().strip(), name.strip())
        try:
            if exe.startswith("ms-"):
                subprocess.Popen(["start", exe], shell=True)
            else:
                subprocess.Popen([exe], shell=True)
            logger.info(f"Opened: {exe}")
            return {"success": True, "message": f"Opening {name}."}
        except FileNotFoundError:
            return {"success": False, "message": f"Cannot find '{name}'. Is it installed?"}
        except Exception as e:
            logger.error(f"app_open error: {e}")
            return {"success": False, "message": f"Failed to open {name}: {e}"}

    def close_app(self, name: str) -> Dict[str, Any]:
        if not name:
            return {"success": False, "message": "Specify an application name."}

        exe = APP_MAP.get(name.lower().strip(), name.strip())
        exe_lower = exe.lower().replace(".exe", "")
        killed = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                proc_name = proc.info["name"].lower().replace(".exe", "")
                if proc_name == exe_lower or name.lower() in proc_name:
                    proc.terminate()
                    killed.append(proc.info["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed:
            return {"success": True, "message": f"Closed: {', '.join(set(killed))}."}
        return {"success": False, "message": f"'{name}' is not running."}
