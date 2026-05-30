---
type: community
cohesion: 0.13
members: 23
---

# LokiBrain / DailyBriefing / CodeAssistant

**Cohesion:** 0.13 - loosely connected
**Members:** 23 nodes

## Members
- [[.__init__()_8]] - code - loki/core/brain.py
- [[._load_history()]] - code - loki/core/brain.py
- [[._log_provider_status()]] - code - loki/core/brain.py
- [[._warmup_ollama()]] - code - loki/core/brain.py
- [[.get_conversation_summary()]] - code - loki/core/brain.py
- [[.get_dismissal_message()]] - code - loki/core/brain.py
- [[.get_user_name()]] - code - loki/core/brain.py
- [[.parse_intent()]] - code - loki/core/brain.py
- [[.set_user_name()]] - code - loki/core/brain.py
- [[CalendarManager_1]] - code - loki/features/calendar_manager.py
- [[CitationGenerator_1]] - code - loki/features/citation_generator.py
- [[CodeAssistant_1]] - code - loki/features/code_assistant.py
- [[CurrencyConverter_1]] - code - loki/features/currency_converter.py
- [[DailyBriefing_1]] - code - loki/features/daily_briefing.py
- [[EmailDrafter_1]] - code - loki/features/email_drafter.py
- [[ExpenseTracker_1]] - code - loki/features/expense_tracker.py
- [[FactChecker_1]] - code - loki/features/fact_checker.py
- [[FileSearch_1]] - code - loki/features/file_search.py
- [[GhostWriter_1]] - code - loki/features/ghostwriter.py
- [[GrammarPolisher_1]] - code - loki/features/grammar_polisher.py
- [[KnowledgeGraph_1]] - code - loki/features/knowledge_graph.py
- [[LLM integration with KORTEX-style context engineering.      Provider priority (s]] - rationale - loki/core/brain.py
- [[LokiBrain]] - code - loki/core/brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/_DailyBriefing_/_CodeAssistant
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_._call_llm()  ._compress_old_turns()  ._save_history()]]
- 6 edges to [[_COMMUNITY_.ask()  ._build_messages()  ._get_kg_context()]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_GitHelper  GhostWriter  ._ask()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_Preview-First Pattern (pending_writ  WatchJob (polling thread, snapshot   No auto git add -A (only staged fil]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_ApiMocker  .generate_mock()  ._ask()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  ._execute_task()]]
- 1 edge to [[_COMMUNITY_CalendarManager  ._load_events()  calendar_manager.py]]
- 1 edge to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 1 edge to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 1 edge to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 1 edge to [[_COMMUNITY_DailyBriefing  .generate()  daily_briefing.py]]
- 1 edge to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 1 edge to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 1 edge to [[_COMMUNITY_ExpenseTracker  .extract_from_text()  .extract_from_file()]]
- 1 edge to [[_COMMUNITY_FactChecker  .check()  ._search_web()]]
- 1 edge to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 1 edge to [[_COMMUNITY_KnowledgeGraph  .ingest_file()  ._extract_entities()]]
- 1 edge to [[_COMMUNITY_MeetingTranscriber  .transcribe()  .extract_action_items()]]
- 1 edge to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 1 edge to [[_COMMUNITY_PhishingDetector  .analyze_email()  .analyze_url()]]
- 1 edge to [[_COMMUNITY_ScreenshotSearch  screenshot_search.py  _capture_screen()]]
- 1 edge to [[_COMMUNITY_SemanticBrowserHistory  ._read_history()  .semantic_search()]]
- 1 edge to [[_COMMUNITY_test_brain.py  brain()  test_clear_conversation()]]
- 1 edge to [[_COMMUNITY_MeetingTranscriber  PDFChat  PDFChat._extract_text]]
- 1 edge to [[_COMMUNITY_PhishingDetector  DeepfakeAI Media Detector  URLEmail Heuristic Engine]]
- 1 edge to [[_COMMUNITY_SemanticBrowserHistory  SQLite Browser History Reader]]

## Top bridge nodes
- [[LokiBrain]] - degree 65, connects to 29 communities
- [[CodeAssistant_1]] - degree 3, connects to 1 community