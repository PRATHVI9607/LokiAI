---
type: community
cohesion: 1.00
members: 2
---

# Community 88

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Config min_audio_seconds=0.35 (prevent Whisper hallucinations on short clips)]] - document - loki/config.yaml
- [[Rationale Min Audio Clip 0.35s (shorter clips cause Whisper hallucinations)]] - document - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_88
SORT file.name ASC
```
