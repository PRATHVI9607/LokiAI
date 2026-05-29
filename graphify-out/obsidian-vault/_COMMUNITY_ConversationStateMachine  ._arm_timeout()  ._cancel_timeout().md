---
type: community
cohesion: 0.23
members: 15
---

# ConversationStateMachine / ._arm_timeout() / ._cancel_timeout()

**Cohesion:** 0.23 - loosely connected
**Members:** 15 nodes

## Members
- [[.__init__()_8]] - code - loki/core/conversation_sm.py
- [[._arm_timeout()]] - code - loki/core/conversation_sm.py
- [[._cancel_timeout()]] - code - loki/core/conversation_sm.py
- [[._emit_response()]] - code - loki/core/conversation_sm.py
- [[._handle_intent()]] - code - loki/core/conversation_sm.py
- [[._on_timeout()]] - code - loki/core/conversation_sm.py
- [[._process_worker()]] - code - loki/core/conversation_sm.py
- [[.end_conversation()]] - code - loki/core/conversation_sm.py
- [[.on_tts_done()]] - code - loki/core/conversation_sm.py
- [[.process_input()]] - code - loki/core/conversation_sm.py
- [[.start_conversation()]] - code - loki/core/conversation_sm.py
- [[Called by LokiApplication when TTS queue drains completely.]] - rationale - loki/core/conversation_sm.py
- [[ConversationStateMachine]] - code - loki/core/conversation_sm.py
- [[Immediately end (browser close, mute, etc.) — no farewell.]] - rationale - loki/core/conversation_sm.py
- [[Manages conversation state and drives LLMactionTTS flow.]] - rationale - loki/core/conversation_sm.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ConversationStateMachine_/__arm_timeout_/__cancel_timeout
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 2 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_AuditLog  .log()  ._rotate_if_needed()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ConversationStateMachine]] - degree 28, connects to 14 communities