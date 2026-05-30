---
source_file: "loki/core/wakeword.py"
type: "code"
community: "SpeechListener / WakewordDetector / _whisper_device()"
location: "L43"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__whisper_device
---

# WakewordDetector

## Connections
- [[.__init__()_18]] - `method` [EXTRACTED]
- [[._detect_loop()]] - `method` [EXTRACTED]
- [[._init_all()]] - `calls` [INFERRED]
- [[._is_wakeword()]] - `method` [EXTRACTED]
- [[.start()]] - `method` [EXTRACTED]
- [[.stop()_1]] - `method` [EXTRACTED]
- [[Detects 'Hey Loki' using a rolling audio buffer + Whisper tiny.en.]] - `rationale_for` [EXTRACTED]
- [[LokiApplication]] - `uses` [INFERRED]
- [[VoicePipeline]] - `uses` [INFERRED]
- [[wakeword.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__whisper_device