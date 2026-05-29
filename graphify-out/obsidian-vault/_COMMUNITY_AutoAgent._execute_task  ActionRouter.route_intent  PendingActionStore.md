---
type: community
cohesion: 0.08
members: 26
---

# AutoAgent._execute_task / ActionRouter.route_intent / PendingActionStore

**Cohesion:** 0.08 - loosely connected
**Members:** 26 nodes

## Members
- [[ActionRouter_1]] - code - loki/core/action_router.py
- [[ActionRouter.route_intent]] - code - loki/core/action_router.py
- [[AuditLog_1]] - code - loki/core/audit.py
- [[AutoAgent.SAFE_INTENTS whitelist]] - code - loki/features/auto_agent.py
- [[AutoAgent._abort threading.Event]] - code - loki/features/auto_agent.py
- [[AutoAgent._execute_task]] - code - loki/features/auto_agent.py
- [[AutoAgent._plan]] - code - loki/features/auto_agent.py
- [[AutoAgent.run]] - code - loki/features/auto_agent.py
- [[ConversationStateMachine._arm_timeout]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._emit_response]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._handle_intent]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._on_timeout]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine._process_worker]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine.on_tts_done]] - code - loki/core/conversation_sm.py
- [[ConversationStateMachine.process_input]] - code - loki/core/conversation_sm.py
- [[INTENT_TIERS Security Classification]] - code - loki/core/audit.py
- [[PROTECTED_PROCESSES set]] - code - loki/features/process_manager.py
- [[PendingAction_1]] - code - loki/core/pending_actions.py
- [[PendingActionStore_1]] - code - loki/core/pending_actions.py
- [[ProcessManager.kill]] - code - loki/features/process_manager.py
- [[Vault secret-never-in-message rule]] - code - loki/features/vault.py
- [[Vault.retrieve]] - code - loki/features/vault.py
- [[VoicePipeline.resume_listening]] - code - loki/core/voice_pipeline.py
- [[VoicePipeline.return_to_wakeword]] - code - loki/core/voice_pipeline.py
- [[_DESTRUCTIVE_INTENTS Frozenset]] - code - loki/core/action_router.py
- [[_PLAN_PROMPT LLM template]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AutoAgent_execute_task_/_ActionRouterroute_intent_/_PendingActionStore
SORT file.name ASC
```
