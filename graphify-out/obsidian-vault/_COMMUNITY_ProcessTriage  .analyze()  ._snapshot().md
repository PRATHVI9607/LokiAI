---
type: community
cohesion: 0.20
members: 12
---

# ProcessTriage / .analyze() / ._snapshot()

**Cohesion:** 0.20 - loosely connected
**Members:** 12 nodes

## Members
- [[._snapshot()]] - code - loki/features/process_triage.py
- [[.analyze()_1]] - code - loki/features/process_triage.py
- [[.resume_process()]] - code - loki/features/process_triage.py
- [[.suspend_process()]] - code - loki/features/process_triage.py
- [[.triage_for_app()]] - code - loki/features/process_triage.py
- [[Kill safe non-essential processes to free resources for app_name.]] - rationale - loki/features/process_triage.py
- [[ProcessTriage]] - code - loki/features/process_triage.py
- [[ProcessTriage — identify and optionally terminate resource-heavy background proc]] - rationale - loki/features/process_triage.py
- [[Resume a previously suspended process.]] - rationale - loki/features/process_triage.py
- [[Show top resource consumers and flag safe-to-kill candidates.]] - rationale - loki/features/process_triage.py
- [[Suspend (pause) a process by name or PID.]] - rationale - loki/features/process_triage.py
- [[process_triage.py]] - code - loki/features/process_triage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProcessTriage_/_analyze_/__snapshot
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[ProcessTriage]] - degree 9, connects to 2 communities