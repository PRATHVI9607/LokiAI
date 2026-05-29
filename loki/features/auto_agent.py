"""
AutoAgent — autonomous multi-step task executor (harness agent).

The user describes a goal; AutoAgent asks the LLM to plan it as a sequence of
Loki intents, then executes each intent through the action router, streaming
progress back via the server's add_loki_message callback.

Usage examples (voice or text):
  "Agent: rename all .jpeg files in Downloads to .jpg"
  "Agent: check system health, backup my notes, then give me a briefing"
  "Cancel agent" — abort any running task
"""

import logging
import threading
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain
    from loki.core.action_router import ActionRouter

logger = logging.getLogger(__name__)

_MAX_STEPS = 10
_PLAN_PROMPT = """You are a task planner for Loki AI assistant.
The user wants: {goal}

Break this into at most {max_steps} sequential Loki intents.
Return a JSON array of intent objects — each with "intent" (string) and "params" (object).
Only use intents from this list: {intent_list}

Rules:
- Use only safe, reversible intents where possible.
- Never use shell, file_delete, folder_delete, or process_kill unless the user explicitly asked.
- Return [] if the goal cannot be safely automated.

Return ONLY valid JSON array, no explanation:
[{{"intent": "...", "params": {{...}}}}, ...]"""


class AutoAgent:
    """Runs multi-step plans autonomously using Loki's action router."""

    SAFE_INTENTS = {
        "file_search", "file_create", "file_read", "file_move",
        "folder_create", "system_monitor", "process_list", "volume_get", "brightness_get",
        "task_add", "task_list", "task_complete", "task_prioritize_ai",
        "web_summarize", "pdf_chat", "fact_check", "daily_briefing",
        "news_headlines", "news_briefing", "git_status", "commit_message",
        "code_analyze", "security_scan", "backup_file", "backup_directory",
        "backup_list", "declutter_suggest", "clipboard_show", "clipboard_sync_url",
        "kg_query", "kg_stats", "history_recent", "history_stats",
        "calendar_list", "calendar_conflicts", "expense_list", "expense_summary",
        "window_layouts", "process_analyze", "process_triage",
        "currency_convert", "unit_convert", "media_info", "update_check",
    }

    def __init__(
        self,
        brain: Optional["LokiBrain"] = None,
        router: Optional["ActionRouter"] = None,
        on_progress: Optional[Callable[[str], None]] = None,
    ):
        self._brain = brain
        self._router = router
        self._on_progress = on_progress or (lambda msg: None)
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._abort = threading.Event()

    def run(self, goal: str) -> Dict[str, Any]:
        """Start an agentic task. Returns immediately; progress via on_progress callback."""
        if self._running:
            return {"success": False, "message": "Agent is already running a task. Say 'cancel agent' to stop."}
        if not self._brain or not self._router:
            return {"success": False, "message": "Agent requires LLM and router — not fully initialized."}

        self._abort.clear()
        self._thread = threading.Thread(
            target=self._execute_task,
            args=(goal,),
            daemon=True,
            name="loki-auto-agent",
        )
        self._thread.start()
        return {"success": True, "message": f"Agent started. Working on: {goal}"}

    def cancel(self) -> Dict[str, Any]:
        """Abort any running task."""
        if not self._running:
            return {"success": False, "message": "No agent task is running."}
        self._abort.set()
        return {"success": True, "message": "Agent task cancelled."}

    def is_running(self) -> bool:
        return self._running

    def _execute_task(self, goal: str) -> None:
        self._running = True
        self._on_progress(f"Agent planning: {goal}")

        try:
            plan = self._plan(goal)
        except Exception as e:
            self._on_progress(f"Agent planning failed: {e}")
            self._running = False
            return

        if not plan:
            self._on_progress("Agent: could not build a safe plan for that goal.")
            self._running = False
            return

        self._on_progress(f"Agent: {len(plan)} step plan ready. Executing...")

        completed = 0
        for i, step in enumerate(plan[:_MAX_STEPS], 1):
            if self._abort.is_set():
                self._on_progress(f"Agent aborted after {completed} step(s).")
                self._running = False
                return

            intent_name = step.get("intent", "")
            if intent_name not in self.SAFE_INTENTS:
                self._on_progress(f"Agent: step {i} skipped — '{intent_name}' requires manual confirmation.")
                continue

            self._on_progress(f"Agent step {i}/{len(plan)}: {intent_name}...")

            try:
                result = self._router.route_intent(step)
                msg = result.get("message", "")
                status = "✓" if result.get("success") else "✗"
                self._on_progress(f"Agent {status} {intent_name}: {msg[:200]}")
                completed += 1

                if not result.get("success"):
                    self._on_progress(f"Agent stopping — step {i} failed.")
                    break
            except Exception as e:
                logger.error("AutoAgent step error (%s): %s", intent_name, e, exc_info=True)
                self._on_progress(f"Agent error on step {i}: {e}")
                break

        self._on_progress(f"Agent done. Completed {completed}/{len(plan)} steps.")
        self._running = False

    def _plan(self, goal: str) -> List[Dict[str, Any]]:
        """Ask the LLM to produce a JSON intent plan for the goal."""
        import json
        intent_list = ", ".join(sorted(self.SAFE_INTENTS))
        prompt = _PLAN_PROMPT.format(goal=goal, max_steps=_MAX_STEPS, intent_list=intent_list)
        raw = "".join(self._brain.ask(prompt)).strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        plan = json.loads(raw)
        if not isinstance(plan, list):
            return []
        return plan
