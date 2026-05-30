---
type: community
cohesion: 0.03
members: 77
---

# _missing() / ._handle_api_mock_generate() / ._handle_app_close()

**Cohesion:** 0.03 - loosely connected
**Members:** 77 nodes

## Members
- [[._handle_api_mock_generate()]] - code - loki/core/action_router.py
- [[._handle_app_close()]] - code - loki/core/action_router.py
- [[._handle_app_open()]] - code - loki/core/action_router.py
- [[._handle_backup_file()]] - code - loki/core/action_router.py
- [[._handle_bluetooth_toggle()]] - code - loki/core/action_router.py
- [[._handle_brightness_get()]] - code - loki/core/action_router.py
- [[._handle_bullets_to_prose()]] - code - loki/core/action_router.py
- [[._handle_calendar_import()]] - code - loki/core/action_router.py
- [[._handle_calendar_list()]] - code - loki/core/action_router.py
- [[._handle_calendar_suggest_slot()]] - code - loki/core/action_router.py
- [[._handle_clipboard_get()]] - code - loki/core/action_router.py
- [[._handle_clipboard_set()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_start()]] - code - loki/core/action_router.py
- [[._handle_code_convert()]] - code - loki/core/action_router.py
- [[._handle_computer_click()]] - code - loki/core/action_router.py
- [[._handle_computer_move()]] - code - loki/core/action_router.py
- [[._handle_computer_type()]] - code - loki/core/action_router.py
- [[._handle_currency_convert()]] - code - loki/core/action_router.py
- [[._handle_daily_briefing()]] - code - loki/core/action_router.py
- [[._handle_declutter_large()]] - code - loki/core/action_router.py
- [[._handle_declutter_old()]] - code - loki/core/action_router.py
- [[._handle_email_reply()]] - code - loki/core/action_router.py
- [[._handle_env_compose()]] - code - loki/core/action_router.py
- [[._handle_env_venv()]] - code - loki/core/action_router.py
- [[._handle_expense_extract()]] - code - loki/core/action_router.py
- [[._handle_expense_list()]] - code - loki/core/action_router.py
- [[._handle_expense_scan_folder()]] - code - loki/core/action_router.py
- [[._handle_expense_summary()]] - code - loki/core/action_router.py
- [[._handle_file_create()]] - code - loki/core/action_router.py
- [[._handle_file_delete()]] - code - loki/core/action_router.py
- [[._handle_focus_disable()]] - code - loki/core/action_router.py
- [[._handle_folder_create()]] - code - loki/core/action_router.py
- [[._handle_folder_delete()]] - code - loki/core/action_router.py
- [[._handle_footprint_full()]] - code - loki/core/action_router.py
- [[._handle_footprint_network()]] - code - loki/core/action_router.py
- [[._handle_footprint_tasks()]] - code - loki/core/action_router.py
- [[._handle_git_commit()]] - code - loki/core/action_router.py
- [[._handle_git_status()]] - code - loki/core/action_router.py
- [[._handle_history_recent()]] - code - loki/core/action_router.py
- [[._handle_history_search()]] - code - loki/core/action_router.py
- [[._handle_history_semantic()]] - code - loki/core/action_router.py
- [[._handle_history_stats()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_dir()]] - code - loki/core/action_router.py
- [[._handle_kg_query()]] - code - loki/core/action_router.py
- [[._handle_kg_stats()]] - code - loki/core/action_router.py
- [[._handle_media_convert()]] - code - loki/core/action_router.py
- [[._handle_media_info()]] - code - loki/core/action_router.py
- [[._handle_meeting_action_items()]] - code - loki/core/action_router.py
- [[._handle_meeting_minutes()]] - code - loki/core/action_router.py
- [[._handle_meeting_summarize()]] - code - loki/core/action_router.py
- [[._handle_meeting_transcribe()]] - code - loki/core/action_router.py
- [[._handle_news_briefing()]] - code - loki/core/action_router.py
- [[._handle_phishing_url()]] - code - loki/core/action_router.py
- [[._handle_process_analyze()]] - code - loki/core/action_router.py
- [[._handle_process_list()]] - code - loki/core/action_router.py
- [[._handle_process_resume()]] - code - loki/core/action_router.py
- [[._handle_readme_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_search()]] - code - loki/core/action_router.py
- [[._handle_security_scan()]] - code - loki/core/action_router.py
- [[._handle_system_monitor()]] - code - loki/core/action_router.py
- [[._handle_task_list()]] - code - loki/core/action_router.py
- [[._handle_task_prioritize_ai()]] - code - loki/core/action_router.py
- [[._handle_text_change_tone()]] - code - loki/core/action_router.py
- [[._handle_ui_list_themes()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_mood()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_time()]] - code - loki/core/action_router.py
- [[._handle_unit_convert()]] - code - loki/core/action_router.py
- [[._handle_update_all()]] - code - loki/core/action_router.py
- [[._handle_update_package()]] - code - loki/core/action_router.py
- [[._handle_vault_retrieve()]] - code - loki/core/action_router.py
- [[._handle_vault_store()]] - code - loki/core/action_router.py
- [[._handle_volume_set()]] - code - loki/core/action_router.py
- [[._handle_watch_stop()]] - code - loki/core/action_router.py
- [[._handle_wifi_toggle()]] - code - loki/core/action_router.py
- [[._handle_window_layouts()]] - code - loki/core/action_router.py
- [[._handle_window_tile_all()]] - code - loki/core/action_router.py
- [[_missing()]] - code - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_missing_/__handle_api_mock_generate_/__handle_app_close
SORT file.name ASC
```

## Connections to other communities
- 146 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]

## Top bridge nodes
- [[_missing()]] - degree 147, connects to 2 communities
- [[._handle_api_mock_generate()]] - degree 2, connects to 1 community
- [[._handle_app_close()]] - degree 2, connects to 1 community
- [[._handle_app_open()]] - degree 2, connects to 1 community
- [[._handle_backup_file()]] - degree 2, connects to 1 community