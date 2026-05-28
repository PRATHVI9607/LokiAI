---
source_file: "loki/core/audit.py"
type: "rationale"
community: "AuditLog / .log() / ._rotate_if_needed()"
location: "L78"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/AuditLog_/_log_/__rotate_if_needed
---

# Recursively redact sensitive keys from params.

## Connections
- [[._sanitize()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/AuditLog_/_log_/__rotate_if_needed