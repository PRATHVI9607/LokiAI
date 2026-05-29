---
type: community
cohesion: 0.03
members: 73
---

# ActionRouter / ._handle_agent_cancel() / ._handle_agent_status()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[._handle_agent_cancel()]] - code - loki/core/action_router.py
- [[._handle_agent_status()]] - code - loki/core/action_router.py
- [[._handle_api_mock_generate()]] - code - loki/core/action_router.py
- [[._handle_app_open()]] - code - loki/core/action_router.py
- [[._handle_backup_file()]] - code - loki/core/action_router.py
- [[._handle_bluetooth_toggle()]] - code - loki/core/action_router.py
- [[._handle_brightness_get()]] - code - loki/core/action_router.py
- [[._handle_bullets_to_prose()]] - code - loki/core/action_router.py
- [[._handle_calendar_suggest_slot()]] - code - loki/core/action_router.py
- [[._handle_clipboard_clear()]] - code - loki/core/action_router.py
- [[._handle_clipboard_get()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_stop()]] - code - loki/core/action_router.py
- [[._handle_code_analyze()]] - code - loki/core/action_router.py
- [[._handle_code_convert()]] - code - loki/core/action_router.py
- [[._handle_code_refactor()]] - code - loki/core/action_router.py
- [[._handle_commit_message()]] - code - loki/core/action_router.py
- [[._handle_declutter_dups()]] - code - loki/core/action_router.py
- [[._handle_declutter_large()]] - code - loki/core/action_router.py
- [[._handle_env_compose()]] - code - loki/core/action_router.py
- [[._handle_env_dockerfile()]] - code - loki/core/action_router.py
- [[._handle_expense_from_file()]] - code - loki/core/action_router.py
- [[._handle_expense_scan_folder()]] - code - loki/core/action_router.py
- [[._handle_fact_check()]] - code - loki/core/action_router.py
- [[._handle_file_move()]] - code - loki/core/action_router.py
- [[._handle_file_organize()]] - code - loki/core/action_router.py
- [[._handle_file_read()]] - code - loki/core/action_router.py
- [[._handle_focus_disable()]] - code - loki/core/action_router.py
- [[._handle_folder_create()]] - code - loki/core/action_router.py
- [[._handle_folder_delete()]] - code - loki/core/action_router.py
- [[._handle_footprint_full()]] - code - loki/core/action_router.py
- [[._handle_footprint_network()]] - code - loki/core/action_router.py
- [[._handle_footprint_privacy()]] - code - loki/core/action_router.py
- [[._handle_footprint_startup()]] - code - loki/core/action_router.py
- [[._handle_git_commit()]] - code - loki/core/action_router.py
- [[._handle_git_status()]] - code - loki/core/action_router.py
- [[._handle_history_semantic()]] - code - loki/core/action_router.py
- [[._handle_history_stats()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_dir()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_file()]] - code - loki/core/action_router.py
- [[._handle_kg_stats()]] - code - loki/core/action_router.py
- [[._handle_media_convert()]] - code - loki/core/action_router.py
- [[._handle_meeting_summarize()]] - code - loki/core/action_router.py
- [[._handle_meeting_transcribe()]] - code - loki/core/action_router.py
- [[._handle_news_briefing()]] - code - loki/core/action_router.py
- [[._handle_phishing_email()]] - code - loki/core/action_router.py
- [[._handle_process_resume()]] - code - loki/core/action_router.py
- [[._handle_process_triage()]] - code - loki/core/action_router.py
- [[._handle_regex_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_read()]] - code - loki/core/action_router.py
- [[._handle_screen_search()]] - code - loki/core/action_router.py
- [[._handle_screen_translate()]] - code - loki/core/action_router.py
- [[._handle_screenshot_save()]] - code - loki/core/action_router.py
- [[._handle_sql_build()]] - code - loki/core/action_router.py
- [[._handle_task_delete()]] - code - loki/core/action_router.py
- [[._handle_task_list()]] - code - loki/core/action_router.py
- [[._handle_text_change_tone()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_start()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_mood()]] - code - loki/core/action_router.py
- [[._handle_undo()]] - code - loki/core/action_router.py
- [[._handle_unit_convert()]] - code - loki/core/action_router.py
- [[._handle_update_all()]] - code - loki/core/action_router.py
- [[._handle_update_check()]] - code - loki/core/action_router.py
- [[._handle_update_package()]] - code - loki/core/action_router.py
- [[._handle_vault_retrieve()]] - code - loki/core/action_router.py
- [[._handle_volume_set()]] - code - loki/core/action_router.py
- [[._handle_watch_backup()]] - code - loki/core/action_router.py
- [[._handle_wifi_toggle()]] - code - loki/core/action_router.py
- [[._handle_window_snap()]] - code - loki/core/action_router.py
- [[._handle_window_tile_all()]] - code - loki/core/action_router.py
- [[.register_action()]] - code - loki/core/action_router.py
- [[.register_feature()]] - code - loki/core/action_router.py
- [[ActionRouter]] - code - loki/core/action_router.py
- [[Routes parsed intents to their corresponding action handlers.]] - rationale - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouter_/__handle_agent_cancel_/__handle_agent_status
SORT file.name ASC
```

## Connections to other communities
- 139 edges to [[_COMMUNITY__missing()  ._handle_agent_run()  ._handle_api_mock_data()]]
- 5 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 4 edges to [[_COMMUNITY_FakeTTS  ConvState  TestClipboardSyncToken]]
- 2 edges to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ActionRouter]] - degree 163, connects to 12 communities
- [[._handle_agent_cancel()]] - degree 2, connects to 1 community
- [[._handle_agent_status()]] - degree 2, connects to 1 community
- [[._handle_api_mock_generate()]] - degree 2, connects to 1 community
- [[._handle_app_open()]] - degree 2, connects to 1 community