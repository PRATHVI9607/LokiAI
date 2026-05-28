---
source_file: "loki/core/audit.py"
type: "rationale"
community: "AuditLog / .log() / ._rotate_if_needed()"
location: "L97"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/AuditLog_/_log_/__rotate_if_needed
---

# Trim log to MAX_ENTRIES. Must be called while self._lock is held.

## Connections
- [[._rotate_if_needed()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/AuditLog_/_log_/__rotate_if_needed