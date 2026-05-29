---
type: community
cohesion: 0.50
members: 4
---

# SystemMonitor / ProcessTriage / Safe-to-Kill Process List

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[ProcessTriage_1]] - code - loki/features/process_triage.py
- [[Safe-to-Kill Process List]] - code - loki/features/process_triage.py
- [[SystemMonitor_1]] - code - loki/features/system_monitor.py
- [[nvidia-smi GPU Stats]] - code - loki/features/system_monitor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SystemMonitor_/_ProcessTriage_/_Safe-to-Kill_Process_List
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication._init_all  LokiApplication._wire_callbacks  ConversationStateMachine]]

## Top bridge nodes
- [[SystemMonitor_1]] - degree 3, connects to 1 community