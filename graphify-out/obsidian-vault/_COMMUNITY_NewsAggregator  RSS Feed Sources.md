---
type: community
cohesion: 1.00
members: 2
---

# NewsAggregator / RSS Feed Sources

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[NewsAggregator_1]] - code - loki/features/news_aggregator.py
- [[RSS Feed Sources]] - code - loki/features/news_aggregator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/NewsAggregator_/_RSS_Feed_Sources
SORT file.name ASC
```
