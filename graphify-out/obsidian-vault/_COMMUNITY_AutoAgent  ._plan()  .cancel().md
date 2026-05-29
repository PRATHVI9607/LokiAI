---
type: community
cohesion: 0.17
members: 13
---

# AutoAgent / ._plan() / .cancel()

**Cohesion:** 0.17 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_17]] - code - loki/features/auto_agent.py
- [[._execute_task()]] - code - loki/features/auto_agent.py
- [[._plan()]] - code - loki/features/auto_agent.py
- [[.cancel()]] - code - loki/features/auto_agent.py
- [[.is_running()]] - code - loki/features/auto_agent.py
- [[.run()_1]] - code - loki/features/auto_agent.py
- [[Abort any running task.]] - rationale - loki/features/auto_agent.py
- [[Ask the LLM to produce a JSON intent plan for the goal.]] - rationale - loki/features/auto_agent.py
- [[AutoAgent]] - code - loki/features/auto_agent.py
- [[AutoAgent — autonomous multi-step task executor (harness agent).  The user descr]] - rationale - loki/features/auto_agent.py
- [[Runs multi-step plans autonomously using Loki's action router.]] - rationale - loki/features/auto_agent.py
- [[Start an agentic task. Returns immediately; progress via on_progress callback.]] - rationale - loki/features/auto_agent.py
- [[auto_agent.py]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AutoAgent_/__plan_/_cancel
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_ActionRouter  ._handle_api_mock_data()  ._handle_api_mock_generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[AutoAgent]] - degree 12, connects to 4 communities