---
type: community
cohesion: 1.00
members: 2
---

# Brightness Control via screen_brigh / Requirement: screen-brightness-cont

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Brightness Control via screen_brightness_control]] - document - LokiPRD.md
- [[Requirement screen-brightness-control=0.22.0]] - document - loki/requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Brightness_Control_via_screen_brigh_/_Requirement_screen-brightness-cont
SORT file.name ASC
```
