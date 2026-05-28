---
type: community
cohesion: 0.33
members: 6
---

# DailyBriefing / .generate() / daily_briefing.py

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[.__init__()_22]] - code - loki/features/daily_briefing.py
- [[.generate()]] - code - loki/features/daily_briefing.py
- [[DailyBriefing]] - code - loki/features/daily_briefing.py
- [[DailyBriefing — morning brief combining tasks, system health, datetime, and new]] - rationale - loki/features/daily_briefing.py
- [[Generate a full daily briefing covering date, tasks, system, and news.]] - rationale - loki/features/daily_briefing.py
- [[daily_briefing.py]] - code - loki/features/daily_briefing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DailyBriefing_/_generate_/_daily_briefingpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[DailyBriefing]] - degree 7, connects to 3 communities