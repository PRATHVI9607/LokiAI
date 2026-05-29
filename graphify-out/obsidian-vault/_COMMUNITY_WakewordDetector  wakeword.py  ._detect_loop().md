---
type: community
cohesion: 0.22
members: 10
---

# WakewordDetector / wakeword.py / ._detect_loop()

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[.__init__()_16]] - code - loki/core/wakeword.py
- [[._detect_loop()]] - code - loki/core/wakeword.py
- [[._is_wakeword()]] - code - loki/core/wakeword.py
- [[.start()]] - code - loki/core/wakeword.py
- [[.stop()_1]] - code - loki/core/wakeword.py
- [[Detects 'Hey Loki' using a rolling audio buffer + Whisper tiny.en.]] - rationale - loki/core/wakeword.py
- [[Wakeword detector — rolling-window Whisper-based Hey Loki detection.  Key desi]] - rationale - loki/core/wakeword.py
- [[WakewordDetector]] - code - loki/core/wakeword.py
- [[is_running()]] - code - loki/core/wakeword.py
- [[wakeword.py]] - code - loki/core/wakeword.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WakewordDetector_/_wakewordpy_/__detect_loop
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]

## Top bridge nodes
- [[WakewordDetector]] - degree 10, connects to 2 communities