---
type: community
cohesion: 0.23
members: 13
---

# FileOrganizer / TestFileOrganizer / ._organizer()

**Cohesion:** 0.23 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_31]] - code - loki/features/file_organizer.py
- [[._is_safe_dir()]] - code - loki/features/file_organizer.py
- [[._organizer()]] - code - loki/tests/test_features.py
- [[.organize()]] - code - loki/features/file_organizer.py
- [[.test_empty_directory()]] - code - loki/tests/test_features.py
- [[.test_organizes_document()]] - code - loki/tests/test_features.py
- [[.test_organizes_image()]] - code - loki/tests/test_features.py
- [[.test_unsafe_dir_rejected()]] - code - loki/tests/test_features.py
- [[File organizer — auto-sort downloads and desktop by file type. Restricted to Dow]] - rationale - loki/features/file_organizer.py
- [[FileOrganizer]] - code - loki/features/file_organizer.py
- [[Organize files in a directory by type.]] - rationale - loki/features/file_organizer.py
- [[TestFileOrganizer]] - code - loki/tests/test_features.py
- [[file_organizer.py]] - code - loki/features/file_organizer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileOrganizer_/_TestFileOrganizer_/__organizer
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ClipboardManager  TestClipboardManager  ._add()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]

## Top bridge nodes
- [[FileOrganizer]] - degree 14, connects to 6 communities
- [[TestFileOrganizer]] - degree 12, connects to 6 communities