---
type: community
cohesion: 0.20
members: 10
---

# DailyBriefing Feature (tasks + syst / Clipboard Manager (20-item history  / Persona: Personal Productivity User

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Clipboard Manager (20-item history ring buffer)]] - document - LokiPRD.md
- [[ClipboardSync Feature (HTTP server port 7778 mobile sync)]] - document - LokiPRD.md
- [[DailyBriefing Feature (tasks + system + news)]] - document - LokiPRD.md
- [[NewsAggregator Feature (RSS-based)]] - document - LokiPRD.md
- [[Persona Personal Productivity User]] - document - LokiPRD.md
- [[Process Manager (listkill with protected list)]] - document - LokiPRD.md
- [[Requirement psutil=5.9.8 (Processsystem monitoring)]] - document - loki/requirements.txt
- [[Requirement pyperclip=1.8.2 (Clipboard manager)]] - document - loki/requirements.txt
- [[System Monitor (CPURAMDiskGPUNetwork)]] - document - LokiPRD.md
- [[Task Manager (persistent priority tasks)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DailyBriefing_Feature_tasks__syst_/_Clipboard_Manager_20-item_history__/_Persona_Personal_Productivity_User
SORT file.name ASC
```
