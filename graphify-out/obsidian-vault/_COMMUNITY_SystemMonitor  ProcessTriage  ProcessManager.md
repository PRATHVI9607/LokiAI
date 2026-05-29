---
type: community
cohesion: 0.40
members: 5
---

# SystemMonitor / ProcessTriage / ProcessManager

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[ProcessManager_1]] - code - loki/features/process_manager.py
- [[ProcessTriage_1]] - code - loki/features/process_triage.py
- [[Safe-to-Kill Process List]] - code - loki/features/process_triage.py
- [[SystemMonitor_1]] - code - loki/features/system_monitor.py
- [[nvidia-smi GPU Stats]] - code - loki/features/system_monitor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SystemMonitor_/_ProcessTriage_/_ProcessManager
SORT file.name ASC
```
