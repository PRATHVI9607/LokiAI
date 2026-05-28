---
type: community
cohesion: 0.40
members: 5
---

# MediaConverter Feature (ffmpeg wrapper)

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[BackupManager Feature (timestamped backups)]] - document - LokiPRD.md
- [[FileWatcher Feature (polling-based auto-backupmedia-convert)]] - document - LokiPRD.md
- [[MediaConverter Feature (ffmpeg wrapper)]] - document - LokiPRD.md
- [[Rationale FileWatcher pure Python threading (graceful fallback if watchdog not installed)]] - document - LokiPRD.md
- [[Requirement watchdog=3.0.0 (File watching)]] - document - loki/requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MediaConverter_Feature_ffmpeg_wrapper
SORT file.name ASC
```
