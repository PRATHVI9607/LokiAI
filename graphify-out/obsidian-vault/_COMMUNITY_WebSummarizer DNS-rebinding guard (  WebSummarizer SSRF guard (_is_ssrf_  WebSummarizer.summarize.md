---
type: community
cohesion: 1.00
members: 3
---

# WebSummarizer DNS-rebinding guard ( / WebSummarizer SSRF guard (_is_ssrf_ / WebSummarizer.summarize

**Cohesion:** 1.00 - tightly connected
**Members:** 3 nodes

## Members
- [[WebSummarizer DNS-rebinding guard (_SSRFBlockingAdapter)]] - code - loki/features/web_summarizer.py
- [[WebSummarizer SSRF guard (_is_ssrf_risk)]] - code - loki/features/web_summarizer.py
- [[WebSummarizer.summarize]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WebSummarizer_DNS-rebinding_guard__/_WebSummarizer_SSRF_guard__is_ssrf__/_WebSummarizersummarize
SORT file.name ASC
```
