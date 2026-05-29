---
type: community
cohesion: 1.00
members: 2
---

# File Operations (create/delete/move / File Ops Sandboxed to Home Director

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[File Operations (createdeletemovereadsearchorganize)]] - document - LokiPRD.md
- [[File Ops Sandboxed to Home Directory (~)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/File_Operations_create/delete/move_/_File_Ops_Sandboxed_to_Home_Director
SORT file.name ASC
```
