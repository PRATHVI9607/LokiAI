---
source_file: "loki/core/listener.py"
type: "code"
community: "SpeechListener / WakewordDetector / ._transcribe_worker()"
location: "L46"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__transcribe_worker
---

# SpeechListener

## Connections
- [[.__init__()_9]] - `method` [EXTRACTED]
- [[._init_all()]] - `calls` [INFERRED]
- [[._listen_loop()]] - `method` [EXTRACTED]
- [[._transcribe()]] - `method` [EXTRACTED]
- [[._transcribe_worker()]] - `method` [EXTRACTED]
- [[.start_listening()]] - `method` [EXTRACTED]
- [[.stop_listening()]] - `method` [EXTRACTED]
- [[Listens to microphone, detects speech via VAD, transcribes with Whisper.]] - `rationale_for` [EXTRACTED]
- [[LokiApplication]] - `uses` [INFERRED]
- [[VoicePipeline]] - `uses` [INFERRED]
- [[listener.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__transcribe_worker