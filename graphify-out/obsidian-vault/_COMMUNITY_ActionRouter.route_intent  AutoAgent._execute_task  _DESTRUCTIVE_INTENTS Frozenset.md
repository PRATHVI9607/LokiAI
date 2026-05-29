---
type: community
cohesion: 0.24
members: 10
---

# ActionRouter.route_intent / AutoAgent._execute_task / _DESTRUCTIVE_INTENTS Frozenset

**Cohesion:** 0.24 - loosely connected
**Members:** 10 nodes

## Members
- [[ActionRouter.route_intent]] - code - loki/core/action_router.py
- [[AutoAgent.SAFE_INTENTS whitelist]] - code - loki/features/auto_agent.py
- [[AutoAgent._abort threading.Event]] - code - loki/features/auto_agent.py
- [[AutoAgent._execute_task]] - code - loki/features/auto_agent.py
- [[AutoAgent._plan]] - code - loki/features/auto_agent.py
- [[AutoAgent.run]] - code - loki/features/auto_agent.py
- [[PROTECTED_PROCESSES set]] - code - loki/features/process_manager.py
- [[ProcessManager.kill]] - code - loki/features/process_manager.py
- [[_DESTRUCTIVE_INTENTS Frozenset]] - code - loki/core/action_router.py
- [[_PLAN_PROMPT LLM template]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouterroute_intent_/_AutoAgent_execute_task_/__DESTRUCTIVE_INTENTS_Frozenset
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiBrain.ask  WebSummarizer.summarize  LokiBrain._build_system_prompt]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine.on_tts_done  ConversationStateMachine._arm_timeout]]
- 1 edge to [[_COMMUNITY_PendingActionStore  ActionRouter  INTENT_TIERS Security Classification]]

## Top bridge nodes
- [[ActionRouter.route_intent]] - degree 5, connects to 3 communities
- [[AutoAgent._plan]] - degree 3, connects to 1 community