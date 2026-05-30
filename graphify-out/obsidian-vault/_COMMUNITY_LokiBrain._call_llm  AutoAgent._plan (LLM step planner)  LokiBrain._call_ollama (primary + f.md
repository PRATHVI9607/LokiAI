---
type: community
cohesion: 0.40
members: 5
---

# LokiBrain._call_llm / AutoAgent._plan (LLM step planner) / LokiBrain._call_ollama (primary + f

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[AutoAgent._plan (LLM step planner)]] - code - loki/features/auto_agent.py
- [[LokiBrain._call_llm]] - code - loki/core/brain.py
- [[LokiBrain._call_ollama (primary + fallback model)]] - code - loki/core/brain.py
- [[config ollama_fallback_model (phi3mini)]] - code - loki/config.yaml
- [[config prefer_local]] - code - loki/config.yaml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_call_llm_/_AutoAgent_plan_LLM_step_planner_/_LokiBrain_call_ollama_primary__f
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiBrain  LokiBrain._fast_intent (determinist  TerminalFormatter (color-coded tags]]
- 1 edge to [[_COMMUNITY_ActionRouter  AutoAgent (Multi-Step Automation En  AppCtrl (Open Any App)]]

## Top bridge nodes
- [[LokiBrain._call_llm]] - degree 4, connects to 1 community
- [[AutoAgent._plan (LLM step planner)]] - degree 2, connects to 1 community