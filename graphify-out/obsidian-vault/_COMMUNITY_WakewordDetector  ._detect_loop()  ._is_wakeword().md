---
type: community
cohesion: 0.25
members: 9
---

# WakewordDetector / ._detect_loop() / ._is_wakeword()

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_13]] - code - loki/core/wakeword.py
- [[._detect_loop()]] - code - loki/core/wakeword.py
- [[._is_wakeword()]] - code - loki/core/wakeword.py
- [[.start()]] - code - loki/core/wakeword.py
- [[.stop()_1]] - code - loki/core/wakeword.py
- [[Detects 'Hey Loki' wakeword using Whisper or Porcupine.]] - rationale - loki/core/wakeword.py
- [[Wakeword detector — Whisper-based Hey Loki detection. Porcupine is optional i]] - rationale - loki/core/wakeword.py
- [[WakewordDetector]] - code - loki/core/wakeword.py
- [[wakeword.py]] - code - loki/core/wakeword.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WakewordDetector_/__detect_loop_/__is_wakeword
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[WakewordDetector]] - degree 10, connects to 2 communities