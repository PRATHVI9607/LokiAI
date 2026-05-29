---
source_file: "loki/core/tts.py"
type: "rationale"
community: "LokiTTS / ._queue_worker() / ._speak_edge()"
location: "L91"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/LokiTTS_/__queue_worker_/__speak_edge
---

# Single background thread — serializes all speech, signals when queue drains.

## Connections
- [[._queue_worker()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/LokiTTS_/__queue_worker_/__speak_edge