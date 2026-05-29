---
type: community
cohesion: 0.13
members: 24
---

# FileWatcher / WatchJob / .watch_custom()

**Cohesion:** 0.13 - loosely connected
**Members:** 24 nodes

## Members
- [[.__init__()_34]] - code - loki/features/file_watcher.py
- [[.__init__()_33]] - code - loki/features/file_watcher.py
- [[._job_key()]] - code - loki/features/file_watcher.py
- [[._loop()]] - code - loki/features/file_watcher.py
- [[._scan()_1]] - code - loki/features/file_watcher.py
- [[.list_watchers()]] - code - loki/features/file_watcher.py
- [[.start()_2]] - code - loki/features/file_watcher.py
- [[.stop()_3]] - code - loki/features/file_watcher.py
- [[.stop_all()]] - code - loki/features/file_watcher.py
- [[.stop_watch()]] - code - loki/features/file_watcher.py
- [[.watch_custom()]] - code - loki/features/file_watcher.py
- [[.watch_for_backup()]] - code - loki/features/file_watcher.py
- [[.watch_media_inbox()]] - code - loki/features/file_watcher.py
- [[A single directory watch job with a callback and state tracking.]] - rationale - loki/features/file_watcher.py
- [[Auto-backup a file or directory whenever it changes.]] - rationale - loki/features/file_watcher.py
- [[Auto-convert any media file dropped into inbox_dir.]] - rationale - loki/features/file_watcher.py
- [[FileWatcher]] - code - loki/features/file_watcher.py
- [[FileWatcher — monitor directories for changes and trigger automated actions   -]] - rationale - loki/features/file_watcher.py
- [[List all active watch jobs.]] - rationale - loki/features/file_watcher.py
- [[Start a custom watch job that logs all changes.]] - rationale - loki/features/file_watcher.py
- [[Stop all active watchers.]] - rationale - loki/features/file_watcher.py
- [[Stop all watch jobs for a given path.]] - rationale - loki/features/file_watcher.py
- [[WatchJob]] - code - loki/features/file_watcher.py
- [[file_watcher.py]] - code - loki/features/file_watcher.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileWatcher_/_WatchJob_/_watch_custom
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]

## Top bridge nodes
- [[FileWatcher]] - degree 11, connects to 2 communities