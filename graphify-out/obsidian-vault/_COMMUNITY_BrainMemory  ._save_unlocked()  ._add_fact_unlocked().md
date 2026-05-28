---
type: community
cohesion: 0.12
members: 25
---

# BrainMemory / ._save_unlocked() / ._add_fact_unlocked()

**Cohesion:** 0.12 - loosely connected
**Members:** 25 nodes

## Members
- [[.__init__()_8]] - code - loki/core/brain_memory.py
- [[._add_fact_unlocked()]] - code - loki/core/brain_memory.py
- [[._load()]] - code - loki/core/brain_memory.py
- [[._save_unlocked()]] - code - loki/core/brain_memory.py
- [[.add()]] - code - loki/features/task_manager.py
- [[.add_decision()]] - code - loki/core/brain_memory.py
- [[.add_key_fact()]] - code - loki/core/brain_memory.py
- [[.add_key_facts()]] - code - loki/core/brain_memory.py
- [[.add_session_summary()]] - code - loki/core/brain_memory.py
- [[.get_memory_context()]] - code - loki/core/brain_memory.py
- [[.get_personality_prompt()]] - code - loki/core/brain_memory.py
- [[.get_preference()]] - code - loki/core/brain_memory.py
- [[.save()]] - code - loki/core/brain_memory.py
- [[.set_preference()]] - code - loki/core/brain_memory.py
- [[.to_dict()]] - code - loki/core/brain_memory.py
- [[Add multiple facts and flush to disk exactly once.]] - rationale - loki/core/brain_memory.py
- [[Add one fact without acquiring lock. Caller must hold self._lock.]] - rationale - loki/core/brain_memory.py
- [[Atomically write brain.json. Caller must hold self._lock.]] - rationale - loki/core/brain_memory.py
- [[BrainMemory]] - code - loki/core/brain_memory.py
- [[Build a compact memory block to inject into the system prompt.]] - rationale - loki/core/brain_memory.py
- [[Persistent structured memory. Replaces flat user_profile.json.     All data live]] - rationale - loki/core/brain_memory.py
- [[Structured persistent brain — KORTEX-style brain.json.  Stores key facts, archit]] - rationale - loki/core/brain_memory.py
- [[brain_memory.py]] - code - loki/core/brain_memory.py
- [[personality()]] - code - loki/core/brain_memory.py
- [[user_name()]] - code - loki/core/brain_memory.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/BrainMemory_/__save_unlocked_/__add_fact_unlocked
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]

## Top bridge nodes
- [[BrainMemory]] - degree 19, connects to 2 communities
- [[.add()]] - degree 2, connects to 1 community