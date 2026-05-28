---
type: community
cohesion: 1.00
members: 1
---

# Config: UI port=7777 timeout=30s

**Cohesion:** 1.00 - tightly connected
**Members:** 1 nodes

## Members
- [[Config UI port=7777 timeout=30s]] - document - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Config_UI_port7777_timeout30s
SORT file.name ASC
```
