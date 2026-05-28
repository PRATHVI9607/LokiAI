---
type: community
cohesion: 0.22
members: 10
---

# TaskManager / .ai_prioritize() / .list_tasks()

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[.__init__()_47]] - code - loki/features/task_manager.py
- [[.ai_prioritize()]] - code - loki/features/task_manager.py
- [[.complete()]] - code - loki/features/task_manager.py
- [[.delete()]] - code - loki/features/task_manager.py
- [[.list_tasks()_1]] - code - loki/features/task_manager.py
- [[Manage tasks using persistent MemoryManager storage.]] - rationale - loki/features/task_manager.py
- [[Re-rank tasks using LLM scoring based on urgency, impact, and effort.]] - rationale - loki/features/task_manager.py
- [[Task manager — add, list, complete, delete tasks with priority scoring.]] - rationale - loki/features/task_manager.py
- [[TaskManager]] - code - loki/features/task_manager.py
- [[task_manager.py]] - code - loki/features/task_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TaskManager_/_ai_prioritize_/_list_tasks
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_BrainMemory  ._save_unlocked()  ._add_fact_unlocked()]]
- 1 edge to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 1 edge to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 1 edge to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 1 edge to [[_COMMUNITY_Vault  TestVault  ._save()]]

## Top bridge nodes
- [[TaskManager]] - degree 18, connects to 9 communities