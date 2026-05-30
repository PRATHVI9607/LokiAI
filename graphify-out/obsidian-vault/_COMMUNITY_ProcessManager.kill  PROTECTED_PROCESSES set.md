---
type: community
cohesion: 1.00
members: 2
---

# ProcessManager.kill / PROTECTED_PROCESSES set

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[PROTECTED_PROCESSES set]] - code - loki/features/process_manager.py
- [[ProcessManager.kill]] - code - loki/features/process_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProcessManagerkill_/_PROTECTED_PROCESSES_set
SORT file.name ASC
```
