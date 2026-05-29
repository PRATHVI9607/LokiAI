---
type: community
cohesion: 0.11
members: 22
---

# FakeTTS / ProcessManager / TestProcessManagerExactMatch

**Cohesion:** 0.11 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_54]] - code - loki/tests/test_voice_and_security.py
- [[.drain_and_fire()]] - code - loki/tests/test_voice_and_security.py
- [[.kill()]] - code - loki/features/process_manager.py
- [[.list_processes()]] - code - loki/features/process_manager.py
- [[.speak()_1]] - code - loki/tests/test_voice_and_security.py
- [[.test_is_idle_after_stop()]] - code - loki/tests/test_voice_and_security.py
- [[.test_nonexistent_returns_no_process()]] - code - loki/tests/test_voice_and_security.py
- [[.test_stop_drains_queue()]] - code - loki/tests/test_voice_and_security.py
- [[.test_substring_returns_candidates_not_kills()]] - code - loki/tests/test_voice_and_security.py
- [[FakeTTS]] - code - loki/tests/test_voice_and_security.py
- [[Integration tests for voice lifecycle, TTS, confirmation flow, SSRF, and process]] - rationale - loki/tests/test_voice_and_security.py
- [[List and terminate processes with safety guards.]] - rationale - loki/features/process_manager.py
- [[Minimal TTS stub for state-machine tests.]] - rationale - loki/tests/test_voice_and_security.py
- [[Process manager — list and kill processes safely.  Kill by name requires an EXAC]] - rationale - loki/features/process_manager.py
- [[ProcessManager]] - code - loki/features/process_manager.py
- [[Simulate TTS finishing — drain queue and fire callback.]] - rationale - loki/tests/test_voice_and_security.py
- [[TestProcessManagerExactMatch]] - code - loki/tests/test_voice_and_security.py
- [[TestTTSDrain]] - code - loki/tests/test_voice_and_security.py
- [[is_idle()_1]] - code - loki/tests/test_voice_and_security.py
- [[is_speaking()_1]] - code - loki/tests/test_voice_and_security.py
- [[process_manager.py]] - code - loki/features/process_manager.py
- [[test_voice_and_security.py]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FakeTTS_/_ProcessManager_/_TestProcessManagerExactMatch
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 5 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 5 edges to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 5 edges to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 5 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 3 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 3 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 3 edges to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 3 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 3 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[FakeTTS]] - degree 17, connects to 10 communities
- [[TestProcessManagerExactMatch]] - degree 13, connects to 9 communities
- [[TestTTSDrain]] - degree 13, connects to 9 communities
- [[ProcessManager]] - degree 16, connects to 6 communities
- [[test_voice_and_security.py]] - degree 11, connects to 5 communities