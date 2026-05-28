---
type: community
cohesion: 1.00
members: 2
---

# MediaConverter / ffmpeg External Tool

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[MediaConverter_1]] - code - loki/features/media_converter.py
- [[ffmpeg External Tool]] - code - loki/features/media_converter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MediaConverter_/_ffmpeg_External_Tool
SORT file.name ASC
```
