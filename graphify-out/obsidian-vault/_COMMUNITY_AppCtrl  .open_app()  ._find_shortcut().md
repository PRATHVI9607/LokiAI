---
type: community
cohesion: 0.24
members: 11
---

# AppCtrl / .open_app() / ._find_shortcut()

**Cohesion:** 0.24 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_1]] - code - loki/actions/app_ctrl.py
- [[._find_shortcut()]] - code - loki/actions/app_ctrl.py
- [[._try_startfile()]] - code - loki/actions/app_ctrl.py
- [[.close_app()]] - code - loki/actions/app_ctrl.py
- [[.open_app()]] - code - loki/actions/app_ctrl.py
- [[App control — open and close ANY application on the system.  Resolution order wh]] - rationale - loki/actions/app_ctrl.py
- [[AppCtrl]] - code - loki/actions/app_ctrl.py
- [[Fuzzy-match a Start-Menu .lnk by name (case-insensitive substring).]] - rationale - loki/actions/app_ctrl.py
- [[Open and close any application by name.]] - rationale - loki/actions/app_ctrl.py
- [[_which()]] - code - loki/actions/app_ctrl.py
- [[app_ctrl.py]] - code - loki/actions/app_ctrl.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AppCtrl_/_open_app_/__find_shortcut
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[AppCtrl]] - degree 9, connects to 1 community