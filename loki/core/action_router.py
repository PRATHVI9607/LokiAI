"""
Action router — maps LLM intents to feature/action handlers.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ActionRouter:
    """Routes parsed intents to their corresponding action handlers."""

    def __init__(self, undo_stack, features=None, actions=None):
        self._undo = undo_stack
        self._features: Dict[str, Any] = features or {}
        self._actions: Dict[str, Any] = actions or {}

    def register_feature(self, name: str, handler: Any) -> None:
        self._features[name] = handler

    def register_action(self, name: str, handler: Any) -> None:
        self._actions[name] = handler

    def route_intent(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        intent_name = intent.get("intent", "chat")
        params = intent.get("params", {})

        logger.info(f"Routing intent: {intent_name} params={list(params.keys())}")

        handlers = {
            # File operations
            "file_create": self._handle_file_create,
            "file_delete": self._handle_file_delete,
            "file_move": self._handle_file_move,
            "file_read": self._handle_file_read,
            "folder_create": self._handle_folder_create,
            "folder_delete": self._handle_folder_delete,
            "file_search": self._handle_file_search,
            "file_organize": self._handle_file_organize,
            # Shell
            "shell": self._handle_shell,
            # System
            "volume_set": self._handle_volume_set,
            "volume_get": self._handle_volume_get,
            "brightness_set": self._handle_brightness_set,
            "brightness_get": self._handle_brightness_get,
            "wifi_toggle": self._handle_wifi_toggle,
            "bluetooth_toggle": self._handle_bluetooth_toggle,
            "app_open": self._handle_app_open,
            "app_close": self._handle_app_close,
            "browser_open": self._handle_browser_open,
            "browser_search": self._handle_browser_search,
            "system_monitor": self._handle_system_monitor,
            "process_kill": self._handle_process_kill,
            "process_list": self._handle_process_list,
            # Intelligence
            "web_summarize": self._handle_web_summarize,
            "pdf_chat": self._handle_pdf_chat,
            "code_analyze": self._handle_code_analyze,
            "code_convert": self._handle_code_convert,
            "commit_message": self._handle_commit_message,
            "readme_generate": self._handle_readme_generate,
            "regex_generate": self._handle_regex_generate,
            "sql_build": self._handle_sql_build,
            "git_status": self._handle_git_status,
            "git_commit": self._handle_git_commit,
            "security_scan": self._handle_security_scan,
            # Productivity
            "focus_mode_enable": self._handle_focus_enable,
            "focus_mode_disable": self._handle_focus_disable,
            "task_add": self._handle_task_add,
            "task_list": self._handle_task_list,
            "task_complete": self._handle_task_complete,
            "task_delete": self._handle_task_delete,
            "clipboard_show": self._handle_clipboard_show,
            "clipboard_clear": self._handle_clipboard_clear,
            "vault_store": self._handle_vault_store,
            "vault_retrieve": self._handle_vault_retrieve,
            # Meta
            "undo": self._handle_undo,
            "chat": lambda p: {"success": True, "message": intent.get("message", "")},
        }

        handler = handlers.get(intent_name)
        if handler:
            try:
                return handler(params)
            except Exception as e:
                logger.error(f"Handler error ({intent_name}): {e}", exc_info=True)
                return {"success": False, "message": f"Handler failed: {e}"}

        return {"success": False, "message": f"Unknown intent: {intent_name}"}

    # --- File Operations ---
    def _handle_file_create(self, p):
        ops = self._actions.get("file_ops")
        if ops:
            return ops.create_file(p.get("path", ""), p.get("content", ""))
        return self._missing("file_ops")

    def _handle_file_delete(self, p):
        ops = self._actions.get("file_ops")
        if ops:
            return ops.delete_file(p.get("path", ""))
        return self._missing("file_ops")

    def _handle_file_move(self, p):
        ops = self._actions.get("file_ops")
        if ops:
            return ops.move(p.get("src", ""), p.get("dst", ""))
        return self._missing("file_ops")

    def _handle_file_read(self, p):
        from pathlib import Path
        path = Path(p.get("path", ""))
        if not path.exists():
            return {"success": False, "message": f"File not found: {path}"}
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            return {"success": True, "message": content[:2000], "data": content}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def _handle_folder_create(self, p):
        ops = self._actions.get("file_ops")
        if ops:
            return ops.create_folder(p.get("path", ""))
        return self._missing("file_ops")

    def _handle_folder_delete(self, p):
        ops = self._actions.get("file_ops")
        if ops:
            return ops.delete_folder(p.get("path", ""))
        return self._missing("file_ops")

    def _handle_file_search(self, p):
        feat = self._features.get("file_search")
        if feat:
            return feat.search(p.get("query", ""), p.get("directory"), p.get("type"))
        return self._missing("file_search")

    def _handle_file_organize(self, p):
        feat = self._features.get("file_organizer")
        if feat:
            return feat.organize(p.get("directory"))
        return self._missing("file_organizer")

    # --- Shell ---
    def _handle_shell(self, p):
        shell = self._actions.get("shell_exec")
        if shell:
            return shell.execute(p.get("command", ""))
        return self._missing("shell_exec")

    # --- System ---
    def _handle_volume_set(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.set_volume(int(p.get("percent", 50))) if sys else self._missing("system_ctrl")

    def _handle_volume_get(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.get_volume() if sys else self._missing("system_ctrl")

    def _handle_brightness_set(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.set_brightness(int(p.get("percent", 50))) if sys else self._missing("system_ctrl")

    def _handle_brightness_get(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.get_brightness() if sys else self._missing("system_ctrl")

    def _handle_wifi_toggle(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.toggle_wifi() if sys else self._missing("system_ctrl")

    def _handle_bluetooth_toggle(self, p):
        sys = self._actions.get("system_ctrl")
        return sys.toggle_bluetooth() if sys else self._missing("system_ctrl")

    def _handle_app_open(self, p):
        app = self._actions.get("app_ctrl")
        return app.open_app(p.get("name", "")) if app else self._missing("app_ctrl")

    def _handle_app_close(self, p):
        app = self._actions.get("app_ctrl")
        return app.close_app(p.get("name", "")) if app else self._missing("app_ctrl")

    def _handle_browser_open(self, p):
        browser = self._actions.get("browser_ctrl")
        return browser.open_url(p.get("url", "")) if browser else self._missing("browser_ctrl")

    def _handle_browser_search(self, p):
        browser = self._actions.get("browser_ctrl")
        return browser.search(p.get("query", ""), p.get("engine", "google")) if browser else self._missing("browser_ctrl")

    def _handle_system_monitor(self, p):
        feat = self._features.get("system_monitor")
        return feat.get_stats() if feat else self._missing("system_monitor")

    def _handle_process_kill(self, p):
        feat = self._features.get("process_manager")
        return feat.kill(p.get("name_or_pid")) if feat else self._missing("process_manager")

    def _handle_process_list(self, p):
        feat = self._features.get("process_manager")
        return feat.list_processes() if feat else self._missing("process_manager")

    # --- Intelligence ---
    def _handle_web_summarize(self, p):
        feat = self._features.get("web_summarizer")
        return feat.summarize(p.get("url", "")) if feat else self._missing("web_summarizer")

    def _handle_pdf_chat(self, p):
        feat = self._features.get("pdf_chat")
        return feat.ask(p.get("path", ""), p.get("question", "")) if feat else self._missing("pdf_chat")

    def _handle_code_analyze(self, p):
        feat = self._features.get("code_assistant")
        return feat.analyze(p.get("path", "")) if feat else self._missing("code_assistant")

    def _handle_code_convert(self, p):
        feat = self._features.get("code_assistant")
        return feat.convert(p.get("path", ""), p.get("from_lang"), p.get("to_lang")) if feat else self._missing("code_assistant")

    def _handle_commit_message(self, p):
        feat = self._features.get("git_helper")
        return feat.generate_commit_message(p.get("repo_path")) if feat else self._missing("git_helper")

    def _handle_readme_generate(self, p):
        feat = self._features.get("code_assistant")
        return feat.generate_readme(p.get("repo_path")) if feat else self._missing("code_assistant")

    def _handle_regex_generate(self, p):
        feat = self._features.get("code_assistant")
        return feat.generate_regex(p.get("description", "")) if feat else self._missing("code_assistant")

    def _handle_sql_build(self, p):
        feat = self._features.get("code_assistant")
        return feat.build_sql(p.get("description", ""), p.get("schema")) if feat else self._missing("code_assistant")

    def _handle_git_status(self, p):
        feat = self._features.get("git_helper")
        return feat.get_status(p.get("repo_path")) if feat else self._missing("git_helper")

    def _handle_git_commit(self, p):
        feat = self._features.get("git_helper")
        return feat.commit(p.get("message", ""), p.get("repo_path")) if feat else self._missing("git_helper")

    def _handle_security_scan(self, p):
        feat = self._features.get("security_scanner")
        return feat.scan(p.get("path", ".")) if feat else self._missing("security_scanner")

    # --- Productivity ---
    def _handle_focus_enable(self, p):
        feat = self._features.get("focus_mode")
        return feat.enable(p.get("duration_minutes")) if feat else self._missing("focus_mode")

    def _handle_focus_disable(self, p):
        feat = self._features.get("focus_mode")
        return feat.disable() if feat else self._missing("focus_mode")

    def _handle_task_add(self, p):
        feat = self._features.get("task_manager")
        return feat.add(p.get("title", ""), p.get("priority", "medium"), p.get("due")) if feat else self._missing("task_manager")

    def _handle_task_list(self, p):
        feat = self._features.get("task_manager")
        return feat.list_tasks(p.get("filter")) if feat else self._missing("task_manager")

    def _handle_task_complete(self, p):
        feat = self._features.get("task_manager")
        return feat.complete(int(p.get("id", 0))) if feat else self._missing("task_manager")

    def _handle_task_delete(self, p):
        feat = self._features.get("task_manager")
        return feat.delete(int(p.get("id", 0))) if feat else self._missing("task_manager")

    def _handle_clipboard_show(self, p):
        feat = self._features.get("clipboard_manager")
        return feat.get_history() if feat else self._missing("clipboard_manager")

    def _handle_clipboard_clear(self, p):
        feat = self._features.get("clipboard_manager")
        return feat.clear() if feat else self._missing("clipboard_manager")

    def _handle_vault_store(self, p):
        feat = self._features.get("vault")
        return feat.store(p.get("key", ""), p.get("value", "")) if feat else self._missing("vault")

    def _handle_vault_retrieve(self, p):
        feat = self._features.get("vault")
        return feat.retrieve(p.get("key", "")) if feat else self._missing("vault")

    # --- Meta ---
    def _handle_undo(self, p):
        if self._undo.is_empty():
            return {"success": False, "message": "Nothing to undo. The slate is already clean."}
        success = self._undo.pop_and_undo()
        return {"success": success, "message": "Done. Reversed." if success else "Undo failed. Some things cannot be undone."}

    @staticmethod
    def _missing(name: str) -> Dict[str, Any]:
        return {"success": False, "message": f"Feature '{name}' not initialized."}
