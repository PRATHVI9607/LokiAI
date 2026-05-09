"""
Shell executor — allowlisted command execution with injection prevention.
"""

import re
import logging
import subprocess
import shlex
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Commands blocked regardless of allowlist
BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"format\s+[a-z]:",
    r"del\s+/[sf]",
    r"rd\s+/s\s+/q\s+[a-z]:\\",
    r":()\{.*\};:",    # fork bomb
    r"dd\s+if=",
    r">\s*/dev/(s?d[a-z]|null)",
    r"mkfs\.",
    r"shutdown",
    r"reboot",
    r"halt",
    r"poweroff",
]


class ShellExec:
    """Execute allowlisted shell commands safely."""

    def __init__(self, config: dict, undo_stack):
        self._undo = undo_stack
        self._timeout = config.get("shell_timeout", 30)
        self._allowlist: List[str] = []

        allowlist_path = Path(__file__).parent.parent / "data" / "command_allowlist.txt"
        if allowlist_path.exists():
            with open(allowlist_path, "r", encoding="utf-8") as f:
                self._allowlist = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith("#")
                ]

    def execute(self, command: str) -> Dict[str, Any]:
        if not command or not command.strip():
            return {"success": False, "message": "No command specified."}

        command = command.strip()

        # Block dangerous patterns first
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                logger.warning(f"Blocked dangerous command: {command[:80]}")
                return {"success": False, "message": "That command is not permitted. Nice try."}

        # Check allowlist
        if not self._is_allowed(command):
            logger.warning(f"Command not in allowlist: {command[:80]}")
            return {"success": False, "message": f"Command not in allowlist. Add it to data/command_allowlist.txt to enable."}

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                cwd=str(Path.home()),
            )
            output = (result.stdout + result.stderr).strip()
            success = result.returncode == 0

            logger.info(f"Executed: {command[:60]} -> rc={result.returncode}")
            return {
                "success": success,
                "message": output[:1000] if output else ("Done." if success else "Command returned non-zero exit code."),
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {"success": False, "message": f"Command timed out after {self._timeout}s."}
        except Exception as e:
            logger.error(f"Shell exec error: {e}")
            return {"success": False, "message": f"Execution failed: {e}"}

    def _is_allowed(self, command: str) -> bool:
        cmd_lower = command.lower().strip()
        for allowed in self._allowlist:
            allowed_lower = allowed.lower()
            # Prefix match: "git" allows "git status", "git log", etc.
            if cmd_lower == allowed_lower or cmd_lower.startswith(allowed_lower + " "):
                return True
        return False
