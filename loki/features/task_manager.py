"""
Task manager — add, list, complete, delete tasks with priority scoring.
"""

import logging
from typing import Dict, Any, Optional
from loki.core.memory import MemoryManager

logger = logging.getLogger(__name__)

PRIORITY_WEIGHTS = {"critical": 4, "high": 3, "medium": 2, "low": 1}


class TaskManager:
    """Manage tasks using persistent MemoryManager storage."""

    def __init__(self, memory: MemoryManager):
        self._memory = memory

    def add(self, title: str, priority: str = "medium", due: Optional[str] = None) -> Dict[str, Any]:
        if not title:
            return {"success": False, "message": "Task title required."}

        priority = priority.lower() if priority.lower() in PRIORITY_WEIGHTS else "medium"
        task = self._memory.add_task(title, priority, due)

        msg = f"Task #{task['id']} added: '{title}' [{priority}]"
        if due:
            msg += f" — due {due}"
        return {"success": True, "message": msg, "data": task}

    def list_tasks(self, filter_type: Optional[str] = None) -> Dict[str, Any]:
        show_done = filter_type == "all"
        tasks = self._memory.list_tasks(filter_done=show_done)

        if not tasks:
            return {"success": True, "message": "No tasks. A clean slate — how suspicious."}

        # Sort by priority weight
        tasks.sort(key=lambda t: PRIORITY_WEIGHTS.get(t.get("priority", "medium"), 2), reverse=True)

        lines = [f"Tasks ({len(tasks)}):"]
        for t in tasks:
            status = "✓" if t["completed"] else "○"
            due_str = f" [due: {t['due']}]" if t.get("due") else ""
            lines.append(f"  [{t['id']}] {status} [{t['priority'].upper()}] {t['title']}{due_str}")

        return {"success": True, "message": "\n".join(lines), "data": tasks}

    def complete(self, task_id: int) -> Dict[str, Any]:
        if self._memory.complete_task(task_id):
            return {"success": True, "message": f"Task #{task_id} marked complete."}
        return {"success": False, "message": f"Task #{task_id} not found."}

    def delete(self, task_id: int) -> Dict[str, Any]:
        if self._memory.delete_task(task_id):
            return {"success": True, "message": f"Task #{task_id} deleted."}
        return {"success": False, "message": f"Task #{task_id} not found."}
