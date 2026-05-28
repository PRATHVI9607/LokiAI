---
type: community
cohesion: 0.33
members: 6
---

# ProcessManager / process_manager.py / .kill()

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[.kill()]] - code - loki/features/process_manager.py
- [[.list_processes()]] - code - loki/features/process_manager.py
- [[List and terminate processes with safety guards.]] - rationale - loki/features/process_manager.py
- [[Process manager — list and kill processes safely.]] - rationale - loki/features/process_manager.py
- [[ProcessManager]] - code - loki/features/process_manager.py
- [[process_manager.py]] - code - loki/features/process_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProcessManager_/_process_managerpy_/_kill
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[ProcessManager]] - degree 7, connects to 2 communities