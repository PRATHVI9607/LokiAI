---
type: community
cohesion: 0.29
members: 8
---

# SystemMonitor / ._get_gpu_stats() / .get_stats()

**Cohesion:** 0.29 - loosely connected
**Members:** 8 nodes

## Members
- [[.__init__()_46]] - code - loki/features/system_monitor.py
- [[._get_gpu_stats()]] - code - loki/features/system_monitor.py
- [[.get_stats()_2]] - code - loki/features/system_monitor.py
- [[.get_top_processes()]] - code - loki/features/system_monitor.py
- [[Real-time system resource monitoring.]] - rationale - loki/features/system_monitor.py
- [[System monitor — CPU, RAM, GPU, disk stats with alerting.]] - rationale - loki/features/system_monitor.py
- [[SystemMonitor]] - code - loki/features/system_monitor.py
- [[system_monitor.py]] - code - loki/features/system_monitor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SystemMonitor_/__get_gpu_stats_/_get_stats
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[SystemMonitor]] - degree 9, connects to 2 communities