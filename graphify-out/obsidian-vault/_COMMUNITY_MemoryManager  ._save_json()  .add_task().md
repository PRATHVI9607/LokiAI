---
type: community
cohesion: 0.18
members: 16
---

# MemoryManager / ._save_json() / .add_task()

**Cohesion:** 0.18 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_10]] - code - loki/core/memory.py
- [[._load_json()]] - code - loki/core/memory.py
- [[._next_task_id()]] - code - loki/core/memory.py
- [[._save_json()]] - code - loki/core/memory.py
- [[.add_task()]] - code - loki/core/memory.py
- [[.complete_task()]] - code - loki/core/memory.py
- [[.delete_task()]] - code - loki/core/memory.py
- [[.get_preference()_1]] - code - loki/core/memory.py
- [[.get_user_name()_1]] - code - loki/core/memory.py
- [[.list_tasks()]] - code - loki/core/memory.py
- [[.set_preference()_1]] - code - loki/core/memory.py
- [[.set_user_name()_1]] - code - loki/core/memory.py
- [[Centralized persistent memory for Loki.]] - rationale - loki/core/memory.py
- [[Memory manager — persistent conversation, profile, tasks storage.]] - rationale - loki/core/memory.py
- [[MemoryManager]] - code - loki/core/memory.py
- [[memory.py]] - code - loki/core/memory.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MemoryManager_/__save_json_/_add_task
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]
- 1 edge to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 1 edge to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 1 edge to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  file_organizer.py]]
- 1 edge to [[_COMMUNITY_Vault  TestVault  ._save()]]

## Top bridge nodes
- [[MemoryManager]] - degree 24, connects to 8 communities