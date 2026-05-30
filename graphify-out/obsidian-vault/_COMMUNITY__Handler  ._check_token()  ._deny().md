---
type: community
cohesion: 0.39
members: 8
---

# _Handler / ._check_token() / ._deny()

**Cohesion:** 0.39 - loosely connected
**Members:** 8 nodes

## Members
- [[._check_token()]] - code - loki/features/clipboard_sync.py
- [[._deny()_1]] - code - loki/features/clipboard_sync.py
- [[.do_GET()]] - code - loki/features/clipboard_sync.py
- [[.do_POST()]] - code - loki/features/clipboard_sync.py
- [[.log_message()]] - code - loki/features/clipboard_sync.py
- [[BaseHTTPRequestHandler]] - code
- [[Require t=token on every request.]] - rationale - loki/features/clipboard_sync.py
- [[_Handler]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_Handler_/__check_token_/__deny
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_ClipboardSync  .start()  clipboard_sync.py]]

## Top bridge nodes
- [[_Handler]] - degree 8, connects to 1 community