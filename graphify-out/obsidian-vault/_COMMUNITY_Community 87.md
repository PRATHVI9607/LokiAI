---
type: community
cohesion: 1.00
members: 2
---

# Community 87

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Config Audio sample_rate=16000 vad_aggressiveness=1 silence_duration=1.0s]] - document - loki/config.yaml
- [[Rationale Silence Duration 1.0s (was 2.0s, felt laggy)]] - document - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_87
SORT file.name ASC
```
