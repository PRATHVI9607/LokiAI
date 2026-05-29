---
type: community
cohesion: 0.32
members: 8
---

# NewsAggregator / .get_headlines() / .get_briefing()

**Cohesion:** 0.32 - loosely connected
**Members:** 8 nodes

## Members
- [[._fetch_feed()]] - code - loki/features/news_aggregator.py
- [[.get_briefing()]] - code - loki/features/news_aggregator.py
- [[.get_headlines()]] - code - loki/features/news_aggregator.py
- [[Fetch headlines across multiple topics for a morning briefing.]] - rationale - loki/features/news_aggregator.py
- [[Fetch top headlines for a category from RSS feeds.]] - rationale - loki/features/news_aggregator.py
- [[NewsAggregator]] - code - loki/features/news_aggregator.py
- [[NewsAggregator — pull headlines from RSS feeds, personalised by topic. No API ke]] - rationale - loki/features/news_aggregator.py
- [[news_aggregator.py]] - code - loki/features/news_aggregator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/NewsAggregator_/_get_headlines_/_get_briefing
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[NewsAggregator]] - degree 6, connects to 1 community