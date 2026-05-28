---
type: community
cohesion: 0.20
members: 10
---

# BackupManager / .backup_directory() / .backup_file()

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[.__init__()_15]] - code - loki/features/backup_manager.py
- [[.backup_directory()]] - code - loki/features/backup_manager.py
- [[.backup_file()]] - code - loki/features/backup_manager.py
- [[.list_backups()]] - code - loki/features/backup_manager.py
- [[BackupManager]] - code - loki/features/backup_manager.py
- [[BackupManager — copy filesdirectories to a backup destination with timestamps.]] - rationale - loki/features/backup_manager.py
- [[Copy a single file to the backup directory with a timestamp suffix.]] - rationale - loki/features/backup_manager.py
- [[Copy an entire directory tree to backup with a timestamp.]] - rationale - loki/features/backup_manager.py
- [[List existing backups.]] - rationale - loki/features/backup_manager.py
- [[backup_manager.py]] - code - loki/features/backup_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/BackupManager_/_backup_directory_/_backup_file
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  main.py]]
- 1 edge to [[_COMMUNITY_ConversationManager  .process_input()  ._speak()]]

## Top bridge nodes
- [[BackupManager]] - degree 8, connects to 2 communities