---
type: community
cohesion: 0.40
members: 6
---

# ConvState / conversation_sm.py / Enum

**Cohesion:** 0.40 - moderately connected
**Members:** 6 nodes

## Members
- [[ConvState]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine — replaces the monolithic ConversationManager.  States]] - rationale - loki/core/conversation_sm.py
- [[Enum]] - code
- [[conversation_sm.py]] - code - loki/core/conversation_sm.py
- [[is_active()]] - code - loki/core/conversation_sm.py
- [[state()]] - code - loki/core/conversation_sm.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ConvState_/_conversation_smpy_/_Enum
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ConvState]] - degree 14, connects to 11 communities
- [[conversation_sm.py]] - degree 6, connects to 1 community