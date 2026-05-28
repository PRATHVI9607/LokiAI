---
type: community
cohesion: 2.00
members: 2
---

# FocusMode / FootprintAuditor

**Cohesion:** 2.00 - tightly connected
**Members:** 2 nodes

## Members
- [[FocusMode_1]] - code - loki/features/focus_mode.py
- [[FootprintAuditor_1]] - code - loki/features/footprint_auditor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FocusMode_/_FootprintAuditor
SORT file.name ASC
```
