---
type: community
cohesion: 0.15
members: 19
---

# PendingActionStore / TestPendingActions / .is_expired()

**Cohesion:** 0.15 - loosely connected
**Members:** 19 nodes

## Members
- [[.__init__()_4]] - code - loki/core/action_router.py
- [[.__init__()_12]] - code - loki/core/pending_actions.py
- [[.cancel_all()]] - code - loki/core/pending_actions.py
- [[.is_expired()]] - code - loki/core/pending_actions.py
- [[.peek_last()]] - code - loki/core/pending_actions.py
- [[.pop()]] - code - loki/core/pending_actions.py
- [[.push()]] - code - loki/core/pending_actions.py
- [[.test_cancel_all_clears_store()]] - code - loki/tests/test_voice_and_security.py
- [[.test_expired_action_not_returned()]] - code - loki/tests/test_voice_and_security.py
- [[.test_pop_most_recent_without_token()]] - code - loki/tests/test_voice_and_security.py
- [[.test_push_and_pop_by_token()]] - code - loki/tests/test_voice_and_security.py
- [[.test_router_returns_pending_for_destructive()]] - code - loki/tests/test_voice_and_security.py
- [[PendingAction]] - code - loki/core/pending_actions.py
- [[PendingAction — confirmation gate for destructive operations.  Destructive inten]] - rationale - loki/core/pending_actions.py
- [[PendingActionStore]] - code - loki/core/pending_actions.py
- [[Pop by token or most-recent if token is None.]] - rationale - loki/core/pending_actions.py
- [[TestPendingActions]] - code - loki/tests/test_voice_and_security.py
- [[Thread-safe store for pending confirmations.]] - rationale - loki/core/pending_actions.py
- [[pending_actions.py]] - code - loki/core/pending_actions.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PendingActionStore_/_TestPendingActions_/_is_expired
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_FakeTTS  ProcessManager  TestProcessManagerExactMatch]]
- 4 edges to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 2 edges to [[_COMMUNITY_FileOps  ShellExec  TestFileOps]]
- 2 edges to [[_COMMUNITY_WebSummarizer  TestSSRFProtection  _is_ssrf_risk()]]
- 2 edges to [[_COMMUNITY_ClipboardSync  TestClipboardSyncToken  .stop()]]
- 2 edges to [[_COMMUNITY_VoicePipeline  TestVoicePipeline  ._make()]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]
- 1 edge to [[_COMMUNITY_TestConversationStateMachine  ._make_sm()  .test_end_conversation_goes_to_idle]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]

## Top bridge nodes
- [[TestPendingActions]] - degree 17, connects to 9 communities
- [[PendingActionStore]] - degree 21, connects to 6 communities
- [[.__init__()_4]] - degree 2, connects to 1 community
- [[.test_router_returns_pending_for_destructive()]] - degree 2, connects to 1 community