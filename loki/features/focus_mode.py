"""
Focus mode — block distracting websites by modifying hosts file.
Requires admin privileges on Windows.
"""

import logging
import re
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

HOSTS_MARKER_START = "# === LOKI FOCUS MODE START ==="
HOSTS_MARKER_END = "# === LOKI FOCUS MODE END ==="
REDIRECT_IP = "127.0.0.1"


class FocusMode:
    """Block distracting sites during focus sessions."""

    def __init__(self, config: dict):
        self._hosts_path = Path(config.get("hosts_file", r"C:\Windows\System32\drivers\etc\hosts"))
        self._default_sites: List[str] = config.get("block_sites", [
            "youtube.com", "reddit.com", "twitter.com", "facebook.com",
            "instagram.com", "tiktok.com", "twitch.tv", "netflix.com",
        ])
        self._active = False
        self._timer: Optional[threading.Timer] = None

    def enable(self, duration_minutes: Optional[int] = None) -> Dict[str, Any]:
        if self._active:
            return {"success": False, "message": "Focus mode already active."}

        result = self._block_sites(self._default_sites)
        if not result["success"]:
            return result

        self._active = True

        if duration_minutes and duration_minutes > 0:
            self._timer = threading.Timer(duration_minutes * 60, self._auto_disable)
            self._timer.daemon = True
            self._timer.start()
            return {"success": True, "message": f"Focus mode enabled for {duration_minutes} minutes. {len(self._default_sites)} sites blocked."}

        return {"success": True, "message": f"Focus mode enabled. {len(self._default_sites)} sites blocked. Say 'disable focus mode' to stop."}

    def disable(self) -> Dict[str, Any]:
        if not self._active:
            return {"success": False, "message": "Focus mode is not active."}

        if self._timer:
            self._timer.cancel()
            self._timer = None

        result = self._unblock_sites()
        if result["success"]:
            self._active = False
        return result

    def _auto_disable(self) -> None:
        self._unblock_sites()
        self._active = False
        logger.info("Focus mode auto-disabled")

    def _block_sites(self, sites: List[str]) -> Dict[str, Any]:
        try:
            hosts_content = self._hosts_path.read_text(encoding="utf-8")

            if HOSTS_MARKER_START in hosts_content:
                return {"success": False, "message": "Focus mode entries already in hosts file."}

            block_lines = [HOSTS_MARKER_START]
            for site in sites:
                block_lines.append(f"{REDIRECT_IP} {site}")
                block_lines.append(f"{REDIRECT_IP} www.{site}")
            block_lines.append(HOSTS_MARKER_END)

            new_content = hosts_content + "\n" + "\n".join(block_lines) + "\n"
            self._hosts_path.write_text(new_content, encoding="utf-8")
            self._flush_dns()
            return {"success": True}

        except PermissionError:
            return {"success": False, "message": "Cannot modify hosts file. Run Loki as Administrator for focus mode."}
        except Exception as e:
            return {"success": False, "message": f"Focus mode failed: {e}"}

    def _unblock_sites(self) -> Dict[str, Any]:
        try:
            content = self._hosts_path.read_text(encoding="utf-8")
            start_idx = content.find(HOSTS_MARKER_START)
            end_idx = content.find(HOSTS_MARKER_END)

            if start_idx == -1:
                return {"success": True, "message": "No focus mode entries found. Focus mode disabled."}

            if end_idx == -1:
                return {"success": False, "message": "Corrupted hosts file markers. Edit manually."}

            new_content = content[:start_idx] + content[end_idx + len(HOSTS_MARKER_END):]
            new_content = re.sub(r'\n{3,}', '\n\n', new_content)
            self._hosts_path.write_text(new_content, encoding="utf-8")
            self._flush_dns()
            return {"success": True, "message": "Focus mode disabled. All sites unblocked."}

        except PermissionError:
            return {"success": False, "message": "Cannot modify hosts file. Run as Administrator."}
        except Exception as e:
            return {"success": False, "message": f"Failed to disable focus mode: {e}"}

    def _flush_dns(self) -> None:
        try:
            import subprocess
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, timeout=5)
        except Exception:
            pass

    @property
    def is_active(self) -> bool:
        return self._active
