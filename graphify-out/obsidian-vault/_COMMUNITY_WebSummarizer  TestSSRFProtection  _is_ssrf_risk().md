---
type: community
cohesion: 0.17
members: 18
---

# WebSummarizer / TestSSRFProtection / _is_ssrf_risk()

**Cohesion:** 0.17 - loosely connected
**Members:** 18 nodes

## Members
- [[.__init__()_52]] - code - loki/features/web_summarizer.py
- [[.summarize()]] - code - loki/features/web_summarizer.py
- [[.test_file_scheme_blocked()]] - code - loki/tests/test_voice_and_security.py
- [[.test_localhost_blocked()]] - code - loki/tests/test_voice_and_security.py
- [[.test_private_ipv4_blocked()]] - code - loki/tests/test_voice_and_security.py
- [[.test_public_ip_allowed()]] - code - loki/tests/test_voice_and_security.py
- [[.test_summarizer_blocks_localhost()]] - code - loki/tests/test_voice_and_security.py
- [[Fetch web pages and summarize their content.]] - rationale - loki/features/web_summarizer.py
- [[Return True if the URL points to a privateinternal address (SSRF risk).]] - rationale - loki/features/web_summarizer.py
- [[TestSSRFProtection]] - code - loki/tests/test_voice_and_security.py
- [[Web summarizer — fetch URL content and summarize via LLM. SSRF guard rejects pr]] - rationale - loki/features/web_summarizer.py
- [[WebSummarizer]] - code - loki/features/web_summarizer.py
- [[Wraps a requests Session to verify the connected peer IP after each request.]] - rationale - loki/features/web_summarizer.py
- [[_SSRFBlockingAdapter]] - code - loki/features/web_summarizer.py
- [[_ip_is_internal()]] - code - loki/features/web_summarizer.py
- [[_is_ssrf_risk()]] - code - loki/features/web_summarizer.py
- [[check_response()]] - code - loki/features/web_summarizer.py
- [[web_summarizer.py]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WebSummarizer_/_TestSSRFProtection_/__is_ssrf_risk
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 2 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 2 edges to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 2 edges to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[WebSummarizer]] - degree 16, connects to 10 communities
- [[TestSSRFProtection]] - degree 16, connects to 10 communities
- [[_SSRFBlockingAdapter]] - degree 3, connects to 1 community