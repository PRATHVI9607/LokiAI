---
source_file: "loki/core/conversation_sm.py"
type: "code"
community: "AutoAgent._execute_task / ActionRouter.route_intent / PendingActionStore"
location: "def on_tts_done"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/AutoAgent_execute_task_/_ActionRouterroute_intent_/_PendingActionStore
---

# ConversationStateMachine.on_tts_done

## Connections
- [[ConversationStateMachine._arm_timeout]] - `calls` [EXTRACTED]
- [[VoicePipeline.resume_listening]] - `calls` [EXTRACTED]
- [[VoicePipeline.return_to_wakeword]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/AutoAgent_execute_task_/_ActionRouterroute_intent_/_PendingActionStore