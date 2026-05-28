---
type: community
cohesion: 2.00
members: 2
---

# ClipboardSync / ClipboardManager

**Cohesion:** 2.00 - tightly connected
**Members:** 2 nodes

## Members
- [[ClipboardManager_1]] - code - loki/features/clipboard_manager.py
- [[ClipboardSync_1]] - code - loki/features/clipboard_sync.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardSync_/_ClipboardManager
SORT file.name ASC
```
