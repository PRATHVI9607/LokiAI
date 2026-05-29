---
type: community
cohesion: 0.15
members: 18
---

# LokiTTS / ._queue_worker() / ._speak_edge()

**Cohesion:** 0.15 - loosely connected
**Members:** 18 nodes

## Members
- [[.__init__()_13]] - code - loki/core/tts.py
- [[._init_pyttsx3()]] - code - loki/core/tts.py
- [[._play_audio()]] - code - loki/core/tts.py
- [[._queue_worker()]] - code - loki/core/tts.py
- [[._speak_edge()]] - code - loki/core/tts.py
- [[._speak_pyttsx3()]] - code - loki/core/tts.py
- [[.speak()]] - code - loki/core/tts.py
- [[.stop()]] - code - loki/core/tts.py
- [[Enqueue text for speaking. Never drops messages.]] - rationale - loki/core/tts.py
- [[Loki TTS — edge-tts primary (Microsoft Neural), pyttsx3 fallback. Callback-base]] - rationale - loki/core/tts.py
- [[LokiTTS]] - code - loki/core/tts.py
- [[Single background thread — serializes all speech, signals when queue drains.]] - rationale - loki/core/tts.py
- [[Stop current playback and drain all queued speech.]] - rationale - loki/core/tts.py
- [[Text-to-speech engine with edge-tts primary, pyttsx3 fallback.      Uses a que]] - rationale - loki/core/tts.py
- [[create_tts_engine()]] - code - loki/core/tts.py
- [[is_idle()]] - code - loki/core/tts.py
- [[is_speaking()]] - code - loki/core/tts.py
- [[tts.py]] - code - loki/core/tts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiTTS_/__queue_worker_/__speak_edge
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 1 edge to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 1 edge to [[_COMMUNITY_SoftwareUpdater  ._run()  ._check_winget()]]

## Top bridge nodes
- [[LokiTTS]] - degree 23, connects to 8 communities
- [[._speak_edge()]] - degree 5, connects to 1 community
- [[create_tts_engine()]] - degree 3, connects to 1 community