---
type: community
cohesion: 0.20
members: 11
---

# AutoAgent / ._plan() / ._execute_task()

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_20]] - code - loki/features/auto_agent.py
- [[._execute_task()]] - code - loki/features/auto_agent.py
- [[._plan()]] - code - loki/features/auto_agent.py
- [[.cancel()]] - code - loki/features/auto_agent.py
- [[.is_running()]] - code - loki/features/auto_agent.py
- [[.run()_1]] - code - loki/features/auto_agent.py
- [[Ask the LLM for a JSON step plan. Uses _call_llm directly (not the         conve]] - rationale - loki/features/auto_agent.py
- [[AutoAgent]] - code - loki/features/auto_agent.py
- [[AutoAgent — autonomous multi-step task executor (the use the computer like a pe]] - rationale - loki/features/auto_agent.py
- [[Plans and runs multi-step desktop automations via the action router.]] - rationale - loki/features/auto_agent.py
- [[auto_agent.py]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AutoAgent_/__plan_/__execute_task
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_agent_cancel()  ._handle_agent_run()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[AutoAgent]] - degree 12, connects to 3 communities