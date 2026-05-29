---
type: community
cohesion: 0.21
members: 14
---

# FootprintAuditor / .full_audit() / .audit_network_listeners()

**Cohesion:** 0.21 - loosely connected
**Members:** 14 nodes

## Members
- [[.audit_network_listeners()]] - code - loki/features/footprint_auditor.py
- [[.audit_privacy_settings()]] - code - loki/features/footprint_auditor.py
- [[.audit_scheduled_tasks()]] - code - loki/features/footprint_auditor.py
- [[.audit_startup()]] - code - loki/features/footprint_auditor.py
- [[.full_audit()]] - code - loki/features/footprint_auditor.py
- [[Check key Windows privacy registry settings.]] - rationale - loki/features/footprint_auditor.py
- [[FootprintAuditor]] - code - loki/features/footprint_auditor.py
- [[FootprintAuditor — audit Windows privacy settings, installed apps with network a]] - rationale - loki/features/footprint_auditor.py
- [[List all programs set to run at startup.]] - rationale - loki/features/footprint_auditor.py
- [[List processes with active network listeners.]] - rationale - loki/features/footprint_auditor.py
- [[List scheduled tasks with network or file system triggers.]] - rationale - loki/features/footprint_auditor.py
- [[Run all audits and return a combined report.]] - rationale - loki/features/footprint_auditor.py
- [[_run_ps()]] - code - loki/features/footprint_auditor.py
- [[footprint_auditor.py]] - code - loki/features/footprint_auditor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FootprintAuditor_/_full_audit_/_audit_network_listeners
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_LokiApplication  ._init_all()  .__init__()]]

## Top bridge nodes
- [[FootprintAuditor]] - degree 8, connects to 1 community