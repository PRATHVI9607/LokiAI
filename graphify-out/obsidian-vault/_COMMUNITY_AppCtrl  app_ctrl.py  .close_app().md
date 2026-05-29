---
type: community
cohesion: 0.33
members: 6
---

# AppCtrl / app_ctrl.py / .close_app()

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[.close_app()]] - code - loki/actions/app_ctrl.py
- [[.open_app()]] - code - loki/actions/app_ctrl.py
- [[App control — open and close applications.]] - rationale - loki/actions/app_ctrl.py
- [[AppCtrl]] - code - loki/actions/app_ctrl.py
- [[Open and close applications by name.]] - rationale - loki/actions/app_ctrl.py
- [[app_ctrl.py]] - code - loki/actions/app_ctrl.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AppCtrl_/_app_ctrlpy_/_close_app
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]

## Top bridge nodes
- [[AppCtrl]] - degree 6, connects to 2 communities