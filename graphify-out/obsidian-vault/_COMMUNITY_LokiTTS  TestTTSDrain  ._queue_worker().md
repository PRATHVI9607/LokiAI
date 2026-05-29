---
type: community
cohesion: 0.13
members: 22
---

# LokiTTS / TestTTSDrain / ._queue_worker()

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_12]] - code - loki/core/tts.py
- [[._init_pyttsx3()]] - code - loki/core/tts.py
- [[._play_audio()]] - code - loki/core/tts.py
- [[._queue_worker()]] - code - loki/core/tts.py
- [[._speak_edge()]] - code - loki/core/tts.py
- [[._speak_pyttsx3()]] - code - loki/core/tts.py
- [[.speak()]] - code - loki/core/tts.py
- [[.speak()_1]] - code - loki/tests/test_voice_and_security.py
- [[.stop()]] - code - loki/core/tts.py
- [[.test_is_idle_after_stop()]] - code - loki/tests/test_voice_and_security.py
- [[.test_stop_drains_queue()]] - code - loki/tests/test_voice_and_security.py
- [[Enqueue text for speaking. Never drops messages.]] - rationale - loki/core/tts.py
- [[Loki TTS — edge-tts primary (Microsoft Neural), pyttsx3 fallback. Callback-base]] - rationale - loki/core/tts.py
- [[LokiTTS]] - code - loki/core/tts.py
- [[Single background thread — serializes all speech, signals when queue drains.]] - rationale - loki/core/tts.py
- [[Stop current playback and drain all queued speech.]] - rationale - loki/core/tts.py
- [[TestTTSDrain]] - code - loki/tests/test_voice_and_security.py
- [[Text-to-speech engine with edge-tts primary, pyttsx3 fallback.      Uses a que]] - rationale - loki/core/tts.py
- [[create_tts_engine()]] - code - loki/core/tts.py
- [[is_idle()]] - code - loki/core/tts.py
- [[is_speaking()]] - code - loki/core/tts.py
- [[tts.py]] - code - loki/core/tts.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiTTS_/_TestTTSDrain_/__queue_worker
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 3 edges to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 2 edges to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 2 edges to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]
- 1 edge to [[_COMMUNITY_SoftwareUpdater  ._run()  ._check_winget()]]
- 1 edge to [[_COMMUNITY_VoicePipeline  voice_pipeline.py  .activate()]]

## Top bridge nodes
- [[TestTTSDrain]] - degree 13, connects to 10 communities
- [[LokiTTS]] - degree 23, connects to 9 communities
- [[._speak_edge()]] - degree 5, connects to 1 community
- [[.test_stop_drains_queue()]] - degree 4, connects to 1 community
- [[create_tts_engine()]] - degree 3, connects to 1 community