---
type: community
cohesion: 0.14
members: 17
---

# ClipboardSync / .start() / clipboard_sync.py

**Cohesion:** 0.14 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_25]] - code - loki/features/clipboard_sync.py
- [[._build_url()]] - code - loki/features/clipboard_sync.py
- [[.get_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.get_url()]] - code - loki/features/clipboard_sync.py
- [[.is_running()_1]] - code - loki/features/clipboard_sync.py
- [[.set_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.start()_1]] - code - loki/features/clipboard_sync.py
- [[.stop()_2]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync — expose clipboard over localhost HTTP for local browser access.]] - rationale - loki/features/clipboard_sync.py
- [[Get current clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Return the sync URL if running.]] - rationale - loki/features/clipboard_sync.py
- [[Set clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Start the clipboard sync HTTP server.]] - rationale - loki/features/clipboard_sync.py
- [[Stop the clipboard sync server.]] - rationale - loki/features/clipboard_sync.py
- [[_make_token()]] - code - loki/features/clipboard_sync.py
- [[clipboard_sync.py]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardSync_/_start_/_clipboard_syncpy
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_FakeTTS  TestClipboardSyncToken  TestTTSDrain]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY__Handler  ._check_token()  ._deny()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]

## Top bridge nodes
- [[ClipboardSync]] - degree 21, connects to 7 communities
- [[clipboard_sync.py]] - degree 4, connects to 1 community