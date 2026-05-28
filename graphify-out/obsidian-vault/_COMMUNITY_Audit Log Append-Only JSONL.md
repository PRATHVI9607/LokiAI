---
type: community
cohesion: 0.67
members: 3
---

# Audit Log Append-Only JSONL

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Audit Log Append-Only JSONL]] - document - LokiPRD.md
- [[Audit Log Automatic Sanitization (REDACTED for secrets)]] - document - LokiPRD.md
- [[Audit Tier Classification (Tier 1 Safe  Tier 2 Moderate  Tier 3 Restricted)]] - document - LokiPRD.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Audit_Log_Append-Only_JSONL
SORT file.name ASC
```
