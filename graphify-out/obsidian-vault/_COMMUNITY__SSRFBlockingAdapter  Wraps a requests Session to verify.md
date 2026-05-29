---
type: community
cohesion: 1.00
members: 2
---

# _SSRFBlockingAdapter / Wraps a requests Session to verify 

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Wraps a requests Session to verify the connected peer IP after each request.]] - rationale - loki/features/web_summarizer.py
- [[_SSRFBlockingAdapter]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_SSRFBlockingAdapter_/_Wraps_a_requests_Session_to_verify_
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]

## Top bridge nodes
- [[_SSRFBlockingAdapter]] - degree 3, connects to 2 communities