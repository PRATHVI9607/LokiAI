---
source_file: "loki/features/auto_agent.py"
type: "code"
community: "AutoAgent._execute_task / ActionRouter.route_intent / PendingActionStore"
location: "def _execute_task"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/AutoAgent_execute_task_/_ActionRouterroute_intent_/_PendingActionStore
---

# AutoAgent._execute_task

## Connections
- [[ActionRouter.route_intent]] - `calls` [EXTRACTED]
- [[AutoAgent.SAFE_INTENTS whitelist]] - `references` [EXTRACTED]
- [[AutoAgent._abort threading.Event]] - `references` [EXTRACTED]
- [[AutoAgent._plan]] - `calls` [EXTRACTED]
- [[AutoAgent.run]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/AutoAgent_execute_task_/_ActionRouterroute_intent_/_PendingActionStore