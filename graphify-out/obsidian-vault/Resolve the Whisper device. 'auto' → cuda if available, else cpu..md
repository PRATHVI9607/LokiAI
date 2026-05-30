---
source_file: "loki/core/listener.py"
type: "rationale"
community: "SpeechListener / WakewordDetector / _whisper_device()"
location: "L47"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/SpeechListener_/_WakewordDetector_/__whisper_device
---

# Resolve the Whisper device. 'auto' → cuda if available, else cpu.

## Connections
- [[_whisper_device()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/SpeechListener_/_WakewordDetector_/__whisper_device