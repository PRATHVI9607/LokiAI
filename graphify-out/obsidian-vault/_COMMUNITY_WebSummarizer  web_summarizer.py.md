---
type: community
cohesion: 0.33
members: 6
---

# WebSummarizer / web_summarizer.py

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[.__init__()_49]] - code - loki/features/web_summarizer.py
- [[.summarize()]] - code - loki/features/web_summarizer.py
- [[Fetch web pages and summarize their content.]] - rationale - loki/features/web_summarizer.py
- [[Web summarizer — fetch URL content and summarize via LLM.]] - rationale - loki/features/web_summarizer.py
- [[WebSummarizer]] - code - loki/features/web_summarizer.py
- [[web_summarizer.py]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WebSummarizer_/_web_summarizerpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[WebSummarizer]] - degree 8, connects to 3 communities