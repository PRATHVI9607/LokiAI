---
source_file: "loki/core/wakeword.py"
type: "code"
community: "SpeechListener / WakewordDetector / ._transcribe_worker()"
location: "L33"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__transcribe_worker
---

# WakewordDetector

## Connections
- [[.__init__()_15]] - `method` [EXTRACTED]
- [[._detect_loop()]] - `method` [EXTRACTED]
- [[._init_all()]] - `calls` [INFERRED]
- [[._is_wakeword()]] - `method` [EXTRACTED]
- [[.start()]] - `method` [EXTRACTED]
- [[.stop()_1]] - `method` [EXTRACTED]
- [[Detects 'Hey Loki' wakeword using Whisper or Porcupine.]] - `rationale_for` [EXTRACTED]
- [[LokiApplication]] - `uses` [INFERRED]
- [[VoicePipeline]] - `uses` [INFERRED]
- [[wakeword.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__transcribe_worker