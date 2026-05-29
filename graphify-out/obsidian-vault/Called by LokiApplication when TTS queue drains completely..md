---
source_file: "loki/core/conversation_sm.py"
type: "rationale"
community: "ConversationStateMachine / ._arm_timeout() / ._cancel_timeout()"
location: "L141"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/ConversationStateMachine_/__arm_timeout_/__cancel_timeout
---

# Called by LokiApplication when TTS queue drains completely.

## Connections
- [[.on_tts_done()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/ConversationStateMachine_/__arm_timeout_/__cancel_timeout