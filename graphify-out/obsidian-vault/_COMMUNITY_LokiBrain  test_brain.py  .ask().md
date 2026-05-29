---
type: community
cohesion: 0.05
members: 59
---

# LokiBrain / test_brain.py / .ask()

**Cohesion:** 0.05 - loosely connected
**Members:** 59 nodes

## Members
- [[.__init__()_6]] - code - loki/core/brain.py
- [[._build_messages()]] - code - loki/core/brain.py
- [[._build_system_prompt()]] - code - loki/core/brain.py
- [[._call_llm()]] - code - loki/core/brain.py
- [[._compress_old_turns()]] - code - loki/core/brain.py
- [[._extract_facts()]] - code - loki/core/brain.py
- [[._get_kg_context()]] - code - loki/core/brain.py
- [[._get_rag_context()]] - code - loki/core/brain.py
- [[._load_history()]] - code - loki/core/brain.py
- [[._log_provider_status()]] - code - loki/core/brain.py
- [[._save_history()]] - code - loki/core/brain.py
- [[._store_turn()]] - code - loki/core/brain.py
- [[.ask()]] - code - loki/core/brain.py
- [[.clear_conversation()]] - code - loki/core/brain.py
- [[.get_conversation_summary()]] - code - loki/core/brain.py
- [[.get_dismissal_message()]] - code - loki/core/brain.py
- [[.get_user_name()]] - code - loki/core/brain.py
- [[.parse_intent()]] - code - loki/core/brain.py
- [[.set_user_name()]] - code - loki/core/brain.py
- [[Assemble context in priority order         1. System prompt (personality + brai]] - rationale - loki/core/brain.py
- [[CalendarManager_1]] - code - loki/features/calendar_manager.py
- [[CitationGenerator_1]] - code - loki/features/citation_generator.py
- [[CodeAssistant_1]] - code - loki/features/code_assistant.py
- [[CurrencyConverter_1]] - code - loki/features/currency_converter.py
- [[DailyBriefing_1]] - code - loki/features/daily_briefing.py
- [[DeepfakeAI Media Detector]] - code - loki/features/phishing_detector.py
- [[EmailDrafter_1]] - code - loki/features/email_drafter.py
- [[ExpenseTracker_1]] - code - loki/features/expense_tracker.py
- [[FactChecker_1]] - code - loki/features/fact_checker.py
- [[FileSearch_1]] - code - loki/features/file_search.py
- [[GhostWriter_1]] - code - loki/features/ghostwriter.py
- [[GrammarPolisher_1]] - code - loki/features/grammar_polisher.py
- [[KnowledgeGraph_1]] - code - loki/features/knowledge_graph.py
- [[LLM integration with KORTEX-style context engineering.     LLM priority Kimi K2]] - rationale - loki/core/brain.py
- [[Layer 3 knowledge graph entity lookup — structured relational context.]] - rationale - loki/core/brain.py
- [[Layer 4 ChromaDB semantic chunks from indexed files.]] - rationale - loki/core/brain.py
- [[Loki's brain — LLM integration with KORTEX-style context engineering.  LLM prior]] - rationale - loki/core/brain.py
- [[LokiBrain]] - code - loki/core/brain.py
- [[MeetingTranscriber_1]] - code - loki/features/meeting_transcriber.py
- [[PhishingDetector_1]] - code - loki/features/phishing_detector.py
- [[SQLite Browser History Reader]] - code - loki/features/semantic_browser_history.py
- [[ScreenshotSearch_1]] - code - loki/features/screenshot_search.py
- [[Secret Detection Regex Patterns]] - code - loki/features/security_scanner.py
- [[SecurityScanner_1]] - code - loki/features/security_scanner.py
- [[SemanticBrowserHistory_1]] - code - loki/features/semantic_browser_history.py
- [[Tesseract OCR (pytesseract fallback)]] - code - loki/features/screenshot_search.py
- [[TestBrain (test_brain.py)]] - code - loki/tests/test_brain.py
- [[URLEmail Heuristic Engine]] - code - loki/features/phishing_detector.py
- [[Whisper Model (shared)]] - code - loki/features/meeting_transcriber.py
- [[Windows WinRT OCR (PowerShell)]] - code - loki/features/screenshot_search.py
- [[brain()]] - code - loki/tests/test_brain.py
- [[brain.py]] - code - loki/core/brain.py
- [[test_brain.py]] - code - loki/tests/test_brain.py
- [[test_clear_conversation()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_invalid_returns_none()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_markdown_wrapped()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_missing_intent_key()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_plain_json()]] - code - loki/tests/test_brain.py
- [[test_store_turn()]] - code - loki/tests/test_brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/_test_brainpy_/_ask
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_Community 21]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_FakeTTS  ConvState  TestClipboardSyncToken]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_ApiMocker  .generate_mock()  ._ask()]]
- 1 edge to [[_COMMUNITY_AutoAgent  ._plan()  .cancel()]]
- 1 edge to [[_COMMUNITY_CalendarManager  ._load_events()  calendar_manager.py]]
- 1 edge to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 1 edge to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 1 edge to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 1 edge to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 1 edge to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 1 edge to [[_COMMUNITY_ExpenseTracker  .extract_from_text()  .extract_from_file()]]
- 1 edge to [[_COMMUNITY_FactChecker  .check()  ._search_web()]]
- 1 edge to [[_COMMUNITY_GhostWriter  ._ask()  .bullets_to_prose()]]
- 1 edge to [[_COMMUNITY_GitHelper  ._get_repo()  .commit()]]
- 1 edge to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 1 edge to [[_COMMUNITY_KnowledgeGraph  .ingest_file()  ._extract_entities()]]
- 1 edge to [[_COMMUNITY_MeetingTranscriber  .transcribe()  .extract_action_items()]]
- 1 edge to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 1 edge to [[_COMMUNITY_PhishingDetector  .analyze_email()  .analyze_url()]]
- 1 edge to [[_COMMUNITY_ScreenshotSearch  .capture_and_read()  _capture_screen()]]
- 1 edge to [[_COMMUNITY_SemanticBrowserHistory  ._read_history()  .semantic_search()]]
- 1 edge to [[_COMMUNITY_MessageBubble Component  useMemo Caching for renderMarkdown]]

## Top bridge nodes
- [[LokiBrain]] - degree 64, connects to 24 communities
- [[CodeAssistant_1]] - degree 3, connects to 1 community
- [[MeetingTranscriber_1]] - degree 3, connects to 1 community