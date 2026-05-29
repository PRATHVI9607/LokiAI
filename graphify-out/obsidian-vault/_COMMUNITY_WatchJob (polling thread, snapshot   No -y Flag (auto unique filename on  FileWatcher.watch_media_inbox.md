---
type: community
cohesion: 0.29
members: 7
---

# WatchJob (polling thread, snapshot  / No -y Flag (auto unique filename on / FileWatcher.watch_media_inbox

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[FileWatcher_1]] - code - loki/features/file_watcher.py
- [[FileWatcher.watch_for_backup]] - code - loki/features/file_watcher.py
- [[FileWatcher.watch_media_inbox]] - code - loki/features/file_watcher.py
- [[MediaConverter_1]] - code - loki/features/media_converter.py
- [[MediaConverter.convert]] - code - loki/features/media_converter.py
- [[No -y Flag (auto unique filename on collision)]] - concept - loki/features/media_converter.py
- [[WatchJob (polling thread, snapshot diff)]] - code - loki/features/file_watcher.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WatchJob_polling_thread_snapshot__/_No_-y_Flag_auto_unique_filename_on_/_FileWatcherwatch_media_inbox
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Preview-First Pattern (pending_writ  CodeAssistant  No auto git add -A (only staged fil]]

## Top bridge nodes
- [[No -y Flag (auto unique filename on collision)]] - degree 3, connects to 1 community