---
type: community
cohesion: 0.05
members: 52
---

# LokiBrain / ApiMocker / FactChecker

**Cohesion:** 0.05 - loosely connected
**Members:** 52 nodes

## Members
- [[.__init__()_7]] - code - loki/core/brain.py
- [[.__init__()_14]] - code - loki/features/api_mocker.py
- [[.__init__()_27]] - code - loki/features/fact_checker.py
- [[._ask()]] - code - loki/features/api_mocker.py
- [[._ask()_6]] - code - loki/features/fact_checker.py
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
- [[._search_web()]] - code - loki/features/fact_checker.py
- [[._store_turn()]] - code - loki/core/brain.py
- [[.ask()]] - code - loki/core/brain.py
- [[.check()]] - code - loki/features/fact_checker.py
- [[.clear_conversation()]] - code - loki/core/brain.py
- [[.generate_mock()]] - code - loki/features/api_mocker.py
- [[.generate_mock_data()]] - code - loki/features/api_mocker.py
- [[.get_conversation_summary()]] - code - loki/core/brain.py
- [[.get_dismissal_message()]] - code - loki/core/brain.py
- [[.get_user_name()]] - code - loki/core/brain.py
- [[.parse_intent()]] - code - loki/core/brain.py
- [[.set_user_name()]] - code - loki/core/brain.py
- [[ApiMocker]] - code - loki/features/api_mocker.py
- [[ApiMocker — generate mock REST API server code from a plain-English description.]] - rationale - loki/features/api_mocker.py
- [[Assemble context in priority order         1. System prompt (personality + brai]] - rationale - loki/core/brain.py
- [[FactChecker]] - code - loki/features/fact_checker.py
- [[FactChecker — verify claims by cross-referencing web sources and LLM reasoning.]] - rationale - loki/features/fact_checker.py
- [[Fetch snippets from DuckDuckGo HTML search.]] - rationale - loki/features/fact_checker.py
- [[Generate a mock API server from a description.]] - rationale - loki/features/api_mocker.py
- [[Generate mock JSON data matching a schema description.]] - rationale - loki/features/api_mocker.py
- [[LLM integration with KORTEX-style context engineering.     LLM priority Kimi K2]] - rationale - loki/core/brain.py
- [[Layer 3 knowledge graph entity lookup — structured relational context.]] - rationale - loki/core/brain.py
- [[Layer 4 ChromaDB semantic chunks from indexed files.]] - rationale - loki/core/brain.py
- [[Loki's brain — LLM integration with KORTEX-style context engineering.  LLM prior]] - rationale - loki/core/brain.py
- [[LokiBrain]] - code - loki/core/brain.py
- [[Verify a claim against web evidence and LLM reasoning.]] - rationale - loki/features/fact_checker.py
- [[api_mocker.py]] - code - loki/features/api_mocker.py
- [[brain()]] - code - loki/tests/test_brain.py
- [[brain.py]] - code - loki/core/brain.py
- [[fact_checker.py]] - code - loki/features/fact_checker.py
- [[test_brain.py]] - code - loki/tests/test_brain.py
- [[test_clear_conversation()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_invalid_returns_none()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_markdown_wrapped()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_missing_intent_key()]] - code - loki/tests/test_brain.py
- [[test_parse_intent_plain_json()]] - code - loki/tests/test_brain.py
- [[test_store_turn()]] - code - loki/tests/test_brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/_ApiMocker_/_FactChecker
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 3 edges to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 2 edges to [[_COMMUNITY_GitHelper  GhostWriter  ._ask()]]
- 1 edge to [[_COMMUNITY_CalendarManager  ._load_events()  calendar_manager.py]]
- 1 edge to [[_COMMUNITY_CitationGenerator  ._format()  .from_url()]]
- 1 edge to [[_COMMUNITY_CodeAssistant  ._ask()  ._require_brain()]]
- 1 edge to [[_COMMUNITY_CurrencyConverter  .convert_currency()  .convert_unit()]]
- 1 edge to [[_COMMUNITY_DailyBriefing  .generate()  daily_briefing.py]]
- 1 edge to [[_COMMUNITY_EmailDrafter  ._ask()  .draft()]]
- 1 edge to [[_COMMUNITY_EnvSetup  ._read_project_files()  ._ask()]]
- 1 edge to [[_COMMUNITY_ExpenseTracker  .extract_from_text()  .extract_from_file()]]
- 1 edge to [[_COMMUNITY_GrammarPolisher  ._ask()  .change_tone()]]
- 1 edge to [[_COMMUNITY_KnowledgeGraph  .ingest_file()  ._extract_entities()]]
- 1 edge to [[_COMMUNITY_MeetingTranscriber  .transcribe()  .extract_action_items()]]
- 1 edge to [[_COMMUNITY_PDFChat  .ask()  ._extract_text()]]
- 1 edge to [[_COMMUNITY_PhishingDetector  .analyze_email()  .analyze_url()]]
- 1 edge to [[_COMMUNITY_ScreenshotSearch  .capture_and_read()  _capture_screen()]]
- 1 edge to [[_COMMUNITY_SemanticBrowserHistory  ._read_history()  .semantic_search()]]
- 1 edge to [[_COMMUNITY_WebSummarizer  web_summarizer.py]]

## Top bridge nodes
- [[LokiBrain]] - degree 45, connects to 19 communities
- [[ApiMocker]] - degree 9, connects to 2 communities
- [[FactChecker]] - degree 9, connects to 2 communities