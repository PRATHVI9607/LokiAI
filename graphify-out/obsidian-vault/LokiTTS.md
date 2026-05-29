---
source_file: "loki/core/tts.py"
type: "code"
community: "LokiTTS / ._queue_worker() / ._speak_edge()"
location: "L39"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/LokiTTS_/__queue_worker_/__speak_edge
---

# LokiTTS

## Connections
- [[.__init__()_12]] - `method` [EXTRACTED]
- [[._init_pyttsx3()]] - `method` [EXTRACTED]
- [[._play_audio()]] - `method` [EXTRACTED]
- [[._queue_worker()]] - `method` [EXTRACTED]
- [[._speak_edge()]] - `method` [EXTRACTED]
- [[._speak_pyttsx3()]] - `method` [EXTRACTED]
- [[.speak()]] - `method` [EXTRACTED]
- [[.stop()]] - `method` [EXTRACTED]
- [[.test_is_idle_after_stop()]] - `calls` [INFERRED]
- [[.test_stop_drains_queue()]] - `calls` [INFERRED]
- [[ConvState]] - `uses` [INFERRED]
- [[ConversationStateMachine]] - `uses` [INFERRED]
- [[FakeTTS]] - `uses` [INFERRED]
- [[TestClipboardSyncToken]] - `uses` [INFERRED]
- [[TestConversationStateMachine]] - `uses` [INFERRED]
- [[TestPendingActions]] - `uses` [INFERRED]
- [[TestProcessManagerExactMatch]] - `uses` [INFERRED]
- [[TestSSRFProtection]] - `uses` [INFERRED]
- [[TestTTSDrain]] - `uses` [INFERRED]
- [[TestVoicePipeline]] - `uses` [INFERRED]
- [[Text-to-speech engine with edge-tts primary, pyttsx3 fallback.      Uses a que]] - `rationale_for` [EXTRACTED]
- [[create_tts_engine()]] - `calls` [EXTRACTED]
- [[tts.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/LokiTTS_/__queue_worker_/__speak_edge