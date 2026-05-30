---
type: community
cohesion: 0.25
members: 9
---

# ._call_llm() / ._compress_old_turns() / ._save_history()

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[._call_llm()]] - code - loki/core/brain.py
- [[._call_ollama()]] - code - loki/core/brain.py
- [[._compress_old_turns()]] - code - loki/core/brain.py
- [[._extract_facts()]] - code - loki/core/brain.py
- [[._run_maintenance()]] - code - loki/core/brain.py
- [[._save_history()]] - code - loki/core/brain.py
- [[._store_turn()]] - code - loki/core/brain.py
- [[.clear_conversation()]] - code - loki/core/brain.py
- [[Call the local Ollama model. Returns '' on failure.]] - rationale - loki/core/brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_call_llm_/__compress_old_turns_/__save_history
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 2 edges to [[_COMMUNITY_.ask()  ._build_messages()  ._get_kg_context()]]

## Top bridge nodes
- [[._call_llm()]] - degree 5, connects to 2 communities
- [[._store_turn()]] - degree 3, connects to 2 communities
- [[._compress_old_turns()]] - degree 4, connects to 1 community
- [[._save_history()]] - degree 4, connects to 1 community
- [[._call_ollama()]] - degree 3, connects to 1 community