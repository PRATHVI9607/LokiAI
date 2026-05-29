---
type: community
cohesion: 0.27
members: 14
---

# CodeAssistant / ._ask() / ._require_brain()

**Cohesion:** 0.27 - loosely connected
**Members:** 14 nodes

## Members
- [[.__init__()_23]] - code - loki/features/code_assistant.py
- [[._ask()_2]] - code - loki/features/code_assistant.py
- [[._require_brain()]] - code - loki/features/code_assistant.py
- [[.analyze()]] - code - loki/features/code_assistant.py
- [[.build_sql()]] - code - loki/features/code_assistant.py
- [[.convert()]] - code - loki/features/code_assistant.py
- [[.generate_readme()]] - code - loki/features/code_assistant.py
- [[.generate_regex()]] - code - loki/features/code_assistant.py
- [[.refactor()]] - code - loki/features/code_assistant.py
- [[Code assistant — analyze bugs, generate commit messages, README, regex, SQL.]] - rationale - loki/features/code_assistant.py
- [[CodeAssistant]] - code - loki/features/code_assistant.py
- [[Identify code smells and suggest specific refactoring improvements.]] - rationale - loki/features/code_assistant.py
- [[LLM-powered code analysis and generation.]] - rationale - loki/features/code_assistant.py
- [[code_assistant.py]] - code - loki/features/code_assistant.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CodeAssistant_/__ask_/__require_brain
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]

## Top bridge nodes
- [[CodeAssistant]] - degree 14, connects to 3 communities