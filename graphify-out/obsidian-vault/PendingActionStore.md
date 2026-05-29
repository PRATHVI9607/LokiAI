---
source_file: "loki/core/pending_actions.py"
type: "code"
community: "PendingActionStore / TestPendingActions / .is_expired()"
location: "L30"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/PendingActionStore_/_TestPendingActions_/_is_expired
---

# PendingActionStore

## Connections
- [[.__init__()_11]] - `method` [EXTRACTED]
- [[.__init__()_4]] - `calls` [INFERRED]
- [[.cancel_all()]] - `method` [EXTRACTED]
- [[.peek_last()]] - `method` [EXTRACTED]
- [[.pop()]] - `method` [EXTRACTED]
- [[.push()]] - `method` [EXTRACTED]
- [[.test_cancel_all_clears_store()]] - `calls` [INFERRED]
- [[.test_expired_action_not_returned()]] - `calls` [INFERRED]
- [[.test_pop_most_recent_without_token()]] - `calls` [INFERRED]
- [[.test_push_and_pop_by_token()]] - `calls` [INFERRED]
- [[ActionRouter]] - `uses` [INFERRED]
- [[FakeTTS]] - `uses` [INFERRED]
- [[TestClipboardSyncToken]] - `uses` [INFERRED]
- [[TestConversationStateMachine]] - `uses` [INFERRED]
- [[TestPendingActions]] - `uses` [INFERRED]
- [[TestProcessManagerExactMatch]] - `uses` [INFERRED]
- [[TestSSRFProtection]] - `uses` [INFERRED]
- [[TestTTSDrain]] - `uses` [INFERRED]
- [[TestVoicePipeline]] - `uses` [INFERRED]
- [[Thread-safe store for pending confirmations.]] - `rationale_for` [EXTRACTED]
- [[pending_actions.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/PendingActionStore_/_TestPendingActions_/_is_expired