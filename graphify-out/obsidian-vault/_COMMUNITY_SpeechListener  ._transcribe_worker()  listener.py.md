---
type: community
cohesion: 0.18
members: 12
---

# SpeechListener / ._transcribe_worker() / listener.py

**Cohesion:** 0.18 - loosely connected
**Members:** 12 nodes

## Members
- [[.__init__()_9]] - code - loki/core/listener.py
- [[._listen_loop()]] - code - loki/core/listener.py
- [[._transcribe()]] - code - loki/core/listener.py
- [[._transcribe_worker()]] - code - loki/core/listener.py
- [[.start_listening()]] - code - loki/core/listener.py
- [[.stop_listening()]] - code - loki/core/listener.py
- [[Drain the work queue and run Whisper on each frame list.         Completely sepa]] - rationale - loki/core/listener.py
- [[Listens to microphone, detects speech via VAD, transcribes with Whisper.]] - rationale - loki/core/listener.py
- [[Speech listener — microphone + VAD + Whisper STT.  Key design - Audio callback]] - rationale - loki/core/listener.py
- [[SpeechListener]] - code - loki/core/listener.py
- [[is_listening()]] - code - loki/core/listener.py
- [[listener.py]] - code - loki/core/listener.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SpeechListener_/__transcribe_worker_/_listenerpy
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]

## Top bridge nodes
- [[SpeechListener]] - degree 11, connects to 3 communities