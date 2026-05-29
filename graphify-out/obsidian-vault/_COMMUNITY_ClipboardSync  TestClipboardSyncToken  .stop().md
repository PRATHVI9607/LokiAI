---
type: community
cohesion: 0.12
members: 21
---

# ClipboardSync / TestClipboardSyncToken / .stop()

**Cohesion:** 0.12 - loosely connected
**Members:** 21 nodes

## Members
- [[.__init__()_23]] - code - loki/features/clipboard_sync.py
- [[._build_url()]] - code - loki/features/clipboard_sync.py
- [[.get_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.get_url()]] - code - loki/features/clipboard_sync.py
- [[.is_running()_1]] - code - loki/features/clipboard_sync.py
- [[.set_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.start()_1]] - code - loki/features/clipboard_sync.py
- [[.stop()_2]] - code - loki/features/clipboard_sync.py
- [[.stop()_4]] - code - loki/tests/test_voice_and_security.py
- [[.test_get_url_includes_token()]] - code - loki/tests/test_voice_and_security.py
- [[.test_start_generates_token()]] - code - loki/tests/test_voice_and_security.py
- [[ClipboardSync]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync — expose clipboard over localhost HTTP for local browser access.]] - rationale - loki/features/clipboard_sync.py
- [[Get current clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Return the sync URL if running.]] - rationale - loki/features/clipboard_sync.py
- [[Set clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Start the clipboard sync HTTP server.]] - rationale - loki/features/clipboard_sync.py
- [[Stop the clipboard sync server.]] - rationale - loki/features/clipboard_sync.py
- [[TestClipboardSyncToken]] - code - loki/tests/test_voice_and_security.py
- [[_make_token()]] - code - loki/features/clipboard_sync.py
- [[clipboard_sync.py]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardSync_/_TestClipboardSyncToken_/_stop
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY__Handler  ._check_token()  ._deny()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]

## Top bridge nodes
- [[TestClipboardSyncToken]] - degree 13, connects to 9 communities
- [[ClipboardSync]] - degree 21, connects to 6 communities
- [[.stop()_4]] - degree 5, connects to 1 community
- [[clipboard_sync.py]] - degree 4, connects to 1 community