"""
Task manager — add, list, complete, delete tasks with priority scoring.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from loki.core.memory import MemoryManager

logger = logging.getLogger(__name__)

PRIORITY_WEIGHTS = {"critical": 4, "high": 3, "medium": 2, "low": 1}
_MAX_FUTURE_DAYS = 36500  # ~100 years — anything beyond this is almost certainly a typo


def _validate_due(due: str) -> Optional[str]:
    """Return an error message if `due` is unparseable / past / absurd, else None."""
    try:
        due_dt = datetime.fromisoformat(due)
    except ValueError:
        return f"I couldn't read the due date '{due}' — use a format like 2026-06-01 or 2026-06-01T15:00."
    now = datetime.now()
    # tolerate same-day past times (e.g. "today"); reject clearly-past dates
    if due_dt.date() < now.date():
        return "That due date is in the past."
    if due_dt > now + timedelta(days=_MAX_FUTURE_DAYS):
        return "That due date is unreasonably far in the future."
    return None


class TaskManager:
    """Manage tasks using persistent MemoryManager storage."""

    def __init__(self, memory: MemoryManager):
        self._memory = memory

    def add(self, title: str, priority: str = "medium", due: Optional[str] = None,
            recurrence: Optional[str] = None) -> Dict[str, Any]:
        if not title:
            return {"success": False, "message": "Task title required."}

        priority = priority.lower() if priority.lower() in PRIORITY_WEIGHTS else "medium"

        if recurrence is not None and recurrence not in ("daily", "weekly", "monthly"):
            return {"success": False, "message": "Recurrence must be daily, weekly, or monthly."}

        if due:
            err = _validate_due(due)
            if err:
                return {"success": False, "message": err}

        task = self._memory.add_task(title, priority, due, recurrence)

        msg = f"Task #{task['id']} added: '{title}' [{priority}]"
        if due:
            msg += f" — due {due}"
        if recurrence:
            msg += f" (repeats {recurrence})"
        return {"success": True, "message": msg, "data": task}

    def list_tasks(self, filter_type: Optional[str] = None) -> Dict[str, Any]:
        show_done = filter_type == "all"
        tasks = self._memory.list_tasks(filter_done=show_done)

        if not tasks:
            return {"success": True, "message": "No tasks. A clean slate — how suspicious.", "data": []}

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

    def ai_prioritize(self, brain=None) -> Dict[str, Any]:
        """Re-rank tasks using LLM scoring based on urgency, impact, and effort."""
        if not brain:
            return {"success": False, "message": "LLM required for AI prioritization."}

        tasks = self._memory.list_tasks(filter_done=False)
        if not tasks:
            return {"success": True, "message": "No pending tasks to prioritize.", "data": []}

        task_lines = "\n".join(
            f"  [{t['id']}] {t['title']} (priority: {t.get('priority','medium')}, due: {t.get('due','unset')})"
            for t in tasks
        )
        prompt = (
            f"Rank these tasks by urgency and importance. "
            f"Consider deadlines, difficulty, and dependencies. "
            f"Return ONLY a JSON list of task IDs in priority order, e.g. [3, 1, 2].\n\n"
            f"Tasks:\n{task_lines}"
        )
        import json as _json, re as _re
        raw = "".join(brain.ask(prompt))
        try:
            match = _re.search(r"\[[\d,\s]+\]", raw)
            if match:
                ranked_ids = _json.loads(match.group())
                id_to_task = {t["id"]: t for t in tasks}
                ranked = [id_to_task[tid] for tid in ranked_ids if tid in id_to_task]
                # Append any tasks not in the LLM's output
                ranked_set = {t["id"] for t in ranked}
                ranked += [t for t in tasks if t["id"] not in ranked_set]

                lines = [f"AI-prioritized task order:"]
                for i, t in enumerate(ranked, 1):
                    due = f" [due: {t['due']}]" if t.get("due") else ""
                    lines.append(f"  {i}. [{t['id']}] {t['title']}{due}")
                return {"success": True, "message": "\n".join(lines), "data": {"ranked": ranked}}
        except Exception:
            pass

        return {"success": False, "message": "Could not parse LLM ranking response."}
