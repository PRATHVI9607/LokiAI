---
type: community
cohesion: 0.50
members: 5
---

# ClipboardSync / ClipboardSync token auth pattern / ClipboardSync 127.0.0.1 loopback-on

**Cohesion:** 0.50 - moderately connected
**Members:** 5 nodes

## Members
- [[ClipboardManager_1]] - code - loki/features/clipboard_manager.py
- [[ClipboardSync_1]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync 127.0.0.1 loopback-only bind]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync _Handler]] - code - loki/features/clipboard_sync.py
- [[ClipboardSync token auth pattern]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardSync_/_ClipboardSync_token_auth_pattern_/_ClipboardSync_127001_loopback-on
SORT file.name ASC
```
