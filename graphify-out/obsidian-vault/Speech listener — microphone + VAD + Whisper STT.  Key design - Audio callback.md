---
source_file: "loki/core/listener.py"
type: "rationale"
community: "SpeechListener / WakewordDetector / ._transcribe_worker()"
location: "L1"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__transcribe_worker
---

# Speech listener — microphone + VAD + Whisper STT.  Key design: - Audio callback

## Connections
- [[listener.py]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__transcribe_worker