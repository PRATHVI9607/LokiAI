---
type: community
cohesion: 0.22
members: 9
---

# SpeechListener / listener.py

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[.__init__()_9]] - code - loki/core/listener.py
- [[._listen_loop()]] - code - loki/core/listener.py
- [[._transcribe()]] - code - loki/core/listener.py
- [[.start_listening()]] - code - loki/core/listener.py
- [[.stop_listening()]] - code - loki/core/listener.py
- [[Listens to microphone, detects speech via VAD, transcribes with Whisper.]] - rationale - loki/core/listener.py
- [[Speech listener — microphone + VAD + Whisper STT.  Key fixes over the original]] - rationale - loki/core/listener.py
- [[SpeechListener]] - code - loki/core/listener.py
- [[listener.py]] - code - loki/core/listener.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SpeechListener_/_listenerpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[SpeechListener]] - degree 10, connects to 2 communities