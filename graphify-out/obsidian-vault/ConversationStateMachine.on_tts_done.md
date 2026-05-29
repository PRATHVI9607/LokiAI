---
source_file: "loki/core/conversation_sm.py"
type: "code"
community: "ConversationStateMachine.on_tts_done / ConversationStateMachine._arm_timeout"
location: "def on_tts_done"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/ConversationStateMachineon_tts_done_/_ConversationStateMachine_arm_timeout
---

# ConversationStateMachine.on_tts_done

## Connections
- [[ConversationStateMachine._arm_timeout]] - `calls` [EXTRACTED]
- [[LokiTTS.on_speaking_stopped callback]] - `calls` [EXTRACTED]
- [[VoicePipeline.resume_listening]] - `calls` [EXTRACTED]
- [[VoicePipeline.return_to_wakeword]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/ConversationStateMachineon_tts_done_/_ConversationStateMachine_arm_timeout