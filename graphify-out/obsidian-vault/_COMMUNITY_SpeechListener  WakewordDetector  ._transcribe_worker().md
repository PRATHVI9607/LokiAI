---
type: community
cohesion: 0.10
members: 22
---

# SpeechListener / WakewordDetector / ._transcribe_worker()

**Cohesion:** 0.10 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_9]] - code - loki/core/listener.py
- [[.__init__()_15]] - code - loki/core/wakeword.py
- [[._detect_loop()]] - code - loki/core/wakeword.py
- [[._is_wakeword()]] - code - loki/core/wakeword.py
- [[._listen_loop()]] - code - loki/core/listener.py
- [[._transcribe()]] - code - loki/core/listener.py
- [[._transcribe_worker()]] - code - loki/core/listener.py
- [[.start()]] - code - loki/core/wakeword.py
- [[.start_listening()]] - code - loki/core/listener.py
- [[.stop()_1]] - code - loki/core/wakeword.py
- [[.stop_listening()]] - code - loki/core/listener.py
- [[Detects 'Hey Loki' wakeword using Whisper or Porcupine.]] - rationale - loki/core/wakeword.py
- [[Drain the work queue and run Whisper on each frame list.         Completely sepa]] - rationale - loki/core/listener.py
- [[Listens to microphone, detects speech via VAD, transcribes with Whisper.]] - rationale - loki/core/listener.py
- [[Speech listener — microphone + VAD + Whisper STT.  Key design - Audio callback]] - rationale - loki/core/listener.py
- [[SpeechListener]] - code - loki/core/listener.py
- [[Wakeword detector — Whisper-based Hey Loki detection. Porcupine is optional i]] - rationale - loki/core/wakeword.py
- [[WakewordDetector]] - code - loki/core/wakeword.py
- [[is_listening()]] - code - loki/core/listener.py
- [[is_running()]] - code - loki/core/wakeword.py
- [[listener.py]] - code - loki/core/listener.py
- [[wakeword.py]] - code - loki/core/wakeword.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SpeechListener_/_WakewordDetector_/__transcribe_worker
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 2 edges to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 2 edges to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]

## Top bridge nodes
- [[SpeechListener]] - degree 11, connects to 3 communities
- [[WakewordDetector]] - degree 10, connects to 3 communities