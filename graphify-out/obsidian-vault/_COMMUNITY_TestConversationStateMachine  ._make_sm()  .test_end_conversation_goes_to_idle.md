---
type: community
cohesion: 0.46
members: 8
---

# TestConversationStateMachine / ._make_sm() / .test_end_conversation_goes_to_idle

**Cohesion:** 0.46 - moderately connected
**Members:** 8 nodes

## Members
- [[._make_sm()]] - code - loki/tests/test_voice_and_security.py
- [[.test_end_conversation_goes_to_idle()]] - code - loki/tests/test_voice_and_security.py
- [[.test_initial_state_is_idle()]] - code - loki/tests/test_voice_and_security.py
- [[.test_on_tts_done_from_ending_fires_on_ended()]] - code - loki/tests/test_voice_and_security.py
- [[.test_process_input_goes_to_thinking()]] - code - loki/tests/test_voice_and_security.py
- [[.test_start_moves_to_listening()]] - code - loki/tests/test_voice_and_security.py
- [[.test_timeout_fires_farewell()]] - code - loki/tests/test_voice_and_security.py
- [[TestConversationStateMachine]] - code - loki/tests/test_voice_and_security.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestConversationStateMachine_/__make_sm_/_test_end_conversation_goes_to_idle
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 2 edges to [[_COMMUNITY_FakeTTS  TestClipboardSyncToken  TestTTSDrain]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  .start()  clipboard_sync.py]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]

## Top bridge nodes
- [[TestConversationStateMachine]] - degree 18, connects to 11 communities
- [[._make_sm()]] - degree 9, connects to 2 communities