---
type: community
cohesion: 0.24
members: 12
---

# FocusMode / ._unblock_sites() / ._block_sites()

**Cohesion:** 0.24 - loosely connected
**Members:** 12 nodes

## Members
- [[.__init__()_38]] - code - loki/features/focus_mode.py
- [[._auto_disable()]] - code - loki/features/focus_mode.py
- [[._block_sites()]] - code - loki/features/focus_mode.py
- [[._flush_dns()]] - code - loki/features/focus_mode.py
- [[._unblock_sites()]] - code - loki/features/focus_mode.py
- [[.disable()]] - code - loki/features/focus_mode.py
- [[.enable()]] - code - loki/features/focus_mode.py
- [[Block distracting sites during focus sessions.]] - rationale - loki/features/focus_mode.py
- [[Focus mode — block distracting websites by modifying hosts file. Requires admin]] - rationale - loki/features/focus_mode.py
- [[FocusMode]] - code - loki/features/focus_mode.py
- [[focus_mode.py]] - code - loki/features/focus_mode.py
- [[is_active()_1]] - code - loki/features/focus_mode.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FocusMode_/__unblock_sites_/__block_sites
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[FocusMode]] - degree 11, connects to 1 community