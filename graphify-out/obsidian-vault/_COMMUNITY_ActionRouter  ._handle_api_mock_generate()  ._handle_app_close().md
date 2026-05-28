---
type: community
cohesion: 0.03
members: 73
---

# ActionRouter / ._handle_api_mock_generate() / ._handle_app_close()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[.__init__()_5]] - code - loki/core/action_router.py
- [[._handle_api_mock_generate()]] - code - loki/core/action_router.py
- [[._handle_app_close()]] - code - loki/core/action_router.py
- [[._handle_backup_file()]] - code - loki/core/action_router.py
- [[._handle_brightness_get()]] - code - loki/core/action_router.py
- [[._handle_brightness_set()]] - code - loki/core/action_router.py
- [[._handle_bullets_to_prose()]] - code - loki/core/action_router.py
- [[._handle_calendar_conflicts()]] - code - loki/core/action_router.py
- [[._handle_calendar_list()]] - code - loki/core/action_router.py
- [[._handle_calendar_suggest_slot()]] - code - loki/core/action_router.py
- [[._handle_citation_info()]] - code - loki/core/action_router.py
- [[._handle_citation_url()]] - code - loki/core/action_router.py
- [[._handle_clipboard_clear()]] - code - loki/core/action_router.py
- [[._handle_clipboard_show()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_start()]] - code - loki/core/action_router.py
- [[._handle_code_convert()]] - code - loki/core/action_router.py
- [[._handle_currency_convert()]] - code - loki/core/action_router.py
- [[._handle_deepfake_check()]] - code - loki/core/action_router.py
- [[._handle_expense_from_file()]] - code - loki/core/action_router.py
- [[._handle_expense_scan_folder()]] - code - loki/core/action_router.py
- [[._handle_fact_check()]] - code - loki/core/action_router.py
- [[._handle_file_read()]] - code - loki/core/action_router.py
- [[._handle_file_search()]] - code - loki/core/action_router.py
- [[._handle_focus_disable()]] - code - loki/core/action_router.py
- [[._handle_focus_enable()]] - code - loki/core/action_router.py
- [[._handle_folder_create()]] - code - loki/core/action_router.py
- [[._handle_footprint_full()]] - code - loki/core/action_router.py
- [[._handle_footprint_privacy()]] - code - loki/core/action_router.py
- [[._handle_git_status()]] - code - loki/core/action_router.py
- [[._handle_history_semantic()]] - code - loki/core/action_router.py
- [[._handle_history_stats()]] - code - loki/core/action_router.py
- [[._handle_install_package()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_dir()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_file()]] - code - loki/core/action_router.py
- [[._handle_kg_query()]] - code - loki/core/action_router.py
- [[._handle_meeting_action_items()]] - code - loki/core/action_router.py
- [[._handle_meeting_minutes()]] - code - loki/core/action_router.py
- [[._handle_news_briefing()]] - code - loki/core/action_router.py
- [[._handle_news_headlines()]] - code - loki/core/action_router.py
- [[._handle_process_list()]] - code - loki/core/action_router.py
- [[._handle_process_resume()]] - code - loki/core/action_router.py
- [[._handle_process_suspend()]] - code - loki/core/action_router.py
- [[._handle_process_triage()]] - code - loki/core/action_router.py
- [[._handle_screen_describe()]] - code - loki/core/action_router.py
- [[._handle_screen_translate()]] - code - loki/core/action_router.py
- [[._handle_screenshot_save()]] - code - loki/core/action_router.py
- [[._handle_system_monitor()]] - code - loki/core/action_router.py
- [[._handle_task_delete()]] - code - loki/core/action_router.py
- [[._handle_task_prioritize_ai()]] - code - loki/core/action_router.py
- [[._handle_text_change_tone()]] - code - loki/core/action_router.py
- [[._handle_text_expand()]] - code - loki/core/action_router.py
- [[._handle_text_polish()]] - code - loki/core/action_router.py
- [[._handle_text_translate()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_stop()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_mood()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_time()]] - code - loki/core/action_router.py
- [[._handle_ui_wallpaper()]] - code - loki/core/action_router.py
- [[._handle_undo()]] - code - loki/core/action_router.py
- [[._handle_unit_convert()]] - code - loki/core/action_router.py
- [[._handle_update_all()]] - code - loki/core/action_router.py
- [[._handle_vault_store()]] - code - loki/core/action_router.py
- [[._handle_volume_get()]] - code - loki/core/action_router.py
- [[._handle_watch_backup()]] - code - loki/core/action_router.py
- [[._handle_watch_stop()]] - code - loki/core/action_router.py
- [[._handle_web_summarize()]] - code - loki/core/action_router.py
- [[._handle_wifi_toggle()]] - code - loki/core/action_router.py
- [[._handle_window_layouts()]] - code - loki/core/action_router.py
- [[._handle_window_snap()]] - code - loki/core/action_router.py
- [[.register_action()]] - code - loki/core/action_router.py
- [[.register_feature()]] - code - loki/core/action_router.py
- [[.route_intent()]] - code - loki/core/action_router.py
- [[ActionRouter]] - code - loki/core/action_router.py
- [[Routes parsed intents to their corresponding action handlers.]] - rationale - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouter_/__handle_api_mock_generate_/__handle_app_close
SORT file.name ASC
```

## Connections to other communities
- 136 edges to [[_COMMUNITY__missing()  ._handle_api_mock_data()  ._handle_app_open()]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_action_router.py]]

## Top bridge nodes
- [[ActionRouter]] - degree 147, connects to 4 communities
- [[._handle_api_mock_generate()]] - degree 2, connects to 1 community
- [[._handle_app_close()]] - degree 2, connects to 1 community
- [[._handle_backup_file()]] - degree 2, connects to 1 community
- [[._handle_brightness_get()]] - degree 2, connects to 1 community