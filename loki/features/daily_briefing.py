"""
DailyBriefing — morning brief combining tasks, system health, date/time, and news headlines.
"""

import logging
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


class DailyBriefing:
    def __init__(self, brain: Optional["LokiBrain"] = None,
                 task_manager=None, system_monitor=None, news_aggregator=None):
        self._brain = brain
        self._tasks = task_manager
        self._monitor = system_monitor
        self._news = news_aggregator

    def generate(self) -> dict:
        """Generate a full daily briefing covering date, tasks, system, and news."""
        now = datetime.now()
        day_str = now.strftime("%A, %B %d %Y")
        time_str = now.strftime("%I:%M %p")

        sections = [f"Good morning. Today is {day_str}, {time_str}."]

        # Tasks
        if self._tasks:
            try:
                task_result = self._tasks.list_tasks()
                tasks = task_result.get("data", {}).get("tasks", []) if task_result.get("success") else []
                pending = [t for t in tasks if not t.get("completed")]
                if pending:
                    high = [t for t in pending if t.get("priority") in ("critical", "high")]
                    sections.append(
                        f"You have {len(pending)} pending task{'s' if len(pending) != 1 else ''}."
                        + (f" {len(high)} are high priority." if high else "")
                    )
                    for t in pending[:3]:
                        due = f" (due {t['due']})" if t.get("due") else ""
                        sections.append(f"  • [{t['priority'].upper()}] {t['title']}{due}")
                    if len(pending) > 3:
                        sections.append(f"  … and {len(pending) - 3} more.")
                else:
                    sections.append("No pending tasks. Clean slate.")
            except Exception as e:
                logger.warning(f"DailyBriefing tasks error: {e}")

        # System health
        if self._monitor:
            try:
                stats = self._monitor.get_stats()
                if stats.get("success"):
                    d = stats.get("data", {})
                    cpu = d.get("cpu_percent", 0)
                    ram = d.get("ram", {}).get("percent", 0)
                    sections.append(f"System: CPU at {cpu:.0f}%, RAM at {ram:.0f}%.")
                    if cpu > 85:
                        sections.append("Warning: CPU is running hot.")
                    if ram > 85:
                        sections.append("Warning: RAM usage is high.")
            except Exception as e:
                logger.warning(f"DailyBriefing monitor error: {e}")

        # News headlines
        if self._news:
            try:
                news_result = self._news.get_headlines()
                headlines = news_result.get("data", {}).get("headlines", []) if news_result.get("success") else []
                if headlines:
                    sections.append("Top headlines:")
                    for h in headlines[:3]:
                        sections.append(f"  • {h}")
            except Exception as e:
                logger.warning(f"DailyBriefing news error: {e}")

        briefing = "\n".join(sections)
        return {"success": True, "message": briefing, "data": {"briefing": briefing, "date": day_str, "time": time_str}}
