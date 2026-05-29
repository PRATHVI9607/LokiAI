---
type: community
cohesion: 0.03
members: 73
---

# _missing() / ._handle_agent_cancel() / ._handle_agent_run()

**Cohesion:** 0.03 - loosely connected
**Members:** 73 nodes

## Members
- [[._handle_agent_cancel()]] - code - loki/core/action_router.py
- [[._handle_agent_run()]] - code - loki/core/action_router.py
- [[._handle_agent_status()]] - code - loki/core/action_router.py
- [[._handle_app_close()]] - code - loki/core/action_router.py
- [[._handle_backup_list()]] - code - loki/core/action_router.py
- [[._handle_brightness_get()]] - code - loki/core/action_router.py
- [[._handle_calendar_conflicts()]] - code - loki/core/action_router.py
- [[._handle_calendar_import()]] - code - loki/core/action_router.py
- [[._handle_calendar_list()]] - code - loki/core/action_router.py
- [[._handle_citation_info()]] - code - loki/core/action_router.py
- [[._handle_citation_url()]] - code - loki/core/action_router.py
- [[._handle_clipboard_clear()]] - code - loki/core/action_router.py
- [[._handle_clipboard_set()]] - code - loki/core/action_router.py
- [[._handle_clipboard_show()]] - code - loki/core/action_router.py
- [[._handle_clipboard_sync_stop()]] - code - loki/core/action_router.py
- [[._handle_code_convert()]] - code - loki/core/action_router.py
- [[._handle_code_refactor()]] - code - loki/core/action_router.py
- [[._handle_commit_message()]] - code - loki/core/action_router.py
- [[._handle_currency_convert()]] - code - loki/core/action_router.py
- [[._handle_declutter_dups()]] - code - loki/core/action_router.py
- [[._handle_declutter_old()]] - code - loki/core/action_router.py
- [[._handle_email_draft()]] - code - loki/core/action_router.py
- [[._handle_email_reply()]] - code - loki/core/action_router.py
- [[._handle_env_compose()]] - code - loki/core/action_router.py
- [[._handle_env_dockerfile()]] - code - loki/core/action_router.py
- [[._handle_env_venv()]] - code - loki/core/action_router.py
- [[._handle_expense_from_file()]] - code - loki/core/action_router.py
- [[._handle_expense_summary()]] - code - loki/core/action_router.py
- [[._handle_file_create()]] - code - loki/core/action_router.py
- [[._handle_file_delete()]] - code - loki/core/action_router.py
- [[._handle_file_search()]] - code - loki/core/action_router.py
- [[._handle_focus_disable()]] - code - loki/core/action_router.py
- [[._handle_folder_create()]] - code - loki/core/action_router.py
- [[._handle_footprint_network()]] - code - loki/core/action_router.py
- [[._handle_footprint_privacy()]] - code - loki/core/action_router.py
- [[._handle_footprint_tasks()]] - code - loki/core/action_router.py
- [[._handle_git_commit()]] - code - loki/core/action_router.py
- [[._handle_git_status()]] - code - loki/core/action_router.py
- [[._handle_history_search()]] - code - loki/core/action_router.py
- [[._handle_history_stats()]] - code - loki/core/action_router.py
- [[._handle_install_package()]] - code - loki/core/action_router.py
- [[._handle_kg_connections()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_dir()]] - code - loki/core/action_router.py
- [[._handle_kg_ingest_file()]] - code - loki/core/action_router.py
- [[._handle_media_info()]] - code - loki/core/action_router.py
- [[._handle_meeting_action_items()]] - code - loki/core/action_router.py
- [[._handle_meeting_minutes()]] - code - loki/core/action_router.py
- [[._handle_pdf_chat()]] - code - loki/core/action_router.py
- [[._handle_phishing_email()]] - code - loki/core/action_router.py
- [[._handle_process_kill()]] - code - loki/core/action_router.py
- [[._handle_process_list()]] - code - loki/core/action_router.py
- [[._handle_process_resume()]] - code - loki/core/action_router.py
- [[._handle_process_suspend()]] - code - loki/core/action_router.py
- [[._handle_readme_generate()]] - code - loki/core/action_router.py
- [[._handle_screen_capture()]] - code - loki/core/action_router.py
- [[._handle_screen_read()]] - code - loki/core/action_router.py
- [[._handle_screen_search()]] - code - loki/core/action_router.py
- [[._handle_shell()]] - code - loki/core/action_router.py
- [[._handle_sql_build()]] - code - loki/core/action_router.py
- [[._handle_system_monitor()]] - code - loki/core/action_router.py
- [[._handle_task_add()]] - code - loki/core/action_router.py
- [[._handle_task_complete()]] - code - loki/core/action_router.py
- [[._handle_task_list()]] - code - loki/core/action_router.py
- [[._handle_text_continue()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_mood()]] - code - loki/core/action_router.py
- [[._handle_ui_theme_time()]] - code - loki/core/action_router.py
- [[._handle_unit_convert()]] - code - loki/core/action_router.py
- [[._handle_update_all()]] - code - loki/core/action_router.py
- [[._handle_vault_store()]] - code - loki/core/action_router.py
- [[._handle_volume_get()]] - code - loki/core/action_router.py
- [[._handle_watch_backup()]] - code - loki/core/action_router.py
- [[._handle_window_tile_all()]] - code - loki/core/action_router.py
- [[_missing()]] - code - loki/core/action_router.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_missing_/__handle_agent_cancel_/__handle_agent_run
SORT file.name ASC
```

## Connections to other communities
- 139 edges to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_action_router.py  .route_intent()  _describe_destructive()]]

## Top bridge nodes
- [[_missing()]] - degree 140, connects to 2 communities
- [[._handle_agent_cancel()]] - degree 2, connects to 1 community
- [[._handle_agent_run()]] - degree 2, connects to 1 community
- [[._handle_agent_status()]] - degree 2, connects to 1 community
- [[._handle_app_close()]] - degree 2, connects to 1 community