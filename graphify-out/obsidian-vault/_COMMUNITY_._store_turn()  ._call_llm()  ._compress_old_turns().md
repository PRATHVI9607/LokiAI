---
type: community
cohesion: 0.47
members: 6
---

# ._store_turn() / ._call_llm() / ._compress_old_turns()

**Cohesion:** 0.47 - moderately connected
**Members:** 6 nodes

## Members
- [[._call_llm()]] - code - loki/core/brain.py
- [[._compress_old_turns()]] - code - loki/core/brain.py
- [[._extract_facts()]] - code - loki/core/brain.py
- [[._save_history()]] - code - loki/core/brain.py
- [[._store_turn()]] - code - loki/core/brain.py
- [[.clear_conversation()]] - code - loki/core/brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_store_turn_/__call_llm_/__compress_old_turns
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 2 edges to [[_COMMUNITY_.ask()  ._build_messages()  ._get_kg_context()]]

## Top bridge nodes
- [[._store_turn()]] - degree 5, connects to 2 communities
- [[._call_llm()]] - degree 4, connects to 2 communities
- [[._compress_old_turns()]] - degree 4, connects to 1 community
- [[._save_history()]] - degree 4, connects to 1 community
- [[._extract_facts()]] - degree 3, connects to 1 community