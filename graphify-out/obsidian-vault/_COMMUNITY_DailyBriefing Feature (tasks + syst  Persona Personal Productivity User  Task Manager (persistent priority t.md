---
type: community
cohesion: 0.33
members: 6
---

# DailyBriefing Feature (tasks + syst / Persona: Personal Productivity User / Task Manager (persistent priority t

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[Clipboard Manager (20-item history ring buffer)]] - document - LokiPRD.md
- [[DailyBriefing Feature (tasks + system + news)]] - document - LokiPRD.md
- [[NewsAggregator Feature (RSS-based)]] - document - LokiPRD.md
- [[Persona Personal Productivity User]] - document - LokiPRD.md
- [[System Monitor (CPURAMDiskGPUNetwork)]] - document - LokiPRD.md
- [[Task Manager (persistent priority tasks)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DailyBriefing_Feature_tasks__syst_/_Persona_Personal_Productivity_User_/_Task_Manager_persistent_priority_t
SORT file.name ASC
```
