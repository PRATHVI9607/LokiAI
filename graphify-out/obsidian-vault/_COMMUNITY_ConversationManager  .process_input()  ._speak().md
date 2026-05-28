---
type: community
cohesion: 0.29
members: 12
---

# ConversationManager / .process_input() / ._speak()

**Cohesion:** 0.29 - loosely connected
**Members:** 12 nodes

## Members
- [[.__init__()]] - code - main.py
- [[._end_conversation()]] - code - main.py
- [[._handle_intent()]] - code - main.py
- [[._on_browser_message()]] - code - main.py
- [[._on_timeout()]] - code - main.py
- [[._on_wakeword()]] - code - main.py
- [[._reset_timeout()]] - code - main.py
- [[._speak()]] - code - main.py
- [[.process_input()]] - code - main.py
- [[.start_conversation()]] - code - main.py
- [[ConversationManager]] - code - main.py
- [[Orchestrates wakeword → listen → process → respond flow.]] - rationale - main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ConversationManager_/_process_input_/__speak
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 3 edges to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]
- 2 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 2 edges to [[_COMMUNITY_GitHelper  GhostWriter  ._ask()]]
- 1 edge to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 1 edge to [[_COMMUNITY_SpeechListener  listener.py]]
- 1 edge to [[_COMMUNITY_WakewordDetector  ._detect_loop()  ._is_wakeword()]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_generate()  ._handle_app_close()]]
- 1 edge to [[_COMMUNITY_UndoStack  ._builtin_undo()  undo_stack.py]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 1 edge to [[_COMMUNITY_RagEngine  rag_engine.py  .index_file()]]
- 1 edge to [[_COMMUNITY_SystemCtrl  .get_brightness()  .set_brightness()]]
- 1 edge to [[_COMMUNITY_AppCtrl  app_ctrl.py  .close_app()]]
- 1 edge to [[_COMMUNITY_BrowserCtrl  browser_ctrl.py  .open_url()]]
- 1 edge to [[_COMMUNITY_FileSearch  ._scan()  .search()]]
- 1 edge to [[_COMMUNITY_SystemMonitor  ._get_gpu_stats()  .get_stats()]]
- 1 edge to [[_COMMUNITY_ProcessManager  process_manager.py  .kill()]]
- 1 edge to [[_COMMUNITY_WebSummarizer  web_summarizer.py]]
- 1 edge to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 1 edge to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 1 edge to [[_COMMUNITY_FocusMode  ._unblock_sites()  ._block_sites()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]
- 1 edge to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 1 edge to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 1 edge to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 1 edge to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 1 edge to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 1 edge to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 1 edge to [[_COMMUNITY_DailyBriefing  .generate()  daily_briefing.py]]
- 1 edge to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 1 edge to [[_COMMUNITY_NewsAggregator  .get_headlines()  .get_briefing()]]
- 1 edge to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 1 edge to [[_COMMUNITY_MediaConverter  ._check_ffmpeg()  .convert()]]
- 1 edge to [[_COMMUNITY_DigitalDeclutter  .suggest_cleanup()  .find_duplicates()]]
- 1 edge to [[_COMMUNITY_BackupManager  .backup_directory()  .backup_file()]]
- 1 edge to [[_COMMUNITY_LokiTTS  SoftwareUpdater  ._run()]]
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
- 1 edge to [[_COMMUNITY_ClipboardSync  _Handler  clipboard_sync.py]]

## Top bridge nodes
- [[ConversationManager]] - degree 65, connects to 51 communities
- [[.process_input()]] - degree 6, connects to 1 community
- [[._on_browser_message()]] - degree 3, connects to 1 community
- [[._on_wakeword()]] - degree 2, connects to 1 community