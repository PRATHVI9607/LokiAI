---
type: community
cohesion: 0.22
members: 9
---

# TestTaskManager / test_features.py / memory_mgr()

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[.test_add_and_list()]] - code - loki/tests/test_features.py
- [[.test_complete_task()]] - code - loki/tests/test_features.py
- [[.test_delete_task()]] - code - loki/tests/test_features.py
- [[.test_empty_title_rejected()]] - code - loki/tests/test_features.py
- [[.test_priority_sorting()]] - code - loki/tests/test_features.py
- [[TestTaskManager]] - code - loki/tests/test_features.py
- [[memory_mgr()]] - code - loki/tests/test_features.py
- [[task_mgr()]] - code - loki/tests/test_features.py
- [[test_features.py]] - code - loki/tests/test_features.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestTaskManager_/_test_featurespy_/_memory_mgr
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]

## Top bridge nodes
- [[TestTaskManager]] - degree 12, connects to 6 communities
- [[test_features.py]] - degree 7, connects to 4 communities
- [[memory_mgr()]] - degree 2, connects to 1 community
- [[task_mgr()]] - degree 2, connects to 1 community