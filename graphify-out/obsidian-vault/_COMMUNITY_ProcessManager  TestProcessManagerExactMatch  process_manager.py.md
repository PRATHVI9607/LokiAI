---
type: community
cohesion: 0.28
members: 9
---

# ProcessManager / TestProcessManagerExactMatch / process_manager.py

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.kill()]] - code - loki/features/process_manager.py
- [[.list_processes()]] - code - loki/features/process_manager.py
- [[.test_nonexistent_returns_no_process()]] - code - loki/tests/test_voice_and_security.py
- [[.test_substring_returns_candidates_not_kills()]] - code - loki/tests/test_voice_and_security.py
- [[List and terminate processes with safety guards.]] - rationale - loki/features/process_manager.py
- [[Process manager — list and kill processes safely.  Kill by name requires an EXAC]] - rationale - loki/features/process_manager.py
- [[ProcessManager]] - code - loki/features/process_manager.py
- [[TestProcessManagerExactMatch]] - code - loki/tests/test_voice_and_security.py
- [[process_manager.py]] - code - loki/features/process_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProcessManager_/_TestProcessManagerExactMatch_/_process_managerpy
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_FakeTTS  ConvState  TestClipboardSyncToken]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_status()]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  .start()  clipboard_sync.py]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[TestProcessManagerExactMatch]] - degree 13, connects to 9 communities
- [[ProcessManager]] - degree 16, connects to 7 communities