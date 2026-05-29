---
type: community
cohesion: 0.13
members: 17
---

# AutoAgent._execute_task / PendingActionStore / _DESTRUCTIVE_INTENTS Frozenset

**Cohesion:** 0.13 - loosely connected
**Members:** 17 nodes

## Members
- [[ActionRouter_1]] - code - loki/core/action_router.py
- [[ActionRouter.route_intent]] - code - loki/core/action_router.py
- [[AuditLog_1]] - code - loki/core/audit.py
- [[AutoAgent.SAFE_INTENTS whitelist]] - code - loki/features/auto_agent.py
- [[AutoAgent._abort threading.Event]] - code - loki/features/auto_agent.py
- [[AutoAgent._execute_task]] - code - loki/features/auto_agent.py
- [[AutoAgent._plan]] - code - loki/features/auto_agent.py
- [[AutoAgent.run]] - code - loki/features/auto_agent.py
- [[INTENT_TIERS Security Classification]] - code - loki/core/audit.py
- [[PROTECTED_PROCESSES set]] - code - loki/features/process_manager.py
- [[PendingAction_1]] - code - loki/core/pending_actions.py
- [[PendingActionStore_1]] - code - loki/core/pending_actions.py
- [[ProcessManager.kill]] - code - loki/features/process_manager.py
- [[Vault secret-never-in-message rule]] - code - loki/features/vault.py
- [[Vault.retrieve]] - code - loki/features/vault.py
- [[_DESTRUCTIVE_INTENTS Frozenset]] - code - loki/core/action_router.py
- [[_PLAN_PROMPT LLM template]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AutoAgent_execute_task_/_PendingActionStore_/__DESTRUCTIVE_INTENTS_Frozenset
SORT file.name ASC
```
