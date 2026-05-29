---
type: community
cohesion: 0.03
members: 73
---

# _missing() / ._handle_api_mock_generate() / ._handle_backup_list()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[._handle_api_mock_generate()]] - code - loki/core/action_router.py
- [[._handle_backup_list()]] - code - loki/core/action_router.py
- [[._handle_brightness_get()]] - code - loki/core/action_router.py
- [[._handle_browser_open()]] - code - loki/core/action_router.py
- [[._handle_bullets_to_prose()]] - code - loki/core/action_router.py
- [[._handle_calendar_suggest_slot()]] - code - loki/core/action_router.py
- [[._handle_citation_url()]] - code - loki/core/action_router.py
- [[._handle_clipboard_get()]] - code - loki/core/action_router.py
- [[._handle_clipboard_set()]] - code - loki/core/action_router.py
- [[._handle_clipboard_show()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_start()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_stop()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_url()]] - code - loki/core/action_router.py
- [[._handle_code_analyze()]] - code - loki/core/action_router.py
- [[._handle_code_convert()]] - code - loki/core/action_router.py
- [[._handle_code_refactor()]] - code - loki/core/action_router.py
- [[._handle_currency_convert()]] - code - loki/core/action_router.py
- [[._handle_declutter_dups()]] - code - loki/core/action_router.py
- [[._handle_declutter_large()]] - code - loki/core/action_router.py
- [[._handle_declutter_old()]] - code - loki/core/action_router.py
- [[._handle_declutter_suggest()]] - code - loki/core/action_router.py
- [[._handle_email_draft()]] - code - loki/core/action_router.py
- [[._handle_email_reply()]] - code - loki/core/action_router.py
- [[._handle_env_compose()]] - code - loki/core/action_router.py
- [[._handle_env_dockerfile()]] - code - loki/core/action_router.py
- [[._handle_expense_from_file()]] - code - loki/core/action_router.py
- [[._handle_expense_scan_folder()]] - code - loki/core/action_router.py
- [[._handle_expense_summary()]] - code - loki/core/action_router.py
- [[._handle_file_create()]] - code - loki/core/action_router.py
- [[._handle_file_delete()]] - code - loki/core/action_router.py
- [[._handle_file_move()]] - code - loki/core/action_router.py
- [[._handle_file_organize()]] - code - loki/core/action_router.py
- [[._handle_file_search()]] - code - loki/core/action_router.py
- [[._handle_focus_disable()]] - code - loki/core/action_router.py
- [[._handle_footprint_network()]] - code - loki/core/action_router.py
- [[._handle_footprint_privacy()]] - code - loki/core/action_router.py
- [[._handle_git_commit()]] - code - loki/core/action_router.py
- [[._handle_history_recent()]] - code - loki/core/action_router.py
- [[._handle_history_search()]] - code - loki/core/action_router.py
- [[._handle_history_semantic()]] - code - loki/core/action_router.py
- [[._handle_kg_connections()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_dir()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_file()]] - code - loki/core/action_router.py
- [[._handle_meeting_action_items()]] - code - loki/core/action_router.py
- [[._handle_meeting_minutes()]] - code - loki/core/action_router.py
- [[._handle_meeting_transcribe()]] - code - loki/core/action_router.py
- [[._handle_news_headlines()]] - code - loki/core/action_router.py
- [[._handle_pdf_chat()]] - code - loki/core/action_router.py
- [[._handle_process_analyze()]] - code - loki/core/action_router.py
- [[._handle_process_kill()]] - code - loki/core/action_router.py
- [[._handle_process_suspend()]] - code - loki/core/action_router.py
- [[._handle_process_triage()]] - code - loki/core/action_router.py
- [[._handle_readme_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_capture()]] - code - loki/core/action_router.py
- [[._handle_screen_describe()]] - code - loki/core/action_router.py
- [[._handle_screenshot_save()]] - code - loki/core/action_router.py
- [[._handle_security_scan()]] - code - loki/core/action_router.py
- [[._handle_system_monitor()]] - code - loki/core/action_router.py
- [[._handle_task_add()]] - code - loki/core/action_router.py
- [[._handle_task_delete()]] - code - loki/core/action_router.py
- [[._handle_task_list()]] - code - loki/core/action_router.py
- [[._handle_text_change_tone()]] - code - loki/core/action_router.py
- [[._handle_text_translate()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_stop()]] - code - loki/core/action_router.py
- [[._handle_ui_list_themes()]] - code - loki/core/action_router.py
- [[._handle_unit_convert()]] - code - loki/core/action_router.py
- [[._handle_update_all()]] - code - loki/core/action_router.py
- [[._handle_watch_media_inbox()]] - code - loki/core/action_router.py
- [[._handle_watch_stop()]] - code - loki/core/action_router.py
- [[._handle_window_layouts()]] - code - loki/core/action_router.py
- [[._handle_window_snap()]] - code - loki/core/action_router.py
- [[._handle_window_tile_all()]] - code - loki/core/action_router.py
- [[_missing()]] - code - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_missing_/__handle_api_mock_generate_/__handle_backup_list
SORT file.name ASC
```

## Connections to other communities
- 139 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]

## Top bridge nodes
- [[_missing()]] - degree 140, connects to 2 communities
- [[._handle_api_mock_generate()]] - degree 2, connects to 1 community
- [[._handle_backup_list()]] - degree 2, connects to 1 community
- [[._handle_brightness_get()]] - degree 2, connects to 1 community
- [[._handle_browser_open()]] - degree 2, connects to 1 community