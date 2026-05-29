---
type: community
cohesion: 0.23
members: 14
---

# SoftwareUpdater / ._run() / ._check_winget()

**Cohesion:** 0.23 - loosely connected
**Members:** 14 nodes

## Members
- [[.__init__()_48]] - code - loki/features/software_updater.py
- [[._check_winget()]] - code - loki/features/software_updater.py
- [[._run()]] - code - loki/features/software_updater.py
- [[.check_updates()]] - code - loki/features/software_updater.py
- [[.install_package()]] - code - loki/features/software_updater.py
- [[.update_all()]] - code - loki/features/software_updater.py
- [[.update_package()]] - code - loki/features/software_updater.py
- [[Install a package by name.]] - rationale - loki/features/software_updater.py
- [[List all packages with available upgrades.]] - rationale - loki/features/software_updater.py
- [[SoftwareUpdater]] - code - loki/features/software_updater.py
- [[SoftwareUpdater — check and apply updates via winget (Windows Package Manager).]] - rationale - loki/features/software_updater.py
- [[Upgrade a specific package by name or ID.]] - rationale - loki/features/software_updater.py
- [[Upgrade all installed packages.]] - rationale - loki/features/software_updater.py
- [[software_updater.py]] - code - loki/features/software_updater.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SoftwareUpdater_/__run_/__check_winget
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiTTS  ._queue_worker()  ._speak_edge()]]

## Top bridge nodes
- [[SoftwareUpdater]] - degree 10, connects to 2 communities
- [[._run()]] - degree 6, connects to 1 community