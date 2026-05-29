---
type: community
cohesion: 0.03
members: 73
---

# ActionRouter / ._handle_agent_cancel() / ._handle_agent_run()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[._handle_agent_cancel()]] - code - loki/core/action_router.py
- [[._handle_agent_run()]] - code - loki/core/action_router.py
- [[._handle_agent_status()]] - code - loki/core/action_router.py
- [[._handle_api_mock_data()]] - code - loki/core/action_router.py
- [[._handle_app_close()]] - code - loki/core/action_router.py
- [[._handle_app_open()]] - code - loki/core/action_router.py
- [[._handle_backup_directory()]] - code - loki/core/action_router.py
- [[._handle_backup_file()]] - code - loki/core/action_router.py
- [[._handle_bluetooth_toggle()]] - code - loki/core/action_router.py
- [[._handle_brightness_set()]] - code - loki/core/action_router.py
- [[._handle_browser_search()]] - code - loki/core/action_router.py
- [[._handle_calendar_conflicts()]] - code - loki/core/action_router.py
- [[._handle_calendar_import()]] - code - loki/core/action_router.py
- [[._handle_calendar_list()]] - code - loki/core/action_router.py
- [[._handle_citation_info()]] - code - loki/core/action_router.py
- [[._handle_clipboard_clear()]] - code - loki/core/action_router.py
- [[._handle_commit_message()]] - code - loki/core/action_router.py
- [[._handle_daily_briefing()]] - code - loki/core/action_router.py
- [[._handle_deepfake_check()]] - code - loki/core/action_router.py
- [[._handle_env_venv()]] - code - loki/core/action_router.py
- [[._handle_expense_extract()]] - code - loki/core/action_router.py
- [[._handle_expense_list()]] - code - loki/core/action_router.py
- [[._handle_fact_check()]] - code - loki/core/action_router.py
- [[._handle_file_read()]] - code - loki/core/action_router.py
- [[._handle_focus_enable()]] - code - loki/core/action_router.py
- [[._handle_folder_create()]] - code - loki/core/action_router.py
- [[._handle_folder_delete()]] - code - loki/core/action_router.py
- [[._handle_footprint_full()]] - code - loki/core/action_router.py
- [[._handle_footprint_startup()]] - code - loki/core/action_router.py
- [[._handle_footprint_tasks()]] - code - loki/core/action_router.py
- [[._handle_git_status()]] - code - loki/core/action_router.py
- [[._handle_history_stats()]] - code - loki/core/action_router.py
- [[._handle_install_package()]] - code - loki/core/action_router.py
- [[._handle_kg_query()]] - code - loki/core/action_router.py
- [[._handle_kg_stats()]] - code - loki/core/action_router.py
- [[._handle_media_convert()]] - code - loki/core/action_router.py
- [[._handle_media_info()]] - code - loki/core/action_router.py
- [[._handle_meeting_summarize()]] - code - loki/core/action_router.py
- [[._handle_news_briefing()]] - code - loki/core/action_router.py
- [[._handle_phishing_email()]] - code - loki/core/action_router.py
- [[._handle_phishing_url()]] - code - loki/core/action_router.py
- [[._handle_process_list()]] - code - loki/core/action_router.py
- [[._handle_process_resume()]] - code - loki/core/action_router.py
- [[._handle_regex_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_read()]] - code - loki/core/action_router.py
- [[._handle_screen_search()]] - code - loki/core/action_router.py
- [[._handle_screen_translate()]] - code - loki/core/action_router.py
- [[._handle_shell()]] - code - loki/core/action_router.py
- [[._handle_sql_build()]] - code - loki/core/action_router.py
- [[._handle_task_complete()]] - code - loki/core/action_router.py
- [[._handle_task_prioritize_ai()]] - code - loki/core/action_router.py
- [[._handle_text_continue()]] - code - loki/core/action_router.py
- [[._handle_text_expand()]] - code - loki/core/action_router.py
- [[._handle_text_polish()]] - code - loki/core/action_router.py
- [[._handle_ui_auto_start()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_mood()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_time()]] - code - loki/core/action_router.py
- [[._handle_ui_wallpaper()]] - code - loki/core/action_router.py
- [[._handle_undo()]] - code - loki/core/action_router.py
- [[._handle_update_check()]] - code - loki/core/action_router.py
- [[._handle_update_package()]] - code - loki/core/action_router.py
- [[._handle_vault_retrieve()]] - code - loki/core/action_router.py
- [[._handle_vault_store()]] - code - loki/core/action_router.py
- [[._handle_volume_get()]] - code - loki/core/action_router.py
- [[._handle_volume_set()]] - code - loki/core/action_router.py
- [[._handle_watch_backup()]] - code - loki/core/action_router.py
- [[._handle_watch_list()]] - code - loki/core/action_router.py
- [[._handle_web_summarize()]] - code - loki/core/action_router.py
- [[._handle_wifi_toggle()]] - code - loki/core/action_router.py
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
- 139 edges to [[_COMMUNITY__missing()  ._handle_api_mock_generate()  ._handle_backup_list()]]
- 4 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 3 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]

## Top bridge nodes
- [[ActionRouter]] - degree 163, connects to 13 communities
- [[._handle_agent_cancel()]] - degree 2, connects to 1 community
- [[._handle_agent_run()]] - degree 2, connects to 1 community
- [[._handle_agent_status()]] - degree 2, connects to 1 community
- [[._handle_api_mock_data()]] - degree 2, connects to 1 community