---
type: community
cohesion: 0.10
members: 20
---

# ClipboardSync / _Handler / clipboard_sync.py

**Cohesion:** 0.10 - loosely connected
**Members:** 20 nodes

## Members
- [[.__init__()_19]] - code - loki/features/clipboard_sync.py
- [[.do_GET()]] - code - loki/features/clipboard_sync.py
- [[.do_POST()]] - code - loki/features/clipboard_sync.py
- [[.get_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.get_url()]] - code - loki/features/clipboard_sync.py
- [[.is_running()]] - code - loki/features/clipboard_sync.py
- [[.log_message()]] - code - loki/features/clipboard_sync.py
- [[.set_clipboard()]] - code - loki/features/clipboard_sync.py
- [[.start()_1]] - code - loki/features/clipboard_sync.py
- [[.stop()_2]] - code - loki/features/clipboard_sync.py
- [[BaseHTTPRequestHandler]] - code
- [[ClipboardSync]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync — expose clipboard over localhost HTTP for local browser access.]] - rationale - loki/features/clipboard_sync.py
- [[Get current clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Return the sync URL if running.]] - rationale - loki/features/clipboard_sync.py
- [[Set clipboard content.]] - rationale - loki/features/clipboard_sync.py
- [[Start the clipboard sync HTTP server.]] - rationale - loki/features/clipboard_sync.py
- [[Stop the clipboard sync server.]] - rationale - loki/features/clipboard_sync.py
- [[_Handler]] - code - loki/features/clipboard_sync.py
- [[clipboard_sync.py]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardSync_/__Handler_/_clipboard_syncpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[ClipboardSync]] - degree 11, connects to 2 communities