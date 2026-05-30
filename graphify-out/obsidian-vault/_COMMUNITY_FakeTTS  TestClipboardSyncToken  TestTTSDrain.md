---
type: community
cohesion: 0.15
members: 17
---

# FakeTTS / TestClipboardSyncToken / TestTTSDrain

**Cohesion:** 0.15 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_56]] - code - loki/tests/test_voice_and_security.py
- [[.drain_and_fire()]] - code - loki/tests/test_voice_and_security.py
- [[.speak()_1]] - code - loki/tests/test_voice_and_security.py
- [[.stop()_4]] - code - loki/tests/test_voice_and_security.py
- [[.test_get_url_includes_token()]] - code - loki/tests/test_voice_and_security.py
- [[.test_is_idle_after_stop()]] - code - loki/tests/test_voice_and_security.py
- [[.test_start_generates_token()]] - code - loki/tests/test_voice_and_security.py
- [[.test_stop_drains_queue()]] - code - loki/tests/test_voice_and_security.py
- [[FakeTTS]] - code - loki/tests/test_voice_and_security.py
- [[Integration tests for voice lifecycle, TTS, confirmation flow, SSRF, and process]] - rationale - loki/tests/test_voice_and_security.py
- [[Minimal TTS stub for state-machine tests.]] - rationale - loki/tests/test_voice_and_security.py
- [[Simulate TTS finishing — drain queue and fire callback.]] - rationale - loki/tests/test_voice_and_security.py
- [[TestClipboardSyncToken]] - code - loki/tests/test_voice_and_security.py
- [[TestTTSDrain]] - code - loki/tests/test_voice_and_security.py
- [[is_idle()_1]] - code - loki/tests/test_voice_and_security.py
- [[is_speaking()_1]] - code - loki/tests/test_voice_and_security.py
- [[test_voice_and_security.py]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FakeTTS_/_TestClipboardSyncToken_/_TestTTSDrain
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 5 edges to [[_COMMUNITY_ClipboardSync  .start()  clipboard_sync.py]]
- 4 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 4 edges to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 4 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 3 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 3 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 3 edges to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 3 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 3 edges to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 2 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[FakeTTS]] - degree 17, connects to 11 communities
- [[TestClipboardSyncToken]] - degree 13, connects to 10 communities
- [[TestTTSDrain]] - degree 13, connects to 10 communities
- [[test_voice_and_security.py]] - degree 11, connects to 5 communities
- [[.test_stop_drains_queue()]] - degree 4, connects to 1 community