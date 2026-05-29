---
type: community
cohesion: 0.22
members: 9
---

# .ask() / ._build_messages() / ._get_kg_context()

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[._build_messages()]] - code - loki/core/brain.py
- [[._build_system_prompt()]] - code - loki/core/brain.py
- [[._get_kg_context()]] - code - loki/core/brain.py
- [[._get_rag_context()]] - code - loki/core/brain.py
- [[._store_turn()]] - code - loki/core/brain.py
- [[.ask()]] - code - loki/core/brain.py
- [[Assemble context in priority order         1. System prompt (personality + brai]] - rationale - loki/core/brain.py
- [[Layer 3 knowledge graph entity lookup — structured relational context.]] - rationale - loki/core/brain.py
- [[Layer 4 ChromaDB semantic chunks from indexed files.]] - rationale - loki/core/brain.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ask_/__build_messages_/__get_kg_context
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_LokiBrain  DailyBriefing  CodeAssistant]]
- 2 edges to [[_COMMUNITY_._call_llm()  ._compress_old_turns()  ._save_history()]]

## Top bridge nodes
- [[.ask()]] - degree 6, connects to 2 communities
- [[._store_turn()]] - degree 3, connects to 2 communities
- [[._build_messages()]] - degree 4, connects to 1 community
- [[._get_kg_context()]] - degree 3, connects to 1 community
- [[._get_rag_context()]] - degree 3, connects to 1 community