---
type: community
cohesion: 0.10
members: 21
---

# VoicePipeline / voice_pipeline.py / .activate()

**Cohesion:** 0.10 - loosely connected
**Members:** 21 nodes

## Members
- [[.__init__()_14]] - code - loki/core/voice_pipeline.py
- [[._handle_partial()]] - code - loki/core/voice_pipeline.py
- [[._handle_transcript()]] - code - loki/core/voice_pipeline.py
- [[._handle_wakeword()]] - code - loki/core/voice_pipeline.py
- [[.activate()]] - code - loki/core/voice_pipeline.py
- [[.deactivate()]] - code - loki/core/voice_pipeline.py
- [[.resume_listening()]] - code - loki/core/voice_pipeline.py
- [[.return_to_wakeword()]] - code - loki/core/voice_pipeline.py
- [[.set_muted()]] - code - loki/core/voice_pipeline.py
- [[After TTS finishes mid-conversation start listener for next utterance.]] - rationale - loki/core/voice_pipeline.py
- [[Conversation ended hand mic back to wakeword detector.]] - rationale - loki/core/voice_pipeline.py
- [[Exclusive-mic manager wakeword ↔ listener handoff.]] - rationale - loki/core/voice_pipeline.py
- [[Full STT transcript ready release listener mic, fire callback.]] - rationale - loki/core/voice_pipeline.py
- [[Partial wakeword transcript (for live transcript display).]] - rationale - loki/core/voice_pipeline.py
- [[Shut down both components.]] - rationale - loki/core/voice_pipeline.py
- [[Start wakeword detection. Call once on app start.]] - rationale - loki/core/voice_pipeline.py
- [[VoicePipeline]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline — owns the microphone.  Only one component can hold the mic at a t]] - rationale - loki/core/voice_pipeline.py
- [[Wakeword detected release wakeword mic, hand to listener.]] - rationale - loki/core/voice_pipeline.py
- [[is_muted()]] - code - loki/core/voice_pipeline.py
- [[voice_pipeline.py]] - code - loki/core/voice_pipeline.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/VoicePipeline_/_voice_pipelinepy_/_activate
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_SpeechListener  WakewordDetector  ._transcribe_worker()]]
- 2 edges to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_FakeTTS  test_voice_and_security.py  .drain_and_fire()]]
- 1 edge to [[_COMMUNITY_LokiTTS  TestTTSDrain  ._queue_worker()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 1 edge to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]

## Top bridge nodes
- [[VoicePipeline]] - degree 24, connects to 11 communities