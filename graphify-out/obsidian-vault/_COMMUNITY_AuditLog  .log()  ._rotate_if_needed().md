---
type: community
cohesion: 0.22
members: 11
---

# AuditLog / .log() / ._rotate_if_needed()

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_5]] - code - loki/core/audit.py
- [[._rotate_if_needed()]] - code - loki/core/audit.py
- [[._sanitize()]] - code - loki/core/audit.py
- [[.get_recent()]] - code - loki/core/audit.py
- [[.log()]] - code - loki/core/audit.py
- [[Append-only audit log stored as JSONL. Thread-safe.]] - rationale - loki/core/audit.py
- [[Audit log — append-only JSONL record of all intent executions. Tier 1 read-only]] - rationale - loki/core/audit.py
- [[AuditLog]] - code - loki/core/audit.py
- [[Recursively redact sensitive keys from params.]] - rationale - loki/core/audit.py
- [[Trim log to MAX_ENTRIES. Must be called while self._lock is held.]] - rationale - loki/core/audit.py
- [[audit.py]] - code - loki/core/audit.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AuditLog_/_log_/__rotate_if_needed
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  BrowserCtrl  DailyBriefing]]
- 1 edge to [[_COMMUNITY_ConvState  conversation_sm.py  Enum]]
- 1 edge to [[_COMMUNITY_ConversationStateMachine  ._arm_timeout()  ._cancel_timeout()]]

## Top bridge nodes
- [[AuditLog]] - degree 11, connects to 4 communities