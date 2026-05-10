"""
Audit log — append-only JSONL record of all intent executions.
Tier 1: read-only ops (not logged).
Tier 2: state changes (logged).
Tier 3: destructive/external ops (logged with full payload).
"""

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

TIER_LABELS = {1: "safe", 2: "moderate", 3: "restricted"}

INTENT_TIERS = {
    # Tier 1 — read-only
    "chat": 1, "volume_get": 1, "brightness_get": 1, "system_monitor": 1,
    "process_list": 1, "task_list": 1, "clipboard_show": 1, "git_status": 1,
    "file_search": 1, "vault_retrieve": 1,
    # Tier 2 — state changes
    "file_create": 2, "file_move": 2, "folder_create": 2, "file_organize": 2,
    "volume_set": 2, "brightness_set": 2, "wifi_toggle": 2, "bluetooth_toggle": 2,
    "app_open": 2, "app_close": 2, "browser_open": 2, "browser_search": 2,
    "task_add": 2, "task_complete": 2, "task_delete": 2, "clipboard_clear": 2,
    "vault_store": 2, "focus_mode_enable": 2, "focus_mode_disable": 2,
    "undo": 2, "commit_message": 2, "readme_generate": 2, "regex_generate": 2,
    "sql_build": 2, "git_commit": 2, "code_analyze": 2, "code_convert": 2,
    # Tier 3 — destructive / external
    "file_delete": 3, "folder_delete": 3, "process_kill": 3, "shell": 3,
    "security_scan": 3, "web_summarize": 3, "pdf_chat": 3,
}

MAX_ENTRIES = 1000


class AuditLog:
    """Append-only audit log stored as JSONL. Thread-safe."""

    def __init__(self, memory_dir: Path):
        self._path = Path(memory_dir) / "audit.jsonl"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log(
        self,
        intent: str,
        params: Optional[Dict[str, Any]] = None,
        success: bool = True,
        result_summary: str = "",
    ) -> None:
        tier = INTENT_TIERS.get(intent, 2)
        if tier == 1:
            return

        entry = {
            "ts": datetime.now().isoformat(),
            "intent": intent,
            "tier": tier,
            "tier_label": TIER_LABELS[tier],
            "params": self._sanitize(params or {}),
            "success": success,
            "result": result_summary[:200] if result_summary else "",
        }
        try:
            with self._lock:
                with open(self._path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                self._rotate_if_needed()
        except Exception as e:
            logger.error(f"Audit log write failed: {e}")

    def _sanitize(self, params: Any, _visited: Optional[set] = None) -> Any:
        """Recursively redact sensitive keys from params."""
        if _visited is None:
            _visited = set()
        obj_id = id(params)
        if obj_id in _visited:
            return "<circular>"
        sensitive = {"value", "password", "key", "secret", "token"}
        if isinstance(params, dict):
            _visited.add(obj_id)
            return {
                k: "***" if k.lower() in sensitive else self._sanitize(v, _visited)
                for k, v in params.items()
            }
        if isinstance(params, list):
            _visited.add(obj_id)
            return [self._sanitize(item, _visited) for item in params]
        return params

    def _rotate_if_needed(self) -> None:
        """Trim log to MAX_ENTRIES. Must be called while self._lock is held."""
        try:
            lines = self._path.read_text(encoding="utf-8").splitlines()
            if len(lines) > MAX_ENTRIES:
                keep = lines[-MAX_ENTRIES:]
                self._path.write_text("\n".join(keep) + "\n", encoding="utf-8")
        except Exception as e:
            logger.error(f"Audit log rotation failed: {e}")

    def get_recent(self, n: int = 20, tier_min: int = 2) -> List[Dict]:
        if not self._path.exists():
            return []
        try:
            with self._lock:
                lines = self._path.read_text(encoding="utf-8").splitlines()
            entries = []
            for line in reversed(lines):
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    if e.get("tier", 1) >= tier_min:
                        entries.append(e)
                    if len(entries) >= n:
                        break
                except Exception:
                    continue
            return entries
        except Exception as e:
            logger.error(f"Audit log read failed: {e}")
            return []
