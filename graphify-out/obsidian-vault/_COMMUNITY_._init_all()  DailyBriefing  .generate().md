---
type: community
cohesion: 0.29
members: 7
---

# ._init_all() / DailyBriefing / .generate()

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[.__init__()_25]] - code - loki/features/daily_briefing.py
- [[._init_all()]] - code - main.py
- [[.generate()]] - code - loki/features/daily_briefing.py
- [[DailyBriefing]] - code - loki/features/daily_briefing.py
- [[DailyBriefing — morning brief combining tasks, system health, datetime, and new]] - rationale - loki/features/daily_briefing.py
- [[Generate a full daily briefing covering date, tasks, system, and news.]] - rationale - loki/features/daily_briefing.py
- [[daily_briefing.py]] - code - loki/features/daily_briefing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_init_all_/_DailyBriefing_/_generate
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 2 edges to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]
- 2 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_UndoStack  ._builtin_undo()  undo_stack.py]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 1 edge to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 1 edge to [[_COMMUNITY_RagEngine  rag_engine.py  .index_file()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY_LokiServer  ._broadcast_sync()  ConnectionManager]]
- 1 edge to [[_COMMUNITY_SystemCtrl  .get_brightness()  .set_brightness()]]
- 1 edge to [[_COMMUNITY_AppCtrl  app_ctrl.py  .close_app()]]
- 1 edge to [[_COMMUNITY_BrowserCtrl  browser_ctrl.py  .open_url()]]
- 1 edge to [[_COMMUNITY_FileSearch  ._scan()  .search()]]
- 1 edge to [[_COMMUNITY_SystemMonitor  ._get_gpu_stats()  .get_stats()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 1 edge to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 1 edge to [[_COMMUNITY_GitHelper  ._get_repo()  .commit()]]
- 1 edge to [[_COMMUNITY_FocusMode  ._unblock_sites()  ._block_sites()]]
- 1 edge to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]
- 1 edge to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 1 edge to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 1 edge to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 1 edge to [[_COMMUNITY_GhostWriter  ._ask()  .bullets_to_prose()]]
- 1 edge to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 1 edge to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 1 edge to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 1 edge to [[_COMMUNITY_FactChecker  .check()  ._search_web()]]
- 1 edge to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 1 edge to [[_COMMUNITY_NewsAggregator  .get_headlines()  .get_briefing()]]
- 1 edge to [[_COMMUNITY_ApiMocker  .generate_mock()  ._ask()]]
- 1 edge to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 1 edge to [[_COMMUNITY_MediaConverter  ._check_ffmpeg()  .convert()]]
- 1 edge to [[_COMMUNITY_DigitalDeclutter  .suggest_cleanup()  .find_duplicates()]]
- 1 edge to [[_COMMUNITY_BackupManager  .backup_directory()  .backup_file()]]
- 1 edge to [[_COMMUNITY_SoftwareUpdater  ._run()  ._check_winget()]]
- 1 edge to [[_COMMUNITY_WindowTiler  .snap_window()  window_tiler.py]]
- 1 edge to [[_COMMUNITY_ProcessTriage  .analyze()  ._snapshot()]]
- 1 edge to [[_COMMUNITY_PhishingDetector  .analyze_email()  .analyze_url()]]
- 1 edge to [[_COMMUNITY_KnowledgeGraph  .ingest_file()  ._extract_entities()]]
- 1 edge to [[_COMMUNITY_MeetingTranscriber  .transcribe()  .extract_action_items()]]
- 1 edge to [[_COMMUNITY_FootprintAuditor  .full_audit()  .audit_network_listeners()]]
- 1 edge to [[_COMMUNITY_SemanticBrowserHistory  ._read_history()  .semantic_search()]]
- 1 edge to [[_COMMUNITY_ScreenshotSearch  .capture_and_read()  _capture_screen()]]
- 1 edge to [[_COMMUNITY_CalendarManager  ._load_events()  calendar_manager.py]]
- 1 edge to [[_COMMUNITY_ExpenseTracker  .extract_from_text()  .extract_from_file()]]
- 1 edge to [[_COMMUNITY_DynamicUI  .apply_time_theme()  dynamic_ui.py]]
- 1 edge to [[_COMMUNITY_FileWatcher  WatchJob  .watch_custom()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  .start()  clipboard_sync.py]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_status()]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_WakewordDetector  wakeword.py  ._detect_loop()]]
- 1 edge to [[_COMMUNITY_SpeechListener  ._transcribe_worker()  listener.py]]

## Top bridge nodes
- [[._init_all()]] - degree 61, connects to 58 communities
- [[DailyBriefing]] - degree 6, connects to 2 communities