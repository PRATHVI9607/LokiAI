---
type: community
cohesion: 0.20
members: 16
---

# WebSummarizer / TestSSRFProtection / _is_ssrf_risk()

**Cohesion:** 0.20 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_53]] - code - loki/features/web_summarizer.py
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
- 5 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 2 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY__SSRFBlockingAdapter  Wraps a requests Session to verify]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]

## Top bridge nodes
- [[TestSSRFProtection]] - degree 16, connects to 9 communities
- [[WebSummarizer]] - degree 16, connects to 7 communities
- [[web_summarizer.py]] - degree 6, connects to 1 community