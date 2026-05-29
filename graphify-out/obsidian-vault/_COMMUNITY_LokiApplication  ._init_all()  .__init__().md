---
type: community
cohesion: 0.19
members: 15
---

# LokiApplication / ._init_all() / .__init__()

**Cohesion:** 0.19 - loosely connected
**Members:** 15 nodes

## Members
- [[.__init__()]] - code - main.py
- [[._init_all()]] - code - main.py
- [[._on_browser_message()]] - code - main.py
- [[._on_undo()]] - code - main.py
- [[._on_voice_transcript()]] - code - main.py
- [[._on_wakeword()]] - code - main.py
- [[._wire_callbacks()]] - code - main.py
- [[.run()]] - code - main.py
- [[.shutdown()]] - code - main.py
- [[Kill any process holding the given port so re-runs never fail with EADDRINUSE.]] - rationale - main.py
- [[LokiApplication]] - code - main.py
- [[Main application coordinator — FastAPI + uvicorn, no Qt.]] - rationale - main.py
- [[_free_port()]] - code - main.py
- [[main()]] - code - main.py
- [[main.py]] - code - main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiApplication_/__init_all_/___init__
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 2 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 2 edges to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 2 edges to [[_COMMUNITY_SpeechListener  ._transcribe_worker()  listener.py]]
- 2 edges to [[_COMMUNITY_WakewordDetector  wakeword.py  ._detect_loop()]]
- 2 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 2 edges to [[_COMMUNITY_UndoStack  ._builtin_undo()  undo_stack.py]]
- 2 edges to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 2 edges to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 2 edges to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 2 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 2 edges to [[_COMMUNITY_RagEngine  rag_engine.py  ._embed_batch()]]
- 2 edges to [[_COMMUNITY_SystemCtrl  .get_brightness()  .set_brightness()]]
- 2 edges to [[_COMMUNITY_AppCtrl  app_ctrl.py  .close_app()]]
- 2 edges to [[_COMMUNITY_BrowserCtrl  browser_ctrl.py  .open_url()]]
- 2 edges to [[_COMMUNITY_FileSearch  ._scan()  .search()]]
- 2 edges to [[_COMMUNITY_SystemMonitor  ._get_gpu_stats()  .get_stats()]]
- 2 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 2 edges to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 2 edges to [[_COMMUNITY_GitHelper  ._get_repo()  .commit()]]
- 2 edges to [[_COMMUNITY_FocusMode  ._unblock_sites()  ._block_sites()]]
- 2 edges to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 2 edges to [[_COMMUNITY_GhostWriter  ._ask()  .bullets_to_prose()]]
- 2 edges to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 2 edges to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 2 edges to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 2 edges to [[_COMMUNITY_DailyBriefing  .generate()  daily_briefing.py]]
- 2 edges to [[_COMMUNITY_FactChecker  .check()  ._search_web()]]
- 2 edges to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 2 edges to [[_COMMUNITY_NewsAggregator  .get_headlines()  .get_briefing()]]
- 2 edges to [[_COMMUNITY_ApiMocker  .generate_mock()  ._ask()]]
- 2 edges to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 2 edges to [[_COMMUNITY_MediaConverter  ._check_ffmpeg()  .convert()]]
- 2 edges to [[_COMMUNITY_DigitalDeclutter  .suggest_cleanup()  .find_duplicates()]]
- 2 edges to [[_COMMUNITY_BackupManager  .backup_directory()  .backup_file()]]
- 2 edges to [[_COMMUNITY_SoftwareUpdater  ._run()  ._check_winget()]]
- 2 edges to [[_COMMUNITY_WindowTiler  .snap_window()  window_tiler.py]]
- 2 edges to [[_COMMUNITY_ProcessTriage  .analyze()  ._snapshot()]]
- 2 edges to [[_COMMUNITY_PhishingDetector  .analyze_email()  .analyze_url()]]
- 2 edges to [[_COMMUNITY_KnowledgeGraph  .ingest_file()  ._extract_entities()]]
- 2 edges to [[_COMMUNITY_MeetingTranscriber  .transcribe()  .extract_action_items()]]
- 2 edges to [[_COMMUNITY_FootprintAuditor  .full_audit()  .audit_network_listeners()]]
- 2 edges to [[_COMMUNITY_SemanticBrowserHistory  ._read_history()  .semantic_search()]]
- 2 edges to [[_COMMUNITY_ScreenshotSearch  .capture_and_read()  _capture_screen()]]
- 2 edges to [[_COMMUNITY_CalendarManager  ._load_events()  calendar_manager.py]]
- 2 edges to [[_COMMUNITY_ExpenseTracker  .extract_from_text()  .extract_from_file()]]
- 2 edges to [[_COMMUNITY_DynamicUI  .apply_time_theme()  dynamic_ui.py]]
- 2 edges to [[_COMMUNITY_FileWatcher  WatchJob  .watch_custom()]]
- 2 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 2 edges to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_log_setup.py  setup_logging()  TerminalFormatter]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY_LokiServer  ._broadcast_sync()  ConnectionManager]]

## Top bridge nodes
- [[._init_all()]] - degree 61, connects to 58 communities
- [[LokiApplication]] - degree 69, connects to 56 communities
- [[.__init__()]] - degree 4, connects to 1 community