---
type: community
cohesion: 0.15
members: 17
---

# ClipboardManager / TestClipboardManager / ._add()

**Cohesion:** 0.15 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_22]] - code - loki/features/clipboard_manager.py
- [[._add()]] - code - loki/features/clipboard_manager.py
- [[._monitor_loop()]] - code - loki/features/clipboard_manager.py
- [[.clear()_1]] - code - loki/features/clipboard_manager.py
- [[.get_history()]] - code - loki/features/clipboard_manager.py
- [[.get_item()]] - code - loki/features/clipboard_manager.py
- [[.start_monitoring()]] - code - loki/features/clipboard_manager.py
- [[.stop_monitoring()]] - code - loki/features/clipboard_manager.py
- [[.test_clear()]] - code - loki/tests/test_features.py
- [[.test_get_item_copies_to_clipboard()]] - code - loki/tests/test_features.py
- [[.test_get_item_out_of_range()]] - code - loki/tests/test_features.py
- [[.test_history_tracks_entries()]] - code - loki/tests/test_features.py
- [[Clipboard manager — maintain clipboard history.]] - rationale - loki/features/clipboard_manager.py
- [[ClipboardManager]] - code - loki/features/clipboard_manager.py
- [[TestClipboardManager]] - code - loki/tests/test_features.py
- [[Track and manage clipboard history.]] - rationale - loki/features/clipboard_manager.py
- [[clipboard_manager.py]] - code - loki/features/clipboard_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClipboardManager_/_TestClipboardManager_/__add
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]
- 2 edges to [[_COMMUNITY_TestTaskManager  test_features.py  memory_mgr()]]
- 2 edges to [[_COMMUNITY_SecurityScanner  TestSecurityScanner  ._iter_files()]]
- 2 edges to [[_COMMUNITY_FileOrganizer  TestFileOrganizer  ._organizer()]]
- 2 edges to [[_COMMUNITY_Vault  TestVault  ._save()]]
- 1 edge to [[_COMMUNITY_MemoryManager  ._save_json()  .add_task()]]
- 1 edge to [[_COMMUNITY_TaskManager  .get_memory_context()  .ai_prioritize()]]

## Top bridge nodes
- [[TestClipboardManager]] - degree 11, connects to 6 communities
- [[ClipboardManager]] - degree 21, connects to 5 communities