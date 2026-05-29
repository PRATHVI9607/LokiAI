---
type: community
cohesion: 0.16
members: 14
---

# ConversationStateMachine.on_tts_done / ConversationStateMachine._arm_timeout

**Cohesion:** 0.16 - loosely connected
**Members:** 14 nodes

## Members
- [[ConversationStateMachine._arm_timeout]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._emit_response]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._handle_intent]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._on_timeout]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._process_worker]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine.on_tts_done]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine.process_input]] - code - loki/core/conversation_sm.py
- [[LokiBrain.parse_intent]] - code - loki/core/brain.py
- [[LokiTTS._queue_worker]] - code - loki/core/tts.py
- [[LokiTTS._speak_edge (edge-tts async)]] - code - loki/core/tts.py
- [[LokiTTS.on_speaking_stopped callback]] - code - loki/core/tts.py
- [[LokiTTS.speak]] - code - loki/core/tts.py
- [[VoicePipeline.resume_listening]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline.return_to_wakeword]] - code - loki/core/voice_pipeline.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ConversationStateMachineon_tts_done_/_ConversationStateMachine_arm_timeout
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication._init_all  LokiApplication._wire_callbacks  ConversationStateMachine]]
- 1 edge to [[_COMMUNITY_LokiBrain.ask  WebSummarizer.summarize  LokiBrain._build_system_prompt]]
- 1 edge to [[_COMMUNITY_ActionRouter.route_intent  AutoAgent._execute_task  _DESTRUCTIVE_INTENTS Frozenset]]

## Top bridge nodes
- [[ConversationStateMachine._process_worker]] - degree 4, connects to 1 community
- [[ConversationStateMachine._handle_intent]] - degree 3, connects to 1 community
- [[LokiTTS.on_speaking_stopped callback]] - degree 3, connects to 1 community