---
type: community
cohesion: 0.27
members: 10
---

# FileOrganizer / TestFileOrganizer / file_organizer.py

**Cohesion:** 0.27 - loosely connected
**Members:** 10 nodes

## Members
- [[.__init__()_28]] - code - loki/features/file_organizer.py
- [[.organize()]] - code - loki/features/file_organizer.py
- [[.test_empty_directory()]] - code - loki/tests/test_features.py
- [[.test_organizes_document()]] - code - loki/tests/test_features.py
- [[.test_organizes_image()]] - code - loki/tests/test_features.py
- [[File organizer — auto-sort downloads and desktop by file type.]] - rationale - loki/features/file_organizer.py
- [[FileOrganizer]] - code - loki/features/file_organizer.py
- [[Organize files in a directory by type.]] - rationale - loki/features/file_organizer.py
- [[TestFileOrganizer]] - code - loki/tests/test_features.py
- [[file_organizer.py]] - code - loki/features/file_organizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileOrganizer_/_TestFileOrganizer_/_file_organizerpy
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .ai_prioritize()  .list_tasks()]]

## Top bridge nodes
- [[FileOrganizer]] - degree 15, connects to 6 communities
- [[TestFileOrganizer]] - degree 10, connects to 6 communities