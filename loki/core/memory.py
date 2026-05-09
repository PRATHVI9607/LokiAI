"""
Memory manager — persistent conversation, profile, tasks storage.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class MemoryManager:
    """Centralized persistent memory for Loki."""

    def __init__(self, memory_dir: Path):
        self._dir = Path(memory_dir)
        self._dir.mkdir(parents=True, exist_ok=True)

        self._profile_file = self._dir / "user_profile.json"
        self._tasks_file = self._dir / "tasks.json"

        self._profile: Dict[str, Any] = self._load_json(self._profile_file, {
            "name": "User",
            "created": datetime.now().isoformat(),
            "preferences": {},
        })
        self._tasks: List[Dict[str, Any]] = self._load_json(self._tasks_file, [])

    def _load_json(self, path: Path, default: Any) -> Any:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load {path.name}: {e}")
        return default

    def _save_json(self, path: Path, data: Any) -> None:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save {path.name}: {e}")

    # Profile
    def get_user_name(self) -> str:
        return self._profile.get("name", "User")

    def set_user_name(self, name: str) -> None:
        self._profile["name"] = name
        self._save_json(self._profile_file, self._profile)

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self._profile.get("preferences", {}).get(key, default)

    def set_preference(self, key: str, value: Any) -> None:
        self._profile.setdefault("preferences", {})[key] = value
        self._save_json(self._profile_file, self._profile)

    # Tasks
    def add_task(self, title: str, priority: str = "medium", due: Optional[str] = None) -> Dict:
        task = {
            "id": self._next_task_id(),
            "title": title,
            "priority": priority,
            "due": due,
            "completed": False,
            "created": datetime.now().isoformat(),
        }
        self._tasks.append(task)
        self._save_json(self._tasks_file, self._tasks)
        return task

    def list_tasks(self, filter_done: bool = False) -> List[Dict]:
        if filter_done:
            return self._tasks
        return [t for t in self._tasks if not t["completed"]]

    def complete_task(self, task_id: int) -> bool:
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self._save_json(self._tasks_file, self._tasks)
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t["id"] != task_id]
        if len(self._tasks) < before:
            self._save_json(self._tasks_file, self._tasks)
            return True
        return False

    def _next_task_id(self) -> int:
        if not self._tasks:
            return 1
        return max(t["id"] for t in self._tasks) + 1
