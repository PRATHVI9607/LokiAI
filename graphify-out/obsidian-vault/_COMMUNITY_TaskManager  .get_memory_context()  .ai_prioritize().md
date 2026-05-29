---
type: community
cohesion: 0.17
members: 13
---

# TaskManager / .get_memory_context() / .ai_prioritize()

**Cohesion:** 0.17 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_51]] - code - loki/features/task_manager.py
- [[.add()]] - code - loki/features/task_manager.py
- [[.ai_prioritize()]] - code - loki/features/task_manager.py
- [[.complete()]] - code - loki/features/task_manager.py
- [[.delete()]] - code - loki/features/task_manager.py
- [[.get_memory_context()]] - code - loki/core/brain_memory.py
- [[.list_tasks()_1]] - code - loki/features/task_manager.py
- [[Build a compact memory block to inject into the system prompt.]] - rationale - loki/core/brain_memory.py
- [[Manage tasks using persistent MemoryManager storage.]] - rationale - loki/features/task_manager.py
- [[Re-rank tasks using LLM scoring based on urgency, impact, and effort.]] - rationale - loki/features/task_manager.py
- [[Task manager — add, list, complete, delete tasks with priority scoring.]] - rationale - loki/features/task_manager.py
- [[TaskManager]] - code - loki/features/task_manager.py
- [[task_manager.py]] - code - loki/features/task_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TaskManager_/_get_memory_context_/_ai_prioritize
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 1 edge to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 1 edge to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 1 edge to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 1 edge to [[_COMMUNITY_Vault  TestVault  ._save()]]

## Top bridge nodes
- [[TaskManager]] - degree 17, connects to 7 communities
- [[.get_memory_context()]] - degree 3, connects to 1 community