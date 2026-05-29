---
type: community
cohesion: 0.08
members: 29
---

# VoicePipeline / TestVoicePipeline / ._make()

**Cohesion:** 0.08 - loosely connected
**Members:** 29 nodes

## Members
- [[.__init__()_15]] - code - loki/core/voice_pipeline.py
- [[._handle_partial()]] - code - loki/core/voice_pipeline.py
- [[._handle_transcript()]] - code - loki/core/voice_pipeline.py
- [[._handle_wakeword()]] - code - loki/core/voice_pipeline.py
- [[._make()]] - code - loki/tests/test_voice_and_security.py
- [[._start_listener_safe()]] - code - loki/core/voice_pipeline.py
- [[.activate()]] - code - loki/core/voice_pipeline.py
- [[.deactivate()]] - code - loki/core/voice_pipeline.py
- [[.resume_listening()]] - code - loki/core/voice_pipeline.py
- [[.return_to_wakeword()]] - code - loki/core/voice_pipeline.py
- [[.set_muted()]] - code - loki/core/voice_pipeline.py
- [[.test_activate_starts_wakeword()]] - code - loki/tests/test_voice_and_security.py
- [[.test_deactivate_stops_both()]] - code - loki/tests/test_voice_and_security.py
- [[.test_mute_stops_voice()]] - code - loki/tests/test_voice_and_security.py
- [[.test_transcript_callback_stops_listener()]] - code - loki/tests/test_voice_and_security.py
- [[.test_wakeword_callback_stops_wakeword_starts_listener()]] - code - loki/tests/test_voice_and_security.py
- [[After TTS finishes mid-conversation start listener for next utterance.]] - rationale - loki/core/voice_pipeline.py
- [[Conversation ended hand mic back to wakeword detector.]] - rationale - loki/core/voice_pipeline.py
- [[Exclusive-mic manager wakeword ↔ listener handoff.]] - rationale - loki/core/voice_pipeline.py
- [[Full STT transcript ready release listener mic, fire callback.]] - rationale - loki/core/voice_pipeline.py
- [[Shut down both components.]] - rationale - loki/core/voice_pipeline.py
- [[Start wakeword detection. Call once on app start.]] - rationale - loki/core/voice_pipeline.py
- [[TestVoicePipeline]] - code - loki/tests/test_voice_and_security.py
- [[Timer callback — only starts listener if still active and not already running.]] - rationale - loki/core/voice_pipeline.py
- [[VoicePipeline]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline — owns the microphone.  Only one component can hold the mic at a t]] - rationale - loki/core/voice_pipeline.py
- [[Wakeword detected release wakeword mic, hand to listener.]] - rationale - loki/core/voice_pipeline.py
- [[is_muted()]] - code - loki/core/voice_pipeline.py
- [[voice_pipeline.py]] - code - loki/core/voice_pipeline.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/VoicePipeline_/_TestVoicePipeline_/__make
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 1 edge to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_SpeechListener  ._transcribe_worker()  listener.py]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]
- 1 edge to [[_COMMUNITY_WakewordDetector  wakeword.py  ._detect_loop()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]

## Top bridge nodes
- [[TestVoicePipeline]] - degree 17, connects to 9 communities
- [[VoicePipeline]] - degree 25, connects to 8 communities