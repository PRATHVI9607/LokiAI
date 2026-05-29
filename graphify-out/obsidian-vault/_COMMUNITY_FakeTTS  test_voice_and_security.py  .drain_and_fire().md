---
type: community
cohesion: 0.22
members: 9
---

# FakeTTS / test_voice_and_security.py / .drain_and_fire()

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_53]] - code - loki/tests/test_voice_and_security.py
- [[.drain_and_fire()]] - code - loki/tests/test_voice_and_security.py
- [[FakeTTS]] - code - loki/tests/test_voice_and_security.py
- [[Integration tests for voice lifecycle, TTS, confirmation flow, SSRF, and process]] - rationale - loki/tests/test_voice_and_security.py
- [[Minimal TTS stub for state-machine tests.]] - rationale - loki/tests/test_voice_and_security.py
- [[Simulate TTS finishing — drain queue and fire callback.]] - rationale - loki/tests/test_voice_and_security.py
- [[is_idle()_1]] - code - loki/tests/test_voice_and_security.py
- [[is_speaking()_1]] - code - loki/tests/test_voice_and_security.py
- [[test_voice_and_security.py]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FakeTTS_/_test_voice_and_securitypy_/_drain_and_fire
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 3 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[FakeTTS]] - degree 17, connects to 11 communities
- [[test_voice_and_security.py]] - degree 11, connects to 7 communities