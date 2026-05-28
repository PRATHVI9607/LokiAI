---
type: community
cohesion: 0.20
members: 17
---

# SemanticBrowserHistory / ._read_history() / .semantic_search()

**Cohesion:** 0.20 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_44]] - code - loki/features/semantic_browser_history.py
- [[._find_history_db()]] - code - loki/features/semantic_browser_history.py
- [[._llm()_6]] - code - loki/features/semantic_browser_history.py
- [[._read_history()]] - code - loki/features/semantic_browser_history.py
- [[.get_stats()_1]] - code - loki/features/semantic_browser_history.py
- [[.recent()]] - code - loki/features/semantic_browser_history.py
- [[.search()_2]] - code - loki/features/semantic_browser_history.py
- [[.semantic_search()]] - code - loki/features/semantic_browser_history.py
- [[Copy DB (Chrome locks it) and query visits.]] - rationale - loki/features/semantic_browser_history.py
- [[Keyword search over recent browser history.]] - rationale - loki/features/semantic_browser_history.py
- [[LLM-assisted semantic search — finds conceptually related pages.]] - rationale - loki/features/semantic_browser_history.py
- [[Return browsing stats for the last 30 days.]] - rationale - loki/features/semantic_browser_history.py
- [[SemanticBrowserHistory]] - code - loki/features/semantic_browser_history.py
- [[SemanticBrowserHistory — read ChromeEdge SQLite history and perform keyword or]] - rationale - loki/features/semantic_browser_history.py
- [[Show most recently visited pages.]] - rationale - loki/features/semantic_browser_history.py
- [[_chrome_ts_to_dt()]] - code - loki/features/semantic_browser_history.py
- [[semantic_browser_history.py]] - code - loki/features/semantic_browser_history.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SemanticBrowserHistory_/__read_history_/_semantic_search
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_LokiBrain  ApiMocker  FactChecker]]

## Top bridge nodes
- [[SemanticBrowserHistory]] - degree 13, connects to 3 communities