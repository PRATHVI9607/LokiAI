---
source_file: "loki/core/listener.py"
type: "rationale"
community: "SpeechListener / WakewordDetector / _whisper_device()"
location: "L210"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__whisper_device
---

# Drain the work queue and run Whisper on each frame list.         Completely sepa

## Connections
- [[._transcribe_worker()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__whisper_device