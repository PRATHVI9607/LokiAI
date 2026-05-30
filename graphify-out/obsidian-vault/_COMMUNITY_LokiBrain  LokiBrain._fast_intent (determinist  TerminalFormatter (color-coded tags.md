---
type: community
cohesion: 0.20
members: 11
---

# LokiBrain / LokiBrain._fast_intent (determinist / TerminalFormatter (color-coded tags

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[AutoAgent.run]] - code - loki/features/auto_agent.py
- [[ConversationStateMachine_1]] - code - loki/core/conversation_sm.py
- [[LokiBrain_1]] - code - loki/core/brain.py
- [[LokiBrain._fast_intent (deterministic fast-path)]] - code - loki/core/brain.py
- [[Rationale fast-path multi-step detection]] - code - loki/core/brain.py
- [[TerminalFormatter (color-coded tags)]] - code - loki/core/log_setup.py
- [[_NOISY_LOGGERS suppression]] - code - loki/core/log_setup.py
- [[_force_utf8_stdout]] - code - loki/core/log_setup.py
- [[_handle_intent (route-first then speak)]] - code - loki/core/conversation_sm.py
- [[_process_worker]] - code - loki/core/conversation_sm.py
- [[setup_logging]] - code - loki/core/log_setup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LokiBrain_/_LokiBrain_fast_intent_determinist_/_TerminalFormatter_color-coded_tags
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_ComputerControl (Desktop Control En  pyautogui FAILSAFE (corner-abort sa  ComputerControl.click]]
- 1 edge to [[_COMMUNITY_LokiBrain._call_llm  AutoAgent._plan (LLM step planner)  LokiBrain._call_ollama (primary + f]]
- 1 edge to [[_COMMUNITY_RagEngine  LokiServer (FastAPI)  _embed_batch (32call batch embeddi]]
- 1 edge to [[_COMMUNITY_ActionRouter  AutoAgent (Multi-Step Automation En  AppCtrl (Open Any App)]]

## Top bridge nodes
- [[LokiBrain_1]] - degree 4, connects to 1 community
- [[LokiBrain._fast_intent (deterministic fast-path)]] - degree 4, connects to 1 community
- [[TerminalFormatter (color-coded tags)]] - degree 4, connects to 1 community
- [[AutoAgent.run]] - degree 2, connects to 1 community