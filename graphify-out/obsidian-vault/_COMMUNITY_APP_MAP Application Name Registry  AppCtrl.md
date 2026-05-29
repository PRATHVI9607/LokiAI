---
type: community
cohesion: 1.00
members: 2
---

# APP_MAP Application Name Registry / AppCtrl

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[APP_MAP Application Name Registry]] - code - loki/actions/app_ctrl.py
- [[AppCtrl_1]] - code - loki/actions/app_ctrl.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/APP_MAP_Application_Name_Registry_/_AppCtrl
SORT file.name ASC
```
