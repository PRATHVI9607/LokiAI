---
type: community
cohesion: 0.03
members: 73
---

# ActionRouter / ._handle_api_mock_data() / ._handle_api_mock_generate()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[._handle_api_mock_data()]] - code - loki/core/action_router.py
- [[._handle_api_mock_generate()]] - code - loki/core/action_router.py
- [[._handle_app_open()]] - code - loki/core/action_router.py
- [[._handle_backup_directory()]] - code - loki/core/action_router.py
- [[._handle_backup_file()]] - code - loki/core/action_router.py
- [[._handle_bluetooth_toggle()]] - code - loki/core/action_router.py
- [[._handle_brightness_set()]] - code - loki/core/action_router.py
- [[._handle_browser_open()]] - code - loki/core/action_router.py
- [[._handle_browser_search()]] - code - loki/core/action_router.py
- [[._handle_bullets_to_prose()]] - code - loki/core/action_router.py
- [[._handle_calendar_suggest_slot()]] - code - loki/core/action_router.py
- [[._handle_clipboard_get()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_start()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_url()]] - code - loki/core/action_router.py
- [[._handle_code_analyze()]] - code - loki/core/action_router.py
- [[._handle_daily_briefing()]] - code - loki/core/action_router.py
- [[._handle_declutter_large()]] - code - loki/core/action_router.py
- [[._handle_declutter_suggest()]] - code - loki/core/action_router.py
- [[._handle_deepfake_check()]] - code - loki/core/action_router.py
- [[._handle_expense_extract()]] - code - loki/core/action_router.py
- [[._handle_expense_list()]] - code - loki/core/action_router.py
- [[._handle_expense_scan_folder()]] - code - loki/core/action_router.py
- [[._handle_fact_check()]] - code - loki/core/action_router.py
- [[._handle_file_move()]] - code - loki/core/action_router.py
- [[._handle_file_organize()]] - code - loki/core/action_router.py
- [[._handle_file_read()]] - code - loki/core/action_router.py
- [[._handle_focus_enable()]] - code - loki/core/action_router.py
- [[._handle_folder_delete()]] - code - loki/core/action_router.py
- [[._handle_footprint_full()]] - code - loki/core/action_router.py
- [[._handle_footprint_startup()]] - code - loki/core/action_router.py
- [[._handle_history_recent()]] - code - loki/core/action_router.py
- [[._handle_history_semantic()]] - code - loki/core/action_router.py
- [[._handle_kg_query()]] - code - loki/core/action_router.py
- [[._handle_kg_stats()]] - code - loki/core/action_router.py
- [[._handle_media_convert()]] - code - loki/core/action_router.py
- [[._handle_meeting_summarize()]] - code - loki/core/action_router.py
- [[._handle_meeting_transcribe()]] - code - loki/core/action_router.py
- [[._handle_news_briefing()]] - code - loki/core/action_router.py
- [[._handle_news_headlines()]] - code - loki/core/action_router.py
- [[._handle_phishing_url()]] - code - loki/core/action_router.py
- [[._handle_process_analyze()]] - code - loki/core/action_router.py
- [[._handle_process_triage()]] - code - loki/core/action_router.py
- [[._handle_regex_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_describe()]] - code - loki/core/action_router.py
- [[._handle_screen_translate()]] - code - loki/core/action_router.py
- [[._handle_screenshot_save()]] - code - loki/core/action_router.py
- [[._handle_security_scan()]] - code - loki/core/action_router.py
- [[._handle_task_delete()]] - code - loki/core/action_router.py
- [[._handle_task_prioritize_ai()]] - code - loki/core/action_router.py
- [[._handle_text_change_tone()]] - code - loki/core/action_router.py
- [[._handle_text_expand()]] - code - loki/core/action_router.py
- [[._handle_text_polish()]] - code - loki/core/action_router.py
- [[._handle_text_translate()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_start()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_stop()]] - code - loki/core/action_router.py
- [[._handle_ui_list_themes()]] - code - loki/core/action_router.py
- [[._handle_ui_wallpaper()]] - code - loki/core/action_router.py
- [[._handle_undo()]] - code - loki/core/action_router.py
- [[._handle_update_check()]] - code - loki/core/action_router.py
- [[._handle_update_package()]] - code - loki/core/action_router.py
- [[._handle_vault_retrieve()]] - code - loki/core/action_router.py
- [[._handle_volume_set()]] - code - loki/core/action_router.py
- [[._handle_watch_list()]] - code - loki/core/action_router.py
- [[._handle_watch_media_inbox()]] - code - loki/core/action_router.py
- [[._handle_watch_stop()]] - code - loki/core/action_router.py
- [[._handle_web_summarize()]] - code - loki/core/action_router.py
- [[._handle_wifi_toggle()]] - code - loki/core/action_router.py
- [[._handle_window_layouts()]] - code - loki/core/action_router.py
- [[._handle_window_snap()]] - code - loki/core/action_router.py
- [[.register_action()]] - code - loki/core/action_router.py
- [[.register_feature()]] - code - loki/core/action_router.py
- [[ActionRouter]] - code - loki/core/action_router.py
- [[Routes parsed intents to their corresponding action handlers.]] - rationale - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouter_/__handle_api_mock_data_/__handle_api_mock_generate
SORT file.name ASC
```

## Connections to other communities
- 139 edges to [[_COMMUNITY__missing()  ._handle_agent_cancel()  ._handle_agent_run()]]
- 5 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 1 edge to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ActionRouter]] - degree 163, connects to 15 communities
- [[._handle_api_mock_data()]] - degree 2, connects to 1 community
- [[._handle_api_mock_generate()]] - degree 2, connects to 1 community
- [[._handle_app_open()]] - degree 2, connects to 1 community
- [[._handle_backup_directory()]] - degree 2, connects to 1 community