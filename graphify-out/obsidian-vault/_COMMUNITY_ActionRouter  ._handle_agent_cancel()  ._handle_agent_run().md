---
type: community
cohesion: 0.03
members: 76
---

# ActionRouter / ._handle_agent_cancel() / ._handle_agent_run()

**Cohesion:** 0.03 - loosely connected
**Members:** 76 nodes

## Members
- [[._handle_agent_cancel()]] - code - loki/core/action_router.py
- [[._handle_agent_run()]] - code - loki/core/action_router.py
- [[._handle_agent_status()]] - code - loki/core/action_router.py
- [[._handle_api_mock_data()]] - code - loki/core/action_router.py
- [[._handle_backup_directory()]] - code - loki/core/action_router.py
- [[._handle_backup_list()]] - code - loki/core/action_router.py
- [[._handle_brightness_set()]] - code - loki/core/action_router.py
- [[._handle_browser_open()]] - code - loki/core/action_router.py
- [[._handle_browser_search()]] - code - loki/core/action_router.py
- [[._handle_calendar_conflicts()]] - code - loki/core/action_router.py
- [[._handle_citation_info()]] - code - loki/core/action_router.py
- [[._handle_citation_url()]] - code - loki/core/action_router.py
- [[._handle_clipboard_clear()]] - code - loki/core/action_router.py
- [[._handle_clipboard_show()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_stop()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_url()]] - code - loki/core/action_router.py
- [[._handle_code_analyze()]] - code - loki/core/action_router.py
- [[._handle_code_refactor()]] - code - loki/core/action_router.py
- [[._handle_commit_message()]] - code - loki/core/action_router.py
- [[._handle_computer_action()]] - code - loki/core/action_router.py
- [[._handle_computer_click_text()]] - code - loki/core/action_router.py
- [[._handle_computer_press()]] - code - loki/core/action_router.py
- [[._handle_computer_scroll()]] - code - loki/core/action_router.py
- [[._handle_declutter_dups()]] - code - loki/core/action_router.py
- [[._handle_declutter_suggest()]] - code - loki/core/action_router.py
- [[._handle_deepfake_check()]] - code - loki/core/action_router.py
- [[._handle_email_draft()]] - code - loki/core/action_router.py
- [[._handle_env_dockerfile()]] - code - loki/core/action_router.py
- [[._handle_expense_from_file()]] - code - loki/core/action_router.py
- [[._handle_fact_check()]] - code - loki/core/action_router.py
- [[._handle_file_move()]] - code - loki/core/action_router.py
- [[._handle_file_organize()]] - code - loki/core/action_router.py
- [[._handle_file_read()]] - code - loki/core/action_router.py
- [[._handle_file_search()]] - code - loki/core/action_router.py
- [[._handle_focus_enable()]] - code - loki/core/action_router.py
- [[._handle_footprint_privacy()]] - code - loki/core/action_router.py
- [[._handle_footprint_startup()]] - code - loki/core/action_router.py
- [[._handle_install_package()]] - code - loki/core/action_router.py
- [[._handle_kg_connections()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_file()]] - code - loki/core/action_router.py
- [[._handle_news_headlines()]] - code - loki/core/action_router.py
- [[._handle_pdf_chat()]] - code - loki/core/action_router.py
- [[._handle_phishing_email()]] - code - loki/core/action_router.py
- [[._handle_process_kill()]] - code - loki/core/action_router.py
- [[._handle_process_suspend()]] - code - loki/core/action_router.py
- [[._handle_process_triage()]] - code - loki/core/action_router.py
- [[._handle_regex_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_capture()]] - code - loki/core/action_router.py
- [[._handle_screen_describe()]] - code - loki/core/action_router.py
- [[._handle_screen_read()]] - code - loki/core/action_router.py
- [[._handle_screen_translate()]] - code - loki/core/action_router.py
- [[._handle_screenshot_save()]] - code - loki/core/action_router.py
- [[._handle_shell()]] - code - loki/core/action_router.py
- [[._handle_sql_build()]] - code - loki/core/action_router.py
- [[._handle_task_add()]] - code - loki/core/action_router.py
- [[._handle_task_complete()]] - code - loki/core/action_router.py
- [[._handle_task_delete()]] - code - loki/core/action_router.py
- [[._handle_text_continue()]] - code - loki/core/action_router.py
- [[._handle_text_expand()]] - code - loki/core/action_router.py
- [[._handle_text_polish()]] - code - loki/core/action_router.py
- [[._handle_text_translate()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_start()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_stop()]] - code - loki/core/action_router.py
- [[._handle_ui_wallpaper()]] - code - loki/core/action_router.py
- [[._handle_undo()]] - code - loki/core/action_router.py
- [[._handle_update_check()]] - code - loki/core/action_router.py
- [[._handle_volume_get()]] - code - loki/core/action_router.py
- [[._handle_watch_backup()]] - code - loki/core/action_router.py
- [[._handle_watch_list()]] - code - loki/core/action_router.py
- [[._handle_watch_media_inbox()]] - code - loki/core/action_router.py
- [[._handle_web_summarize()]] - code - loki/core/action_router.py
- [[._handle_window_snap()]] - code - loki/core/action_router.py
- [[.register_action()]] - code - loki/core/action_router.py
- [[.register_feature()]] - code - loki/core/action_router.py
- [[ActionRouter]] - code - loki/core/action_router.py
- [[Routes parsed intents to their corresponding action handlers.]] - rationale - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouter_/__handle_agent_cancel_/__handle_agent_run
SORT file.name ASC
```

## Connections to other communities
- 146 edges to [[_COMMUNITY__missing()  ._handle_api_mock_generate()  ._handle_app_close()]]
- 5 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 3 edges to [[_COMMUNITY_FakeTTS  TestClipboardSyncToken  TestTTSDrain]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  ._execute_task()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ActionRouter]] - degree 170, connects to 12 communities
- [[._handle_agent_cancel()]] - degree 2, connects to 1 community
- [[._handle_agent_run()]] - degree 2, connects to 1 community
- [[._handle_agent_status()]] - degree 2, connects to 1 community
- [[._handle_api_mock_data()]] - degree 2, connects to 1 community