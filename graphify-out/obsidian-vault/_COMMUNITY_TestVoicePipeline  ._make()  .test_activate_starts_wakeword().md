---
type: community
cohesion: 0.52
members: 7
---

# TestVoicePipeline / ._make() / .test_activate_starts_wakeword()

**Cohesion:** 0.52 - moderately connected
**Members:** 7 nodes

## Members
- [[._make()]] - code - loki/tests/test_voice_and_security.py
- [[.test_activate_starts_wakeword()]] - code - loki/tests/test_voice_and_security.py
- [[.test_deactivate_stops_both()]] - code - loki/tests/test_voice_and_security.py
- [[.test_mute_stops_voice()]] - code - loki/tests/test_voice_and_security.py
- [[.test_transcript_callback_stops_listener()]] - code - loki/tests/test_voice_and_security.py
- [[.test_wakeword_callback_stops_wakeword_starts_listener()]] - code - loki/tests/test_voice_and_security.py
- [[TestVoicePipeline]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestVoicePipeline_/__make_/_test_activate_starts_wakeword
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]

## Top bridge nodes
- [[TestVoicePipeline]] - degree 17, connects to 11 communities
- [[._make()]] - degree 7, connects to 1 community