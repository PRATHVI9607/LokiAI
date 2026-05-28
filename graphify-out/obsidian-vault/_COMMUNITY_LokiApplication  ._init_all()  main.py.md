---
type: community
cohesion: 0.17
members: 16
---

# LokiApplication / ._init_all() / main.py

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_1]] - code - main.py
- [[._init_all()]] - code - main.py
- [[._on_conversation_ended()]] - code - main.py
- [[._on_mute()]] - code - main.py
- [[._on_speaking_stopped()]] - code - main.py
- [[._on_undo()]] - code - main.py
- [[._on_voice_transcript()]] - code - main.py
- [[._wire_callbacks()]] - code - main.py
- [[.run()]] - code - main.py
- [[.shutdown()]] - code - main.py
- [[LokiApplication]] - code - main.py
- [[Main application coordinator — FastAPI + uvicorn, no Qt.]] - rationale - main.py
- [[is_active()]] - code - main.py
- [[main()]] - code - main.py
- [[main.py]] - code - main.py
- [[setup_logging()]] - code - main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiApplication_/__init_all_/_mainpy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]
- 5 edges to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 4 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 4 edges to [[_COMMUNITY_GitHelper  GhostWriter  ._ask()]]
- 3 edges to [[_COMMUNITY_LokiTTS  SoftwareUpdater  ._run()]]
- 2 edges to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 2 edges to [[_COMMUNITY_SpeechListener  listener.py]]
- 2 edges to [[_COMMUNITY_WakewordDetector  ._detect_loop()  ._is_wakeword()]]
- 2 edges to [[_COMMUNITY_ActionRouter  ._handle_api_mock_generate()  ._handle_app_close()]]
- 2 edges to [[_COMMUNITY_UndoStack  ._builtin_undo()  undo_stack.py]]
- 2 edges to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 2 edges to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 2 edges to [[_COMMUNITY_RagEngine  rag_engine.py  .index_file()]]
- 2 edges to [[_COMMUNITY_SystemCtrl  .get_brightness()  .set_brightness()]]
- 2 edges to [[_COMMUNITY_AppCtrl  app_ctrl.py  .close_app()]]
- 2 edges to [[_COMMUNITY_BrowserCtrl  browser_ctrl.py  .open_url()]]
- 2 edges to [[_COMMUNITY_FileSearch  ._scan()  .search()]]
- 2 edges to [[_COMMUNITY_SystemMonitor  ._get_gpu_stats()  .get_stats()]]
- 2 edges to [[_COMMUNITY_ProcessManager  process_manager.py  .kill()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  web_summarizer.py]]
- 2 edges to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 2 edges to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 2 edges to [[_COMMUNITY_FocusMode  ._unblock_sites()  ._block_sites()]]
- 2 edges to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 2 edges to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 2 edges to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 2 edges to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 2 edges to [[_COMMUNITY_DailyBriefing  .generate()  daily_briefing.py]]
- 2 edges to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 2 edges to [[_COMMUNITY_NewsAggregator  .get_headlines()  .get_briefing()]]
- 2 edges to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 2 edges to [[_COMMUNITY_MediaConverter  ._check_ffmpeg()  .convert()]]
- 2 edges to [[_COMMUNITY_DigitalDeclutter  .suggest_cleanup()  .find_duplicates()]]
- 2 edges to [[_COMMUNITY_BackupManager  .backup_directory()  .backup_file()]]
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
- 2 edges to [[_COMMUNITY_ClipboardSync  _Handler  clipboard_sync.py]]
- 1 edge to [[_COMMUNITY_LokiServer  ._broadcast_sync()  ConnectionManager]]

## Top bridge nodes
- [[._init_all()]] - degree 59, connects to 52 communities
- [[LokiApplication]] - degree 69, connects to 51 communities
- [[main.py]] - degree 5, connects to 1 community
- [[._on_voice_transcript()]] - degree 2, connects to 1 community