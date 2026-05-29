---
type: community
cohesion: 0.23
members: 12
---

# CitationGenerator / ._format() / .from_url()

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[.__init__()_20]] - code - loki/features/citation_generator.py
- [[._ask()_1]] - code - loki/features/citation_generator.py
- [[._fetch_metadata()]] - code - loki/features/citation_generator.py
- [[._format()]] - code - loki/features/citation_generator.py
- [[.from_info()]] - code - loki/features/citation_generator.py
- [[.from_url()]] - code - loki/features/citation_generator.py
- [[CitationGenerator]] - code - loki/features/citation_generator.py
- [[CitationGenerator — produce APA, MLA, Chicago, IEEE citations from URLs or raw i]] - rationale - loki/features/citation_generator.py
- [[Extract title, author, date, site from a URL's meta tags.]] - rationale - loki/features/citation_generator.py
- [[Generate a citation from a URL.]] - rationale - loki/features/citation_generator.py
- [[Generate a citation from manually supplied info.]] - rationale - loki/features/citation_generator.py
- [[citation_generator.py]] - code - loki/features/citation_generator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CitationGenerator_/__format_/_from_url
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[CitationGenerator]] - degree 10, connects to 3 communities