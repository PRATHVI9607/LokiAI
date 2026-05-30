---
type: community
cohesion: 0.50
members: 4
---

# FileWatcher Feature (polling-based  / BackupManager Feature (timestamped  / MediaConverter Feature (ffmpeg wrap

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[BackupManager Feature (timestamped backups)]] - document - LokiPRD.md
- [[FileWatcher Feature (polling-based auto-backupmedia-convert)]] - document - LokiPRD.md
- [[MediaConverter Feature (ffmpeg wrapper)]] - document - LokiPRD.md
- [[Rationale FileWatcher pure Python threading (graceful fallback if watchdog not installed)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FileWatcher_Feature_polling-based__/_BackupManager_Feature_timestamped__/_MediaConverter_Feature_ffmpeg_wrap
SORT file.name ASC
```
