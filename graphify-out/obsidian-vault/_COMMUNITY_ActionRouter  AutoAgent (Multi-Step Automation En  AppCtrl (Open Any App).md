---
type: community
cohesion: 0.24
members: 10
---

# ActionRouter / AutoAgent (Multi-Step Automation En / AppCtrl (Open Any App)

**Cohesion:** 0.24 - loosely connected
**Members:** 10 nodes

## Members
- [[ActionRouter_1]] - code - loki/core/action_router.py
- [[AppCtrl (Open Any App)]] - code - loki/actions/app_ctrl.py
- [[AppCtrl.close_app]] - code - loki/actions/app_ctrl.py
- [[AuditLog_1]] - code - loki/core/audit.py
- [[AutoAgent (Multi-Step Automation Engine)]] - code - loki/features/auto_agent.py
- [[AutoAgent.SAFE_INTENTS]] - code - loki/features/auto_agent.py
- [[AutoAgent._execute_task]] - code - loki/features/auto_agent.py
- [[INTENT_TIERS Security Classification]] - code - loki/core/audit.py
- [[Rationale per-step delays (apps need launch time)]] - code - loki/features/auto_agent.py
- [[_STEP_DELAY (per-step launch delays)]] - code - loki/features/auto_agent.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ActionRouter_/_AutoAgent_Multi-Step_Automation_En_/_AppCtrl_Open_Any_App
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ComputerControl (Desktop Control En  pyautogui FAILSAFE (corner-abort sa  ComputerControl.click]]
- 1 edge to [[_COMMUNITY_AppCtrl.open_app (4-step resolution  AppCtrl._find_shortcut (Start-Menu   APP_MAP (spoken-name alias map)]]
- 1 edge to [[_COMMUNITY_LokiBrain  LokiBrain._fast_intent (determinist  TerminalFormatter (color-coded tags]]
- 1 edge to [[_COMMUNITY_LokiBrain._call_llm  AutoAgent._plan (LLM step planner)  LokiBrain._call_ollama (primary + f]]

## Top bridge nodes
- [[AutoAgent (Multi-Step Automation Engine)]] - degree 5, connects to 2 communities
- [[ActionRouter_1]] - degree 5, connects to 1 community
- [[AppCtrl (Open Any App)]] - degree 4, connects to 1 community
- [[AutoAgent.SAFE_INTENTS]] - degree 3, connects to 1 community