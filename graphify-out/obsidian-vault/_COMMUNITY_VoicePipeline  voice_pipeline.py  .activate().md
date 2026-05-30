---
type: community
cohesion: 0.09
members: 22
---

# VoicePipeline / voice_pipeline.py / .activate()

**Cohesion:** 0.09 - loosely connected
**Members:** 22 nodes

## Members
- [[.__init__()_17]] - code - loki/core/voice_pipeline.py
- [[._handle_partial()]] - code - loki/core/voice_pipeline.py
- [[._handle_transcript()]] - code - loki/core/voice_pipeline.py
- [[._handle_wakeword()]] - code - loki/core/voice_pipeline.py
- [[._start_listener_safe()]] - code - loki/core/voice_pipeline.py
- [[.activate()]] - code - loki/core/voice_pipeline.py
- [[.deactivate()]] - code - loki/core/voice_pipeline.py
- [[.resume_listening()]] - code - loki/core/voice_pipeline.py
- [[.return_to_wakeword()]] - code - loki/core/voice_pipeline.py
- [[.set_muted()]] - code - loki/core/voice_pipeline.py
- [[After TTS finishes mid-conversation start listener for next utterance.]] - rationale - loki/core/voice_pipeline.py
- [[Conversation ended hand mic back to wakeword detector.]] - rationale - loki/core/voice_pipeline.py
- [[Exclusive-mic manager wakeword ↔ listener handoff.]] - rationale - loki/core/voice_pipeline.py
- [[Full STT transcript ready release listener mic, fire callback.]] - rationale - loki/core/voice_pipeline.py
- [[Shut down both components.]] - rationale - loki/core/voice_pipeline.py
- [[Start wakeword detection. Call once on app start.]] - rationale - loki/core/voice_pipeline.py
- [[Timer callback — only starts listener if still active and not already running.]] - rationale - loki/core/voice_pipeline.py
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
- 3 edges to [[_COMMUNITY_FakeTTS  TestClipboardSyncToken  TestTTSDrain]]
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_SpeechListener  WakewordDetector  _whisper_device()]]
- 2 edges to [[_COMMUNITY_TestVoicePipeline  ._make()  .test_activate_starts_wakeword()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_PendingActionStore  TestPendingActions  .is_expired()]]
- 1 edge to [[_COMMUNITY_ProcessManager  TestProcessManagerExactMatch  process_manager.py]]
- 1 edge to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]

## Top bridge nodes
- [[VoicePipeline]] - degree 25, connects to 8 communities