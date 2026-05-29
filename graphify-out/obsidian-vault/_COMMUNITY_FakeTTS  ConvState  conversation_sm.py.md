---
type: community
cohesion: 0.20
members: 11
---

# FakeTTS / ConvState / conversation_sm.py

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_53]] - code - loki/tests/test_voice_and_security.py
- [[.drain_and_fire()]] - code - loki/tests/test_voice_and_security.py
- [[ConvState]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine — replaces the monolithic ConversationManager.  States]] - rationale - loki/core/conversation_sm.py
- [[Enum]] - code
- [[FakeTTS]] - code - loki/tests/test_voice_and_security.py
- [[Minimal TTS stub for state-machine tests.]] - rationale - loki/tests/test_voice_and_security.py
- [[Simulate TTS finishing — drain queue and fire callback.]] - rationale - loki/tests/test_voice_and_security.py
- [[conversation_sm.py]] - code - loki/core/conversation_sm.py
- [[is_active()]] - code - loki/core/conversation_sm.py
- [[state()]] - code - loki/core/conversation_sm.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FakeTTS_/_ConvState_/_conversation_smpy
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 4 edges to [[_COMMUNITY_TestVoicePipeline  ProcessManager  TestProcessManagerExactMatch]]
- 3 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 2 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 2 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 2 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  .__init__()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]

## Top bridge nodes
- [[FakeTTS]] - degree 17, connects to 10 communities
- [[ConvState]] - degree 14, connects to 9 communities
- [[conversation_sm.py]] - degree 6, connects to 1 community