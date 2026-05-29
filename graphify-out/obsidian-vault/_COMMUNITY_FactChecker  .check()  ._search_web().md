---
type: community
cohesion: 0.28
members: 9
---

# FactChecker / .check() / ._search_web()

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_31]] - code - loki/features/fact_checker.py
- [[._ask()_6]] - code - loki/features/fact_checker.py
- [[._search_web()]] - code - loki/features/fact_checker.py
- [[.check()]] - code - loki/features/fact_checker.py
- [[FactChecker]] - code - loki/features/fact_checker.py
- [[FactChecker — verify claims by cross-referencing web sources and LLM reasoning.]] - rationale - loki/features/fact_checker.py
- [[Fetch snippets from DuckDuckGo HTML search.]] - rationale - loki/features/fact_checker.py
- [[Verify a claim against web evidence and LLM reasoning.]] - rationale - loki/features/fact_checker.py
- [[fact_checker.py]] - code - loki/features/fact_checker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FactChecker_/_check_/__search_web
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[FactChecker]] - degree 8, connects to 2 communities