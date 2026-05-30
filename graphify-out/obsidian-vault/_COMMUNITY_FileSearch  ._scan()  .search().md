---
type: community
cohesion: 0.29
members: 10
---

# FileSearch / ._scan() / .search()

**Cohesion:** 0.29 - loosely connected
**Members:** 10 nodes

## Members
- [[.__init__()_35]] - code - loki/features/file_search.py
- [[._parse_query()]] - code - loki/features/file_search.py
- [[._scan()]] - code - loki/features/file_search.py
- [[._score_file()]] - code - loki/features/file_search.py
- [[.search()_1]] - code - loki/features/file_search.py
- [[FileSearch]] - code - loki/features/file_search.py
- [[Natural language file search — find files by name, content, type, date.]] - rationale - loki/features/file_search.py
- [[Search files using natural language queries.]] - rationale - loki/features/file_search.py
- [[_fmt_size()]] - code - loki/features/file_search.py
- [[file_search.py]] - code - loki/features/file_search.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileSearch_/__scan_/_search
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[FileSearch]] - degree 9, connects to 1 community