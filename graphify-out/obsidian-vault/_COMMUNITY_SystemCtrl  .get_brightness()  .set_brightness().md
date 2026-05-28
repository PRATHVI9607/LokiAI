---
type: community
cohesion: 0.20
members: 11
---

# SystemCtrl / .get_brightness() / .set_brightness()

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_4]] - code - loki/actions/system_ctrl.py
- [[.get_brightness()]] - code - loki/actions/system_ctrl.py
- [[.get_volume()]] - code - loki/actions/system_ctrl.py
- [[.set_brightness()]] - code - loki/actions/system_ctrl.py
- [[.set_volume()]] - code - loki/actions/system_ctrl.py
- [[.toggle_bluetooth()]] - code - loki/actions/system_ctrl.py
- [[.toggle_wifi()]] - code - loki/actions/system_ctrl.py
- [[System controls — volume, brightness, WiFi, Bluetooth.]] - rationale - loki/actions/system_ctrl.py
- [[SystemCtrl]] - code - loki/actions/system_ctrl.py
- [[Windows system controls with undo support.]] - rationale - loki/actions/system_ctrl.py
- [[system_ctrl.py]] - code - loki/actions/system_ctrl.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SystemCtrl_/_get_brightness_/_set_brightness
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[SystemCtrl]] - degree 12, connects to 2 communities