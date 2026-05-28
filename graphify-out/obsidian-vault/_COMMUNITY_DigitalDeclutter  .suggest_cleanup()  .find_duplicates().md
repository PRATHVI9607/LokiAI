---
type: community
cohesion: 0.23
members: 12
---

# DigitalDeclutter / .suggest_cleanup() / .find_duplicates()

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[._hash_file()]] - code - loki/features/digital_declutter.py
- [[.find_duplicates()]] - code - loki/features/digital_declutter.py
- [[.find_large_files()]] - code - loki/features/digital_declutter.py
- [[.find_old_files()]] - code - loki/features/digital_declutter.py
- [[.suggest_cleanup()]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter]] - code - loki/features/digital_declutter.py
- [[DigitalDeclutter — find duplicate files, large files, oldunused files, and sugg]] - rationale - loki/features/digital_declutter.py
- [[Find duplicate files by MD5 hash.]] - rationale - loki/features/digital_declutter.py
- [[Find files larger than threshold_mb.]] - rationale - loki/features/digital_declutter.py
- [[Find files not accessed in the past N days.]] - rationale - loki/features/digital_declutter.py
- [[Run all checks and return a combined cleanup report.]] - rationale - loki/features/digital_declutter.py
- [[digital_declutter.py]] - code - loki/features/digital_declutter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DigitalDeclutter_/_suggest_cleanup_/_find_duplicates
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[DigitalDeclutter]] - degree 9, connects to 2 communities