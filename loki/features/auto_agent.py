"""
AutoAgent — autonomous multi-step task executor (the "use the computer like a
person" engine).

The user describes a goal; AutoAgent plans it as a sequence of Loki intents
(opening apps, typing, hotkeys, clicking on-screen text, file ops, web, system
queries…) and executes them through the action router with sensible delays
between steps, streaming progress back to the chat.

Examples:
  "open notepad, type my address, and save it as address.txt"
  "open chrome, go to youtube, and search for lofi music"
  "check my system health then back up my notes folder"
  "cancel agent" — abort any running task
"""

import json
import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain
    from loki.core.action_router import ActionRouter

logger = logging.getLogger(__name__)

_MAX_STEPS = 12

# Delay AFTER a step completes, before the next — gives apps/windows time to be
# ready (you can't type into Notepad the instant you launch it).
_STEP_DELAY: Dict[str, float] = {
    "app_open": 2.0, "browser_open": 2.2, "browser_search": 2.2,
    "computer_action": 0.7, "computer_press": 0.4, "computer_click": 0.4,
    "computer_click_text": 0.6, "computer_type": 0.3,
}
_DEFAULT_DELAY = 0.3

_PLAN_PROMPT = """You are the task planner for Loki, an AI that directly controls a Windows PC.
Break the user's request into a sequence of concrete steps it can execute.

The user wants: {goal}

Return ONLY a JSON array (no prose, no markdown) of step objects, each:
{{"intent": "<name>", "params": {{...}}}}

Available intents:
- app_open {{name}}            open an application
- app_close {{name}}           close an application
- browser_open {{url}}         open a website
- browser_search {{query, engine?}}   web/youtube search (engine: "youtube" or "google")
- computer_type {{text}}       type text into the focused window
- computer_press {{key}}       a key or hotkey ("enter", "ctrl+s", "alt+tab")
- computer_click_text {{target}}   find on-screen text and click it
- computer_action {{action}}   minimize, maximize, show desktop, save, copy, paste, select all, new tab, screenshot
- computer_scroll {{amount}}   negative=down, positive=up
- screen_read {{}}             read what's on screen
- file_create {{path, content}}   create a file
- system_monitor {{}}, process_list {{}}, volume_get {{}}, brightness_get {{}}
- task_add {{title}}, news_briefing {{}}, daily_briefing {{}}, backup_directory {{path}}

EXAMPLE — "open notepad, type my address and save it as address.txt":
[{{"intent":"app_open","params":{{"name":"notepad"}}}},
 {{"intent":"computer_type","params":{{"text":"221B Baker Street, London"}}}},
 {{"intent":"computer_press","params":{{"key":"ctrl+s"}}}},
 {{"intent":"computer_type","params":{{"text":"address.txt"}}}},
 {{"intent":"computer_press","params":{{"key":"enter"}}}}]

EXAMPLE — "open youtube and search for lofi music":
[{{"intent":"browser_search","params":{{"query":"lofi music","engine":"youtube"}}}}]

Keep it to {max_steps} steps max. Return [] if it can't be done. JSON array only:"""


class AutoAgent:
    """Plans and runs multi-step desktop automations via the action router."""

    # Intents the agent may run without per-step confirmation
    SAFE_INTENTS = {
        # apps + web
        "app_open", "app_close", "browser_open", "browser_search",
        # computer control (act like a person)
        "computer_type", "computer_press", "computer_click", "computer_click_text",
        "computer_action", "computer_scroll", "screen_read",
        # files / info / productivity (read-mostly)
        "file_search", "file_create", "file_read", "file_move", "folder_create",
        "system_monitor", "process_list", "volume_get", "volume_set",
        "brightness_get", "brightness_set",
        "task_add", "task_list", "task_complete", "task_prioritize_ai",
        "web_summarize", "pdf_chat", "fact_check", "daily_briefing",
        "news_headlines", "news_briefing", "git_status", "commit_message",
        "code_analyze", "security_scan", "backup_file", "backup_directory",
        "backup_list", "declutter_suggest", "clipboard_show", "clipboard_sync_url",
        "kg_query", "kg_stats", "history_recent", "history_stats",
        "calendar_list", "calendar_conflicts", "expense_list", "expense_summary",
        "window_layouts", "window_snap", "process_analyze", "process_triage",
        "currency_convert", "unit_convert", "media_info", "update_check",
        "ui_theme_time", "ui_theme_mood",
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
        if self._running:
            return {"success": False, "message": "Agent is already running a task. Say 'cancel agent' to stop."}
        if not self._brain or not self._router:
            return {"success": False, "message": "Agent requires LLM and router — not fully initialized."}
        self._abort.clear()
        self._thread = threading.Thread(target=self._execute_task, args=(goal,), daemon=True, name="loki-auto-agent")
        self._thread.start()
        return {"success": True, "message": f"On it — working on: {goal}"}

    def cancel(self) -> Dict[str, Any]:
        if not self._running:
            return {"success": False, "message": "No agent task is running."}
        self._abort.set()
        return {"success": True, "message": "Agent task cancelled."}

    def is_running(self) -> bool:
        return self._running

    def _execute_task(self, goal: str) -> None:
        self._running = True
        self._on_progress(f"🧩 Planning: {goal}")
        try:
            plan = self._plan(goal)
        except Exception as e:
            self._on_progress(f"Planning failed: {e}")
            self._running = False
            return

        if not plan:
            self._on_progress("I couldn't break that into steps I can run. Try rephrasing.")
            self._running = False
            return

        self._on_progress(f"📋 {len(plan)}-step plan ready. Executing…")
        completed = 0
        for i, step in enumerate(plan[:_MAX_STEPS], 1):
            if self._abort.is_set():
                self._on_progress(f"⏹ Aborted after {completed} step(s).")
                self._running = False
                return

            intent_name = step.get("intent", "")
            if intent_name not in self.SAFE_INTENTS:
                self._on_progress(f"⊘ Step {i} skipped — '{intent_name}' needs manual confirmation.")
                continue

            self._on_progress(f"▸ Step {i}/{len(plan)}: {intent_name}…")
            try:
                result = self._router.route_intent(step)
                ok = result.get("success")
                self._on_progress(f"{'✓' if ok else '✗'} {result.get('message', '')[:180]}")
                completed += 1
                if not ok:
                    self._on_progress(f"Stopped — step {i} failed.")
                    break
            except Exception as e:
                logger.error("AutoAgent step error (%s): %s", intent_name, e, exc_info=True)
                self._on_progress(f"Error on step {i}: {e}")
                break

            # give the UI/app time to settle before the next step
            time.sleep(_STEP_DELAY.get(intent_name, _DEFAULT_DELAY))

        self._on_progress(f"✅ Done — {completed}/{len(plan)} steps.")
        self._running = False

    def _plan(self, goal: str) -> List[Dict[str, Any]]:
        """Ask the LLM for a JSON step plan. Uses _call_llm directly (not the
        conversational ask pipeline) so there's no fast-path/RAG interference."""
        prompt = _PLAN_PROMPT.format(goal=goal, max_steps=_MAX_STEPS)
        messages = [
            {"role": "system", "content": "You output only valid JSON arrays. No prose."},
            {"role": "user", "content": prompt},
        ]
        raw = self._brain._call_llm(messages, max_tokens=700).strip()

        # strip code fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.lower().startswith("json"):
                raw = raw[4:]
        # extract the first [...] block if there's stray text
        if not raw.startswith("["):
            s, e = raw.find("["), raw.rfind("]")
            if s != -1 and e != -1:
                raw = raw[s:e + 1]
        try:
            plan = json.loads(raw)
        except json.JSONDecodeError:
            return []
        return plan if isinstance(plan, list) else []
