---
type: community
cohesion: 0.21
members: 14
---

# WindowTiler / .snap_window() / window_tiler.py

**Cohesion:** 0.21 - loosely connected
**Members:** 14 nodes

## Members
- [[._calc()]] - code - loki/features/window_tiler.py
- [[.list_layouts()]] - code - loki/features/window_tiler.py
- [[.snap_window()]] - code - loki/features/window_tiler.py
- [[.tile_all()]] - code - loki/features/window_tiler.py
- [[Find the first window whose title contains fragment (case-insensitive).]] - rationale - loki/features/window_tiler.py
- [[Return (left, top, right, bottom) of the primary monitor work area.]] - rationale - loki/features/window_tiler.py
- [[Snap the foreground (or named) window to a layout position.]] - rationale - loki/features/window_tiler.py
- [[Tile all visible non-minimized windows in a grid.]] - rationale - loki/features/window_tiler.py
- [[WindowTiler]] - code - loki/features/window_tiler.py
- [[WindowTiler — snap and tile application windows using Windows API (ctypes). No p]] - rationale - loki/features/window_tiler.py
- [[_get_work_area()]] - code - loki/features/window_tiler.py
- [[_hwnd_by_title()]] - code - loki/features/window_tiler.py
- [[_move_window()]] - code - loki/features/window_tiler.py
- [[window_tiler.py]] - code - loki/features/window_tiler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WindowTiler_/_snap_window_/_window_tilerpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[WindowTiler]] - degree 7, connects to 1 community