---
type: community
cohesion: 0.03
members: 72
---

# _missing() / ._handle_api_mock_data() / ._handle_app_open()

**Cohesion:** 0.03 - loosely connected
**Members:** 72 nodes

## Members
- [[._handle_api_mock_data()]] - code - loki/core/action_router.py
- [[._handle_app_open()]] - code - loki/core/action_router.py
- [[._handle_backup_directory()]] - code - loki/core/action_router.py
- [[._handle_backup_list()]] - code - loki/core/action_router.py
- [[._handle_bluetooth_toggle()]] - code - loki/core/action_router.py
- [[._handle_browser_open()]] - code - loki/core/action_router.py
- [[._handle_browser_search()]] - code - loki/core/action_router.py
- [[._handle_calendar_import()]] - code - loki/core/action_router.py
- [[._handle_clipboard_get()]] - code - loki/core/action_router.py
- [[._handle_clipboard_set()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_stop()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_url()]] - code - loki/core/action_router.py
- [[._handle_code_analyze()]] - code - loki/core/action_router.py
- [[._handle_code_refactor()]] - code - loki/core/action_router.py
- [[._handle_commit_message()]] - code - loki/core/action_router.py
- [[._handle_daily_briefing()]] - code - loki/core/action_router.py
- [[._handle_declutter_dups()]] - code - loki/core/action_router.py
- [[._handle_declutter_large()]] - code - loki/core/action_router.py
- [[._handle_declutter_old()]] - code - loki/core/action_router.py
- [[._handle_declutter_suggest()]] - code - loki/core/action_router.py
- [[._handle_email_draft()]] - code - loki/core/action_router.py
- [[._handle_email_reply()]] - code - loki/core/action_router.py
- [[._handle_env_compose()]] - code - loki/core/action_router.py
- [[._handle_env_dockerfile()]] - code - loki/core/action_router.py
- [[._handle_env_venv()]] - code - loki/core/action_router.py
- [[._handle_expense_extract()]] - code - loki/core/action_router.py
- [[._handle_expense_list()]] - code - loki/core/action_router.py
- [[._handle_expense_summary()]] - code - loki/core/action_router.py
- [[._handle_file_create()]] - code - loki/core/action_router.py
- [[._handle_file_delete()]] - code - loki/core/action_router.py
- [[._handle_file_move()]] - code - loki/core/action_router.py
- [[._handle_file_organize()]] - code - loki/core/action_router.py
- [[._handle_folder_delete()]] - code - loki/core/action_router.py
- [[._handle_footprint_network()]] - code - loki/core/action_router.py
- [[._handle_footprint_startup()]] - code - loki/core/action_router.py
- [[._handle_footprint_tasks()]] - code - loki/core/action_router.py
- [[._handle_git_commit()]] - code - loki/core/action_router.py
- [[._handle_history_recent()]] - code - loki/core/action_router.py
- [[._handle_history_search()]] - code - loki/core/action_router.py
- [[._handle_kg_connections()]] - code - loki/core/action_router.py
- [[._handle_kg_stats()]] - code - loki/core/action_router.py
- [[._handle_media_convert()]] - code - loki/core/action_router.py
- [[._handle_media_info()]] - code - loki/core/action_router.py
- [[._handle_meeting_summarize()]] - code - loki/core/action_router.py
- [[._handle_meeting_transcribe()]] - code - loki/core/action_router.py
- [[._handle_pdf_chat()]] - code - loki/core/action_router.py
- [[._handle_phishing_email()]] - code - loki/core/action_router.py
- [[._handle_phishing_url()]] - code - loki/core/action_router.py
- [[._handle_process_analyze()]] - code - loki/core/action_router.py
- [[._handle_process_kill()]] - code - loki/core/action_router.py
- [[._handle_readme_generate()]] - code - loki/core/action_router.py
- [[._handle_regex_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_capture()]] - code - loki/core/action_router.py
- [[._handle_screen_read()]] - code - loki/core/action_router.py
- [[._handle_screen_search()]] - code - loki/core/action_router.py
- [[._handle_security_scan()]] - code - loki/core/action_router.py
- [[._handle_shell()]] - code - loki/core/action_router.py
- [[._handle_sql_build()]] - code - loki/core/action_router.py
- [[._handle_task_add()]] - code - loki/core/action_router.py
- [[._handle_task_complete()]] - code - loki/core/action_router.py
- [[._handle_task_list()]] - code - loki/core/action_router.py
- [[._handle_text_continue()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_start()]] - code - loki/core/action_router.py
- [[._handle_ui_list_themes()]] - code - loki/core/action_router.py
- [[._handle_update_check()]] - code - loki/core/action_router.py
- [[._handle_update_package()]] - code - loki/core/action_router.py
- [[._handle_vault_retrieve()]] - code - loki/core/action_router.py
- [[._handle_volume_set()]] - code - loki/core/action_router.py
- [[._handle_watch_list()]] - code - loki/core/action_router.py
- [[._handle_watch_media_inbox()]] - code - loki/core/action_router.py
- [[._handle_window_tile_all()]] - code - loki/core/action_router.py
- [[_missing()]] - code - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_missing_/__handle_api_mock_data_/__handle_app_open
SORT file.name ASC
```

## Connections to other communities
- 136 edges to [[_COMMUNITY_ActionRouter  ._handle_api_mock_generate()  ._handle_app_close()]]
- 1 edge to [[_COMMUNITY_action_router.py]]

## Top bridge nodes
- [[_missing()]] - degree 137, connects to 2 communities
- [[._handle_api_mock_data()]] - degree 2, connects to 1 community
- [[._handle_app_open()]] - degree 2, connects to 1 community
- [[._handle_backup_directory()]] - degree 2, connects to 1 community
- [[._handle_backup_list()]] - degree 2, connects to 1 community