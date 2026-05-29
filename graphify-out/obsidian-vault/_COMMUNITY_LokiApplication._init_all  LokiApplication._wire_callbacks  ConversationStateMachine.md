---
type: community
cohesion: 0.20
members: 12
---

# LokiApplication._init_all / LokiApplication._wire_callbacks / ConversationStateMachine

**Cohesion:** 0.20 - loosely connected
**Members:** 12 nodes

## Members
- [[ApiMocker_1]] - code - loki/features/api_mocker.py
- [[AutoAgent_1]] - code - loki/features/auto_agent.py
- [[ConvState Enum (IDLELISTENINGTHINKINGSPEAKINGENDING)]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine_1]] - code - loki/core/conversation_sm.py
- [[LokiApplication_1]] - code - main.py
- [[LokiApplication._init_all]] - code - main.py
- [[LokiApplication._wire_callbacks]] - code - main.py
- [[LokiBrain_1]] - code - loki/core/brain.py
- [[LokiTTS_1]] - code - loki/core/tts.py
- [[ProcessManager_1]] - code - loki/features/process_manager.py
- [[Vault (AES-256-GCM encrypted KV)]] - code - loki/features/vault.py
- [[WebSummarizer_1]] - code - loki/features/web_summarizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiApplication_init_all_/_LokiApplication_wire_callbacks_/_ConversationStateMachine
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_SpeechListener  VoicePipeline  SpeechListener._transcribe_worker]]
- 1 edge to [[_COMMUNITY_SystemMonitor  ProcessTriage  Safe-to-Kill Process List]]
- 1 edge to [[_COMMUNITY_PendingActionStore  ActionRouter  INTENT_TIERS Security Classification]]
- 1 edge to [[_COMMUNITY_ClipboardSync  ClipboardSync token auth pattern]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine.on_tts_done  ConversationStateMachine._arm_timeout]]

## Top bridge nodes
- [[LokiApplication._init_all]] - degree 12, connects to 3 communities
- [[LokiApplication._wire_callbacks]] - degree 5, connects to 2 communities
- [[ProcessManager_1]] - degree 2, connects to 1 community