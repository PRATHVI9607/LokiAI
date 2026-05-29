---
type: community
cohesion: 1.00
members: 1
---

# ExpenseTracker Feature (email/EML p

**Cohesion:** 1.00 - tightly connected
**Members:** 1 nodes

## Members
- [[ExpenseTracker Feature (emailEML parsing + CSV ledger)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ExpenseTracker_Feature_email/EML_p
SORT file.name ASC
```
