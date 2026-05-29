---
source_file: "loki/tests/test_voice_and_security.py"
type: "code"
community: "PendingActionStore / TestPendingActions / .is_expired()"
location: "L145"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/PendingActionStore_/_TestPendingActions_/_is_expired
---

# TestPendingActions

## Connections
- [[.test_cancel_all_clears_store()]] - `method` [EXTRACTED]
- [[.test_confirm_action_executes()]] - `method` [EXTRACTED]
- [[.test_expired_action_not_returned()]] - `method` [EXTRACTED]
- [[.test_pop_most_recent_without_token()]] - `method` [EXTRACTED]
- [[.test_push_and_pop_by_token()]] - `method` [EXTRACTED]
- [[.test_router_returns_pending_for_destructive()]] - `method` [EXTRACTED]
- [[ActionRouter]] - `uses` [INFERRED]
- [[ClipboardSync]] - `uses` [INFERRED]
- [[ConvState]] - `uses` [INFERRED]
- [[ConversationStateMachine]] - `uses` [INFERRED]
- [[FileOps]] - `uses` [INFERRED]
- [[LokiTTS]] - `uses` [INFERRED]
- [[PendingActionStore]] - `uses` [INFERRED]
- [[ProcessManager]] - `uses` [INFERRED]
- [[VoicePipeline]] - `uses` [INFERRED]
- [[WebSummarizer]] - `uses` [INFERRED]
- [[test_voice_and_security.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/PendingActionStore_/_TestPendingActions_/_is_expired