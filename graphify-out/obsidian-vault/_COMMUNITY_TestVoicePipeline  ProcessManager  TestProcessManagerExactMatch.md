---
type: community
cohesion: 0.14
members: 20
---

# TestVoicePipeline / ProcessManager / TestProcessManagerExactMatch

**Cohesion:** 0.14 - loosely connected
**Members:** 20 nodes

## Members
- [[._make()]] - code - loki/tests/test_voice_and_security.py
- [[.kill()]] - code - loki/features/process_manager.py
- [[.list_processes()]] - code - loki/features/process_manager.py
- [[.test_activate_starts_wakeword()]] - code - loki/tests/test_voice_and_security.py
- [[.test_deactivate_stops_both()]] - code - loki/tests/test_voice_and_security.py
- [[.test_mute_stops_voice()]] - code - loki/tests/test_voice_and_security.py
- [[.test_nonexistent_returns_no_process()]] - code - loki/tests/test_voice_and_security.py
- [[.test_substring_returns_candidates_not_kills()]] - code - loki/tests/test_voice_and_security.py
- [[.test_transcript_callback_stops_listener()]] - code - loki/tests/test_voice_and_security.py
- [[.test_wakeword_callback_stops_wakeword_starts_listener()]] - code - loki/tests/test_voice_and_security.py
- [[Integration tests for voice lifecycle, TTS, confirmation flow, SSRF, and process]] - rationale - loki/tests/test_voice_and_security.py
- [[List and terminate processes with safety guards.]] - rationale - loki/features/process_manager.py
- [[Process manager — list and kill processes safely.  Kill by name requires an EXAC]] - rationale - loki/features/process_manager.py
- [[ProcessManager]] - code - loki/features/process_manager.py
- [[TestProcessManagerExactMatch]] - code - loki/tests/test_voice_and_security.py
- [[TestVoicePipeline]] - code - loki/tests/test_voice_and_security.py
- [[is_idle()_1]] - code - loki/tests/test_voice_and_security.py
- [[is_speaking()_1]] - code - loki/tests/test_voice_and_security.py
- [[process_manager.py]] - code - loki/features/process_manager.py
- [[test_voice_and_security.py]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestVoicePipeline_/_ProcessManager_/_TestProcessManagerExactMatch
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_FakeTTS  ConvState  conversation_sm.py]]
- 4 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 4 edges to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 4 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 4 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 3 edges to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 2 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 2 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 2 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 2 edges to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  AppCtrl  DailyBriefing]]

## Top bridge nodes
- [[TestVoicePipeline]] - degree 17, connects to 9 communities
- [[TestProcessManagerExactMatch]] - degree 13, connects to 9 communities
- [[ProcessManager]] - degree 16, connects to 8 communities
- [[test_voice_and_security.py]] - degree 11, connects to 6 communities
- [[._make()]] - degree 7, connects to 1 community