---
type: community
cohesion: 0.28
members: 9
---

# MediaConverter / ._check_ffmpeg() / .convert()

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_40]] - code - loki/features/media_converter.py
- [[._check_ffmpeg()]] - code - loki/features/media_converter.py
- [[.convert()_1]] - code - loki/features/media_converter.py
- [[.get_info()]] - code - loki/features/media_converter.py
- [[Convert a media file to a different format.]] - rationale - loki/features/media_converter.py
- [[Get media file metadata using ffprobe.]] - rationale - loki/features/media_converter.py
- [[MediaConverter]] - code - loki/features/media_converter.py
- [[MediaConverter — convert videoaudio files using ffmpeg. ffmpeg must be installe]] - rationale - loki/features/media_converter.py
- [[media_converter.py]] - code - loki/features/media_converter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MediaConverter_/__check_ffmpeg_/_convert
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]

## Top bridge nodes
- [[MediaConverter]] - degree 7, connects to 2 communities