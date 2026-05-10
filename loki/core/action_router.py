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
            # Writing & Text
            "text_expand": self._handle_text_expand,
            "text_continue": self._handle_text_continue,
            "text_bullets_to_prose": self._handle_bullets_to_prose,
            "text_polish": self._handle_text_polish,
            "text_change_tone": self._handle_text_change_tone,
            "text_translate": self._handle_text_translate,
            "citation_from_url": self._handle_citation_url,
            "citation_from_info": self._handle_citation_info,
            "email_draft": self._handle_email_draft,
            "email_reply": self._handle_email_reply,
            "fact_check": self._handle_fact_check,
            "daily_briefing": self._handle_daily_briefing,
            # Data & Conversion
            "currency_convert": self._handle_currency_convert,
            "unit_convert": self._handle_unit_convert,
            "news_headlines": self._handle_news_headlines,
            "news_briefing": self._handle_news_briefing,
            "media_convert": self._handle_media_convert,
            "media_info": self._handle_media_info,
            # Software & Environment
            "update_check": self._handle_update_check,
            "update_all": self._handle_update_all,
            "update_package": self._handle_update_package,
            "install_package": self._handle_install_package,
            "env_dockerfile": self._handle_env_dockerfile,
            "env_venv": self._handle_env_venv,
            "env_compose": self._handle_env_compose,
            "api_mock_generate": self._handle_api_mock_generate,
            "api_mock_data": self._handle_api_mock_data,
            # File Management
            "backup_file": self._handle_backup_file,
            "backup_directory": self._handle_backup_directory,
            "backup_list": self._handle_backup_list,
            "declutter_duplicates": self._handle_declutter_dups,
            "declutter_large": self._handle_declutter_large,
            "declutter_old": self._handle_declutter_old,
            "declutter_suggest": self._handle_declutter_suggest,
            # Window & Process
            "window_snap": self._handle_window_snap,
            "window_tile_all": self._handle_window_tile_all,
            "window_layouts": self._handle_window_layouts,
            "process_analyze": self._handle_process_analyze,
            "process_triage": self._handle_process_triage,
            "process_suspend": self._handle_process_suspend,
            "process_resume": self._handle_process_resume,
            # Security & Privacy
            "phishing_url": self._handle_phishing_url,
            "phishing_email": self._handle_phishing_email,
            "footprint_startup": self._handle_footprint_startup,
            "footprint_tasks": self._handle_footprint_tasks,
            "footprint_privacy": self._handle_footprint_privacy,
            "footprint_network": self._handle_footprint_network,
            "footprint_full": self._handle_footprint_full,
            # Knowledge Graph
            "kg_ingest_file": self._handle_kg_ingest_file,
            "kg_ingest_dir": self._handle_kg_ingest_dir,
            "kg_query": self._handle_kg_query,
            "kg_connections": self._handle_kg_connections,
            "kg_stats": self._handle_kg_stats,
            # Browser History
            "history_search": self._handle_history_search,
            "history_semantic": self._handle_history_semantic,
            "history_recent": self._handle_history_recent,
            "history_stats": self._handle_history_stats,
            # Screen & Visual
            "screen_capture": self._handle_screen_capture,
            "screen_read": self._handle_screen_read,
            "screen_search": self._handle_screen_search,
            "screen_describe": self._handle_screen_describe,
            "screen_translate": self._handle_screen_translate,
            "screenshot_save": self._handle_screenshot_save,
            # Calendar
            "calendar_list": self._handle_calendar_list,
            "calendar_conflicts": self._handle_calendar_conflicts,
            "calendar_suggest_slot": self._handle_calendar_suggest_slot,
            "calendar_import": self._handle_calendar_import,
            # Expenses
            "expense_extract": self._handle_expense_extract,
            "expense_from_file": self._handle_expense_from_file,
            "expense_scan_folder": self._handle_expense_scan_folder,
            "expense_list": self._handle_expense_list,
            "expense_summary": self._handle_expense_summary,
            # Dynamic UI
            "ui_theme_time": self._handle_ui_theme_time,
            "ui_theme_mood": self._handle_ui_theme_mood,
            "ui_wallpaper": self._handle_ui_wallpaper,
            "ui_auto_theme_start": self._handle_ui_auto_start,
            "ui_auto_theme_stop": self._handle_ui_auto_stop,
            "ui_list_themes": self._handle_ui_list_themes,
            # File Watcher
            "watch_backup": self._handle_watch_backup,
            "watch_media_inbox": self._handle_watch_media_inbox,
            "watch_list": self._handle_watch_list,
            "watch_stop": self._handle_watch_stop,
            # Clipboard Sync
            "clipboard_sync_start": self._handle_clipboard_sync_start,
            "clipboard_sync_stop": self._handle_clipboard_sync_stop,
            "clipboard_sync_url": self._handle_clipboard_sync_url,
            "clipboard_get": self._handle_clipboard_get,
            "clipboard_set": self._handle_clipboard_set,
            # Code Refactor
            "code_refactor": self._handle_code_refactor,
            # Task AI Prioritize
            "task_prioritize_ai": self._handle_task_prioritize_ai,
            # Deepfake
            "deepfake_check": self._handle_deepfake_check,
            # Meetings
            "meeting_transcribe": self._handle_meeting_transcribe,
            "meeting_minutes": self._handle_meeting_minutes,
            "meeting_action_items": self._handle_meeting_action_items,
            "meeting_summarize": self._handle_meeting_summarize,
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
        import os
        from pathlib import Path
        raw = p.get("path", "")
        try:
            resolved = Path(raw).expanduser().resolve()
            home = Path(os.path.expanduser("~")).resolve()
            if not resolved.is_relative_to(home):
                logger.warning(f"Blocked file_read outside home: {raw}")
                return {"success": False, "message": "Access denied. Path must be within your home directory."}
        except Exception:
            return {"success": False, "message": "Invalid path."}
        if not resolved.exists():
            return {"success": False, "message": f"File not found: {resolved.name}"}
        try:
            content = resolved.read_text(encoding="utf-8", errors="replace")
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

    # --- Writing & Text ---
    def _handle_text_expand(self, p):
        f = self._features.get("ghostwriter")
        return f.expand(p.get("text", "")) if f else self._missing("ghostwriter")

    def _handle_text_continue(self, p):
        f = self._features.get("ghostwriter")
        return f.continue_text(p.get("text", "")) if f else self._missing("ghostwriter")

    def _handle_bullets_to_prose(self, p):
        f = self._features.get("ghostwriter")
        return f.bullets_to_prose(p.get("text", "")) if f else self._missing("ghostwriter")

    def _handle_text_polish(self, p):
        f = self._features.get("grammar_polisher")
        return f.polish(p.get("text", "")) if f else self._missing("grammar_polisher")

    def _handle_text_change_tone(self, p):
        f = self._features.get("grammar_polisher")
        return f.change_tone(p.get("text", ""), p.get("tone", "professional")) if f else self._missing("grammar_polisher")

    def _handle_text_translate(self, p):
        f = self._features.get("grammar_polisher")
        return f.translate(p.get("text", ""), p.get("language", "Spanish")) if f else self._missing("grammar_polisher")

    def _handle_citation_url(self, p):
        f = self._features.get("citation_generator")
        return f.from_url(p.get("url", ""), p.get("style", "apa")) if f else self._missing("citation_generator")

    def _handle_citation_info(self, p):
        f = self._features.get("citation_generator")
        return f.from_info(p.get("info", ""), p.get("style", "apa")) if f else self._missing("citation_generator")

    def _handle_email_draft(self, p):
        f = self._features.get("email_drafter")
        return f.draft(p.get("subject", ""), p.get("context", ""), p.get("to")) if f else self._missing("email_drafter")

    def _handle_email_reply(self, p):
        f = self._features.get("email_drafter")
        return f.reply(p.get("original", ""), p.get("intent")) if f else self._missing("email_drafter")

    def _handle_fact_check(self, p):
        f = self._features.get("fact_checker")
        return f.check(p.get("claim", "")) if f else self._missing("fact_checker")

    def _handle_daily_briefing(self, p):
        f = self._features.get("daily_briefing")
        return f.generate() if f else self._missing("daily_briefing")

    # --- Data & Conversion ---
    def _handle_currency_convert(self, p):
        f = self._features.get("currency_converter")
        return f.convert_currency(p.get("amount", 1), p.get("from_currency", "USD"), p.get("to_currency", "EUR")) if f else self._missing("currency_converter")

    def _handle_unit_convert(self, p):
        f = self._features.get("currency_converter")
        return f.convert_unit(p.get("amount", 1), p.get("from_unit", ""), p.get("to_unit", "")) if f else self._missing("currency_converter")

    def _handle_news_headlines(self, p):
        f = self._features.get("news_aggregator")
        return f.get_headlines(p.get("topic"), p.get("count", 10)) if f else self._missing("news_aggregator")

    def _handle_news_briefing(self, p):
        f = self._features.get("news_aggregator")
        return f.get_briefing(p.get("topics")) if f else self._missing("news_aggregator")

    def _handle_media_convert(self, p):
        f = self._features.get("media_converter")
        return f.convert(p.get("input_path", ""), p.get("output_format", ""), p.get("output_path"), p.get("quality", "medium")) if f else self._missing("media_converter")

    def _handle_media_info(self, p):
        f = self._features.get("media_converter")
        return f.get_info(p.get("file_path", "")) if f else self._missing("media_converter")

    # --- Software & Environment ---
    def _handle_update_check(self, p):
        f = self._features.get("software_updater")
        return f.check_updates() if f else self._missing("software_updater")

    def _handle_update_all(self, p):
        f = self._features.get("software_updater")
        return f.update_all() if f else self._missing("software_updater")

    def _handle_update_package(self, p):
        f = self._features.get("software_updater")
        return f.update_package(p.get("package_name", "")) if f else self._missing("software_updater")

    def _handle_install_package(self, p):
        f = self._features.get("software_updater")
        return f.install_package(p.get("package_name", "")) if f else self._missing("software_updater")

    def _handle_env_dockerfile(self, p):
        f = self._features.get("env_setup")
        return f.generate_dockerfile(p.get("project_path", ".")) if f else self._missing("env_setup")

    def _handle_env_venv(self, p):
        f = self._features.get("env_setup")
        return f.generate_venv_script(p.get("project_path", "."), p.get("python", "python")) if f else self._missing("env_setup")

    def _handle_env_compose(self, p):
        f = self._features.get("env_setup")
        return f.generate_docker_compose(p.get("project_path", "."), p.get("services", "")) if f else self._missing("env_setup")

    def _handle_api_mock_generate(self, p):
        f = self._features.get("api_mocker")
        return f.generate_mock(p.get("description", "")) if f else self._missing("api_mocker")

    def _handle_api_mock_data(self, p):
        f = self._features.get("api_mocker")
        return f.generate_mock_data(p.get("schema", "")) if f else self._missing("api_mocker")

    # --- File Management ---
    def _handle_backup_file(self, p):
        f = self._features.get("backup_manager")
        return f.backup_file(p.get("path", ""), p.get("destination")) if f else self._missing("backup_manager")

    def _handle_backup_directory(self, p):
        f = self._features.get("backup_manager")
        return f.backup_directory(p.get("path", ""), p.get("destination")) if f else self._missing("backup_manager")

    def _handle_backup_list(self, p):
        f = self._features.get("backup_manager")
        return f.list_backups(p.get("name_filter")) if f else self._missing("backup_manager")

    def _handle_declutter_dups(self, p):
        f = self._features.get("digital_declutter")
        return f.find_duplicates(p.get("directory", "~")) if f else self._missing("digital_declutter")

    def _handle_declutter_large(self, p):
        f = self._features.get("digital_declutter")
        return f.find_large_files(p.get("directory", "~"), float(p.get("threshold_mb", 100))) if f else self._missing("digital_declutter")

    def _handle_declutter_old(self, p):
        f = self._features.get("digital_declutter")
        return f.find_old_files(p.get("directory", "~/Downloads"), int(p.get("days", 180))) if f else self._missing("digital_declutter")

    def _handle_declutter_suggest(self, p):
        f = self._features.get("digital_declutter")
        return f.suggest_cleanup(p.get("directory", "~")) if f else self._missing("digital_declutter")

    # --- Window & Process ---
    def _handle_window_snap(self, p):
        f = self._features.get("window_tiler")
        return f.snap_window(p.get("layout", "left"), p.get("window_title", "")) if f else self._missing("window_tiler")

    def _handle_window_tile_all(self, p):
        f = self._features.get("window_tiler")
        return f.tile_all() if f else self._missing("window_tiler")

    def _handle_window_layouts(self, p):
        f = self._features.get("window_tiler")
        return f.list_layouts() if f else self._missing("window_tiler")

    def _handle_process_analyze(self, p):
        f = self._features.get("process_triage")
        return f.analyze(int(p.get("top_n", 10))) if f else self._missing("process_triage")

    def _handle_process_triage(self, p):
        f = self._features.get("process_triage")
        dry = p.get("dry_run", True)
        if isinstance(dry, str):
            dry = dry.lower() != "false"
        return f.triage_for_app(p.get("app_name", ""), dry_run=dry) if f else self._missing("process_triage")

    def _handle_process_suspend(self, p):
        f = self._features.get("process_triage")
        return f.suspend_process(p.get("name_or_pid", "")) if f else self._missing("process_triage")

    def _handle_process_resume(self, p):
        f = self._features.get("process_triage")
        return f.resume_process(p.get("name_or_pid", "")) if f else self._missing("process_triage")

    # --- Security & Privacy ---
    def _handle_phishing_url(self, p):
        f = self._features.get("phishing_detector")
        return f.analyze_url(p.get("url", "")) if f else self._missing("phishing_detector")

    def _handle_phishing_email(self, p):
        f = self._features.get("phishing_detector")
        return f.analyze_email(p.get("email_text", "")) if f else self._missing("phishing_detector")

    def _handle_footprint_startup(self, p):
        f = self._features.get("footprint_auditor")
        return f.audit_startup() if f else self._missing("footprint_auditor")

    def _handle_footprint_tasks(self, p):
        f = self._features.get("footprint_auditor")
        return f.audit_scheduled_tasks() if f else self._missing("footprint_auditor")

    def _handle_footprint_privacy(self, p):
        f = self._features.get("footprint_auditor")
        return f.audit_privacy_settings() if f else self._missing("footprint_auditor")

    def _handle_footprint_network(self, p):
        f = self._features.get("footprint_auditor")
        return f.audit_network_listeners() if f else self._missing("footprint_auditor")

    def _handle_footprint_full(self, p):
        f = self._features.get("footprint_auditor")
        return f.full_audit() if f else self._missing("footprint_auditor")

    # --- Knowledge Graph ---
    def _handle_kg_ingest_file(self, p):
        f = self._features.get("knowledge_graph")
        return f.ingest_file(p.get("file_path", "")) if f else self._missing("knowledge_graph")

    def _handle_kg_ingest_dir(self, p):
        f = self._features.get("knowledge_graph")
        return f.ingest_directory(p.get("directory", "")) if f else self._missing("knowledge_graph")

    def _handle_kg_query(self, p):
        f = self._features.get("knowledge_graph")
        return f.query(p.get("question", "")) if f else self._missing("knowledge_graph")

    def _handle_kg_connections(self, p):
        f = self._features.get("knowledge_graph")
        return f.find_connections(p.get("entity", "")) if f else self._missing("knowledge_graph")

    def _handle_kg_stats(self, p):
        f = self._features.get("knowledge_graph")
        return f.get_stats() if f else self._missing("knowledge_graph")

    # --- Browser History ---
    def _handle_history_search(self, p):
        f = self._features.get("browser_history")
        return f.search(p.get("query", ""), p.get("browser", "auto"), int(p.get("days", 30))) if f else self._missing("browser_history")

    def _handle_history_semantic(self, p):
        f = self._features.get("browser_history")
        return f.semantic_search(p.get("query", ""), p.get("browser", "auto"), int(p.get("days", 30))) if f else self._missing("browser_history")

    def _handle_history_recent(self, p):
        f = self._features.get("browser_history")
        return f.recent(p.get("browser", "auto"), int(p.get("days", 1))) if f else self._missing("browser_history")

    def _handle_history_stats(self, p):
        f = self._features.get("browser_history")
        return f.get_stats(p.get("browser", "auto")) if f else self._missing("browser_history")

    # --- Screen & Visual ---
    def _handle_screen_capture(self, p):
        f = self._features.get("screenshot_search")
        return f.capture_and_read(p.get("region")) if f else self._missing("screenshot_search")

    def _handle_screen_read(self, p):
        f = self._features.get("screenshot_search")
        return f.capture_and_read(p.get("region")) if f else self._missing("screenshot_search")

    def _handle_screen_search(self, p):
        f = self._features.get("screenshot_search")
        return f.search_screen(p.get("query", "")) if f else self._missing("screenshot_search")

    def _handle_screen_describe(self, p):
        f = self._features.get("screenshot_search")
        return f.describe_screen() if f else self._missing("screenshot_search")

    def _handle_screen_translate(self, p):
        f = self._features.get("screenshot_search")
        return f.translate_screen(p.get("target_language", "English")) if f else self._missing("screenshot_search")

    def _handle_screenshot_save(self, p):
        f = self._features.get("screenshot_search")
        return f.save_screenshot(p.get("output_path")) if f else self._missing("screenshot_search")

    # --- Calendar ---
    def _handle_calendar_list(self, p):
        f = self._features.get("calendar_manager")
        return f.list_events(int(p.get("days", 7)), p.get("ics_path")) if f else self._missing("calendar_manager")

    def _handle_calendar_conflicts(self, p):
        f = self._features.get("calendar_manager")
        return f.find_conflicts(p.get("ics_path")) if f else self._missing("calendar_manager")

    def _handle_calendar_suggest_slot(self, p):
        f = self._features.get("calendar_manager")
        return f.suggest_alternatives(p.get("event_title", "Meeting"), int(p.get("duration_minutes", 60)), p.get("ics_path")) if f else self._missing("calendar_manager")

    def _handle_calendar_import(self, p):
        f = self._features.get("calendar_manager")
        return f.import_ics(p.get("ics_path", "")) if f else self._missing("calendar_manager")

    # --- Expenses ---
    def _handle_expense_extract(self, p):
        f = self._features.get("expense_tracker")
        return f.extract_from_text(p.get("text", "")) if f else self._missing("expense_tracker")

    def _handle_expense_from_file(self, p):
        f = self._features.get("expense_tracker")
        return f.extract_from_file(p.get("file_path", "")) if f else self._missing("expense_tracker")

    def _handle_expense_scan_folder(self, p):
        f = self._features.get("expense_tracker")
        return f.scan_folder(p.get("folder", "")) if f else self._missing("expense_tracker")

    def _handle_expense_list(self, p):
        f = self._features.get("expense_tracker")
        return f.list_expenses(p.get("month")) if f else self._missing("expense_tracker")

    def _handle_expense_summary(self, p):
        f = self._features.get("expense_tracker")
        return f.monthly_summary() if f else self._missing("expense_tracker")

    # --- Dynamic UI ---
    def _handle_ui_theme_time(self, p):
        f = self._features.get("dynamic_ui")
        return f.apply_time_theme() if f else self._missing("dynamic_ui")

    def _handle_ui_theme_mood(self, p):
        f = self._features.get("dynamic_ui")
        return f.apply_mood_theme(p.get("mood", "focus")) if f else self._missing("dynamic_ui")

    def _handle_ui_wallpaper(self, p):
        f = self._features.get("dynamic_ui")
        return f.set_wallpaper(p.get("image_path", "")) if f else self._missing("dynamic_ui")

    def _handle_ui_auto_start(self, p):
        f = self._features.get("dynamic_ui")
        return f.start_auto_theme() if f else self._missing("dynamic_ui")

    def _handle_ui_auto_stop(self, p):
        f = self._features.get("dynamic_ui")
        return f.stop_auto_theme() if f else self._missing("dynamic_ui")

    def _handle_ui_list_themes(self, p):
        f = self._features.get("dynamic_ui")
        return f.list_themes() if f else self._missing("dynamic_ui")

    # --- File Watcher ---
    def _handle_watch_backup(self, p):
        f = self._features.get("file_watcher")
        return f.watch_for_backup(p.get("path", ""), p.get("destination"), float(p.get("poll_seconds", 30))) if f else self._missing("file_watcher")

    def _handle_watch_media_inbox(self, p):
        f = self._features.get("file_watcher")
        return f.watch_media_inbox(p.get("inbox_dir", ""), p.get("output_format", "mp4")) if f else self._missing("file_watcher")

    def _handle_watch_list(self, p):
        f = self._features.get("file_watcher")
        return f.list_watchers() if f else self._missing("file_watcher")

    def _handle_watch_stop(self, p):
        f = self._features.get("file_watcher")
        return f.stop_watch(p.get("path", "")) if f else self._missing("file_watcher")

    # --- Clipboard Sync ---
    def _handle_clipboard_sync_start(self, p):
        f = self._features.get("clipboard_sync")
        return f.start() if f else self._missing("clipboard_sync")

    def _handle_clipboard_sync_stop(self, p):
        f = self._features.get("clipboard_sync")
        return f.stop() if f else self._missing("clipboard_sync")

    def _handle_clipboard_sync_url(self, p):
        f = self._features.get("clipboard_sync")
        return f.get_url() if f else self._missing("clipboard_sync")

    def _handle_clipboard_get(self, p):
        f = self._features.get("clipboard_sync")
        return f.get_clipboard() if f else self._missing("clipboard_sync")

    def _handle_clipboard_set(self, p):
        f = self._features.get("clipboard_sync")
        return f.set_clipboard(p.get("text", "")) if f else self._missing("clipboard_sync")

    # --- Code Refactor ---
    def _handle_code_refactor(self, p):
        f = self._features.get("code_assistant")
        return f.refactor(p.get("path", "")) if f else self._missing("code_assistant")

    # --- Task AI Prioritize ---
    def _handle_task_prioritize_ai(self, p):
        f = self._features.get("task_manager")
        if not f:
            return self._missing("task_manager")
        # Pass the brain from phishing_detector or any available feature that has it
        brain = None
        for feat in self._features.values():
            if hasattr(feat, "_brain") and feat._brain:
                brain = feat._brain
                break
        return f.ai_prioritize(brain)

    # --- Deepfake Check ---
    def _handle_deepfake_check(self, p):
        f = self._features.get("phishing_detector")
        return f.analyze_media_file(p.get("file_path", "")) if f else self._missing("phishing_detector")

    # --- Meetings ---
    def _handle_meeting_transcribe(self, p):
        f = self._features.get("meeting_transcriber")
        return f.transcribe(p.get("audio_path", ""), p.get("language", "en")) if f else self._missing("meeting_transcriber")

    def _handle_meeting_minutes(self, p):
        f = self._features.get("meeting_transcriber")
        return f.generate_minutes(p.get("audio_path", ""), p.get("language", "en")) if f else self._missing("meeting_transcriber")

    def _handle_meeting_action_items(self, p):
        f = self._features.get("meeting_transcriber")
        return f.extract_action_items(p.get("text_or_path", "")) if f else self._missing("meeting_transcriber")

    def _handle_meeting_summarize(self, p):
        f = self._features.get("meeting_transcriber")
        return f.summarize_transcript(p.get("transcript", "")) if f else self._missing("meeting_transcriber")

    # --- Meta ---
    def _handle_undo(self, p):
        if self._undo.is_empty():
            return {"success": False, "message": "Nothing to undo. The slate is already clean."}
        success = self._undo.pop_and_undo()
        return {"success": success, "message": "Done. Reversed." if success else "Undo failed. Some things cannot be undone."}

    @staticmethod
    def _missing(name: str) -> Dict[str, Any]:
        return {"success": False, "message": f"Feature '{name}' not initialized."}
