---
source_file: "loki/features/auto_agent.py"
type: "code"
community: "ActionRouter.route_intent / AutoAgent._execute_task / _DESTRUCTIVE_INTENTS Frozenset"
location: "def _execute_task"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/ActionRouterroute_intent_/_AutoAgent_execute_task_/__DESTRUCTIVE_INTENTS_Frozenset
---

# AutoAgent._execute_task

## Connections
- [[ActionRouter.route_intent]] - `calls` [EXTRACTED]
- [[AutoAgent.SAFE_INTENTS whitelist]] - `references` [EXTRACTED]
- [[AutoAgent._abort threading.Event]] - `references` [EXTRACTED]
- [[AutoAgent._plan]] - `calls` [EXTRACTED]
- [[AutoAgent.run]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/ActionRouterroute_intent_/_AutoAgent_execute_task_/__DESTRUCTIVE_INTENTS_Frozenset