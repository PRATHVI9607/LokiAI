---
type: community
cohesion: 0.22
members: 11
---

# SpeechListener / VoicePipeline / SpeechListener._transcribe_worker

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[SpeechListener_1]] - code - loki/core/listener.py
- [[SpeechListener STT Work Queue]] - code - loki/core/listener.py
- [[SpeechListener._listen_loop]] - code - loki/core/listener.py
- [[SpeechListener._transcribe_worker]] - code - loki/core/listener.py
- [[VoicePipeline_1]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline._handle_transcript]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline._handle_wakeword]] - code - loki/core/voice_pipeline.py
- [[WAKEWORD_VARIANTS set]] - code - loki/core/wakeword.py
- [[WakewordDetector_1]] - code - loki/core/wakeword.py
- [[WakewordDetector._detect_loop]] - code - loki/core/wakeword.py
- [[WakewordDetector._is_wakeword]] - code - loki/core/wakeword.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SpeechListener_/_VoicePipeline_/_SpeechListener_transcribe_worker
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication._init_all  LokiApplication._wire_callbacks  ConversationStateMachine]]

## Top bridge nodes
- [[VoicePipeline_1]] - degree 4, connects to 1 community